from datetime import datetime, timedelta

from src.domain.time_duration import TimeDuration


class TestTimeDuration:
    def test_end_time(self):
        # given
        start_time = datetime.now()
        td = timedelta(minutes=21, seconds=100)

        # when
        time_duration = TimeDuration.of(start_time, td)

        # then
        assert time_duration.end_time == start_time + td

    def test_add(self):
        # given
        start_time = datetime.now()
        td1 = timedelta(minutes=21, seconds=100)
        td2 = timedelta(minutes=15, seconds=50)
        time_duration1 = TimeDuration.of(start_time, td1)
        time_duration2 = TimeDuration.of(start_time, td2)

        # when
        added_time_duration = time_duration1.add(time_duration2)

        # then
        assert (
            added_time_duration.total_seconds
            == time_duration1.total_seconds + time_duration2.total_seconds
        )

    def test_add_all(self):
        # given
        start_time1 = datetime.now()
        td1 = timedelta(minutes=21, seconds=100)
        time_duration1 = TimeDuration.of(start_time1, td1)
        start_time2 = datetime.now()
        td2 = timedelta(minutes=15, seconds=50)
        time_duration2 = TimeDuration.of(start_time2, td2)
        time_durations = [time_duration1, time_duration2]

        # when
        added_time_duration = TimeDuration.add_all(time_durations)

        # then
        assert added_time_duration.start_time == time_duration1.start_time
        assert (
            added_time_duration.total_seconds
            == time_duration1.total_seconds + time_duration2.total_seconds
        )

    def test_rounded(self):
        # given
        start_time = datetime.now()
        td1 = timedelta(minutes=22)
        td2 = timedelta(minutes=15)
        td3 = timedelta(minutes=36)
        time_duration1 = TimeDuration.of(start_time, td1)
        time_duration2 = TimeDuration.of(start_time, td2)
        time_duration3 = TimeDuration.of(start_time, td3)

        # when
        rounded_time_duration1 = time_duration1.rounded()
        rounded_time_duration2 = time_duration2.rounded()
        rounded_time_duration3 = time_duration3.rounded()

        # then
        assert rounded_time_duration1.total_minutes == 30
        assert rounded_time_duration2.total_minutes == 15
        assert rounded_time_duration3.total_minutes == 30

    def test_should_be_rounded(self):
        # given
        start_time = datetime.now()
        td = timedelta(minutes=21, seconds=100)
        time_duration = TimeDuration.of(start_time, td)

        # when
        result = time_duration.should_be_rounded()

        # then
        assert result is True

    def test_overtime(self):
        # given
        start_time = datetime.now()
        td = timedelta(hours=8, minutes=21)
        time_duration = TimeDuration.of(start_time, td)

        # when
        overtime_duration = time_duration.overtime()

        # then
        assert overtime_duration.total_minutes == 21

    def test_decimal_repr(self):
        # given
        start_time = datetime.now()
        td = timedelta(minutes=150)
        time_duration = TimeDuration.of(start_time, td)

        # when
        result = time_duration.decimal_repr()

        # then
        assert result == 2.5
