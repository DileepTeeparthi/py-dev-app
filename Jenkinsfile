pipeline {
    agent any
    environment {
        // Define environment variables
        DOCKER_IMAGE = 'dileepteeparthi/devops-hello-world'
        DOCKER_TAG = "build-${env.BUILD_NUMBER}"
        // Jenkins credential ID for your container registry
        REGISTRY_CREDENTIALS = credentials('devdoc')
    }
    stages {
        stage('Checkout') {
            steps {
                // Get the code from your repository - use the actual URL
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
                // Start the stack and run tests - use bat for Windows
                bat 'docker-compose up -d'
                // Wait a few seconds for services to start
                bat 'timeout /t 10 /nobreak > nul'
                // Run a simple test - check if the web server responds
                bat 'curl -f http://localhost:5000 && echo ✓ Application responded successfully. || (echo ✗ Application failed to respond. & exit /b 1)'
            }
            post {
                always {
                    // Always tear down the test environment
                    bat 'docker-compose down'
                }
            }
        }
        
        stage('Push to Registry') {
            steps {
                script {
                    // Log in to Docker registry using Jenkins credentials
                    docker.withRegistry('', env.REGISTRY_CREDENTIALS) {
                        // Push the built image to the registry
                        docker.image("${env.DOCKER_IMAGE}:${env.DOCKER_TAG}").push()
                        // Also push as 'latest' (optional)
                        docker.image("${env.DOCKER_IMAGE}:${env.DOCKER_TAG}").push('latest')
                    }
                }
            }
        }
        
        stage('Deploy to Staging') {
            // This stage is optional - depends on your infrastructure
            steps {
                echo "Deployment would happen here. Configure based on your environment."
            }
        }
    }
    post {
        always {
            // Clean up: remove built images to save disk space - use bat for Windows
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