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
                // Get the code from your repository
                git branch: 'main', url: 'https://github.com/your-username/your-repo-name.git'
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
                // Start the stack and run tests
                sh 'docker-compose up -d'
                // Wait a few seconds for services to start
                sleep 10
                // Run a simple test - check if the web server responds
                sh '''
                    curl -f http://localhost:5000 || exit 1
                    echo "✓ Application responded successfully."
                '''
                // You can add more rigorous tests here (e.g., with pytest)
            }
            post {
                always {
                    // Always tear down the test environment
                    sh 'docker-compose down'
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
                // Example: Deploy to a Kubernetes cluster
                // sh 'kubectl apply -f k8s-deployment.yaml'
                
                // Or: Deploy to a server with Docker Compose
                // sh 'scp docker-compose.prod.yml user@server:/app/ && ssh user@server "cd /app && docker-compose pull && docker-compose up -d"'
                
                echo "Deployment would happen here. Configure based on your environment."
            }
        }
    }
    post {
        always {
            // Clean up: remove built images to save disk space
            sh "docker rmi ${env.DOCKER_IMAGE}:${env.DOCKER_TAG} || true"
        }
        success {
            echo "Pipeline completed successfully! 🎉"
            // Optional: Send notification (e.g., Slack, email)
        }
        failure {
            echo "Pipeline failed! ❌"
            // Optional: Send failure notification
        }
    }
}
