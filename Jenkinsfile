pipeline {
    agent any
    
    environment {
        OCI_REGION = "ap-singapore-1" 
        TENANCY_NS = credentials('oci-tenancy-ns') 
        IMAGE_NAME = "${OCI_REGION}.ocir.io/${TENANCY_NS}/infrabase"
    }

    stages {
        stage('1. Checkout Code') {
            steps {
                checkout scm
            }
        }
        
        stage('2. Build Docker Image') {
            steps {
                echo 'Building InfraBase Django App Image...'
                sh "docker build -t ${IMAGE_NAME}:latest -t ${IMAGE_NAME}:${BUILD_NUMBER} -f docker/Django.Dockerfile ."
            }
        }
        
        stage('3. Push to OCI Registry (OCIR)') {
            steps {
                echo 'Logging into Oracle Container Registry...'
                withCredentials([usernamePassword(credentialsId: 'oci-creds', passwordVariable: 'OCI_PASS', usernameVariable: 'OCI_USER')]) {
                    sh "echo ${OCI_PASS} | docker login ${OCI_REGION}.ocir.io -u ${OCI_USER} --password-stdin"
                }
                
                echo 'Pushing image to the secure cloud pendrive...'
                sh "docker push ${IMAGE_NAME}:latest"
                sh "docker push ${IMAGE_NAME}:${BUILD_NUMBER}"
            }
        }
        
        stage('4. Deploy to Oracle VM') {
            steps {
                echo 'Deploying InfraBase to Production...'
                sh '''
                    # Stop and remove the old Django container
                    docker stop infrabase_app || true
                    docker rm infrabase_app || true
                    
                    # Run the NEW Django App Container
                    docker run -d \
                      --name infrabase_app \
                      --restart unless-stopped \
                      -e DJANGO_SECRET_KEY=change-this-in-prod-$(date +%s) \
                      -e DEBUG=False \
                      -e ALLOWED_HOSTS=infrabase.duckdns.org,localhost,127.0.0.1 \
                      -e DB_HOST=infrabase_db \
                      -e DB_NAME=infrabase_db \
                      -e DB_USER=infrabase_user \
                      -e DB_PASS=supersecretpassword \
                      -e FLASK_AI_URL=http://infrabase_flask_ai:5001 \
                      --network web_network \
                      $IMAGE_NAME:latest
                    
                    # Connect Django to the internal network
                    docker network connect infrabase_internal infrabase_app || true
                    
                    # Wait for MySQL to be ready before running migrations
                    echo "Waiting for MySQL to be ready..."
                    for i in $(seq 1 30); do
                        docker exec infrabase_app python -c "
                    import MySQLdb
                    try:
                        MySQLdb.connect(host='infrabase_db', user='infrabase_user', passwd='supersecretpassword', db='infrabase_db')
                        print('MySQL is ready!')
                        exit(0)
                    except Exception as e:
                        print(f'Waiting for MySQL... ({e})')
                        exit(1)
                    " 2>/dev/null && break
                        sleep 2
                    done
                    
                    # Run database migrations
                    docker exec infrabase_app python manage.py migrate --noinput
                    docker exec infrabase_app python manage.py collectstatic --noinput
                '''
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline SUCCESS: InfraBase is LIVE at infrabase.duckdns.org!'
        }
        failure {
            echo 'Pipeline FAILED: Check Jenkins logs for errors.'
        }
    }
}