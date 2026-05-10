import os
import sys

import tornado.autoreload
from livereload import Server

from src import create_app
from src.utils.helpers import get_watch_patterns

app = create_app("development")

if __name__ == "__main__":
    # Register os.execv() before livereload adds its broken IOLoop.close() hook.
    # When tornado detects a .py change, our hook runs first and replaces the
    # process cleanly — the livereload hook never executes, avoiding the
    # "Cannot close a running event loop" crash on Python 3.11+.
    tornado.autoreload.add_reload_hook(lambda: os.execv(sys.executable, [sys.executable] + sys.argv))

    server = Server(app.wsgi_app)

    for pattern in get_watch_patterns():
        server.watch(pattern)

    server.serve(
        host=app.config["HOST"],
        port=int(app.config["PORT"]),
        liveport=35729,
        debug=True,
    )
