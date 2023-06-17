import datetime

import pandas as pd

from domain.time_duration import TimeDuration
from settings import OVERTIME_FOLDER_PATH


class OvertimeAdapter:
    overtime_date_format = "%Y-%m-%d"

    def get_overtime_until_now(self) -> TimeDuration:
        today = datetime.date.today()
        csv_file = self._get_overtime_path(today)
        df = pd.read_csv(csv_file)
        total = df["Overtime"].sum()
        return TimeDuration.of(today, datetime.timedelta(minutes=total * 60))

    def get_overtime_this_year(self) -> TimeDuration:
        today = datetime.date.today()
        csv_file = self._get_overtime_path(today)
        df = pd.read_csv(csv_file)

        df.drop(df[df["Date"].str.contains(str(today.year - 1))].index, inplace=True)

        total = df["Overtime"].sum()
        return TimeDuration.of(today, datetime.timedelta(minutes=total * 60))

    def export_overtime(self, time_duration: TimeDuration) -> None:
        overtime = time_duration.overtime()
        duration_date = time_duration.start_time
        formatted_date = duration_date.strftime(self.overtime_date_format)
        csv_file = self._get_overtime_path(duration_date)
        df = pd.read_csv(csv_file)

        existing_overtime_index = df["Date"] == formatted_date
        if df[existing_overtime_index].empty:
            df.loc[df.index.max() + 1] = [formatted_date, overtime.decimal_repr()]
        else:
            df.loc[existing_overtime_index] = [formatted_date, overtime.decimal_repr()]

        df.to_csv(csv_file, index=False)

    @staticmethod
    def _get_overtime_path(date: datetime.date) -> str:
        csv_file = f"{OVERTIME_FOLDER_PATH}/{date.year}-Overtime.csv"
        return csv_file
