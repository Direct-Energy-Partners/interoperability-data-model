import { createMDX } from 'fumadocs-mdx/next';

const withMDX = createMDX();

// GitHub Pages needs a static export served under /<repo>. Vercel serves the
// app natively at the domain root. Gate the Pages-specific settings behind
// PAGES_DEPLOY (set in .github/workflows/docs.yml) so a Vercel build gets a
// clean, default Next.js app with no basePath.
const isPagesDeploy = process.env.PAGES_DEPLOY === 'true';

// For a Pages project site the base path is /<repo>. Override with
// PAGES_BASE_PATH (empty for a user site or custom domain served from root).
const pagesConfig = isPagesDeploy
  ? {
      output: 'export',
      basePath: process.env.PAGES_BASE_PATH ?? '/interoperability-data-model',
      trailingSlash: true,
      images: { unoptimized: true },
    }
  : {};

/** @type {import('next').NextConfig} */
const config = {
  reactStrictMode: true,
  // This app has its own lockfile; pin the workspace root to silence the
  // multiple-lockfile inference warning.
  turbopack: { root: import.meta.dirname },
  ...pagesConfig,
};

export default withMDX(config);
