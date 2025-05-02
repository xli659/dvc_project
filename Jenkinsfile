pipeline {
    agent {
        kubernetes {
            yaml '''
                apiVersion: v1
                kind: Pod
                spec:
                  securityContext:
                    runAsNonRoot: true
                    seccompProfile:
                      type: RuntimeDefault
                  containers:
                  - name: python
                    image: python:3.12-slim
                    command:
                    - cat
                    tty: true
                    securityContext:
                      allowPrivilegeEscalation: false
                      capabilities:
                        drop: ["ALL"]
                      runAsUser: 1007010000
                      runAsGroup: 1007010000
                    volumeMounts:
                    - name: cache-volume
                      mountPath: /workspace/.cache
                  volumes:
                  - name: cache-volume
                    emptyDir: {}
            '''
        }
    }

    environment {
        DOCKER_IMAGE = 'fastapi_app'
        GIT_REPO = 'https://github.com/your-repo/dvc_project.git'
        PYTHONUSERBASE = '${WORKSPACE}/.local'
        PATH = '${WORKSPACE}/.local/bin:${PATH}'
        PIP_CACHE_DIR = '/workspace/.cache/pip'
    }

    stages {
        stage('Setup') {
            steps {
                container('python') {
                    // Create local directories in workspace
                    sh '''
                        mkdir -p ${WORKSPACE}/.local/bin
                        mkdir -p ${WORKSPACE}/.cache/pip
                    '''
                    
                    // Install dependencies using local paths
                    sh '''
                        python -m pip install --user --cache-dir=${PIP_CACHE_DIR} pip --upgrade
                        python -m pip install --user --cache-dir=${PIP_CACHE_DIR} gitpython
                    '''
                }
            }
        }

        stage('Clone Repository') {
            steps {
                container('python') {
                    // Clean workspace and clone the repository
                    sh 'rm -rf *'
                    git url: env.GIT_REPO
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                container('python') {
                    sh '''
                        python -m pip install --user --cache-dir=${PIP_CACHE_DIR} pylint pytest fastapi uvicorn pydantic pytest-asyncio
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
            agent any
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