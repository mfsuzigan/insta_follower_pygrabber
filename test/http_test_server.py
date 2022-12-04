from http.server import BaseHTTPRequestHandler, HTTPServer

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()

        response = None
        outputsByPath = {"/": "1", "/?max_id=100": "2", "/?max_id=200": "3"}
        outputFile = "test/mock_response{}.json".format(outputsByPath[self.path])

        with open(outputFile) as file:
            response = file.read()

        self.wfile.write(bytes(response, "utf8"))

with HTTPServer(('', 8000), handler) as server:
    server.serve_forever()