interface Entry {
	code: string;
	name: string;
	category: string;
	type: string;
	pages: number;
	thumbnail: boolean;
	preview: string | null;
}

const normalize = (text: string) =>
	text
		.toLowerCase()
		.normalize('NFD')
		.replace(/\p{Diacritic}/gu, '');

/**
 * Searches the whole catalog (not just the current page) from the box inside `root`.
 * Matches replace the paginated list; cards are copies of the `[data-card-template]` TemplateCard.
 * Labels come from data-* attributes on `root`; the index is fetched once, on first use.
 */
export function initTemplateSearch(root: HTMLElement) {
	const input = root.querySelector<HTMLInputElement>('input[type="search"]');
	const status = root.querySelector<HTMLElement>('[data-search-status]');
	const results = document.querySelector<HTMLElement>('[data-search-results]');
	const list = document.querySelector<HTMLElement>('[data-catalog-list]');
	const template = document.querySelector<HTMLTemplateElement>('[data-card-template]');
	if (!input || !status || !results || !list || !template) return;

	const label = root.dataset;
	const categories = JSON.parse(label.categories ?? '{}') as Record<string, string>;
	const defaultStatus = status.textContent ?? '';
	let index: Promise<Entry[]> | undefined;
	const load = () => (index ??= fetch(label.indexUrl ?? '').then((response) => response.json() as Promise<Entry[]>));

	function card(entry: Entry) {
		const node = template!.content.firstElementChild!.cloneNode(true) as HTMLElement;
		const text = (hook: string, value: string) => {
			const element = node.querySelector(`[${hook}]`);
			if (element) element.textContent = value;
		};
		node.dataset.category = entry.category;
		text('data-card-code', `#${entry.code}`);
		text('data-card-category', categories[entry.category] ?? '');
		text('data-card-name', entry.name);
		text('data-card-meta', `${entry.type} · ${entry.pages} ${label.pagesLabel}`);

		const image = node.querySelector<HTMLImageElement>('img[data-card-image]');
		if (image && entry.thumbnail) {
			image.src = `/images/templates/${entry.code}.webp`;
			image.alt = (label.thumbAlt ?? '').replace('{name}', entry.name);
		} else if (image) {
			// No screenshot: show the name instead, keeping the card's scoped-style attribute.
			const placeholder = document.createElement('span');
			Array.from(image.attributes)
				.filter((attribute) => attribute.name.startsWith('data-astro-cid'))
				.forEach((attribute) => placeholder.setAttribute(attribute.name, ''));
			placeholder.className = 'template-placeholder';
			placeholder.textContent = entry.name;
			image.replaceWith(placeholder);
		}

		const preview = node.querySelector<HTMLAnchorElement>('[data-card-preview]');
		if (preview && entry.preview) {
			preview.href = entry.preview;
			preview.setAttribute('aria-label', (label.previewLabel ?? '').replace('{name}', entry.name));
		} else preview?.remove();

		const select = node.querySelector<HTMLAnchorElement>('[data-card-select]');
		if (select) select.href = `${label.orderPath}?template=${entry.code}`;
		return node;
	}

	async function run() {
		const query = input!.value.trim();
		if (!query) {
			results!.hidden = true;
			results!.replaceChildren();
			list!.hidden = false;
			status!.textContent = defaultStatus;
			return;
		}
		const entries = await load();
		// Ignore results for a query the visitor has already changed.
		if (query !== input!.value.trim()) return;
		const needle = normalize(query);
		const matches = entries.filter((entry) =>
			normalize(`${entry.name} ${entry.type} ${categories[entry.category] ?? ''} ${entry.code}`).includes(needle),
		);
		results!.replaceChildren(...matches.map(card));
		results!.hidden = matches.length === 0;
		list!.hidden = true;
		status!.textContent = ((matches.length ? label.statusResults : label.statusEmpty) ?? '')
			.replace('{count}', String(matches.length))
			.replace('{query}', query);
	}

	let timer: number | undefined;
	input.addEventListener('input', () => {
		window.clearTimeout(timer);
		timer = window.setTimeout(run, 150);
	});
	input.addEventListener('focus', () => void load(), { once: true });
	root.addEventListener('submit', (event) => {
		event.preventDefault();
		void run();
	});
}
