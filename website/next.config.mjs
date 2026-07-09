import { createMDX } from 'fumadocs-mdx/next';

const withMDX = createMDX();

// GitHub Pages serves a project site under /<repo>. Set the base path so links
// and assets resolve there. Override with PAGES_BASE_PATH (empty for a user or
// custom domain site, where the site is served from the domain root).
const basePath =
  process.env.PAGES_BASE_PATH ?? '/interoperability-data-model';

/** @type {import('next').NextConfig} */
const config = {
  output: 'export',
  reactStrictMode: true,
  basePath,
  // Emit dir/index.html so GitHub Pages serves clean URLs reliably.
  trailingSlash: true,
  images: { unoptimized: true },
  // This app has its own lockfile; pin the workspace root to silence the
  // multiple-lockfile inference warning.
  turbopack: { root: import.meta.dirname },
};

export default withMDX(config);
