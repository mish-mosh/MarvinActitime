import datetime
from dataclasses import dataclass
from typing import Optional

from domain.time_duration import TimeDuration


@dataclass
class ActitimeTrackingEntry:
    date: datetime.date
    task_id: str
    minutes: int
    comment: Optional[str]

    def to_time_duration(self) -> TimeDuration:
        return TimeDuration.of(
            datetime.datetime.combine(self.date, datetime.datetime.now().time()),
            datetime.timedelta(minutes=self.minutes),
        )
