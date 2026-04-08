from collections import defaultdict
from datetime import datetime

from sf_health_scanner.api import run_tooling_query
from sf_health_scanner.config import (
    ACTIVE_FLOWS_OK_MAX,
    ACTIVE_FLOWS_WARNING_MAX,
)


def format_salesforce_datetime(value: str):
    """
    Converts a Salesforce datetime string into EU display format:
    dd.mm.yyyy HH:MM
    """
    if not value:
        return "N/A"

    try:
        dt = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.000+0000")
        return dt.strftime("%d.%m.%Y %H:%M")
    except ValueError:
        return value


def check_flows(instance_url: str, access_token: str):
    """
    Retrieves flow definitions and their versions from Salesforce Tooling API.
    """
    soql = """
    SELECT Id, Definition.DeveloperName, Definition.MasterLabel, VersionNumber,
           Status, ProcessType, LastModifiedDate
    FROM Flow
    """

    result = run_tooling_query(instance_url, access_token, soql)

    return result.get("records", [])


def analyze_flows(flows):
    """
    Builds an overview of active/inactive flows and active flow details.
    """
    grouped = defaultdict(list)

    for flow in flows:
        definition = flow.get("Definition") or {}

        api_name = definition.get("DeveloperName")

        if not api_name:
            continue

        grouped[api_name].append(
            {
                "name": api_name,
                "version_number": flow.get("VersionNumber"),
                "status": flow.get("Status"),
                "process_type": flow.get("ProcessType"),
                "last_modified": format_salesforce_datetime(
                    flow.get("LastModifiedDate")
                ),
            }
        )

    active_flows = []
    inactive_count = 0
    process_type_distribution = defaultdict(int)

    for api_name, versions in grouped.items():
        versions_sorted = sorted(
            versions,
            key=lambda item: item.get("version_number") or 0,
            reverse=True,
        )

        total_versions = len(versions_sorted)

        active_version = next(
            (item for item in versions_sorted if item.get("status") == "Active"),
            None,
        )

        if active_version:
            flow_data = {
                "name": active_version.get("name"),
                "active_version": active_version.get("version_number"),
                "total_versions": total_versions,
                "last_modified": active_version.get("last_modified"),
                "process_type": active_version.get("process_type"),
            }

            active_flows.append(flow_data)
            process_type_distribution[
                active_version.get("process_type") or "Unknown"
            ] += 1
        else:
            inactive_count += 1

    active_flows.sort(key=lambda item: (item["name"] or "").lower())

    process_type_distribution = dict(
        sorted(process_type_distribution.items(), key=lambda item: item[0].lower())
    )

    return {
        "active_flows": active_flows,
        "active_count": len(active_flows),
        "inactive_count": inactive_count,
        "process_type_distribution": process_type_distribution,
    }


def evaluate_active_flows(active_count: int):
    """
    Evaluates automation complexity based on active flow count.
    """
    if active_count <= ACTIVE_FLOWS_OK_MAX:
        status = "OK"
        recommendation = "The number of active flows is within a reasonable range."
    elif active_count <= ACTIVE_FLOWS_WARNING_MAX:
        status = "WARNING"
        recommendation = "Review active flows for overlaps, duplication, or unnecessary automation complexity."
    else:
        status = "HIGH RISK"
        recommendation = "A large number of active flows was found. Consider simplifying automation architecture."

    return {
        "count": active_count,
        "status": status,
        "recommendation": recommendation,
    }
