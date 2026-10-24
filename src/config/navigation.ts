import { content, type Locale } from '../i18n/content';

/** Home section links shared by the header and footer, in the order the sections appear on the page. */
export function navLinks(locale: Locale, showPartners = false) {
	const t = content[locale].nav;
	return [
		...(showPartners ? [{ hash: '#partners', label: t.partners }] : []),
		{ hash: '#templates', label: t.templates },
		{ hash: '#process', label: t.process },
		{ hash: '#packages', label: t.packages },
		{ hash: '#faq', label: t.faq },
	];
}
