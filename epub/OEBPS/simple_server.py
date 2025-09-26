from http.server import HTTPServer, SimpleHTTPRequestHandler
import mimetypes

class XHTMLHandler(SimpleHTTPRequestHandler):
    def guess_type(self, path):
        if path.endswith('.xhtml'):
            return 'application/xhtml+xml'
        return super().guess_type(path)

if __name__ == '__main__':
    # Ensure .xhtml files are served with correct MIME type
    mimetypes.add_type('application/xhtml+xml', '.xhtml')
    
    # Start server
    server_address = ('', 8090)
    httpd = HTTPServer(server_address, XHTMLHandler)
    print('Server running at http://localhost:8090')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down server...')
        httpd.shutdown()
