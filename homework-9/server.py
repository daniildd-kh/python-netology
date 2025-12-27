from http.server import HTTPServer
from pathlib import Path

from handlers import TaskHandler
from storage import TaskStore


TASKS_FILE = Path(__file__).with_name("tasks.txt")


def run_server(host="127.0.0.1", port=8000):
    TaskHandler.store = TaskStore(TASKS_FILE)
    server = HTTPServer((host, port), TaskHandler)
    print(f"Сервер запущен на http://{host}:{port}")
    server.serve_forever()
