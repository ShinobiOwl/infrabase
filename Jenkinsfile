pipeline {
    agent any
    environment {
        OCI_REGION = "ap-mumbai-1"
        TENANCY_NS = credentials('oci-tenancy-ns')
        IMAGE_NAME = "${OCI_REGION}.ocir.io/${TENANCY_NS}/infrabase"
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:latest ."
            }
        }
        stage('Push to OCIR') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'oci-creds', passwordVariable: 'OCI_PASS', usernameVariable: 'OCI_USER')]) {
                    sh "echo ${OCI_PASS} | docker login ${OCI_REGION}.ocir.io -u ${OCI_USER} --password-stdin"
                }
                sh "docker push ${IMAGE_NAME}:latest"
            }
        }
        stage('Deploy to Oracle VM') {
            steps {
                sh """
                    docker stop infrabase_app || true
                    docker rm infrabase_app || true
                    docker run -d \
                      --name infrabase_app \
                      --restart unless-stopped \
                      -e DEBUG=False \
                      -e DB_HOST=infrabase_db \
                      --network web_network \
                      ${IMAGE_NAME}:latest
                """
            }
        }
    }
}