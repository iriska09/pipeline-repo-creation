pipeline {
    agent any

    parameters {
        string(name: 'REPO_NAME', defaultValue: 'demo-repo', description: 'Name of the repository to create')
        string(name: 'JOB_NAME', defaultValue: 'demo-pipeline', description: 'Name of the Jenkins job to create')
    }

    stages {
        stage('Check Workspace') {
            steps {
                script {
                    sh 'pwd'
                    sh 'ls -la'
                }
            }
        }

        stage('Prepare Script') {
            steps {
                sh """
                python3 -m venv .venv
                . .venv/bin/activate
                pip install requests python-dotenv python-jenkins
                python repo_create.py ${params.REPO_NAME}
                python pipeline_create.py ${params.REPO_NAME} ${params.JOB_NAME}
                """
            }
        }
    }

    post {
        always {
            cleanWs() 
        }
    }
}

// #changed