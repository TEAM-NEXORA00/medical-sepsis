from http.server import BaseHTTPRequestHandler
import sys
import os

# Add parent directory to path so wardwatch_portal can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from wardwatch_portal import get_portal_html
except ImportError:
    def get_portal_html():
        return "<h1>WardWatch AI Portal Initializing...</h1>"

def app(environ, start_response):
    """WSGI entrypoint for Vercel Serverless Function deployments."""
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/html; charset=utf-8'),
        ('Cache-Control', 'public, max-age=0, must-revalidate')
    ]
    start_response(status, response_headers)
    html = get_portal_html()
    return [html.encode('utf-8')]

# WSGI standard alias
application = app

class handler(BaseHTTPRequestHandler):
    """BaseHTTPRequestHandler entrypoint for Vercel Python runtime."""
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'public, max-age=0, must-revalidate')
        self.end_headers()
        html = get_portal_html()
        self.wfile.write(html.encode('utf-8'))
