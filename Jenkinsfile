pipeline {
    // agent any
    // agent { 
    //     docker { 
    //         image 'python:3.12-slim-bookworm'
    //         args '-v /var/run/docker.sock:/var/run/docker.sock'
    //     } 
    // }
    agent { 
        dockerfile {
            filename 'Dockerfile'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        } 
    }
    stages {
        stage('File System') {
            steps {
                sh 'ls -l /'
                sh 'pwd'
                sh 'ls -l'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'pytest tests/unit --cov=app --cov-report=term-missing'
                // sh 'pytest /app/tests/unit --cov=app --cov-report=term-missing'
            }
        }
    }
}
