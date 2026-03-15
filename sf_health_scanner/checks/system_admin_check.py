from sf_health_scanner.api import run_soql_query

#pip
def check_system_administrators(instance_url: str, access_token: str):
    soql = """
    SELECT Id, Name, Username, Profile.Name
    FROM User
    WHERE IsActive = true
    AND Profile.Name = 'System Administrator'
    """

    result = run_soql_query(instance_url, access_token, soql)
    records = result.get("records", [])

    return records


def evaluate_system_admins(admin_users: list[dict]):
    count = len(admin_users)

    if count <= 2:
        status = "OK"
        recommendation = "The number of active System Administrator users is within the expected range."
    elif count <= 4:
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
