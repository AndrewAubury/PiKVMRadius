#!/usr/bin/env python3


from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import radius
import json 

class S(BaseHTTPRequestHandler):
    def _set_response(self, response_code=403): # 403 is the default to ensure a fail secure
        self.send_response(response_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response(response_code=404)
        self.wfile.write("This server does not support GET at this route".encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        #logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
        #        str(self.path), str(self.headers), post_data.decode('utf-8'))
        post_data = post_data.decode('utf-8')
        post_data = json.loads(post_data)
        username = post_data["user"]
        password = post_data["passwd"]
        secret = post_data["secret"]
        logging.info("Attempting to login as "+username);
        
        r = radius.Radius(secret, host='10.0.0.150', port=1812)

        if r.authenticate(username, password):
            self._set_response(response_code=200)
        else:
            self._set_response(response_code=403)
        
        self.wfile.write("Auth response.".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=6930):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...'+str(port)+'\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=6930)
    else:
        run()
