"""Unit tests for the execution plane's health-only shell (standard library unittest)."""

import importlib
import json
import os
import sys
import threading
import unittest

_SRC = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "src"
)
if not sys.path or sys.path[0] != _SRC:
    sys.path.insert(0, _SRC)

_MODULES = ("planeon_execution", "planeon_execution.health", "planeon_execution.health.app")


def _fresh_import():
    for name in _MODULES:
        sys.modules.pop(name, None)
    return importlib.import_module("planeon_execution.health")


def _call(app, method, path):
    captured = {}

    def start_response(status, headers, exc_info=None):
        captured["status"] = status
        captured["headers"] = headers

    environ = {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
        "SERVER_NAME": "localhost",
        "SERVER_PORT": "0",
        "wsgi.url_scheme": "http",
    }
    body = b"".join(app(environ, start_response))
    return captured["status"], dict(captured["headers"]), body


class HealthShellTest(unittest.TestCase):
    def test_import_starts_no_thread(self):
        before = threading.active_count()
        _fresh_import()
        self.assertEqual(threading.active_count(), before)

    def test_health_mapping_is_exact(self):
        health = _fresh_import().health
        self.assertEqual(health(), {"status": "ok", "plane": "execution"})

    def test_get_health_answers_200_json(self):
        app = _fresh_import().application
        status, headers, body = _call(app, "GET", "/health")
        self.assertEqual(status, "200 OK")
        self.assertEqual(headers["Content-Type"], "application/json")
        self.assertEqual(json.loads(body.decode("utf-8")), {"status": "ok", "plane": "execution"})

    def test_other_path_answers_404(self):
        app = _fresh_import().application
        status, headers, body = _call(app, "GET", "/missing")
        self.assertEqual(status.split()[0], "404")
        self.assertNotIn(b"missing", body)

    def test_post_health_answers_405(self):
        app = _fresh_import().application
        status, headers, body = _call(app, "POST", "/health")
        self.assertEqual(status.split()[0], "405")
        self.assertNotIn(b"POST", body)


if __name__ == "__main__":
    unittest.main()
