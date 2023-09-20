pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = 'us-east-1'
        AWS_ACCESS_KEY_ID     = credentials('aws-access-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')
        DOCKER_IMAGE_NAME = 'mindmate-main-app'
        ECR_REPOSITORY = 'mindmate-main-app'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout your Django app code from your version control system (e.g., Git)
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image of your Django app
                    def dockerImage = docker.build(env.DOCKER_IMAGE_NAME)

                    // Tag the Docker image for ECR repository
                    dockerImage.tag("${env.ECR_REPOSITORY}:latest")
                }
            }
        }

        stage('Push to ECR') {
            steps {
                script {
                    // Authenticate Docker with AWS ECR
                    withCredentials([
                            [$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'your-aws-credentials-id']
                        ]) {
                        docker.withRegistry("https://${env.AWS_DEFAULT_REGION}.dkr.ecr.${env.AWS_DEFAULT_REGION}.amazonaws.com", 'ecr:us-east-1') {
                            // Push the Docker image to ECR
                            docker.image("${env.ECR_REPOSITORY}:latest").push()
                        }
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Docker image successfully built and pushed to ECR!'
        }
        failure {
            echo 'Docker image failed to bu built and pushed to ECR!'
        }
    }
}
