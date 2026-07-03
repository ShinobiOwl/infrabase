pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'infrabase'
        OCIR_REPO = 'your-region.ocir.io/your-tenancy-namespace/infrabase'
        DOCKER_TAG = "${BUILD_NUMBER}"
        CONTAINER_NAME = 'infrabase-app'
        DEPLOY_PORT = '5000'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                        docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${OCIR_REPO}:${DOCKER_TAG}
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${OCIR_REPO}:latest
                    """
                }
            }
        }

        stage('Push to OCIR') {
            steps {
                script {
                    withCredentials([
                        string(credentialsId: 'oci-tenancy-ns', variable: 'TENANCY_NS'),
                        usernamePassword(credentialsId: 'oci-creds', usernameVariable: 'OCI_USER', passwordVariable: 'OCI_AUTH_TOKEN')
                    ]) {
                        sh """
                            docker login -u '${TENANCY_NS}/${OCI_USER}' -p '${OCI_AUTH_TOKEN}' your-region.ocir.io
                            docker push ${OCIR_REPO}:${DOCKER_TAG}
                            docker push ${OCIR_REPO}:latest
                        """
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    withCredentials([
                        sshUserPrivateKey(
                            credentialsId: 'server-ssh-key',
                            keyFileVariable: 'SSH_KEY',
                            usernameVariable: 'SSH_USER'
                        )
                    ]) {
                        sh """
                            ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no ${SSH_USER}@your-vm-ip << 'EOF'
                                docker pull ${OCIR_REPO}:latest
                                docker stop ${CONTAINER_NAME} || true
                                docker rm ${CONTAINER_NAME} || true
                                docker run -d \\
                                    --name ${CONTAINER_NAME} \\
                                    --restart unless-stopped \\
                                    -p ${DEPLOY_PORT}:5000 \\
                                    ${OCIR_REPO}:latest
                                docker image prune -f
EOF
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully! Image: ${OCIR_REPO}:${DOCKER_TAG}"
        }
        failure {
            echo "Pipeline failed. Check Jenkins console output for details."
        }
    }
}