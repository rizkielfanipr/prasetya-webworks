// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
	// Production URL: used for canonical links, Open Graph URLs and the sitemap.
	site: 'https://prasetyawebworks.web.id',
	integrations: [
		sitemap({
			i18n: {
				defaultLocale: 'id',
				locales: { id: 'id-ID', en: 'en-US' },
			},
		}),
	],
	i18n: {
		locales: ['id', 'en'],
		defaultLocale: 'id',
		routing: {
			prefixDefaultLocale: false,
		},
	},
});
