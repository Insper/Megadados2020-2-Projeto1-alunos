# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring
import uuid


class DBSession:
    tasks = {}

    def __init__(self):
        self.tasks = DBSession.tasks

    def read_tasks(self, completed=None):
        if completed is None:
            return self.tasks.copy()
        return {
            uuid_: item
            for uuid_, item in self.tasks.items()
            if item.completed == completed
        }

    def create_task(self, item):
        uuid_ = uuid.uuid4()
        self.tasks[uuid_] = item
        return uuid_

    def read_task(self, uuid_):
        return self.tasks[uuid_]

    def replace_task(self, uuid_, item):
        self.tasks[uuid_] = item

    def remove_task(self, uuid_):
        del self.tasks[uuid_]


def get_db():
    return DBSession()
