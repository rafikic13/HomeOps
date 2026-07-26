import docker
from docker.errors import DockerException


def get_docker_client():
    """
    Create and return a Docker client using the local Docker socket.
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
