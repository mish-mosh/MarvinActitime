import datetime

import requests

from adapter.actitime.actitime_tracking_entry import ActitimeTrackingEntry
from domain.time_duration import TimeDuration
from settings import (
    ACTITIME_BASE_URI,
    ACTITIME_USERNAME,
    ACTITIME_CREDENTIALS,
    ACTITIME_USER_ID,
)


class ActitimeAdapter:
    actitime_date_format = "%Y-%m-%d"
    _actitime_base_uri = ACTITIME_BASE_URI
    _actitime_headers = {"authorization": f"Basic {ACTITIME_CREDENTIALS}"}

    def get_accounted_time_by(
        self, task_id: str, date=datetime.date.today()
    ) -> TimeDuration:
        uri = "/".join(
            [
                self._actitime_base_uri,
                "timetrack",
                ACTITIME_USERNAME,
                date.strftime(self.actitime_date_format),
                task_id,
            ]
        )
        response = requests.get(
            uri,
            headers=self._actitime_headers,
        )
        assert (
            response.status_code == 200
        ), f"Couldn't get accounted time for task {task_id}, code {response.status_code} - reason {response.reason} - message {response.content}"

        data = response.json()

        return ActitimeTrackingEntry(
            date, task_id, data.get("time", 0), data.get("comment", "")
        ).to_time_duration()

    def get_accounted_time_for_date(self, date=datetime.date.today()) -> TimeDuration:
        uri = "/".join([self._actitime_base_uri, "timetrack"])
        formatted_date = date.strftime(self.actitime_date_format)
        params = {
            "userIds": ACTITIME_USER_ID,
            "dateFrom": formatted_date,
        }
        response = requests.get(uri, headers=self._actitime_headers, params=params)
        assert (
            response.status_code == 200
        ), f"Couldn't get accounted time for {formatted_date}, code {response.status_code} - {response.reason} {response.content}"

        records = response.json().get("data", dict())[0].get("records", [])

        return TimeDuration.add_all(
            [
                ActitimeTrackingEntry(
                    date,
                    record.get("taskId"),
                    record.get("time", 0),
                    record.get("comment", ""),
                ).to_time_duration()
                for record in records
            ]
        )

    def account_time(
        self,
        task_id: str,
        time_duration: TimeDuration,
        comment: str = None,
        update_time: bool = True,
    ) -> None:
        if not task_id:
            raise ValueError("No actitime taskId")

        updated_duration = (
            time_duration.add(
                self.get_accounted_time_by(task_id, time_duration.start_time)
            )
            if update_time
            else time_duration
        )
        req_body = {"time": updated_duration.total_minutes}
        if comment is not None:
            req_body["comment"] = comment

        uri = "/".join(
            [
                self._actitime_base_uri,
                "timetrack",
                ACTITIME_USERNAME,
                time_duration.start_time.strftime(self.actitime_date_format),
                task_id,
            ]
        )

        response = requests.patch(
            uri,
            headers=self._actitime_headers,
            json=req_body,
        )
        assert (
            response.status_code == 200
        ), f"Couldn't account time for task {task_id}, code {response.status_code} - reason {response.reason} - message {response.content}"

        assert (
            response.json().get("time", 0) == updated_duration.total_minutes
        ), f"Accounted duration for task {task_id} did not match!"


if __name__ == "__main__":
    adapter = ActitimeAdapter()
    today = datetime.date.today()
    # time_duration = adapter.get_accounted_time_by("55147", today)
    # print(time_duration)

    # adapter.account_time_for(
    #     "55147",
    #     TimeDuration.of(
    #         datetime.date.today(),
    #     ),
    # )

    duration = adapter.get_accounted_time_for_date(today)
    print(duration)
