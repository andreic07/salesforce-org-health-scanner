from sf_health_scanner.api import run_soql_query
from sf_health_scanner.config import (
    SYSTEM_ADMIN_OK_MAX,
    SYSTEM_ADMIN_WARNING_MAX,
)


def check_system_administrators(instance_url: str, access_token: str):
    """
    Retrieves all active users with the System Administrator profile.
    """
    soql = """
    SELECT Id, Name, Username, Profile.Name
    FROM User
    WHERE IsActive = true
    AND Profile.Name = 'System Administrator'
    """

    result = run_soql_query(instance_url, access_token, soql)

    return result.get("records", [])


def evaluate_system_admins(admin_users):
    """
    Evaluates the number of active System Administrator users.
    """
    count = len(admin_users)

    if count <= SYSTEM_ADMIN_OK_MAX:
        status = "OK"
        recommendation = "The number of active System Administrator users is within the expected range."
    elif count <= SYSTEM_ADMIN_WARNING_MAX:
        status = "WARNING"
        recommendation = "Review whether all active System Administrator users still require elevated access."
    else:
        status = "HIGH RISK"
        recommendation = "Too many active System Administrator users were found. Reduce privileged access where possible."

    return {
        "count": count,
        "status": status,
        "recommendation": recommendation,
    }
