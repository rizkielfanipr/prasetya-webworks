import { prefersReducedMotion } from './motion';

/** Fades matching elements in as they enter the viewport (styles in src/styles/global.css). */
export function initScrollReveal(selectors: string[]) {
	const items = Array.from(document.querySelectorAll<HTMLElement>(selectors.join(',')));

	items.forEach((item, index) => {
		item.classList.add('scroll-reveal');
		item.style.setProperty('--reveal-delay', `${(index % 6) * 65}ms`);
	});

	if (prefersReducedMotion() || !('IntersectionObserver' in window)) {
		items.forEach((item) => item.classList.add('is-visible'));
		return;
	}

	const observer = new IntersectionObserver(
		(entries) => {
			entries.forEach((entry) => {
				if (!entry.isIntersecting) return;
				entry.target.classList.add('is-visible');
				observer.unobserve(entry.target);
			});
		},
		{ threshold: 0.12, rootMargin: '0px 0px -7% 0px' },
	);

	items.forEach((item) => observer.observe(item));
}
