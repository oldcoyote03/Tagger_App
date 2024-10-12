pipeline {
    agent { 
        dockerfile {
            filename 'Dockerfile'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        } 
    }
    stages {
        
        // Unit tests run for all pipelines
        stage('Unit Tests') {
            steps {
                echo 'Running unit tests'
                sh 'pytest tests/unit --cov=app --cov-report=term-missing'
            }
            post {
                success {
                    echo 'Unit tests passed'
                }
                failure {
                    echo 'Unit tests failed'
                }
            }
        }

        // Local tests run for merges to 'develop'
        stage('Develop Branch Pipeline') {
            when {
                branch 'develop'
            }
            steps {
                echo 'Running pipeline for the develop branch...'
                sh 'pytest tests/local'
            }
            post {
                success {
                    echo 'Code successfully merged to develop branch and tested'
                }
                failure {
                    echo 'Develop branch pipeline failed'
                }
            }
        }

        // Integration tests run for merges to 'main'
        stage('Main Branch Pipeline') {
            when {
                branch 'main'
            }
            steps {
                echo 'Running integration tests'
                sh 'pytest tests/integration'
            }
            post {
                success {
                    echo 'Code successfully merged to main branch and tested'
                }
                failure {
                    echo 'Main branch pipeline failed'
                }
            }
        }
    }
}
