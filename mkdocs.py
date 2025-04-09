"""""" # pylint: disable=empty-docstring

from pathlib import Path
import http.server
import socketserver
import webbrowser
import sys
import traceback
import logging
from time import perf_counter
from threading import Thread
from sphinx.cmd.build import build_main
from ptcx.utils.wrap import exc, kill_processes_by_port
from ptcx.utils.fs import writes

CWD = Path(__file__).parent
HTML=CWD.joinpath("htmldocs/")


class Handler(http.server.SimpleHTTPRequestHandler):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=HTML, **kwargs)
    def log_message(self, *args):
        pass
    def end_headers(self):
        # Add no-cache headers
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

def serve(start_timeout:float=10,port:int=8080):
    """Serve htmldocs"""
    start = perf_counter()
    while True:
        try:
            with socketserver.TCPServer(("", port), Handler) as httpd:
                httpd.serve_forever()
        except OSError as e:
            kill_processes_by_port(port)
            if (perf_counter()-start)>=start_timeout:
                raise e
        except KeyboardInterrupt:
            logging.error(traceback.format_exc())
            exit(0)
        else:
            break


if __name__ == "__main__":
    usage = exc(sys.executable,"-m", "ptcx", "--help", dbg=False)
    assert usage is not None
    writes(usage, CWD.joinpath("docs/usage.txt"))

    PORT=8080

    build_main(["-b", "html", str(CWD.joinpath("docs/")), str(HTML)])
    if "--debug" in sys.argv:
        thread = Thread(target=serve)
        thread.start()
        url = f"http://localhost:{PORT}" # pylint: disable=invalid-name
        print(f"serving docs on {url}")
        webbrowser.open(url=url)
        thread.join()
