pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'dileepteeparthi/devops-hello-world'
        DOCKER_TAG = "build-${env.BUILD_NUMBER}"
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', 
                url: 'https://github.com/DileepTeeparthi/py-dev-app.git', 
                credentialsId: 'devdoc'
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
                        bat "echo %REGISTRY_CREDENTIALS_PSW% | docker login -u %REGISTRY_CREDENTIALS% --password-stdin"
                        bat "docker build -t ${env.DOCKER_IMAGE}:${env.DOCKER_TAG} ."
                    }
                }
            }
        }
        
        stage('Test with Docker Compose') {
            steps {
                powershell '''
                    $containers = docker ps -q --filter "publish=5002"
                    if ($containers) {
                        docker stop $containers
                    } else {
                        Write-Host "No containers on port 5002"
                    }
                '''
                bat 'docker-compose up -d'
                powershell 'Start-Sleep -Seconds 10'
                bat 'curl -f http://localhost:5002 && echo ✓ Application responded successfully. || (echo ✗ Application failed to respond. & exit /b 1)'
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
        
        stage('Prepare Kubernetes') {
    steps {
        script {
            // Switch to Docker Desktop Kubernetes
            bat 'kubectl config use-context docker-desktop'
            
            // Verify Kubernetes is working with timeout
            bat '''
                timeout 30 kubectl get nodes >nul 2>&1
                if errorlevel 1 (
                    echo "Kubernetes not ready - but continuing pipeline"
                    exit 0
                )
            '''
        }
    }
}

stage('Deploy to Kubernetes') {
    steps {
        script {
            // Check if Kubernetes is responsive
            def KUBE_READY = bat(script: 'kubectl get nodes 2>nul && echo "READY" || echo "NOT_READY"', returnStdout: true).trim()
            
            if (KUBE_READY == "READY") {
                echo "🚀 Deploying to Docker Desktop Kubernetes..."
                
                // Update image in deployment file
                powershell """
                    (Get-Content k8s-deployment.yaml) -replace 'dileepteeparthi/devops-hello-world:blue', '${env.DOCKER_IMAGE}:${env.DOCKER_TAG}' | Set-Content k8s-deployment.yaml
                """
                
                // Apply deployment
                bat 'kubectl apply -f k8s-deployment.yaml --validate=false'
                bat 'kubectl rollout status deployment/devops-hello-world --timeout=120s'
                
                echo "🎉 Successfully deployed to Kubernetes!"
                
                // Create port-forward for access
                bat 'start /B kubectl port-forward service/devops-hello-world-service 8080:80'
                echo "🌐 Application accessible at: http://localhost:8080"
                
            } else {
                echo "⏭️ Kubernetes not available - skipping deployment"
                echo "✅ CI Pipeline completed successfully!"
                echo "📦 Docker image: ${env.DOCKER_IMAGE}:${env.DOCKER_TAG}"
            }
        }
    }
}
}
    post {
        always {
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