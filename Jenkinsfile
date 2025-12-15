pipeline {
    agent any

    environment {
        DOCKER_NETWORK = 'ci-network'
    }

    stages {

        stage('Clone Main Repository') {
            steps {
                git branch: 'selenium', url: 'https://github.com/Muhammad-Daud-0/Shop-Sphere.git'
            }
        }

        stage('Build & Run Main Containers') {
            steps {
                sh '''
                docker compose down || true
                docker compose up -d --build
                '''
            }
        }

        stage('Verify Running Containers') {
            steps {
                sh 'docker ps'
            }
        }
        post {
        success {
            script {
                echo "✅ CI Build Completed Successfully!"
                mail (
                    subject: "Tests PASSED: ${env.JOB_NAME} [${env.BUILD_NUMBER}]",
                    body: "All tests passed.\nBuild: ${env.BUILD_URL}",
                    to: "mdaud9062@gmail.com"
                )
            }
        }
        failure {
            script {
                echo "❌ Build Failed. Check logs."
                mail (
                    subject: "Tests FAILED: ${env.JOB_NAME} [${env.BUILD_NUMBER}]",
                    body: "Tests failed.\nBuild: ${env.BUILD_URL}",
                    to: "mdaud9062@gmail.com"
                )
            }
        }
    }    
        stage('Wait for Frontend to Start') {
            steps {
                script {
                    sh '''
                    echo "Waiting for user-frontend-ci (5173) to be ready..."
                    while ! sudo docker run --rm --network=ci-network busybox nc -z user-frontend-ci 5173; do
                        echo "Frontend not ready... retrying..."
                        sleep 2
                    done
                    echo "Frontend is UP!"
                    '''
                }
            }
        }

        stage('Run Selenium Tests') {
            steps {
                dir('selenium-tests') {
                    sh '''
                    echo "Building Selenium Test Image..."
                    docker build -t selenium-tests .
                    echo "Running Selenium Tests..."
                    docker run --rm \
                        --network=ci-network \
                        -e BASE_URL="http://user-frontend-ci:5173" \
                        selenium-tests
                    '''
                }
            }
        }

        stage('Show Logs') {
            steps {
                sh 'docker compose logs --tail=100'
            }
        }
    }

    
}
