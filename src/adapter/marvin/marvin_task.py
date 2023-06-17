import re
from dataclasses import dataclass
from typing import Optional

from adapter.marvin.utils import parse_marvin_timestamp
from domain.task import Task
from domain.time_duration import TimeDuration


@dataclass
class MarvinTask:
    _id: str
    _rev: str
    created_at: int
    title: str
    parent_id: str
    times: list[int]
    note: Optional[str]

    ACTITIME_TASK_ID_PATTERN = re.compile(
        r"[\S\w\n\s]+actitimeUri:.+taskId=([0-9]+)[\S\w\n\s]+"
    )

    def to_task(self) -> Task:
        return Task(
            self.title,
            [
                TimeDuration.of(
                    parse_marvin_timestamp(start_time),
                    parse_marvin_timestamp(end_time)
                    - parse_marvin_timestamp(start_time),
                )
                for (start_time, end_time) in zip(self.times[0::2], self.times[1::2])
            ],
            self._id,
            self._parse_actitime_id_from_note(),
        )

    def _parse_actitime_id_from_note(self) -> Optional[str]:
        if self.note is None:
            return None

        match = self.ACTITIME_TASK_ID_PATTERN.match(self.note)
        if not match:
            return None

        re_groups = match.groups()
        if not re_groups:
            return None

        return re_groups[0]
