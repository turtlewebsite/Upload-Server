from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import cgi

class UploadHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()

            file_list = os.listdir('.')
            html_content = "<html><head><title>File Upload</title></head><body>"
            html_content += "<h1>File Upload</h1>"
            html_content += '<form action="/" method="post" enctype="multipart/form-data">'
            html_content += '<label for="file">Choose a file:</label>'
            html_content += '<input type="file" id="file" name="file" required>'
            html_content += '<button type="submit">Upload</button>'
            html_content += '</form>'

            html_content += "<h2>Files in Directory:</h2><ul>"
            for file in file_list:
                file_path = os.path.join('.', file)
                if os.path.isfile(file_path):
                    html_content += f'<li><a href="{file}">{file}</a></li>'
            html_content += "</ul></body></html>"

            self.wfile.write(html_content.encode())
        else:
            # Serve the requested file if it exists
            if os.path.exists(self.path.strip("/")) and os.path.isfile(self.path.strip("/")):
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.end_headers()
                with open(self.path.strip("/"), "rb") as file:
                    self.wfile.write(file.read())
            else:
                self.send_error(404, "File not found")

    def do_POST(self):
        content_type, params = cgi.parse_header(self.headers.get('Content-Type'))
        if content_type == 'multipart/form-data':
            form_data = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            file_field = form_data["file"]
            if file_field.filename:
                file_path = os.path.join('.', file_field.filename)
                with open(file_path, 'wb') as output_file:
                    output_file.write(file_field.file.read())
                
                # basically refreshing after you upload
                self.send_response(303)  
                self.send_header("Location", "/")
                self.end_headers()
                return

        self.send_response(400)
        self.end_headers()
        self.wfile.write(b"Invalid request!")
#hosting
if __name__ == "__main__":
    port = 8000
    server = HTTPServer(('0.0.0.0', port), UploadHandler)
    print(f"Starting server on port {port}...")
    server.serve_forever()