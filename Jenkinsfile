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
                pip install requests python-dotenv python-jenkins
                python repo_create.py ${params.REPO_NAME}
                python pipeline_create.py ${params.REPO_NAME} ${params.JOB_NAME}
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

    // post {
    //     always {
    //         cleanWs() 
    //     }
    // }
}
