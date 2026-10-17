import { prefersReducedMotion } from './motion';

/** Puts a message into the home contact form and moves the visitor there. */
export function prefillContactMessage(message: string, { scroll = true } = {}) {
	const form = document.querySelector<HTMLFormElement>('#contact-form');
	const textarea = form?.querySelector<HTMLTextAreaElement>('textarea[name="message"]');
	if (!form || !textarea) return;

	textarea.value = message;
	if (scroll) document.querySelector('#contact')?.scrollIntoView({ behavior: prefersReducedMotion() ? 'auto' : 'smooth', block: 'start' });
	form.querySelector<HTMLInputElement>('input[name="name"]')?.focus({ preventScroll: true });
}
