from adapter.actitime.actitime_adapter import ActitimeAdapter
from adapter.cli import CliController
from adapter.file.overtime import OvertimeAdapter
from adapter.file.pinned_tasks import PinnedTasksYamlAdapter
from adapter.marvin.marvin_adapter import MarvinAdapter


def main():
    marvin_adapter = MarvinAdapter()
    actitime_adapter = ActitimeAdapter()
    overtime_adapter = OvertimeAdapter()
    pinned_tasks_adapter = PinnedTasksYamlAdapter()
    cli = CliController(
        marvin_adapter, actitime_adapter, overtime_adapter, pinned_tasks_adapter
    )

    cli.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
