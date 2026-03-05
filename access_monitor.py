import json
import csv
from datetime import datetime

  # Load the AWS access data
with open("aws_users.json") as f:
  aws_users = json.load(f)

  # Load HR system data
with open("hr_users.json") as f:
  hr_users = json.load(f)

  # Convert HR users to directory
hr_lookup = {user["username"]: user["status"] for user in hr_users}

alerts =[]
access_inventory =[]

for users in aws_users:

  username = user["username"]
  privilege = user["privilege"]
  last_login = user["last_login_days"]

  hr_status = hr_lookup.get(username)

  access_inventory.append({
    "username": username,
    "privilege": privilege,
    "last_login_days": last_login,
    "hr_status": hr_status
  })

  # Rule 1: Orphaned privileged account
  if privilege == "admin" and hr_status is None:
    alerts.append({
      "type": "orphaned_admin_account",
      "username": username,
      "severity": "HIGH",
      "message": "Admin account not linked to HR employee"
    })

  # Rule 2: Dormat privileged access
  if privilege == "admin" and last_login > 90:
    alerts.append({
      "type": "dormant_privileged_access",
      "username": username,
      "severity": "MEDIUM",
      "message": "Admin access unused for 90+ days"
    })

  # Rule 3: Terminated user with access
  if hr_status =="terminated":
    alerts.append({
      "type": "terminated_user_with_access",
      "username": username,
      "severity": "CRITICAL"
      "message": "Terminated user still has system access"
    })

# Save all alerts
with open("alerts.json", "w") as f:
  json.dump(alerts, f, indent=4)

# Generate access inventory evidence
with open("access_inventory.csv", "w", newline="") as f:
  writer = csv.DictWriter(f, fieldnames=["username", "privilege", "last_login_days", "hr_status"])
  writer.writeheader()
  writer.writerows(access_inventory)

print("Access monitoring scan complete")
print("Alerts generated:", len(alerts))

          
