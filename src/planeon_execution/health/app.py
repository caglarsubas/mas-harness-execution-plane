"""Health-only shell of the execution plane.

Standard library only. Importing this module starts no thread, socket,
subprocess or listener, and reads no environment variable or file.
"""

import json

__all__ = ["application", "health"]

_HEALTH_PATH = "/health"
_JSON = "application/json"


def health():
    """Return the plane's health mapping (a new dict on every call)."""
    return {"status": "ok", "plane": "execution"}


def _respond(start_response, status, payload, extra_headers=()):
    body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    headers = [("Content-Type", _JSON), ("Content-Length", str(len(body)))]
    headers.extend(extra_headers)
    start_response(status, headers)
    return [body]


def application(environ, start_response):
    """WSGI callable: GET /health answers 200 with health() as JSON.

    Any other path answers 404 and any other method on /health answers 405.
    No response echoes any part of the request.
    """
    path = environ.get("PATH_INFO", "")
    method = environ.get("REQUEST_METHOD", "")
    if path != _HEALTH_PATH:
        return _respond(start_response, "404 Not Found", {"error": "not_found"})
    if method != "GET":
        return _respond(
            start_response,
            "405 Method Not Allowed",
            {"error": "method_not_allowed"},
            (("Allow", "GET"),),
        )
    return _respond(start_response, "200 OK", health())
