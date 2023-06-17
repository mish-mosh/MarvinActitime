from dataclasses import dataclass

import yaml

from domain.task import Task
from settings import PINNED_TASKS_YAML_PATH


@dataclass
class YamlPinnedTask:
    title: str
    actitime_uri: str

    def to_task(self) -> Task:
        actitime_id = self.actitime_uri.split("/tasks/tasklist.do?taskId=")[1]

        return Task(self.title, [], actitime_id=actitime_id)


class PinnedTasksYamlAdapter:
    path = PINNED_TASKS_YAML_PATH

    def gett_all(self) -> list[Task]:
        try:
            with open(self.path, "r") as file:
                pinned_tasks = yaml.load(file, Loader=yaml.FullLoader)
                return [YamlPinnedTask(**task).to_task() for task in pinned_tasks]
        except FileNotFoundError:
            return []
