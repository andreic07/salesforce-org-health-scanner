from sf_health_scanner.auth import get_org_details
from sf_health_scanner.api import run_soql_query
from sf_health_scanner.checks.system_admin_check import (
    check_system_administrators,
    evaluate_system_admins,
)
from sf_health_scanner.checks.limits_check import (
    check_org_limits,
    evaluate_org_limits,
)
from sf_health_scanner.checks.flows_check import (
    check_flows,
    analyze_flows,
    evaluate_active_flows,
)
from sf_health_scanner.checks.custom_fields_check import (
    check_custom_fields,
    evaluate_custom_fields,
)


def main():
    alias = input("Enter org alias: ").strip()

    if not alias:
        print("You must provide an org alias.")
        return

    try:
        org = get_org_details(alias)

        print("\nConnected to org\n")
        print("Username:", org["username"])
        print("Org Id:", org["org_id"])
        print("Instance:", org["instance_url"])

        soql = "SELECT Id, Name FROM Organization LIMIT 1"
        query_result = run_soql_query(
            instance_url=org["instance_url"],
            access_token=org["access_token"],
            soql=soql,
        )

        print("\nSOQL query executed successfully.\n")

        records = query_result.get("records", [])
        if records:
            print("Organization Name:", records[0]["Name"])
            print("Organization Id:", records[0]["Id"])
        else:
            print("No records returned.")

        admin_users = check_system_administrators(
            instance_url=org["instance_url"],
            access_token=org["access_token"],
        )

        admin_check = evaluate_system_admins(admin_users)

        print("\nSYSTEM ADMINISTRATOR CHECK\n")
        print(f"Found {admin_check['count']} active System Administrator users.\n")

        for user in admin_users:
            print(f"- {user['Name']} ({user['Username']})")

        print(f"\nResult: {admin_check['status']}")
        print(f"Recommendation: {admin_check['recommendation']}")

        limits = check_org_limits(
            instance_url=org["instance_url"],
            access_token=org["access_token"],
        )

        limits = evaluate_org_limits(limits)

        print("\nORG LIMITS\n")

        if not limits:
            print("No tracked limits were returned by the org.\n")
        else:
            for limit in limits:
                print(f"{limit['name']}")
                print(f"Used: {limit['used']} / {limit['max']} ({limit['percent']}%)")
                print(f"Remaining: {limit['remaining']}")
                print(f"Status: {limit['status']}")
                print()

        flows = check_flows(
            instance_url=org["instance_url"],
            access_token=org["access_token"],
        )

        flow_analysis = analyze_flows(flows)
        flow_check = evaluate_active_flows(flow_analysis["active_count"])

        print("\nACTIVE FLOWS OVERVIEW\n")
        print(f"Total Active Flows   : {flow_analysis['active_count']}")
        print(f"Total Inactive Flows : {flow_analysis['inactive_count']}")
        print(f"Result               : {flow_check['status']}")
        print(f"Recommendation       : {flow_check['recommendation']}")

        print("\nFLOWS BY PROCESS TYPE\n")
        if flow_analysis["process_type_distribution"]:
            for process_type, count in flow_analysis[
                "process_type_distribution"
            ].items():
                print(f"- {process_type} - {count} flows")
        else:
            print("No active flows found.")

        print("\nACTIVE FLOW DETAILS\n")
        if flow_analysis["active_flows"]:
            for flow in flow_analysis["active_flows"]:
                print(f"{flow['name']}")
                print(f"  Active Version : {flow['active_version']}")
                print(f"  Total Versions : {flow['total_versions']}")
                print(f"  Last Modified  : {flow['last_modified']}")
                print(f"  Process Type   : {flow['process_type']}")
                print()
        else:
            print("No active flows found.")
            # CUSTOM FIELDS CHECK
        custom_fields_data = check_custom_fields(
            instance_url=org["instance_url"],
            access_token=org["access_token"],
        )

        custom_fields_check = evaluate_custom_fields(custom_fields_data)

        print("\nCUSTOM FIELDS OVERVIEW\n")
        print(f"Total Custom Fields : {custom_fields_check['total_custom_fields']}")
        print(f"Objects Evaluated   : {custom_fields_check['objects_evaluated']}")
        print(f"Objects Above Limit : {custom_fields_check['objects_above_limit']}")
        print(f"Result              : {custom_fields_check['status']}")
        print(f"Recommendation      : {custom_fields_check['recommendation']}")

        print("\nTOP OBJECTS\n")
        for item in custom_fields_check["objects"]:
            print(
                f"- {item['object_name']} : "
                f"{item['custom_field_count']} custom fields ({item['status']})"
            )

    except Exception as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
