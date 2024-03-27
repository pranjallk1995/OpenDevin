from typing import List

class Task:
    id: str
    goal: str
    closed: bool
    completed: bool
    subtasks: List[Task]

    def __init__(self, id: str, goal: str, completed: bool = False, subtasks: List = []):
        self.id = id
        self.goal = goal
        self.closed = False
        self.completed = completed
        self.subtasks = subtasks

    def __to_dict__(self):
        return {
            'id': self.id,
            'goal': self.goal,
            'closed': self.closed,
            'completed': self.completed,
            'subtasks': [t.__to_dict__() for t in self.subtasks]
        }

    def close(self, completed=True):
        self.closed = True
        self.completed = completed

class Plan:
    task: Task

    def __init__(self, task: str):
        self.task = Task(id='0', goal=task, completed=False, subtasks=[])

    def get_task_by_id(self, id: str) -> Task:
        try:
            parts = [int(p) for p in id.split('.')]
        except ValueError:
            raise ValueError('Invalid task id:' + id)
        if parts[0] != 0:
            raise ValueError('Invalid task id:' + id)
        parts = parts[1:]
        task = self.task
        for part in parts:
            if part >= len(task.subtasks):
                raise ValueError('Invalid task id:' + id)
            task = task.subtasks[part]
        return task

    def add_subtask(self, parent_id: str, goal: str):
        parent = self.get_task_by_id(parent_id)
        id = parent.id + '.' + str(len(parent.subtasks))
        parent.subtasks.append(Task(id=id, goal=goal))

    def close_task(self, id: str, completed: bool = True):
        task = self.get_task_by_id(id)
        task.close(completed)
