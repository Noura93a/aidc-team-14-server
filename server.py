"""A tiny HTTP server. Standard library only: nothing to install.

Every file in routes/ that defines PATH and handle() becomes an endpoint.
Add your own file. Do not edit this one.
"""
import importlib.util, json, pathlib
from http.server import BaseHTTPRequestHandler, HTTPServer

def load_routes():
    routes = {}
    for f in sorted(pathlib.Path(__file__).parent.glob("routes/*.py")):
        if f.name.startswith("_"):
            continue
        spec = importlib.util.spec_from_file_location(f.stem, f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if hasattr(mod, "PATH") and hasattr(mod, "handle"):
            routes[mod.PATH] = mod.handle
    return routes

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        routes = load_routes()
        if self.path == "/":
            self.reply(200, {"endpoints": sorted(routes) + ["/"]})
        elif self.path in routes:
            self.reply(200, routes[self.path]())
        else:
            self.reply(404, {"error": "no such path", "try": sorted(routes)})

    def reply(self, code, body):
        payload = json.dumps(body, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, fmt, *args):
        print("  %s" % (fmt % args))

if __name__ == "__main__":
    print("listening on 0.0.0.0:8000")
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
