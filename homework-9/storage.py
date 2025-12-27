import json

from models import Task


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
        task = Task(task_id=self._next_id, title=title, priority=priority, is_done=False)
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
