pipeline {
    agent any
    environment {
        // Define environment variables
        DOCKER_IMAGE = 'dileepteeparthi/devops-hello-world'
        DOCKER_TAG = "build-${env.BUILD_NUMBER}"
        // Jenkins credential ID for your container registry
        REGISTRY_CREDENTIALS = credentials('docker-hub-credentials')
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
                    // Build the Docker image, tag it with the build number
                    docker.build("${env.DOCKER_IMAGE}:${env.DOCKER_TAG}")
                }
            }
        }
        
        stage('Test with Docker Compose') {
            steps {
                bat 'docker-compose up -d'
                // Use PowerShell to wait
                powershell 'Start-Sleep -Seconds 10'
                // Test the application
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
                    // Use the environment variables instead of hardcoded values
                    docker.withRegistry('', env.REGISTRY_CREDENTIALS) {
                        docker.image("${env.DOCKER_IMAGE}:${env.DOCKER_TAG}").push()
                        // Optional: push as latest
                        docker.image("${env.DOCKER_IMAGE}:${env.DOCKER_TAG}").push('latest')
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
            // Clean up: remove built images to save disk space
            bat "docker rmi ${env.DOCKER_IMAGE}:${env.DOCKER_TAG} 2>nul || echo Image not found, skipping delete"
        }
        success {
            echo "Pipeline completed successfully! 🎉"
        }
        failure {
            echo "Pipeline failed! ❌"
        }
    }
}