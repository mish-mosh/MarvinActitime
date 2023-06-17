import datetime
from dataclasses import dataclass
from datetime import timedelta
from functools import reduce
from typing import Self


@dataclass
class TimeDuration:
    start_time: datetime.datetime
    total_seconds: int

    MINUTES_ROUND_CAP = 15
    MINUTES_ROUND_MIDDLE = 7
    SECONDS_ROUND_CAP = 100
    REGULAR_WORKDAY_MINUTES = 8 * 60

    @classmethod
    def of(cls, start_time: datetime, td: timedelta) -> Self:
        return TimeDuration(
            start_time,
            int(td.total_seconds()),
        )

    @property
    def end_time(self) -> datetime.datetime:
        return self.start_time + datetime.timedelta(seconds=self.total_seconds)

    @property
    def seconds(self) -> int:
        return int(self.total_seconds % 3600 % 60)

    @property
    def minutes(self) -> int:
        return int((self.total_seconds // 60)) % 60

    @property
    def total_minutes(self) -> int:
        return self.total_seconds // 60

    @property
    def total_microseconds(self) -> int:
        return self.total_seconds * 1000

    @property
    def hours(self) -> int:
        return int(self.total_seconds // 3600)

    def add(self, other: Self) -> Self:
        return self.of(
            self.start_time, timedelta(seconds=self.total_seconds + other.total_seconds)
        )

    @classmethod
    def add_all(cls, time_durations: list[Self]) -> Self:
        if not time_durations:
            return TimeDuration.of(datetime.date.today(), timedelta(0))

        return reduce(cls.add, time_durations)

    def rounded(self) -> Self:
        difference_in_minutes = self.minutes % self.MINUTES_ROUND_CAP
        if difference_in_minutes == 0:
            return self._rounded_to_100_seconds()

        new_total_seconds = self.total_seconds + (
            (
                self.MINUTES_ROUND_CAP - difference_in_minutes
                if difference_in_minutes >= self.MINUTES_ROUND_MIDDLE
                else -difference_in_minutes
            )
            * 60
        )
        return self.of(
            self.start_time, timedelta(seconds=new_total_seconds)
        )._rounded_to_100_seconds()

    def should_be_rounded(self) -> bool:
        return self.total_seconds != self.rounded().total_seconds

    def overtime(self) -> Self:
        return self.of(
            self.start_time,
            timedelta(minutes=self.total_minutes - self.REGULAR_WORKDAY_MINUTES),
        )

    def decimal_repr(self) -> float:
        return self.total_minutes / 60

    def _rounded_to_100_seconds(self) -> Self:
        return self.of(
            self.start_time,
            timedelta(
                seconds=self.total_seconds
                - (self.total_seconds % self.SECONDS_ROUND_CAP)
            ),
        )

    def _to_timedelta(self) -> timedelta:
        return timedelta(seconds=self.total_seconds)

    def __str__(self):
        return f"{self.hours}h {self.minutes}m {self.seconds}s"


if __name__ == "__main__":
    time_duration = TimeDuration.of(
        not datetime.datetime.now(), timedelta(minutes=21, seconds=100)
    ).rounded()
    print(time_duration)
