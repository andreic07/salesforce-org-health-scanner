from auth import get_org_details
from api import run_soql_query
from checks import check_system_administrators, evaluate_system_admins



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

        print("\nSystem Administrator Check\n")
        print(f"Found {admin_check['count']} active System Administrator users.\n")

        for user in admin_users:
            print(f"- {user['Name']} ({user['Username']})")

        print(f"\nResult: {admin_check['status']}")
        print(f"Recommendation: {admin_check['recommendation']}")

    except Exception as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()