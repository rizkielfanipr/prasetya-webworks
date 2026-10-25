import { prefersReducedMotion } from './motion';

const DISMISSED = 'satamu-float-dismissed';

/**
 * Satamu prompt above the WhatsApp button: the speech bubble appears after a short delay and can be
 * closed; once closed it stays hidden for the rest of the browser session. While the footer is on screen the
 * bubble fades out (`data-near-footer`) so it never covers footer text. The Satamu icon always stays.
 */
export function initSatamuFloat(root: HTMLElement) {
	const bubble = root.querySelector<HTMLElement>('[data-satamu-bubble]');
	if (!bubble) return;

	let dismissed = false;
	try {
		dismissed = sessionStorage.getItem(DISMISSED) === '1';
	} catch {
		// Storage can be blocked (private mode); the bubble then simply shows every time.
	}
	if (dismissed) return;

	window.setTimeout(() => (bubble.hidden = false), prefersReducedMotion() ? 0 : 1200);

	const footer = document.querySelector('footer');
	if (footer && 'IntersectionObserver' in window) {
		new IntersectionObserver(([entry]) => root.toggleAttribute('data-near-footer', entry.isIntersecting)).observe(footer);
	}

	root.querySelector('[data-satamu-close]')?.addEventListener('click', () => {
		bubble.hidden = true;
		try {
			sessionStorage.setItem(DISMISSED, '1');
		} catch {
			// Ignore: the bubble is already hidden for this page view.
		}
	});
}
