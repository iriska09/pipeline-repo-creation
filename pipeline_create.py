import jenkins
import requests
from dotenv import load_dotenv
import os
import sys

# Add this line to check the value prints the list of command-line arguments passed to the script
print(f"sys.argv: {sys.argv}")

# Get variables from .env
# load_dotenv()

# Fetch environment variables
JENKINS_URL = os.getenv('JENKINS_URL')
JENKINS_USER = os.getenv('JENKINS_USER')
JENKINS_PASSWORD = os.getenv('JENKINS_PASSWORD')
GITHUB_WEBHOOK = os.getenv('GITHUB_WEBHOOK')
SLACK_TOKEN = os.getenv('SLACK_TOKEN')
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL')

# This woner name will be used to create the full GitHub repository URL later for webhooks 
GITHUB_OWNER = 'iriska09'

#these lines will read first and second command-line arguments passed to the script and assign them to REPO_NAME and JOB_NAME 
REPO_NAME = sys.argv[1]
JOB_NAME = sys.argv[2]

# creates the full GITHUB_REPO url combining the name and repo name 
GITHUB_REPO = f'{GITHUB_OWNER}/{REPO_NAME}'

# Add this line to check the value of GITHUB_REPO url to check if it is correct url
print(f"GITHUB_REPO: {GITHUB_REPO}")

# Extract GitHub owner and repository name from GITHUB_REPO takes the user name and repo name by splitting and makes list
repo_parts = GITHUB_REPO.split('/')
print(f"repo_parts: {repo_parts}")
# and then it will check if there is small than 2 elements it will give error 
if len(repo_parts) < 2:
    print("Error: GITHUB_REPO  is not in the expected format 'owner/repo'.")
    sys.exit(1)

repo_owner = repo_parts[-2]
repo_name = repo_parts[-1].replace('.git', '')

# XML configuration for the pipeline job with webhook trigger setting branches and all from jenkins APIs 
# use open() and close() function that will read pipline.xml
pipeline_config = f"""\
<?xml version='1.1' encoding='UTF-8'?>
<flow-definition plugin="workflow-job@2.39">
  <actions/>
  <description></description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <org.jenkinsci.plugins.workflow.job.properties.PipelineTriggersJobProperty>
      <triggers>
        <com.cloudbees.jenkins.GitHubPushTrigger plugin="github@1.29.4">
          <spec></spec>
        </com.cloudbees.jenkins.GitHubPushTrigger>
      </triggers>
    </org.jenkinsci.plugins.workflow.job.properties.PipelineTriggersJobProperty>
  </properties>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition" plugin="workflow-cps@2.93">
    <scm class="hudson.plugins.git.GitSCM" plugin="git@4.8.1">
      <configVersion>2</configVersion>
      <userRemoteConfigs>
        <hudson.plugins.git.UserRemoteConfig>
          <url>git@github.com:{GITHUB_REPO}.git</url>
        </hudson.plugins.git.UserRemoteConfig>
      </userRemoteConfigs>
      <branches>
        <hudson.plugins.git.BranchSpec>
          <name>*/main</name>
        </hudson.plugins.git.BranchSpec>
      </branches>
    </scm>
    <scriptPath>Jenkinsfile</scriptPath>
    <lightweight>true</lightweight>
  </definition>
  <triggers>
    <com.cloudbees.jenkins.GitHubPushTrigger plugin="github@1.29.4"/>
  </triggers>
  <disabled>false</disabled>
</flow-definition>
"""

# Create Jenkins server connection with user name and password using the URL
try:
    server = jenkins.Jenkins(JENKINS_URL, username=JENKINS_USER, password=JENKINS_PASSWORD)

    if server.job_exists(JOB_NAME):            #checks if the job exists with that name 
        server.delete_job(JOB_NAME)            # if it exists it will delete

    server.create_job(JOB_NAME, pipeline_config)

    print(f"Pipeline job '{JOB_NAME}' created successfully.")

except jenkins.JenkinsException as e:
    print(f"Failed to create pipeline job: {e}")

# Setup GitHub webhook makes APi call to check if webhook is already exist or no 
try:
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'token {GITHUB_WEBHOOK}',
    }
    response = requests.get(f'https://api.github.com/repos/{repo_owner}/{repo_name}/hooks', headers=headers)
    
    existing_webhook = False
    if response.status_code == 200:
        hooks = response.json()
        for hook in hooks:
            if hook['config']['url'] == f'{JENKINS_URL}/github-webhook/':    #it will Checks if the webhook URL matches the Jenkins webhook URL
                existing_webhook = True
                break

    if not existing_webhook:
        data = {
            'name': 'web',
            'active': True,
            'events': ['push'],
            'config': {
                'url': f'{JENKINS_URL}/github-webhook/',
                'content_type': 'json',
            }
        }
        response = requests.post(f'https://api.github.com/repos/{repo_owner}/{repo_name}/hooks', headers=headers, json=data)
        if response.status_code == 201:
            print("GitHub webhook created successfully.")
        else:
            print(f"Failed to create GitHub webhook: {response.json()}")
    else:
        print("GitHub webhook already exists.")

except requests.RequestException as e:
    print(f"Failed to create GitHub webhook: {e}")
