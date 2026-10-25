import { prefersReducedMotion } from './motion';

/**
 * Rotating carousel for `[data-carousel]`. The active dot's CSS progress animation is the timer:
 * when it ends the next slide shows, and pausing the animation (hover, focus, hidden tab, pause button)
 * pauses the rotation. With reduced motion the animation is off, so slides only change on request.
 */
export function initCarousel(root: HTMLElement) {
	const slides = Array.from(root.querySelectorAll<HTMLElement>('[data-carousel-slide]'));
	const dots = Array.from(root.querySelectorAll<HTMLButtonElement>('[data-carousel-dot]'));
	const toggle = root.querySelector<HTMLButtonElement>('[data-carousel-toggle]');
	const live = root.querySelector<HTMLElement>('[data-carousel-live]');
	const holds = new Set<string>();
	let current = 0;
	let stopped = false;

	const sync = () => root.classList.toggle('is-paused', stopped || holds.size > 0);
	const hold = (reason: string, on: boolean) => {
		if (on) holds.add(reason);
		else holds.delete(reason);
		sync();
	};

	function show(index: number, fromUser = false) {
		current = (index + slides.length) % slides.length;
		slides.forEach((slide, i) => {
			const active = i === current;
			slide.classList.toggle('is-active', active);
			slide.inert = !active;
		});
		dots.forEach((dot, i) => {
			dot.classList.remove('is-active');
			dot.setAttribute('aria-current', String(i === current));
		});
		// Reading offsetWidth restarts the progress animation on the newly active dot.
		void dots[current]?.offsetWidth;
		dots[current]?.classList.add('is-active');
		// Announce only changes the visitor asked for, not automatic ones.
		live?.setAttribute('aria-live', fromUser ? 'polite' : 'off');
	}

	dots.forEach((dot, index) => {
		dot.addEventListener('click', () => show(index, true));
		dot.addEventListener('animationend', () => show(current + 1));
	});
	root.querySelector('[data-carousel-prev]')?.addEventListener('click', () => show(current - 1, true));
	root.querySelector('[data-carousel-next]')?.addEventListener('click', () => show(current + 1, true));

	toggle?.addEventListener('click', () => {
		stopped = !stopped;
		toggle.classList.toggle('is-stopped', stopped);
		toggle.setAttribute('aria-label', (stopped ? toggle.dataset.labelPlay : toggle.dataset.labelPause) ?? '');
		sync();
	});
	if (prefersReducedMotion() && toggle) toggle.hidden = true;

	root.querySelectorAll('[data-carousel-hold]').forEach((area) => {
		area.addEventListener('pointerenter', (event) => (event as PointerEvent).pointerType === 'mouse' && hold('hover', true));
		area.addEventListener('pointerleave', () => hold('hover', false));
	});
	root.addEventListener('focusin', () => hold('focus', true));
	root.addEventListener('focusout', (event) => {
		if (!root.contains(event.relatedTarget as Node | null)) hold('focus', false);
	});
	document.addEventListener('visibilitychange', () => hold('hidden', document.hidden));

	root.addEventListener('keydown', (event) => {
		if (!(event.target as HTMLElement).closest('[data-carousel-controls]')) return;
		if (event.key === 'ArrowLeft') show(current - 1, true);
		if (event.key === 'ArrowRight') show(current + 1, true);
	});

	// Horizontal swipe on touch screens; vertical movement still scrolls the page.
	let startX = 0;
	let startY = 0;
	root.addEventListener('pointerdown', (event) => {
		if (event.pointerType === 'mouse') return;
		startX = event.clientX;
		startY = event.clientY;
	});
	root.addEventListener('pointerup', (event) => {
		if (event.pointerType === 'mouse') return;
		const dx = event.clientX - startX;
		if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(event.clientY - startY)) show(current + (dx < 0 ? 1 : -1), true);
	});

	show(0);
}
