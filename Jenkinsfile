pipeline {
    agent any
    //agent { 
        //docker { image 'python:3.8.12-slim-buster' } 
    //}
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
