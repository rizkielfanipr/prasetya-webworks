import { CheckoutError, formatRupiah, type OrderRequest, packageAmount, startPayment } from './checkout';
import { openWhatsApp } from './whatsapp';

interface ChoiceRequest {
	order: OrderRequest;
	whatsappMessage: string;
	onConsult: () => void;
}

const dialog = () => document.querySelector<HTMLDialogElement>('#order-choice');

/** The dialog is only rendered when online payment is configured. */
export const hasOrderChoice = () => dialog() !== null;

let current: ChoiceRequest | undefined;
let wired = false;

function wire(modal: HTMLDialogElement) {
	if (wired) return;
	wired = true;
	const label = modal.dataset;
	const pay = modal.querySelector<HTMLButtonElement>('[data-choice-pay]');
	const error = modal.querySelector<HTMLElement>('[data-choice-error]');

	modal.querySelector('[data-choice-close]')?.addEventListener('click', () => modal.close());
	modal.addEventListener('click', (event) => {
		if (event.target === modal) modal.close();
	});

	modal.querySelector('[data-choice-consult]')?.addEventListener('click', () => {
		if (!current) return;
		openWhatsApp(current.whatsappMessage);
		current.onConsult();
		modal.close();
	});

	pay?.addEventListener('click', () => {
		if (!current) return;
		const idleText = pay.textContent;
		pay.disabled = true;
		pay.textContent = label.paying ?? '';
		if (error) error.textContent = '';
		startPayment(current.order, label.locale ?? 'id', label.statusPath ?? '')
			.then((url) => window.location.assign(url))
			.catch((reason: unknown) => {
				const failure = reason instanceof CheckoutError ? reason.failure : 'unavailable';
				if (error)
					error.textContent = { invalid: label.errorInvalid, busy: label.errorBusy, unavailable: label.errorUnavailable }[failure] ?? '';
				pay.disabled = false;
				pay.textContent = idleText;
			});
	});
}

export function openOrderChoice(request: ChoiceRequest) {
	const modal = dialog();
	if (!modal) return;
	wire(modal);
	current = request;
	const label = modal.dataset;
	const total = modal.querySelector<HTMLElement>('[data-choice-total]');
	const pay = modal.querySelector<HTMLButtonElement>('[data-choice-pay]');
	const error = modal.querySelector<HTMLElement>('[data-choice-error]');
	if (total) total.textContent = label.totalLoading ?? '';
	if (error) error.textContent = '';
	if (pay) pay.disabled = true;
	modal.showModal();

	packageAmount(request.order.packageCode)
		.then((amount) => {
			if (total) total.textContent = formatRupiah(amount);
			if (pay) pay.disabled = false;
		})
		.catch(() => {
			// WhatsApp still works, so a platform outage does not lose the order.
			if (total) total.textContent = '-';
			if (error) error.textContent = label.errorUnavailable ?? '';
		});
}
