pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'fastapi_app'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh '''
                    python -m pip install --upgrade pip
                    pip install pylint pytest fastapi uvicorn pydantic pytest-asyncio
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    pylint --disable=C0111,C0103,C0301,W0621 *.py
                    pylint --disable=C0111,C0103,C0301,W0621 test/*.py
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    cd test
                    pytest -v test_fastapi.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    sh "docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} ."
                    // Tag as latest
                    sh "docker tag ${DOCKER_IMAGE}:${BUILD_NUMBER} ${DOCKER_IMAGE}:latest"
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
        always {
            // Clean up old Docker images to save space
            sh '''
                docker image prune -f
                docker images -q -f dangling=true | xargs -r docker rmi
            '''
        }
    }
}