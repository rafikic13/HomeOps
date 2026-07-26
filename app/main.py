from rich.console import Console
from rich.table import Table

from app.docker import get_container_statuses
from app.prometheus import get_target_statuses


console = Console()


def show_prometheus_status() -> None:
    table = Table(title="Infrastructure Status")

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


def show_container_status() -> None:
    table = Table(title="Docker Containers")

    table.add_column("Name")
    table.add_column("Image")
    table.add_column("Status")

    for container in get_container_statuses():
        table.add_row(
            container["name"],
            container["image"],
            container["status"].upper(),
        )

    console.print(table)


def main() -> None:
    show_prometheus_status()
    console.print()
    show_container_status()


if __name__ == "__main__":
    main()
