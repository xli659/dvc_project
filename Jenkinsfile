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
    stage('Lint') {
      steps {
        container('python') {
          sh '''
            pip install --upgrade pip
            pip install flake8
            flake8 .
          '''
        }
      }
    }
    stage('Test') {
      steps {
        container('python') {
          sh '''
            pip install pytest fastapi uvicorn pydantic pytest-asyncio
            pytest
          '''
        }
      }
    }
    stage('Build Image') {
      steps {
        container('oc') {
          sh '''
            oc start-build my-python-app --from-dir=. --wait
          '''
        }
      }
    }
  }
  post {
    always {
      cleanWs()
    }
  }
}
