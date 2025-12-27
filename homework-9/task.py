import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse


TASKS_FILE = Path(__file__).with_name("tasks.txt")
ALLOWED_PRIORITIES = {"low", "normal", "high"}


class Task:
    def __init__(self, task_id, title, priority, is_done=False):
        self.id = task_id
        self.title = title
        self.priority = priority
        self.is_done = is_done

    def to_dict(self):
        return {
            "title": self.title,
            "priority": self.priority,
            "isDone": self.is_done,
            "id": self.id,
        }

    @staticmethod
    def from_dict(data):
        return Task(
            task_id=int(data["id"]),
            title=str(data["title"]),
            priority=str(data["priority"]),
            is_done=bool(data["isDone"]),
        )


class TaskStore:
    def __init__(self, file_path):
        self._file_path = file_path
        self._tasks = []
        self._next_id = 1
        self._load()

    def _load(self):
        if not self._file_path.exists():
            return
        try:
            with self._file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError):
            return
        tasks = []
        max_id = 0
        for item in data if isinstance(data, list) else []:
            try:
                task = Task.from_dict(item)
            except (KeyError, TypeError, ValueError):
                continue
            tasks.append(task)
            max_id = max(max_id, task.id)
        self._tasks = tasks
        self._next_id = max_id + 1

    def _save(self):
        data = [task.to_dict() for task in self._tasks]
        with self._file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file)

    def list_tasks(self):
        return list(self._tasks)

    def create_task(self, title, priority):
        task = Task(
            task_id=self._next_id, title=title, priority=priority, is_done=False
        )
        self._next_id += 1
        self._tasks.append(task)
        self._save()
        return task

    def complete_task(self, task_id):
        task = self._find_task(task_id)
        if task is None:
            return False
        task.is_done = True
        self._save()
        return True

    def _find_task(self, task_id):
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None


class TaskHandler(BaseHTTPRequestHandler):

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
            if not payload or "title" not in payload or "priority" not in payload:
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


def run_server(host="127.0.0.1", port=8000):
    TaskHandler.store = TaskStore(TASKS_FILE)
    server = HTTPServer((host, port), TaskHandler)
    print(f"Сервер запущен на http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
