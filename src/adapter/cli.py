import datetime
import re

from InquirerPy import inquirer
from InquirerPy.base import Choice

from adapter.actitime.actitime_adapter import ActitimeAdapter
from adapter.file.overtime import OvertimeAdapter
from adapter.file.pinned_tasks import PinnedTasksYamlAdapter
from adapter.marvin.marvin_adapter import MarvinAdapter
from domain.time_duration import TimeDuration


class CliController:
    DATE_FORMAT = "%y-%m-%d"
    TIME_DURATION_PATTERN = re.compile(r"([0-9]{1,2}):([0-9]{1,2})")

    marvin_adapter: MarvinAdapter
    actitime_adapter: ActitimeAdapter
    overtime_adapter: OvertimeAdapter
    pinned_tasks_adapter: PinnedTasksYamlAdapter

    def __init__(
        self,
        marvin_adapter: MarvinAdapter,
        actitime_adapter: ActitimeAdapter,
        overtime_adapter: OvertimeAdapter,
        pinned_tasks_adapter: PinnedTasksYamlAdapter,
    ):
        self.marvin_adapter = marvin_adapter
        self.actitime_adapter = actitime_adapter
        self.overtime_adapter = overtime_adapter
        self.pinned_tasks_adapter = pinned_tasks_adapter

    def start(self) -> None:
        routines = {
            "Time accounting for pinned tasks": self.pinned_accounting_routine,
            "Marvin daily time accounting": self.marvin_accounting_routine,
            "Get accounted time for date": self.get_accounted_time,
            "Get Overtime balance": self.get_overtime_balance,
        }
        selected_routine_key = inquirer.select(
            "Select a routine", choices=list(routines.keys()), default=None
        ).execute()
        selected_routine = routines.get(selected_routine_key)
        if selected_routine is None:
            raise ValueError("Cannot select a routine")

        return selected_routine()

    def pinned_accounting_routine(self) -> None:
        print("Time accounting routine for pinned tasks")

        pinned_tasks = self.pinned_tasks_adapter.gett_all()
        if not pinned_tasks:
            print("No pinned tasks found")
            return

        date = self._get_date()
        selected_task_id = inquirer.fuzzy(
            "For which task?",
            choices=[
                Choice(task.actitime_id, name=task.title) for task in pinned_tasks
            ],
        ).execute()
        duration = self._get_duration(date)
        comment = inquirer.text("Enter a comment:").execute()

        print(selected_task_id)
        self.actitime_adapter.account_time(selected_task_id, duration, comment)

        print(f"Accounted {duration} for task: {selected_task_id}")
        print("---\n")

        self._handle_after_accounting(date)

    def marvin_accounting_routine(self) -> None:
        print("Marvin daily time accounting routine")

        date = self._get_date()
        tasks = self.marvin_adapter.find_tracked_tasks_for_date(date)

        print(f"The following tasks were tracked for {date}:")
        for task in tasks:
            tracked_time = task.tracked_for_date(date)

            print(
                f"- {task.title} - {tracked_time.rounded()}{' (rounded)' if tracked_time.should_be_rounded() else ''}"
            )

        should_export = inquirer.confirm("Export to actitime?:", default=True).execute()
        if not should_export:
            return

        to_be_exported = inquirer.select(
            "Select the tasks to account duration for?",
            choices=[Choice(task.title, enabled=True) for task in tasks],
            multiselect=True,
        ).execute()
        to_export_tasks = [task for task in tasks if task.title in to_be_exported]

        for task in to_export_tasks:
            # if task.tracked_for_date(date).should_be_rounded():
            #     self.marvin_adapter.round_to_fifteen_minutes(task, date)
            #     print(f"Rounded task {task.title}")

            self.actitime_adapter.account_time(
                task.actitime_id, task.tracked_for_date(date).rounded(), task.title
            )
            print(
                f"Accounted {task.tracked_for_date(date).rounded()} for task: {task.title}"
            )

        print("---\n")

        self._handle_after_accounting(date)

    def get_accounted_time(self) -> None:
        print("Total accounted time routine")

        date = self._get_date()
        self._show_accounted_duration_for_date(date)

    def get_overtime_balance(self) -> None:
        overtime_this_year = self.overtime_adapter.get_overtime_this_year()
        overtime_until_now = self.overtime_adapter.get_overtime_until_now()

        print(
            f"""
Total overtime balance:
    - this year: {overtime_this_year.decimal_repr()} hours
    - as of now: {overtime_until_now.decimal_repr()} hours
        """
        )

    def _handle_after_accounting(self, date):
        self._show_accounted_duration_for_date(date)
        self.overtime_adapter.export_overtime(
            self.actitime_adapter.get_accounted_time_for_date(date)
        )

        print("---")
        self.get_overtime_balance()

    def _show_accounted_duration_for_date(self, date):
        duration = self.actitime_adapter.get_accounted_time_for_date(date)
        print(
            f"Overtime accounted for {date}: {duration} ({duration.overtime().decimal_repr()} hours overtime)\n"
        )

    def _get_duration(self, date: datetime.date) -> TimeDuration:
        raw_duration = inquirer.text(f"For how long? - formatted like hh:mm").execute()
        duration_match = self.TIME_DURATION_PATTERN.fullmatch(raw_duration)
        if duration_match is None:
            print(f"{raw_duration} doesn't have the format hh:mm!")
            return self._get_duration(date)

        return TimeDuration.of(
            date,
            datetime.timedelta(
                hours=int(duration_match.groups()[0]),
                minutes=int(duration_match.groups()[1]),
            ),
        ).rounded()

    def _get_date(self) -> datetime.date:
        raw_date = inquirer.text(
            f"Enter date in {self.DATE_FORMAT} format or proceed with today:",
            default="today",
        ).execute()
        date = (
            datetime.date.today()
            if raw_date == "today"
            else datetime.datetime.strptime(raw_date, self.DATE_FORMAT).date()
        )
        return date
