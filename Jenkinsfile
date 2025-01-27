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

        stage('Prepare Script [Abduls version]') {
            steps {
                sh """
                python3 -m venv ${params.REPO_NAME}
                source activate ${params.REPO_NAME}/bin/activate
                pip install requests python-dotenv python-jenkins
                python "$WORKSPACE/repo_create.py" "$1"
                python "$WORKSPACE/pipeline_create.py" "$1" "$2"
                """
            }
        }

        stage('Prepare Script') {
            steps {
                sh 'chmod +x run_pipeline.sh'
            }
        }

        stage('Run Pipeline Script') {
            steps {
                sh "./run_pipeline.sh ${params.REPO_NAME} ${params.JOB_NAME}"
            }
        }
    }

    post {
        always {
            cleanWs() 
        }
    }
}
