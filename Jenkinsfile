pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.9'
        VENV_NAME = 'venv'
        ALLURE_RESULTS = 'allure-results'
        ALLURE_REPORT = 'allure-report'
        TEST_RESULTS = 'test-results'
        SCREENSHOTS = 'screenshots'
        LOGS = 'logs'
    }
    
    options {
        // Discard old builds to save disk space
        buildDiscarder(logRotator(numToKeepStr: '10'))
        // Timeout for the entire pipeline
        timeout(time: 30, unit: 'MINUTES')
        // Disable concurrent builds
        disableConcurrentBuilds()
    }
    
    stages {
        stage('Checkout') {
            steps {
                // Clean workspace before checkout
                cleanWs()
                // Checkout code from SCM
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                script {
                    // Create virtual environment
                    sh '''
                        python3 -m venv ${VENV_NAME}
                        . ${VENV_NAME}/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                    
                    // Create necessary directories
                    sh '''
                        mkdir -p ${ALLURE_RESULTS}
                        mkdir -p ${TEST_RESULTS}
                        mkdir -p ${SCREENSHOTS}
                        mkdir -p ${LOGS}
                    '''
                }
            }
        }
        
        stage('Lint and Validate') {
            steps {
                script {
                    sh '''
                        . ${VENV_NAME}/bin/activate
                        # Run flake8 for code linting
                        pip install flake8
                        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
                        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
                    '''
                }
            }
        }
        
        stage('Run Tests') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        script {
                            sh '''
                                . ${VENV_NAME}/bin/activate
                                pytest tests/ -v --junitxml=${TEST_RESULTS}/unit-tests.xml --alluredir=${ALLURE_RESULTS}
                            '''
                        }
                    }
                }
                
                stage('Integration Tests') {
                    steps {
                        script {
                            sh '''
                                . ${VENV_NAME}/bin/activate
                                pytest tests/test_login.py -v --junitxml=${TEST_RESULTS}/integration-tests.xml --alluredir=${ALLURE_RESULTS}
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Generate Reports') {
            steps {
                script {
                    // Generate Allure report
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: '${ALLURE_RESULTS}']]
                    ])
                    
                    // Archive test results
                    archiveArtifacts artifacts: '${TEST_RESULTS}/**/*', allowEmptyArchive: true
                    archiveArtifacts artifacts: '${SCREENSHOTS}/**/*', allowEmptyArchive: true
                    archiveArtifacts artifacts: '${LOGS}/**/*', allowEmptyArchive: true
                }
            }
        }
    }
    
    post {
        always {
            script {
                // Publish test results
                junit '${TEST_RESULTS}/*.xml'
                
                // Clean up workspace
                cleanWs()
            }
        }
        success {
            script {
                echo 'Pipeline completed successfully!'
                // You can add notifications here (email, Slack, etc.)
            }
        }
        failure {
            script {
                echo 'Pipeline failed!'
                // You can add failure notifications here
            }
        }
        unstable {
            script {
                echo 'Pipeline is unstable!'
            }
        }
    }
} 