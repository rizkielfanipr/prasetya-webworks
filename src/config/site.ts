/** Site-wide constants. Change them here instead of searching the components. */
export const site = {
	name: 'Prasetya Webworks',
	email: 'hello@prasetyawebworks.com',
	/** WhatsApp number that receives orders and questions, international format without "+". */
	whatsapp: '628995449805',
	/** Logo for light backgrounds, and the white-text version for dark ones (see docs/design.md). */
	logo: '/images/prasetya-webworks-logo.svg',
	logoOnDark: '/images/prasetya-webworks-logo-white.svg',
	/** 1200×630 preview image for search results and shared links (Open Graph). */
	ogImage: '/images/og-image.png',
	/** Square raster logo for structured data; Google does not use the SVG wordmark there. */
	logoSquare: '/favicon.png',
	/** Social profiles shown in the footer, in this order. Placeholders: replace with the real profile URLs before deploying. */
	social: [
		{ network: 'Instagram', icon: 'fa-instagram', url: 'https://www.instagram.com/' },
		{ network: 'TikTok', icon: 'fa-tiktok', url: 'https://www.tiktok.com/' },
		{ network: 'Facebook', icon: 'fa-facebook-f', url: 'https://www.facebook.com/' },
		{ network: 'LinkedIn', icon: 'fa-linkedin-in', url: 'https://www.linkedin.com/' },
	],
	/** Satamu, the digital invitation brand, promoted by the floating button above WhatsApp. */
	satamu: { url: 'https://satamu.prasetyawebworks.web.id', mark: '/images/satamu-mark.svg' },
	/** WordPress Multisite that hosts the live template demos (see docs/wordpress-preview.md). */
	previewBaseUrl: 'https://preview.prasetyawebworks.web.id',
} as const;
