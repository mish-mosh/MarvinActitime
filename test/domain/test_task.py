import datetime
from datetime import timedelta

from domain.task import Task
from domain.time_duration import TimeDuration


class TestTask:
    def test_total_tracked(self):
        # given
        start_time = datetime.datetime.now()
        td1 = timedelta(minutes=21, seconds=100)
        td2 = timedelta(minutes=15, seconds=50)
        time_duration1 = TimeDuration.of(start_time, td1)
        time_duration2 = TimeDuration.of(start_time, td2)
        task = Task("Test Task", [time_duration1, time_duration2], "marvin_id")

        # when
        total_tracked = task.total_tracked()

        # then
        assert (
            total_tracked.total_seconds
            == time_duration1.total_seconds + time_duration2.total_seconds
        )

    def test_tracked_for_date(self):
        # given
        date = datetime.date.today()
        start_time = datetime.datetime.now()
        td1 = timedelta(minutes=21)
        td2 = timedelta(minutes=15)
        td3 = timedelta(minutes=30)
        time_duration1 = TimeDuration.of(start_time, td1)
        time_duration2 = TimeDuration.of(start_time - timedelta(days=1), td2)
        time_duration3 = TimeDuration.of(start_time, td3)
        task = Task(
            "Test Task", [time_duration1, time_duration2, time_duration3], "marvin_id"
        )

        # when
        tracked_for_date = task.tracked_for_date(date)

        # then
        assert tracked_for_date.total_minutes == 51

    def test_round_tracked_durations_for_date(self):
        # given
        date = datetime.date.today()
        start_time = datetime.datetime.now()
        td1 = timedelta(minutes=22)
        time_duration1 = TimeDuration.of(start_time, td1)
        task = Task("Test Task", [time_duration1], "marvin_id")

        # when
        task.round_tracked_durations_for_date(date)
        rounded_duration = task.tracked_for_date(date)

        # then
        assert rounded_duration.total_minutes == 30
