<?php
/**
 * Plugin Name: Network Noindex
 * Description: Keeps every site in the preview network out of search engines, including sites created later.
 *
 * Upload manually to public_html/preview.prasetyawebworks.web.id/wp-content/mu-plugins/
 */

defined( 'ABSPATH' ) || exit;

// Same effect as ticking "Discourage search engines" on every site:
// adds <meta name="robots" content="noindex, nofollow"> to every page.
add_filter( 'pre_option_blog_public', '__return_zero' );
