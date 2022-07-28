
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def write_response(self, content):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(content)
        print(self.headers)
        print(content.decode('utf-8'))

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self.write_response(b'aaa')
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s",
                str(self.path), str(self.headers), post_data.decode('utf-8'),)
        body=post_data.decode('utf-8')

        if body.startswith('{'):
            localjson= json.loads(body)  
            print(f"as i have{localjson}")

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
       run()
# from http.server import HTTPServer, BaseHTTPRequestHandler
# from sys import argv

# BIND_HOST = 'localhost'
# PORT = 8080


# class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         self.write_response(b'aaa')

#     def do_POST(self):
#         content_length = int(self.headers.get('content-length', 0))
#         body = self.rfile.read(content_length)

#         self.write_response(body)

#     def write_response(self, content):
#         self.send_response(200)
#         self.end_headers()
#         self.wfile.write(content)

#         print(self.headers)
#         print(content.decode('utf-8'))


# if len(argv) > 1:
#     arg = argv[1].split(':')
#     BIND_HOST = arg[0]
#     PORT = int(arg[1])

# print(f'Listening on http://{BIND_HOST}:{PORT}\n')

# httpd = HTTPServer((BIND_HOST, PORT), SimpleHTTPRequestHandler)
# httpd.serve_forever()