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
                    image: python:3.12
                    command:
                      - /bin/sh
                      - -c
                      - "while true; do sleep 30; done;"
                    tty: true
                    securityContext:
                      allowPrivilegeEscalation: false
                      capabilities:
                        drop: ["ALL"]
                      runAsUser: 1007010000
                      runAsGroup: 1007010000
                    workingDir: /home/jenkins/agent
                    volumeMounts:
                    - name: workspace-volume
                      mountPath: /home/jenkins/agent
                  volumes:
                  - name: workspace-volume
                    emptyDir: {}
            '''
        }
    }

    environment {
        DOCKER_IMAGE = 'fastapi_app'
        GIT_REPO = 'https://github.com/your-repo/dvc_project.git'
        PYTHONUSERBASE = '/home/jenkins/agent/.local'
        PATH = '/home/jenkins/agent/.local/bin:${PATH}'
        PIP_CACHE_DIR = '/home/jenkins/agent/.cache/pip'
    }

    stages {
        stage('Setup Python Environment') {
            steps {
                container('python') {
                    sh '''
                        mkdir -p /home/jenkins/agent/.local/bin
                        mkdir -p /home/jenkins/agent/.cache/pip
                        python -m pip install --user pip --upgrade
                        python -m pip install --user gitpython
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
                        python -m pip install --user pylint pytest fastapi uvicorn pydantic pytest-asyncio
                    '''
                }
            }
        }

        stage('Lint') {
            steps {
                container('python') {
                    sh '''
                        export PATH=/home/jenkins/agent/.local/bin:$PATH
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
                        export PATH=/home/jenkins/agent/.local/bin:$PATH
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
        always {
            script {
                // Clean up Docker images
                sh '''
                    docker image prune -f
                    docker images -q -f dangling=true | xargs -r docker rmi
                '''
                
                // Clean up Python container and workspace
                container('python') {
                    sh '''
                        rm -rf /home/jenkins/agent/.local/*
                        rm -rf /home/jenkins/agent/.cache/*
                    '''
                }
                
                // Clean up the pod and ensure container removal
                sh '''
                    # Get the pod name
                    POD_NAME=$(kubectl get pods -n shawnalexnew-dev -l jenkins=slave --no-headers -o custom-columns=":metadata.name" | grep pipeline-)
                    
                    if [ ! -z "$POD_NAME" ]; then
                        # Force delete the pod to ensure immediate cleanup
                        kubectl delete pod $POD_NAME -n shawnalexnew-dev --force --grace-period=0 || true
                        
                        # Wait for pod deletion
                        kubectl wait --for=delete pod/$POD_NAME -n shawnalexnew-dev --timeout=30s || true
                    fi
                '''
            }
            
            cleanWs() // Clean workspace after pipeline
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}