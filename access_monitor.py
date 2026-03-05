import json
import csv
from datetime import datetime

// Load the AWS access data
with open("aws_users.json") as f:
  aws_users = json.load(f)

// Load HR system data
with open("hr_users.json") as f:
  hr_users = json.load(f)

  // 
          
