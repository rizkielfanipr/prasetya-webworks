/** @type {import('stylelint').Config} */
export default {
	extends: ['stylelint-config-recommended'],
	overrides: [{ files: ['**/*.astro'], customSyntax: 'postcss-html' }],
	rules: {
		// One rule per selector: change the existing rule instead of adding a second one.
		'no-duplicate-selectors': true,
		'declaration-block-no-duplicate-properties': true,
		// Safari iOS clips filter: blur() to a square inside rounded, overflow-hidden containers. Use radial-gradient.
		'declaration-property-value-disallowed-list': { filter: ['/blur\\(/'] },
		// Scoped component styles make specificity order across components irrelevant.
		'no-descending-specificity': null,
		// Astro's :global() is allowed, but prefer src/styles/global.css (see docs/development.md).
		'selector-pseudo-class-no-unknown': [true, { ignorePseudoClasses: ['global'] }],
	},
};
