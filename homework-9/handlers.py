import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse


ALLOWED_PRIORITIES = {"low", "normal", "high"}


class TaskHandler(BaseHTTPRequestHandler):
    store = None

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/tasks":
            tasks = [task.to_dict() for task in self.store.list_tasks()]
            self._send_json(200, tasks)
            return
        self._send_status(404)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/tasks":
            payload = self._read_json()
            if not isinstance(payload, dict):
                self._send_status(400)
                return
            if "title" not in payload or "priority" not in payload:
                self._send_status(400)
                return
            title = payload["title"]
            priority = payload["priority"]
            if priority not in ALLOWED_PRIORITIES:
                self._send_status(400)
                return
            task = self.store.create_task(title=title, priority=priority)
            self._send_json(200, task.to_dict())
            return

        parts = parsed.path.strip("/").split("/")
        if len(parts) == 3 and parts[0] == "tasks" and parts[2] == "complete":
            try:
                task_id = int(parts[1])
            except ValueError:
                self._send_status(404)
                return
            if self.store.complete_task(task_id):
                self._send_status(200)
            else:
                self._send_status(404)
            return

        self._send_status(404)

    def _read_json(self):
        length = self.headers.get("Content-Length")
        if length is None:
            return None
        try:
            size = int(length)
        except ValueError:
            return None
        try:
            raw = self.rfile.read(size)
        except OSError:
            return None
        try:
            return json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None

    def _send_json(self, status, data):
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _send_status(self, status):
        self.send_response(status)
        self.end_headers()
