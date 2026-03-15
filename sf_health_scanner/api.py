import urllib.parse
import httpx


def run_soql_query(instance_url: str, access_token: str, soql: str):
    """
    Executes a SOQL query against the Salesforce REST API.
    """
    encoded_soql = urllib.parse.quote(soql)

    url = f"{instance_url}/services/data/v60.0/query?q={encoded_soql}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = httpx.get(url, headers=headers, timeout=30.0)

    if response.status_code != 200:
        raise Exception(
            f"Salesforce API error: {response.status_code} - {response.text}"
        )

    return response.json()


def get_org_limits(instance_url: str, access_token: str):
    """
    Retrieves Salesforce org limits using the REST Limits API.
    """
    url = f"{instance_url}/services/data/v60.0/limits"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = httpx.get(url, headers=headers, timeout=30.0)

    if response.status_code != 200:
        raise Exception(
            f"Salesforce Limits API error: {response.status_code} - {response.text}"
        )

    return response.json()