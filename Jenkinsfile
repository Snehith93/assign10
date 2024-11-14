pipeline {
    agent { label 'slave-node' }

    environment {
        ECR_REPO = '866934333672.dkr.ecr.ca-central-1.amazonaws.com/snehith/assign10'          // Replace with actual ECR URL
        IMAGE_NAME = 'flask-app'
        TAG = "${env.BRANCH_NAME}-${env.BUILD_ID}"
        PORT = "${env.BRANCH_NAME == 'DEV' ? '5001' : env.BRANCH_NAME == 'STAGING' ? '5002' : '5003'}"
        CONTAINER_NAME = "${IMAGE_NAME}-${env.BRANCH_NAME}"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: "${env.BRANCH_NAME}", url: 'https://github.com/Snehith93/assign10.git' // GitHub repository URL
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build an image tagged with the branch name and build ID
                    sh "docker build -t ${env.ECR_REPO}:${env.TAG} ."
                }
            }
        }

        stage('Push to ECR') {
            steps {
                // Log in to ECR using the instance profile attached to the EC2 instance
                sh "aws ecr get-login-password --region ca-central-1 | docker login --username AWS --password-stdin ${env.ECR_REPO}"
                
                // Push the Docker image to ECR with the branch-specific tag
                sh "docker push ${env.ECR_REPO}:${env.TAG}"
            }
            post {
                success {
                // Send a basic email notification after successful image push to ECR
                    mail(
                        to: 'sdatla2000@gmail.com', // Replace with the recipient's email
                        subject: "Jenkins Job - Docker Image Pushed to ECR Successfully",
                        body: "Hello,\n\nThe Docker image '${env.IMAGE_NAME}:${env.TAG}' has been successfully pushed to ECR.\n\nBest regards,\nJenkins"
                    )
                }
            }
        }

        stage('Cleanup Previous Containers') {
            steps {
                script {
                    // Stop and remove any container with the same name for the current branch
                    sh "docker stop ${CONTAINER_NAME} || true"
                    sh "docker rm ${CONTAINER_NAME} || true"
                    sh "fuser -k ${PORT}/tcp || true" // Free up the designated port
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Run the Docker container for testing with the branch-specific port
                    sh "docker run -d --name ${CONTAINER_NAME} -p ${PORT}:5000 ${ECR_REPO}:${TAG}"
                    sh 'sleep 5' // Wait for the container to start

                    // Test if the Flask app is responding on the designated port
                    sh "curl -f http://localhost:${PORT} || exit 1"

                    // Stop and remove the test container after testing
                    sh "docker stop ${CONTAINER_NAME}"
                    sh "docker rm ${CONTAINER_NAME}"
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'main'  // Only deploy if we're on the main branch
            }
            steps {
                script {
                    // Deploy the main branch container to production on port 80
                    sh """
                    docker pull ${ECR_REPO}:${TAG}
                    docker stop ${IMAGE_NAME} || true
                    docker rm ${IMAGE_NAME} || true
                    docker run -d --name ${IMAGE_NAME} -p 80:5000 ${ECR_REPO}:${TAG}
                    """
                }
            }
        }
    }

    post {
        always {
            cleanWs()  // Clean up workspace after the build
        }
    }
}
