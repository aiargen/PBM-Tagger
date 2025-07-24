# pbm/heuristics.py
import re
from .vocab import PRODUCTS, ISSUE_CATEGORIES, ACTION_CATEGORIES

LOWER_ISSUE_KEYWORDS = {
    "config": "Configuration",
    "certificate": "Certificate",
    "rssso": "RSSO",
    "sso": "RSSO",
    "collab": "Collaborators",
    "email": "Email",
    "report": "Report",
    "perf": "Performance",
    "slow": "Performance",
    "api": "RestAPI",
    "restapi": "RestAPI",
    "password": "Password",
    "custom": "Customization",
    "brand": "Branding",
    "db ": "Database",
    "database": "Database",
    "notif": "Notification Template",
    "cache": "Cache",
    "restart": "Restart",
}

LOWER_PRODUCT_KEYWORDS = {
    "dwpc": "DWPC",
    "digital workplace catalog": "DWPC",
    "dwp": "DWP",
    "digital workplace": "DWP",
    "srm": "SRM",
    "service request mgmt": "SRM"
}

def heuristic_product(text: str):
    t = text.lower()
    for k,v in LOWER_PRODUCT_KEYWORDS.items():
        if k in t:
            return v
    return None

def heuristic_issue(text: str):
    t = text.lower()
    for k,v in LOWER_ISSUE_KEYWORDS.items():
        if k in t:
            return v
    return None

def heuristic_action(issue: str | None):
    if not issue:
        return None
    # simple mapping; customize to your org rules
    map_issue_to_action = {
        "Configuration": "R&D",
        "Certificate": "R&D",
        "Customization": "Customization",
        "Collaborators": "Data",
        "Report": "Data",
        "Performance": "Idea",
        "Restart": "NA",
    }
    return map_issue_to_action.get(issue)
