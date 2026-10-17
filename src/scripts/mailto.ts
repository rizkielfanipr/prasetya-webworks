import { site } from '../config/site';

/** Opens the visitor's email app with a prepared message to the business address. */
export function openMailto(subject: string, body: string) {
	window.location.href = `mailto:${site.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}
