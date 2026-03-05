import json
import csv
from datetime import datetime

  # Load the AWS access data
with open("aws_users.json") as f:
  aws_users = json.load(f)

  # Load HR system data
with open("hr_users.json") as f:
  hr_users = json.load(f)

// Convert HR users to directory
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

  // 
          
