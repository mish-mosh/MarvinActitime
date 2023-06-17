import datetime

import couchdb

from adapter.marvin.marvin_task import MarvinTask
from adapter.marvin.utils import datetime_to_marvin_timestamp
from domain.task import Task
from settings import (
    MARVIN_SYNC_DATABASE,
    MARVIN_CONNECTION_STRING,
)


class MarvinAdapter:
    """
    Reference:
    - https://github.com/amazingmarvin/MarvinAPI/wiki/Marvin-Data-Types
    - https://github.com/amazingmarvin/MarvinAPI/wiki/Database-Access
    - https://docs.couchdb.org/en/stable/api/database/find.html

    """

    _marvin_connection_string = MARVIN_CONNECTION_STRING
    _marvin_db_name = MARVIN_SYNC_DATABASE

    def __init__(self):
        self._db = None

    def _get_db(self) -> couchdb.Database:
        """
        Initiates the DB connection to Marvin only at the first request/query
        Note: Always use this to implement marvin features within this adapter
        :return: couchdb.DataBase instance of Marvin
        """
        if self._db is None:
            server = couchdb.Server(self._marvin_connection_string)
            self._db = server[self._marvin_db_name]

        return self._db

    def find_tracked_tasks_for_date(self, date: datetime.date) -> list[Task]:
        start_of_day = datetime.datetime.combine(date, datetime.time.min)
        mango_query = {
            "selector": {
                "db": "Tasks",
                "times": {
                    "$elemMatch": {"$gt": datetime_to_marvin_timestamp(start_of_day)}
                },
            },
            "fields": [
                "_id",
                "_rev",
                "title",
                "createdAt",
                "parentId",
                "times",
                "note",
            ],
        }

        rows = self._get_db().find(mango_query=mango_query)

        return [
            MarvinTask(
                row.get("_id"),
                row.get("_rev"),
                row.get("createdAt"),
                row.get("title"),
                row.get("parentId"),
                row.get("times"),
                row.get("note", None),
            ).to_task()
            for row in rows
        ]

    def find_categories(self) -> list[couchdb.Document]:
        mango_query = {
            "selector": {
                "db": "SmartLists",
            },
        }
        return [doc for doc in self._get_db().find(mango_query=mango_query)]

    def round_to_fifteen_minutes(self, task: Task, date: datetime.date) -> None:
        task.round_tracked_durations_for_date(date)
        new_times = [
            datetime_to_marvin_timestamp(time)
            for duration in task.tracked_durations
            for time in [duration.start_time, duration.end_time]
        ]

        now_marvin_formatted = datetime_to_marvin_timestamp(datetime.datetime.now())

        db_task = self._get_db().get(task.marvin_id)

        db_task["times"] = new_times
        db_task["duration"] = task.total_tracked().total_microseconds

        db_task["updatedAt"] = now_marvin_formatted
        field_updates = db_task["fieldUpdates"]
        field_updates.update(
            {"times": now_marvin_formatted, "updatedAt": now_marvin_formatted}
        )
        db_task["fieldUpdates"] = field_updates

        self._get_db().save(db_task)


if __name__ == "__main__":
    marvin_adapter = MarvinAdapter()

    # res = marvin_adapter.eshi()
    # print(res)
    #
    # today = datetime.date.today() - datetime.timedelta(days=1)
    # tasks = marvin_adapter.find_tracked_tasks_for_date(today)
    # print("Tracked tasks today")
    # for task in tasks:
    #     print(
    #         f"- {task.title} (today {task.tracked_for_date(today)} tracked - overall {task.total_tracked})"
    #     )
    #     print()
