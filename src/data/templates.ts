import catalog from './templates.json';
import livePreviews from './live-previews.json';
import { content, type Locale } from '../i18n/content';
import { site } from '../config/site';

export type TemplateItem = (typeof catalog)[number];
export type TemplateCategory = keyof typeof content.id.templateCategories;

/** WordPress demo for a template, if its code is listed in live-previews.json. */
export const livePreviewUrl = (item: TemplateItem) =>
	livePreviews.includes(item.code) ? `${site.previewBaseUrl}/template-${item.code}/` : undefined;

// Templates with a live demo come first within their category, so visitors see them before screenshot-only ones.
export const templates: TemplateItem[] = [...catalog].sort((a, b) => Number(!livePreviewUrl(a)) - Number(!livePreviewUrl(b)));

/** Categories in tab order, limited to those that have at least one template. */
export const templateCategories = (Object.keys(content.id.templateCategories) as TemplateCategory[]).filter((key) =>
	templates.some((item) => item.category === key),
);

export const templatesIn = (category?: TemplateCategory) => (category ? templates.filter((item) => item.category === category) : templates);

/** Round-robin across categories so an unfiltered list opens with a varied mix. */
/** Catalog size rounded down to the hundred, for "200+ templates" claims that stay true as the catalog grows. */
export const roundedTemplateCount = () => Math.floor(templates.length / 100) * 100;

export const interleaveByCategory = (items: TemplateItem[]) => {
	const groups = templateCategories.map((key) => items.filter((item) => item.category === key));
	return Array.from({ length: Math.max(0, ...groups.map((group) => group.length)) }, (_, round) => groups.map((group) => group[round]))
		.flat()
		.filter((item) => item !== undefined);
};

export const homePath = (locale: Locale) => (locale === 'id' ? '/' : '/en/');

/** Catalog URL; page 1 lives at the base path, later pages at .../page/<n>/. */
export const catalogPath = (locale: Locale, category?: TemplateCategory, page = 1) =>
	`${locale === 'id' ? '' : '/en'}/templates/${category ? `${category}/` : ''}${page > 1 ? `page/${page}/` : ''}`;

export const CATALOG_PAGE_SIZE = 24;

/** Templates in catalog order: the unfiltered list is interleaved across categories. */
export const catalogItems = (category?: TemplateCategory) => (category ? templatesIn(category) : interleaveByCategory(templates));

export const catalogPageCount = (category?: TemplateCategory) => Math.max(1, Math.ceil(catalogItems(category).length / CATALOG_PAGE_SIZE));

/** Page numbers 2..n for getStaticPaths; page 1 is served by the index route. */
export const laterCatalogPages = (category?: TemplateCategory) =>
	Array.from({ length: catalogPageCount(category) - 1 }, (_, index) => String(index + 2));
