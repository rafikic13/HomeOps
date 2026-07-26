import argparse

from rich.console import Console
from rich.table import Table

from app.docker import get_container_statuses, restart_container
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


def restart_service(container_name: str) -> None:
    try:
        result = restart_container(container_name)
        console.print(
            f"[bold green]{result['message']}[/bold green]"
        )

    except (ValueError, RuntimeError) as error:
        console.print(f"[bold red]{error}[/bold red]")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="homeops",
        description="Monitor and manage approved homelab services.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    subparsers.add_parser(
        "status",
        help="Show Prometheus infrastructure status.",
    )

    subparsers.add_parser(
        "containers",
        help="Show Docker container status.",
    )

    restart_parser = subparsers.add_parser(
        "restart",
        help="Restart an approved Docker container.",
    )

    restart_parser.add_argument(
        "container",
        help="Name of the approved container to restart.",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "status":
        show_prometheus_status()

    elif args.command == "containers":
        show_container_status()

    elif args.command == "restart":
        restart_service(args.container)


if __name__ == "__main__":
    main()
