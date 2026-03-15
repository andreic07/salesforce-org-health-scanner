import urllib.parse
import httpx

def run_soql_query(instance_url: str, access_token: str, soql: str):
    encoded_soql = urllib.parse.quote(soql)
    url = f"{instance_url}/services/data/v60.0/query?q={encoded_soql}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = httpx.get(url, headers=headers, timeout=30.0)

    if response.status_code != 200:
        raise Exception(f"Salesforce API error: {response.status_code} - {response.text}")

    return response.json()
