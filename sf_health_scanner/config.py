# Salesforce API
SALESFORCE_API_VERSION = "v60.0"

# -----------------------------
# System Administrator Check
# -----------------------------
SYSTEM_ADMIN_OK_MAX = 2
SYSTEM_ADMIN_WARNING_MAX = 4

# -----------------------------
# ORG LIMITS Check
# -----------------------------
LIMITS_WARNING_THRESHOLD = 70
LIMITS_CRITICAL_THRESHOLD = 90

TRACKED_LIMITS = [
    "DailyApiRequests",
    "DailyAsyncApexExecutions",
    "DailyBulkApiRequests",
    "DataStorageMB",
    "FileStorageMB",
]

# -----------------------------
# Active Flows Check
# -----------------------------
ACTIVE_FLOWS_OK_MAX = 5
ACTIVE_FLOWS_WARNING_MAX = 15

# -----------------------------
# Custom Fields Check
# -----------------------------
CUSTOM_FIELDS_TRACKED_OBJECTS = [
    "Account",
    "Contact",
    "Opportunity",
    "Case",
    "Lead",
]

CUSTOM_FIELDS_OK_MAX = 20
CUSTOM_FIELDS_WARNING_MAX = 50
