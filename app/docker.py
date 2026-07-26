import docker
from docker.errors import DockerException, NotFound


ALLOWED_RESTART_CONTAINERS = {
    "jellyfin",
    "sonarr",
    "radarr",
    "prowlarr",
    "qbittorrent",
    "jellyseerr",
    "flaresolverr",
}


def get_docker_client():
    """
    Create and verify a connection to the local Docker Engine.
    """

    try:
        client = docker.from_env()
        client.ping()
        return client

    except DockerException as error:
        raise RuntimeError(
            f"Could not connect to Docker: {error}"
        ) from error


def get_container_statuses() -> list[dict]:
    """
    Return all Docker containers with simplified status information.
    """

    client = get_docker_client()

    try:
        containers = client.containers.list(all=True)
        statuses = []

        for container in containers:
            image_tags = container.image.tags
            image = image_tags[0] if image_tags else "unknown"

            statuses.append(
                {
                    "name": container.name,
                    "status": container.status,
                    "image": image,
                }
            )

        return statuses

    except DockerException as error:
        raise RuntimeError(
            f"Could not retrieve Docker containers: {error}"
        ) from error


def restart_container(container_name: str) -> dict:
    """
    Restart an approved Docker container.

    Containers not included in ALLOWED_RESTART_CONTAINERS
    are rejected.
    """

    normalized_name = container_name.strip().lower()

    if normalized_name not in ALLOWED_RESTART_CONTAINERS:
        allowed = ", ".join(sorted(ALLOWED_RESTART_CONTAINERS))

        raise ValueError(
            f"Restart denied for '{normalized_name}'. "
            f"Approved containers: {allowed}"
        )

    client = get_docker_client()

    try:
        container = client.containers.get(normalized_name)
        container.restart(timeout=15)
        container.reload()

        return {
            "name": container.name,
            "status": container.status,
            "message": f"{container.name} restarted successfully",
        }

    except NotFound as error:
        raise RuntimeError(
            f"Container '{normalized_name}' was not found"
        ) from error

    except DockerException as error:
        raise RuntimeError(
            f"Could not restart '{normalized_name}': {error}"
        ) from error
