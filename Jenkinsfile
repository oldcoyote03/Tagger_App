pipeline {
    // agent any
    agent { 
        docker { 
            image 'python:3.12-slim-bookworm'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        } 
    }
    // agent { dickerfile true }
    stages {
        stage('Hello') {
            steps {
                echo 'Hello world!'
            }
        }
        stage('Python') {
            steps {
                sh 'python3 --version'
            }
        }
    }
}
