import { templateSearchIndex } from '../../data/templates';

/** Search index for the catalog search box, shared by both languages. */
export const GET = () => new Response(JSON.stringify(templateSearchIndex()), { headers: { 'Content-Type': 'application/json' } });
