# import jenkins
# import requests
# from dotenv import load_dotenv
# import os
# import sys 

# # Get variables from .env
# load_dotenv()

# # Fetch environment variables
# JENKINS_URL = os.getenv('JENKINS_URL')
# JENKINS_USER = os.getenv('JENKINS_USER')
# JENKINS_PASSWORD = os.getenv('JENKINS_PASSWORD')
# GITHUB_WEBHOOK = os.getenv('GITHUB_WEBHOOK')
# SLACK_TOKEN = os.getenv('SLACK_TOKEN')
# SLACK_CHANNEL = os.getenv('SLACK_CHANNEL')

# # Read repository name from command-line argument
# GITHUB_REPO = sys.argv[1]
# JOB_NAME = sys.argv[2]

# # Extract GitHub owner and repository name from GITHUB_REPO
# repo_parts = GITHUB_REPO.split('/')
# repo_owner = repo_parts[-2]
# repo_name = repo_parts[-1].replace('.git', '')

# # XML configuration for the pipeline job with webhook trigger
# pipeline_config = f"""\
# <?xml version='1.1' encoding='UTF-8'?>
# <flow-definition plugin="workflow-job@2.39">
#   <actions/>
#   <description></description>
#   <keepDependencies>false</keepDependencies>
#   <properties>
#     <org.jenkinsci.plugins.workflow.job.properties.PipelineTriggersJobProperty>
#       <triggers>
#         <com.cloudbees.jenkins.GitHubPushTrigger plugin="github@1.29.4">
#           <spec></spec>
#         </com.cloudbees.jenkins.GitHubPushTrigger>
#       </triggers>
#     </org.jenkinsci.plugins.workflow.job.properties.PipelineTriggersJobProperty>
#   </properties>
#   <definition class="org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition" plugin="workflow-cps@2.93">
#     <scm class="hudson.plugins.git.GitSCM" plugin="git@4.8.1">
#       <configVersion>2</configVersion>
#       <userRemoteConfigs>
#         <hudson.plugins.git.UserRemoteConfig>
#           <url>{GITHUB_REPO}</url>
#         </hudson.plugins.git.UserRemoteConfig>
#       </userRemoteConfigs>
#       <branches>
#         <hudson.plugins.git.BranchSpec>
#           <name>*/main</name>
#         </hudson.plugins.git.BranchSpec>
#       </branches>
#     </scm>
#     <scriptPath>Jenkinsfile</scriptPath>
#     <lightweight>true</lightweight>
#   </definition>
#   <triggers>
#     <com.cloudbees.jenkins.GitHubPushTrigger plugin="github@1.29.4"/>
#   </triggers>
#   <disabled>false</disabled>
# </flow-definition>
# """

# # Create Jenkins server connection
# try:
#     server = jenkins.Jenkins(JENKINS_URL, username=JENKINS_USER, password=JENKINS_PASSWORD)

#     if server.job_exists(JOB_NAME):
#         server.delete_job(JOB_NAME)

#     server.create_job(JOB_NAME, pipeline_config)

#     print(f"Pipeline job '{JOB_NAME}' created successfully.")

# except jenkins.JenkinsException as e:
#     print(f"Failed to create pipeline job: {e}")

# # Setup GitHub webhook
# try:
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': f'token {GITHUB_WEBHOOK}',
#     }
#     response = requests.get(f'https://api.github.com/repos/{repo_owner}/{repo_name}/hooks', headers=headers)
    
#     existing_webhook = False
#     if response.status_code == 200:
#         hooks = response.json()
#         for hook in hooks:
#             if hook['config']['url'] == f'{JENKINS_URL}/github-webhook/':
#                 existing_webhook = True
#                 break

#     if not existing_webhook:
#         data = {
#             'name': 'web',
#             'active': True,
#             'events': ['push'],
#             'config': {
#                 'url': f'{JENKINS_URL}/github-webhook/',
#                 'content_type': 'json',
#             }
#         }
#         response = requests.post(f'https://api.github.com/repos/{repo_owner}/{repo_name}/hooks', headers=headers, json=data)
#         if response.status_code == 201:
#             print("GitHub webhook created successfully.")
#         else:
#             print(f"Failed to create GitHub webhook: {response.json()}")
#     else:
#         print("GitHub webhook already exists.")

# except requests.RequestException as e:
#     print(f"Failed to create GitHub webhook: {e}")


#///////new 
import jenkins
import requests
from dotenv import load_dotenv
import os
import sys

# Add this line to check the value of GITHUB_REPO
print(f"sys.argv: {sys.argv}")

# Get variables from .env
load_dotenv()

# Fetch environment variables
JENKINS_URL = os.getenv('JENKINS_URL')
JENKINS_USER = os.getenv('JENKINS_USER')
JENKINS_PASSWORD = os.getenv('JENKINS_PASSWORD')
GITHUB_WEBHOOK = os.getenv('GITHUB_WEBHOOK')
SLACK_TOKEN = os.getenv('SLACK_TOKEN')
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL')

# Default GitHub owner (replace this with the actual owner)
GITHUB_OWNER = 'iriska09'

# Read repository name from command-line argument
REPO_NAME = sys.argv[1]
JOB_NAME = sys.argv[2]

# Construct the full GITHUB_REPO
GITHUB_REPO = f'{GITHUB_OWNER}/{REPO_NAME}'

# Add this line to check the value of GITHUB_REPO
print(f"GITHUB_REPO: {GITHUB_REPO}")

# Extract GitHub owner and repository name from GITHUB_REPO
repo_parts = GITHUB_REPO.split('/')
print(f"repo_parts: {repo_parts}")

if len(repo_parts) < 2:
    print("Error: GITHUB_REPO argument is not in the expected format 'owner/repo'.")
    sys.exit(1)

repo_owner = repo_parts[-2]
repo_name = repo_parts[-1].replace('.git', '')

# XML configuration for the pipeline job with webhook trigger
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

# Create Jenkins server connection
try:
    server = jenkins.Jenkins(JENKINS_URL, username=JENKINS_USER, password=JENKINS_PASSWORD)

    if server.job_exists(JOB_NAME):
        server.delete_job(JOB_NAME)

    server.create_job(JOB_NAME, pipeline_config)

    print(f"Pipeline job '{JOB_NAME}' created successfully.")

except jenkins.JenkinsException as e:
    print(f"Failed to create pipeline job: {e}")

# Setup GitHub webhook
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
            if hook['config']['url'] == f'{JENKINS_URL}/github-webhook/':
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
