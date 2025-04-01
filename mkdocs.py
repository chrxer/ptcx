#!.venv/bin/python3

from pathlib import Path
import http.server
import socketserver
import webbrowser
from threading import Thread

from sphinx.cmd.build import build_main

CWD = Path(__file__).parent
HTML=CWD.joinpath("htmldocs/")
PORT = 8080


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=HTML, **kwargs)
    def log_message(self, format, *args):
        pass

def serve():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
            httpd.serve_forever()



if __name__ == "__main__":
    build_main(["-b", "html", str(CWD.joinpath("docs/")), str(HTML)])
    if __debug__:
        thread = Thread(target=serve)
        thread.start()
        url = f"http://localhost:{PORT}"
        print(f"serving docs on {url}")
        webbrowser.open_new_tab(url)
        thread.join()