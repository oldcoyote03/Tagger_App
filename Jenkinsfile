pipeline {
    agent { docker { image 'python:3.10.7-alpine' } }
    //agent any 
    stages {
        stage('Stage 1') {
            steps {
                echo 'Hello world!'
            }
        }
        stage('Stage 2') {
            steps {
                sh 'python --version'
            }
        }
    }
}
