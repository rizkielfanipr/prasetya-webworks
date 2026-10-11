// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
	i18n: {
		locales: ['id', 'en'],
		defaultLocale: 'id',
		routing: {
			prefixDefaultLocale: false,
		},
	},
});
