from sf_health_scanner.api import describe_object
from sf_health_scanner.config import (
    CUSTOM_FIELDS_TRACKED_OBJECTS,
    CUSTOM_FIELDS_OK_MAX,
    CUSTOM_FIELDS_WARNING_MAX,
)


def check_custom_fields(instance_url: str, access_token: str):
    """
    Retrieves custom field counts for selected Salesforce objects.
    """

    objects_summary = []
    total_custom_fields = 0

    for object_name in CUSTOM_FIELDS_TRACKED_OBJECTS:
        describe_result = describe_object(instance_url, access_token, object_name)

        fields = describe_result.get("fields", [])

        custom_fields = [
            field for field in fields if field.get("name", "").endswith("__c")
        ]

        custom_field_count = len(custom_fields)
        total_custom_fields += custom_field_count

        objects_summary.append(
            {
                "object_name": object_name,
                "custom_field_count": custom_field_count,
            }
        )

    objects_summary.sort(
        key=lambda item: item["custom_field_count"],
        reverse=True,
    )

    return {
        "total_custom_fields": total_custom_fields,
        "objects_evaluated": len(objects_summary),
        "objects": objects_summary,
    }


def evaluate_custom_fields(custom_fields_data):
    """
    Evaluates custom field usage per object and overall section status.
    """

    evaluated_objects = []
    objects_above_limit = 0
    overall_status = "OK"

    for item in custom_fields_data["objects"]:
        count = item["custom_field_count"]

        if count >= CUSTOM_FIELDS_WARNING_MAX:
            status = "HIGH RISK"
        elif count >= CUSTOM_FIELDS_OK_MAX:
            status = "WARNING"
        else:
            status = "OK"

        if status in ["WARNING", "HIGH RISK"]:
            objects_above_limit += 1

        if status == "HIGH RISK":
            overall_status = "HIGH RISK"
        elif status == "WARNING" and overall_status != "HIGH RISK":
            overall_status = "WARNING"

        evaluated_objects.append(
            {
                "object_name": item["object_name"],
                "custom_field_count": count,
                "status": status,
            }
        )

    if overall_status == "HIGH RISK":
        recommendation = (
            "One or more objects contain excessive numbers of custom fields. "
            "Consider schema cleanup and consolidation."
        )
    elif overall_status == "WARNING":
        recommendation = "Review objects with elevated custom field counts to reduce schema complexity."
    else:
        recommendation = "Custom field usage is within a reasonable range."

    return {
        "total_custom_fields": custom_fields_data["total_custom_fields"],
        "objects_evaluated": custom_fields_data["objects_evaluated"],
        "objects_above_limit": objects_above_limit,
        "status": overall_status,
        "recommendation": recommendation,
        "objects": evaluated_objects,
    }
