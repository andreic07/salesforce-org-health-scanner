from sf_health_scanner.api import get_org_limits
from sf_health_scanner.config import (
    LIMITS_WARNING_THRESHOLD,
    LIMITS_CRITICAL_THRESHOLD,
    TRACKED_LIMITS,
)


def check_org_limits(instance_url: str, access_token: str):
    """
    Retrieves selected Salesforce org limits and calculates usage.
    """
    limits_response = get_org_limits(instance_url, access_token)

    tracked_limits = TRACKED_LIMITS

    results = []

    for limit_name in tracked_limits:
        data = limits_response.get(limit_name)

        if not data:
            continue

        max_value = data.get("Max", 0)
        remaining = data.get("Remaining", 0)
        used = max_value - remaining

        if max_value == 0:
            percent = 0.0
        else:
            percent = (used / max_value) * 100

        results.append(
            {
                "name": limit_name,
                "max": max_value,
                "used": used,
                "remaining": remaining,
                "percent": round(percent, 2),
            }
        )

    return results


def evaluate_org_limits(limits):
    """
    Assigns a status based on limit usage percentage.
    """
    evaluated = []

    for limit in limits:
        percent = limit["percent"]

        if percent >= LIMITS_CRITICAL_THRESHOLD:
            status = "CRITICAL"
        elif percent >= LIMITS_WARNING_THRESHOLD:
            status = "WARNING"
        else:
            status = "NORMAL"

        evaluated.append(
            {
                **limit,
                "status": status,
            }
        )

    return evaluated
