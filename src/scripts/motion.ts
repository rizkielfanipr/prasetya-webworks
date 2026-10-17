export const prefersReducedMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/** Calls `update` at most once per animation frame while the page scrolls, and once immediately. */
export function onScrollFrame(update: () => void) {
	let frame: number | null = null;
	window.addEventListener(
		'scroll',
		() => {
			if (frame !== null) return;
			frame = window.requestAnimationFrame(() => {
				update();
				frame = null;
			});
		},
		{ passive: true },
	);
	update();
}
