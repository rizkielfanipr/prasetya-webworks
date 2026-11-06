import { site } from '../config/site';

/** Everything here talks to Prasetya Platform, which owns price and payment state. See ADR 0012. */

export interface OrderRequest {
	packageCode: string;
	name: string;
	email: string;
	whatsapp: string;
	business: string;
	domain: string;
	notes: string;
	templateCode: string;
}

export interface PaymentStatus {
	invoice_number: string;
	order_status: string;
	payment_status: string | null;
	checkout_url: string | null;
}

export type CheckoutFailure = 'invalid' | 'busy' | 'unavailable';

export class CheckoutError extends Error {
	constructor(public readonly failure: CheckoutFailure) {
		super(failure);
	}
}

interface Envelope<T> {
	success: boolean;
	data: T;
	error?: { code: string };
}

const INTENT_KEY = 'prasetya.checkout.intent';
const LOCALE_KEY = 'prasetya.checkout.locale';

async function request<T>(path: string, init?: RequestInit): Promise<{ status: number; body: Envelope<T> }> {
	try {
		const response = await fetch(`${site.platformApiUrl}/api/v1${path}`, {
			...init,
			headers: { Accept: 'application/json', ...init?.headers },
		});
		return { status: response.status, body: (await response.json()) as Envelope<T> };
	} catch {
		throw new CheckoutError('unavailable');
	}
}

function post<T>(path: string, idempotencyKey: string, body?: unknown) {
	return request<T>(path, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json', 'Idempotency-Key': idempotencyKey },
		body: body === undefined ? undefined : JSON.stringify(body),
	});
}

/** Price for display, always from the platform so the site cannot show a stale amount before paying. */
export async function packageAmount(code: string): Promise<number> {
	const { body } = await request<{ code: string; price: { amount: number } }[]>('/packages?application_code=WEBWORKS');
	const item = body.success ? body.data.find((entry) => entry.code === code) : undefined;
	if (!item) throw new CheckoutError('unavailable');
	return item.price.amount;
}

export const formatRupiah = (amount: number) => `Rp${new Intl.NumberFormat('id-ID').format(amount)}`;

interface Intent {
	body: string;
	orderKey: string;
	checkoutKey: string;
}

/** The same form content keeps the same keys, so a refresh or second click cannot create a second order. Keys are not payment data. */
function intentFor(body: string): Intent {
	const stored = sessionStorage.getItem(INTENT_KEY);
	const parsed = stored ? (JSON.parse(stored) as Intent) : undefined;
	if (parsed?.body === body) return parsed;
	const fresh = { body, orderKey: crypto.randomUUID(), checkoutKey: crypto.randomUUID() };
	sessionStorage.setItem(INTENT_KEY, JSON.stringify(fresh));
	return fresh;
}

function failureFor(code: string | undefined): CheckoutFailure {
	if (code === 'VALIDATION_FAILED') return 'invalid';
	if (code === 'CHECKOUT_IN_PROGRESS' || code === 'IDEMPOTENCY_IN_PROGRESS') return 'busy';
	return 'unavailable';
}

/** Returns where to send the customer: checkout, or the status page if already paid. A return from checkout proves nothing; the status page asks the platform. */
export async function startPayment(order: OrderRequest, locale: string, statusPath: string): Promise<string> {
	const payload = JSON.stringify({
		application_code: 'WEBWORKS',
		package_code: order.packageCode,
		customer: { name: order.name, email: order.email, phone: order.whatsapp },
		details: {
			template_code: order.templateCode || null,
			business_name: order.business,
			domain_preference: order.domain,
			notes: order.notes || null,
		},
	});
	const intent = intentFor(payload);

	const created = await post<{ reference: string }>('/orders', intent.orderKey, JSON.parse(payload));
	if (!created.body.success) throw new CheckoutError(failureFor(created.body.error?.code));

	sessionStorage.setItem(LOCALE_KEY, locale);
	const reference = created.body.data.reference;

	// A replayed key points at an attempt that may have ended since, so a second try uses a new key.
	for (const key of [intent.checkoutKey, crypto.randomUUID()]) {
		const outcome = await openCheckout(reference, key);
		if (outcome.alreadyPaid) return `${statusPath}?order=${reference}`;
		if (outcome.notPayable) {
			sessionStorage.removeItem(INTENT_KEY); // The next attempt starts a new order.
			throw new CheckoutError('unavailable');
		}
		if (outcome.url) return outcome.url;
	}
	throw new CheckoutError('unavailable');
}

async function openCheckout(reference: string, key: string): Promise<{ url?: string; alreadyPaid?: boolean; notPayable?: boolean }> {
	const { body } = await post<{ checkout_url: string | null }>(`/orders/${reference}/checkout`, key);
	if (body.success) return { url: body.data.checkout_url ?? undefined };
	if (body.error?.code === 'ORDER_ALREADY_PAID') return { alreadyPaid: true };
	if (body.error?.code === 'ORDER_NOT_PAYABLE') return { notPayable: true };
	throw new CheckoutError(failureFor(body.error?.code));
}

export async function retryPayment(reference: string): Promise<string | null> {
	return (await openCheckout(reference, crypto.randomUUID())).url ?? null;
}

export async function paymentStatus(reference: string): Promise<PaymentStatus> {
	const { body } = await request<PaymentStatus>(`/orders/${reference}/payment-status`);
	if (!body.success) throw new CheckoutError('unavailable');
	return body.data;
}

/** Locale the customer left in. The gateway returns everyone to one URL, so English customers are sent back to their page. */
export const checkoutLocale = () => sessionStorage.getItem(LOCALE_KEY);
