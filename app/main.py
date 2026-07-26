from rich.console import Console
from rich.table import Table

from app.prometheus import get_target_statuses


console = Console()


def main() -> None:
    table = Table(title="HomeOps Infrastructure Status")

    table.add_column("Job")
    table.add_column("Instance")
    table.add_column("Status")

    for target in get_target_statuses():
        table.add_row(
            target["job"],
            target["instance"],
            target["status"],
        )

    console.print(table)


if __name__ == "__main__":
    main()
