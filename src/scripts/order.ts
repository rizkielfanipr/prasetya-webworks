/** Keeps only the name part of what the visitor typed as a domain ("https://www.Kopi Budi.com" → "kopibudi"). */
export function domainName(typed: string) {
	return typed
		.trim()
		.toLowerCase()
		.replace(/\s+/g, '')
		.replace(/^https?:\/\//, '')
		.replace(/^www\./, '')
		.split('.')[0];
}

/** WhatsApp order summary: a greeting, a blank line, then one "Label: value" line per row ("-" when empty). */
export function orderMessage(greeting: string, rows: [label: string, value: string][]) {
	return [greeting, '', ...rows.map(([label, value]) => `${label}: ${value.trim() || '-'}`)].join('\n');
}
