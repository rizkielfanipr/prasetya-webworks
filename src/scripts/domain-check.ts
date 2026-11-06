/**
 * Domain availability through RDAP, the registries' public JSON lookup: 200 means registered, 404 means not registered.
 * "Not registered" is only likely available (reserved names exist), so the order is still confirmed by hand.
 */

export type DomainAvailability = 'available' | 'taken' | 'invalid' | 'unknown';

/** Registries of the extensions we sell. Anything else goes through rdap.org, which redirects to the right registry. */
const registries: Record<string, string> = {
	id: 'https://rdap.pandi.id/rdap/',
	com: 'https://rdap.verisign.com/com/v1/',
	net: 'https://rdap.verisign.com/net/v1/',
};

const fallback = 'https://rdap.org/';

/** One label: letters, digits and inner hyphens, at most 63 characters. */
export const validDomainName = (name: string) => /^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$/.test(name);

const cache = new Map<string, DomainAvailability>();

export async function domainAvailability(name: string, extension: string, signal?: AbortSignal): Promise<DomainAvailability> {
	if (!validDomainName(name)) return 'invalid';
	const domain = `${name}${extension}`;
	const cached = cache.get(domain);
	if (cached) return cached;

	const registry = registries[extension.split('.').pop() ?? ''];
	let result: DomainAvailability = 'unknown';
	try {
		// No custom headers, so the browser sends a simple request without a CORS preflight.
		const response = await fetch(`${registry ?? fallback}domain/${domain}`, { signal });
		// rdap.org answers 404 itself for extensions it cannot route, which would wrongly read as available.
		const routed = registry !== undefined || response.redirected;
		if (routed && response.status === 200) result = 'taken';
		if (routed && response.status === 404) result = 'available';
	} catch (error) {
		if (signal?.aborted) throw error;
	}
	// A failed lookup may work on the next try, so only definite answers are kept.
	if (result !== 'unknown') cache.set(domain, result);
	return result;
}
