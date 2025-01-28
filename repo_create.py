import requests
import json
import sys
from dotenv import load_dotenv
import os

# get all environment variables from .env file
# load_dotenv()

# get GITHUB_WEBHOOK  it is  actually github token from environment variables
GITHUB_WEBHOOK = os.getenv('GITHUB_WEBHOOK')

if not GITHUB_WEBHOOK:
    print("Error: GITHUB_WEBHOOK is not set in env file")
    sys.exit(1)

# Read repository name from command-line argument that we passed to the script argv[0] is script name and argv[1] is repo name 
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

#changed