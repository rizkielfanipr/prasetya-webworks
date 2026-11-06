import { checkoutLocale, paymentStatus, type PaymentStatus, retryPayment } from './checkout';
import { whatsappUrl } from './whatsapp';

type View = 'loading' | 'paid' | 'pending' | 'retry' | 'closed' | 'error';

const POLL_MS = 5000;
const POLL_LIMIT = 36; // Three minutes, then the visitor can refresh.

/** Only ever shows what the platform reports. Arriving back from the gateway proves nothing, see ADR 0012. */
export function initOrderStatus(root: HTMLElement) {
	const reference = new URLSearchParams(window.location.search).get('order') ?? '';
	const invoice = root.querySelector<HTMLElement>('[data-status-invoice]');
	const invoiceRow = root.querySelector<HTMLElement>('[data-status-invoice-row]');
	const help = root.querySelector<HTMLAnchorElement>('[data-status-help]');
	const resume = root.querySelector<HTMLAnchorElement>('[data-status-resume]');
	const retry = root.querySelector<HTMLButtonElement>('[data-status-retry]');
	let polls = 0;

	function show(view: View) {
		root.querySelectorAll<HTMLElement>('[data-status-view]').forEach((panel) => {
			panel.hidden = panel.dataset.statusView !== view;
		});
	}

	function viewFor(status: PaymentStatus): View {
		if (status.payment_status === 'PAID') return 'paid';
		if (status.order_status !== 'PENDING_PAYMENT') return 'closed';
		return status.payment_status === 'PENDING' || status.payment_status === 'CREATED' ? 'pending' : 'retry';
	}

	async function refresh() {
		let status: PaymentStatus;
		try {
			status = await paymentStatus(reference);
		} catch {
			show('error');
			return;
		}
		const view = viewFor(status);
		show(view);
		if (invoice) invoice.textContent = status.invoice_number;
		if (invoiceRow) invoiceRow.hidden = false;
		if (help) help.href = whatsappUrl((help.dataset.message ?? '').replace('{invoice}', status.invoice_number));
		if (resume) {
			resume.hidden = !status.checkout_url;
			resume.href = status.checkout_url ?? '#';
		}
		if (view === 'pending' && polls < POLL_LIMIT) {
			polls += 1;
			window.setTimeout(() => void refresh(), POLL_MS);
		}
	}

	retry?.addEventListener('click', () => {
		retry.disabled = true;
		retryPayment(reference)
			.then((url) => {
				if (url) window.location.assign(url);
				else show('error');
			})
			.catch(() => show('error'))
			.finally(() => {
				retry.disabled = false;
			});
	});

	if (!/^[0-9a-z]{26}$/i.test(reference)) {
		show('error');
		return;
	}
	if (root.dataset.locale === 'id' && checkoutLocale() === 'en') {
		window.location.replace(`${root.dataset.enPath}?order=${reference}`);
		return;
	}
	void refresh();
}
