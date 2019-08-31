import flask
from gevent.pywsgi import WSGIServer
import threading
import json

from cosmo import logger

class WebServer:
    def __init__(self, device):
        self.device = device
        self.cosmo = device.cosmo
        self.web = flask.Flask(__name__)

        self.host = "0.0.0.0"
        self.port = 12890

        self.logger = logger.SubLogger("WebSvr")

    def start(self):
        # self.web.run(self.host, self.port)
        self.logger.ok(f"Starting Web Server on '{self.host}:{self.port}'")
        http = WSGIServer((self.host, self.port), self.web.wsgi_app)
        http.serve_forever()

    def start_threaded(self):
        thd = threading.Thread(target=self.start, daemon=True)
        thd.start()
        return thd


def api_response(code=200, success=None, status_msg=None, data=None):
    if success is None:
        success = (code == 200)
    if status_msg is None:
        status_msg = {200: "Request Successful", 400: "Bad Request", 403: "Forbidden", 500: "Server Error",
                      503: "Server/Service/Endpoint Unavailable", 404: "Endpoint Not Found", 409: "Request Conflict",
                      418: "I'm a teapot"}[code]

    msg = {
        "status": {
            "code": code,
            "success": success,
            "msg": status_msg
        },
        "data": data
    }

    return flask.Response(json.dumps(msg), status=code, mimetype="application/json")


def json_response(data, code=200):
    return flask.Response(json.dumps(data), status=code, mimetype="application/json")


def api_error(code, error_msg):
    return api_response(code, False, data={"error": error_msg})
