pipeline {
    agent { 
        dockerfile {
            filename 'Dockerfile'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        } 
    }
    stages {
        
        // Unit tests for all pipelines
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

        // Code analysis for all pipelines
        stage('Code Analysis') {
            steps {
                echo 'Running code analysis'
                // sh 'mkdir -p $WORKSPACE/.pylint'
                // sh 'export PYLINTHOME=$WORKSPACE/.pylint'
                // sh 'pylint --disable=W1203 \
                //     --output-format=parseable --reports=no app > pylint.log \
                //     | echo "pylint exited with $?"'
                // sh 'cat pylint.log'
                sh '''
                   mkdir -p $WORKSPACE/.pylint
                   export PYLINTHOME=$WORKSPACE/.pylint
                   pylint --disable=W1203 \
                          --output-format=parseable --reports=no app > pylint.log \
                          | echo "pylint exited with $?"'
                   cat pylint.log
                '''
            }
            post {
                success {
                    echo 'Code analysis passed'
                }
                failure {
                    echo 'Code analysis failed'
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
