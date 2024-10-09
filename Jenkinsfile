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
        // stage('Configure System') {
        //     steps {
        //         sh 'python -m pip install --upgrade pip'
        //     }
        // }
        // stage('Checkout') {
        //     steps {
        //         checkout scm
        //     }
        // }
        // stage('Install Dependencies') {
        //     steps {
        //         sh 'pip install -r requirements.txt'
        //     }
        // }
        stage('Run Tests') {
            steps {
                sh 'pytest /app/tests/unit --cov=app --cov-report=term-missing'
            }
        }
    }
}
