pipeline {
    agent any
    environment {
        // Define environment variables
        DOCKER_IMAGE = 'dileepteeparthi/devops-hello-world'
        DOCKER_TAG = "build-${env.BUILD_NUMBER}"
    }
    stages {
        stage('Checkout') {
            steps {
                // Get the code from your repository
                git branch: 'master', url: 'https://github.com/DileepTeeparthi/py-dev-app.git', credentialsId: 'devdoc'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: 'docker-hub-credentials',
                        usernameVariable: 'REGISTRY_CREDENTIALS',
                        passwordVariable: 'REGISTRY_CREDENTIALS_PSW'
                    )]) {
                        // Authenticate with Docker Hub before building
                        bat "echo %REGISTRY_CREDENTIALS_PSW% | docker login -u %REGISTRY_CREDENTIALS% --password-stdin"
                        // Build the Docker image, tag it with the build number
                        docker.build("${env.DOCKER_IMAGE}:${env.DOCKER_TAG}")
                    } // ← This closing brace was missing
                }
            }
        } // ← And this closing brace
        
       stage('Test with Docker Compose') {
    steps {
        // Stop any existing containers using port 5000
        bat 'docker ps -q --filter "publish=5000" | findstr . && docker stop $(docker ps -q --filter "publish=5000") || echo No containers on port 5000'
        
        bat 'docker-compose up -d'
        powershell 'Start-Sleep -Seconds 10'
        bat 'curl -f http://localhost:5000 && echo ✓ Application responded successfully. || (echo ✗ Application failed to respond. & exit /b 1)'
    }
    post {
        always {
            bat 'docker-compose down'
        }
    }
}

        
        stage('Push to Registry') {
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: 'docker-hub-credentials',
                        usernameVariable: 'REGISTRY_CREDENTIALS',
                        passwordVariable: 'REGISTRY_CREDENTIALS_PSW'
                    )]) {
                        bat """
                            echo %REGISTRY_CREDENTIALS_PSW% | docker login -u %REGISTRY_CREDENTIALS% --password-stdin
                            docker push ${env.DOCKER_IMAGE}:${env.DOCKER_TAG}
                            docker logout
                        """
                    }
                }
            }
        }
        
        stage('Deploy to Staging') {
            steps {
                echo "Deployment would happen here. Configure based on your environment."
            }
        }
    }
    post {
        always {
            // Clean up: remove built images and logout
            bat "docker rmi ${env.DOCKER_IMAGE}:${env.DOCKER_TAG} 2>nul || echo Image not found, skipping delete"
            bat "docker logout 2>nul || echo Already logged out"
        }
        success {
            echo "Pipeline completed successfully! 🎉"
        }
        failure {
            echo "Pipeline failed! ❌"
        }
    }
}