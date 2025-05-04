// Jenkinsfile (Declarative Pipeline)

pipeline {
  agent {
    kubernetes {
      yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: python
    image: python:3.11
    command: ["/bin/sh", "-c", "while true; do sleep 30; done;"]
    tty: true
  - name: oc
    image: quay.io/openshift/origin-cli:latest
    command: ["/bin/sh", "-c", "while true; do sleep 30; done;"]
    tty: true
"""
      defaultContainer 'python'
    }
  }
  stages {
    stage('Clone') {
      steps {
        git branch: 'main', url: 'https://github.com/xli659/dvc_project.git'
      }
    }
    stage('Test') {
      steps {
        container('python') {
          sh '''
            export HOME=/home/jenkins/agent
            export PATH=$HOME/.local/bin:$PATH
            pip install pytest fastapi uvicorn pydantic pytest-asyncio httpx
            pytest
          '''
        }
      }
    }
    stage('Build and Deploy with OpenShift') {
      steps {
        container('oc') {
          sh '''
            yum install -y git || true
            oc new-app --name=my-python-app . || true
            oc rollout status dc/my-python-app
          '''
        }
      }
    }
  }
  post {
    always {
      deleteDir()
    }
  }
}
