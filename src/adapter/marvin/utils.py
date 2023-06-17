from datetime import datetime


def parse_marvin_timestamp(marvin_timestamp: int) -> datetime:
    timestamp_in_seconds = marvin_timestamp / 1000
    return datetime.fromtimestamp(timestamp_in_seconds)


def datetime_to_marvin_timestamp(dt: datetime) -> int:
    return int(dt.timestamp() * 1000)
