import threading
from wsgiref import simple_server

from url_shortner import app


def before_all(context):
    context.server = simple_server.WSGIServer(('localhost', 8000), simple_server.WSGIRequestHandler)
    context.server.set_app(app)
    context.thread = threading.Thread(target=context.server.serve_forever)
    context.thread.start()


def after_all(context):
    context.server.shutdown()
    context.thread.join()
