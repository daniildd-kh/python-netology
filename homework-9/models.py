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
