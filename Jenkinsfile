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
            }
        }
        // stage('Run Tests') {
        //     steps {
        //         sh 'pytest /app/tests/unit --cov=app --cov-report=term-missing'
        //     }
        // }
    }
}
