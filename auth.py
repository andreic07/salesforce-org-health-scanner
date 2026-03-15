import json
import subprocess



def get_org_details(target_org: str):
    command = [
        "sf",
        "org",
        "display",
        "--target-org",
        target_org,
        "--json",
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"Salesforce CLI error: {result.stderr.strip()}")

    data = json.loads(result.stdout)
    org = data["result"]

    return {
        "username": org["username"],
        "org_id": org["id"],
        "instance_url": org["instanceUrl"],
        "access_token": org["accessToken"],
    }
