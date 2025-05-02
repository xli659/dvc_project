pipeline {
    agent {
        kubernetes {
            yaml '''
                apiVersion: v1
                kind: Pod
                spec:
                  containers:
                  - name: python
                    image: python:3.12-slim
                    command:
                    - cat
                    tty: true
                    securityContext:
                      runAsUser: 0
                      runAsGroup: 0
                    volumeMounts:
                    - name: cache-volume
                      mountPath: /root/.cache
                  volumes:
                  - name: cache-volume
                    emptyDir: {}
            '''
        }
    }

    environment {
        DOCKER_IMAGE = 'fastapi_app'
        GIT_REPO = 'https://github.com/your-repo/dvc_project.git'  // Replace with actual repo URL
    }

    stages {
        stage('Setup') {
            steps {
                container('python') {
                    // Install git
                    sh '''
                        apt-get update
                        apt-get install -y git
                    '''
                }
            }
        }

        stage('Clone Repository') {
            steps {
                container('python') {
                    // Clean workspace and clone the repository
                    sh 'rm -rf *'
                    sh 'git clone ${GIT_REPO} .'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                container('python') {
                    sh '''
                        python -m pip install --upgrade pip
                        pip install pylint pytest fastapi uvicorn pydantic pytest-asyncio
                    '''
                }
            }
        }

        stage('Lint') {
            steps {
                container('python') {
                    sh '''
                        pylint --disable=C0111,C0103,C0301,W0621 *.py
                        pylint --disable=C0111,C0103,C0301,W0621 test/*.py
                    '''
                }
            }
        }

        stage('Test') {
            steps {
                container('python') {
                    sh '''
                        cd test
                        pytest -v test_fastapi.py
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            agent any  // Switch back to Jenkins agent for Docker operations
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