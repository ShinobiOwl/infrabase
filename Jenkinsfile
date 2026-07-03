pipeline {
    agent any

    environment {
        OCI_REGION = "ap-mumbai-1"
        TENANCY_NS = credentials('oci-tenancy-ns')
        IMAGE_NAME = "${OCI_REGION}.ocir.io/${TENANCY_NS}/infrabase"
    }

    stages {
        stage('1. Git Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('2. Build Production Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:latest -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
            }
        }
        
        stage('3. Push to OCI Registry (OCIR)') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'oci-creds', passwordVariable: 'OCI_PASS', usernameVariable: 'OCI_USER')]) {
                    sh "echo ${OCI_PASS} | docker login ${OCI_REGION}.ocir.io -u ${OCI_USER} --password-stdin"
                }
                sh "docker push ${IMAGE_NAME}:latest"
                sh "docker push ${IMAGE_NAME}:${BUILD_NUMBER}"
                echo '✅ Image pushed to Oracle Container Registry!'
            }
        }
        
        stage('4. Deploy to Oracle VM') {
            steps {
                // Because Jenkins runs on the same VM, we can execute docker commands directly.
                // We stop the old container, remove it, and run the new one from OCIR.
                sh """
                    docker stop infrabase_app || true
                    docker rm infrabase_app || true
                    
                    docker run -d \\
                      --name infrabase_app \\
                      --restart unless-stopped \\
                      -e DEBUG=False \\
                      -e DB_HOST=infrabase_db \\
                      -e DJANGO_SECRET_KEY=\${DJANGO_SECRET_KEY} \\
                      --network web_network \\
                      ${IMAGE_NAME}:latest
                    
                    # Connect the new app container to the internal DB network as well
                    docker network connect infrabase_internal infrabase_app || true
                """
                echo '✅ InfraBase deployed and connected to Caddy!'
            }
        }
    }
    
    post {
        success {
            echo '🚀 PIPELINE SUCCESS: InfraBase is live at infrabase.duckdns.org!'
        }
        failure {
            echo '❌ PIPELINE FAILED: Check Jenkins logs.'
        }
    }
}