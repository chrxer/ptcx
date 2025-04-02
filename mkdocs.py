#!.venv/bin/python3

from pathlib import Path
import http.server
import socketserver
import webbrowser
import sys
from threading import Thread
from sphinx.cmd.build import build_main
from ptcx.utils.wrap import exc
from ptcx.utils.fs import writes

CWD = Path(__file__).parent
HTML=CWD.joinpath("htmldocs/")
PORT = 8080


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=HTML, **kwargs)
    def log_message(self, *args):
        pass

def serve():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    usage = exc(sys.executable,"-m", "ptcx", "--help", dbg=False)
    assert usage is not None
    writes(usage, CWD.joinpath("docs/usage.txt"))
    
    build_main(["-b", "html", str(CWD.joinpath("docs/")), str(HTML)])
    if "--debug" in sys.argv:
        thread = Thread(target=serve)
        thread.start()
        url = f"http://localhost:{PORT}" # pylint: disable=invalid-name
        print(f"serving docs on {url}")
        webbrowser.open(url=url)
        thread.join()
