import catalog from './templates.json';
import livePreviews from './live-previews.json';
import { content, type Locale } from '../i18n/content';

export type TemplateItem = (typeof catalog)[number];
export type TemplateCategory = keyof typeof content.id.templateCategories;

/** WordPress demo for a template, if its code is listed in live-previews.json. */
export const livePreviewUrl = (item: TemplateItem) =>
	livePreviews.includes(item.code) ? `https://preview.prasetyawebworks.web.id/template-${item.code}/` : undefined;

// Templates with a live demo come first within their category, so visitors see them before screenshot-only ones.
export const templates: TemplateItem[] = [...catalog].sort((a, b) => Number(!livePreviewUrl(a)) - Number(!livePreviewUrl(b)));

/** Categories in tab order, limited to those that have at least one template. */
export const templateCategories = (Object.keys(content.id.templateCategories) as TemplateCategory[])
	.filter((key) => templates.some((item) => item.category === key));

export const templatesIn = (category?: TemplateCategory) =>
	category ? templates.filter((item) => item.category === category) : templates;

/** Round-robin across categories so an unfiltered list opens with a varied mix. */
export const interleaveByCategory = (items: TemplateItem[]) => {
	const groups = templateCategories.map((key) => items.filter((item) => item.category === key));
	return Array.from({ length: Math.max(0, ...groups.map((group) => group.length)) }, (_, round) => groups.map((group) => group[round]))
		.flat()
		.filter((item) => item !== undefined);
};

export const homePath = (locale: Locale) => (locale === 'id' ? '/' : '/en/');

export const catalogPath = (locale: Locale, category?: TemplateCategory) =>
	`${locale === 'id' ? '' : '/en'}/templates/${category ? `${category}/` : ''}`;

/** Sends the visitor to the home contact form, which pre-fills the message from these params. */
export const templateRequestPath = (locale: Locale, item: TemplateItem) =>
	`${homePath(locale)}?${new URLSearchParams({ template: item.code, name: item.name })}#contact`;
