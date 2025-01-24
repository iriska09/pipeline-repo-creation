// pipeline {
//     agent any

//     parameters {
//         string(name: 'REPO_NAME', defaultValue: 'Hello-', description: 'Name of the repository to create')
//         string(name: 'JOB_NAME', defaultValue: 'my-pipeline', description: 'Name of the Jenkins job to create')
//     }

//     environment {
//         PYTHON_VENV = 'venv'  // Name of your Python virtual environment
//     }

//     stages {
//         stage('Setup') {
//             steps {
//                 script {
//                     // Ensure the virtual environment is set up
//                     if (!fileExists("${env.PYTHON_VENV}/bin/activate")) {
//                         sh 'python3 -m venv venv'
//                     }
//                 }
//             }
//         }

//         stage('Install Dependencies') {
//             steps {
//                 sh """
//                 source ${env.PYTHON_VENV}/bin/activate
//                 pip install requests python-dotenv
//                 """
//             }
//         }

//         stage('Create Repository') {
//             steps {
//                 sh """
//                 source ${env.PYTHON_VENV}/bin/activate
//                 python repo_creat.py ${params.REPO_NAME}
//                 """
//             }
//         }

//         stage('Create Jenkins Pipeline Job') {
//             steps {
//                 sh """
//                 source ${env.PYTHON_VENV}/bin/activate
//                 python create_pipeline.py ${params.REPO_NAME} ${params.JOB_NAME}
//                 """
//             }
//         }
//     }

//     post {
//         always {
//             cleanWs() // Clean workspace after build
//         }
//     }
// }
pipeline {
    agent any

    parameters {
        string(name: 'REPO_NAME', defaultValue: 'Hello-', description: 'Name of the repository to create')
        string(name: 'JOB_NAME', defaultValue: 'my-pipeline', description: 'Name of the Jenkins job to create')
    }

    environment {
        PATH = "${env.PATH}:${WORKSPACE}/venv/bin"
    }

    stages {
        stage('Setup Python') {
            steps {
                sh 'python3 -m venv venv'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'venv/bin/pip install requests python-dotenv'
            }
        }

        stage('Create Repository') {
            steps {
                sh 'python3 repo_creat.py ${params.REPO_NAME}'
            }
        }

        stage('Create Jenkins Pipeline Job') {
            steps {
                sh 'python3 create_pipeline.py ${params.REPO_NAME} ${params.JOB_NAME}'
            }
        }
    }

    post {
        always {
            cleanWs() // Clean workspace after build
        }
    }
}
