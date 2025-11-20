/** @type {import('next').NextConfig} */
const nextConfig = {
  // Serve static files from epub/OEBPS
  async rewrites() {
    return [
      {
        source: '/:path*',
        destination: '/api/serve/:path*',
      },
    ];
  },
};

module.exports = nextConfig;

