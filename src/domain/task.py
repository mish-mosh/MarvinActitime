import datetime
from dataclasses import dataclass
from typing import Optional

from domain.exceptions import InvalidTaskException
from domain.time_duration import TimeDuration


@dataclass
class Task:
    title: str
    tracked_durations: list[TimeDuration]
    marvin_id: Optional[str] = None
    actitime_id: Optional[str] = None

    def __post_init__(self):
        if self.marvin_id is None and self.actitime_id is None:
            raise InvalidTaskException("Either marvin_id or actitime_id must be set")

    def total_tracked(self) -> TimeDuration:
        return TimeDuration.add_all(self.tracked_durations)

    def tracked_for_date(self, date: datetime.date) -> TimeDuration:
        return TimeDuration.add_all(
            [
                duration
                for duration in self.tracked_durations
                if duration.start_time.date() == date
            ]
        )

    def round_tracked_durations_for_date(self, date: datetime.date) -> None:
        tracked_for_date = self.tracked_for_date(date)
        difference_duration = (
            tracked_for_date.rounded().total_seconds - tracked_for_date.total_seconds
        )
        if difference_duration == 0:
            return

        for duration in sorted(
            self.tracked_durations, key=lambda d: d.start_time, reverse=True
        ):
            if duration.start_time.date() == date:
                duration.total_seconds += difference_duration
                break
