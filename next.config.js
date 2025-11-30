/** @type {import('next').NextConfig} */
const nextConfig = {
  // Serve static files from epub/OEBPS
  async rewrites() {
    return [
      {
        source: '/epub/:path*',
        destination: '/api/serve/:path*',
      },
    ];
  },
  // Disable strict mode to avoid double rendering
  reactStrictMode: false,
};

module.exports = nextConfig;

