import requests

from app.config import PROMETHEUS_URL


def query_prometheus(query: str) -> list[dict]:
    """
    Send a PromQL query to Prometheus and return the result list.
    """

    url = f"{PROMETHEUS_URL}/api/v1/query"

    try:
        response = requests.get(
            url,
            params={"query": query},
            timeout=10,
        )

        response.raise_for_status()

        payload = response.json()

        if payload.get("status") != "success":
            raise RuntimeError(
                "Prometheus returned an unsuccessful response"
            )

        return payload["data"]["result"]

    except requests.RequestException as error:
        raise RuntimeError(
            f"Could not connect to Prometheus: {error}"
        ) from error


def get_target_statuses() -> list[dict]:
    """
    Return Prometheus target statuses in a simplified format.
    """

    results = query_prometheus("up")
    statuses = []

    for result in results:
        metric = result["metric"]
        value = result["value"][1]

        statuses.append(
            {
                "job": metric.get("job", "unknown"),
                "instance": metric.get("instance", "unknown"),
                "status": "UP" if value == "1" else "DOWN",
            }
        )

    return statuses
