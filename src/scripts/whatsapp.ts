import { site } from '../config/site';

/** Link to a WhatsApp chat with the business number and a prepared message. Safe to use at build time. */
export function whatsappUrl(message: string) {
	return `https://wa.me/${site.whatsapp}?text=${encodeURIComponent(message)}`;
}

/** Opens a WhatsApp chat with a prepared message, in a new tab when allowed. */
export function openWhatsApp(message: string) {
	const url = whatsappUrl(message);
	const tab = window.open(url, '_blank');
	if (tab) tab.opener = null;
	else window.location.href = url;
}
