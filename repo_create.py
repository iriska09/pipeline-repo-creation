# import requests
# import json
# import sys
# from config import GITHUB_WEBHOOK

# # Read repository name from command-line argument
# repo_name = sys.argv[1]

# headers = {
#     'Content-Type': 'application/json',
#     'Authorization': f'Bearer {GITHUB_WEBHOOK}',
# }

# data = {
#     "name": repo_name,
#     "include_all_branches": False,
#     "private": True
# }

# response = requests.post(
#     'https://api.github.com/repos/sdfsdf/sfdfs-repository-template/generate',
#     headers=headers,
#     data=json.dumps(data)
# )

# if response.status_code == 201:
#     print(f"Repository '{repo_name}' created successfully.")
# else:
#     print(f"Failed to create repository: {response.json()}")
import requests
import json
import sys
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get GITHUB_WEBHOOK from environment variables
GITHUB_WEBHOOK = os.getenv('GITHUB_WEBHOOK')

# Read repository name from command-line argument
repo_name = sys.argv[1]

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {GITHUB_WEBHOOK}',
}

data = {
    "name": repo_name,
    "include_all_branches": False,
    "private": True
}

response = requests.post(
    'https://api.github.com/repos/iriska09/developer-repository-template/generate',
    headers=headers,
    data=json.dumps(data)
)

if response.status_code == 201:
    print(f"Repository '{repo_name}' created successfully.")
else:
    print(f"Failed to create repository: {response.json()}")
