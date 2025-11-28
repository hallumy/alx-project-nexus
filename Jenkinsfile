pipeline {
    agent any

    environment {
        HEROKU_APP_NAME = "ecommerce-app-d702fa150d9f"
        HEROKU_API_KEY = credentials('HEROKU_API')
        DJANGO_SECRET_KEY = credentials('DJANGO_SECRET_KEY')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/hallumy/alx-project-nexus.git',
                        credentialsId: 'github-pat'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t django-app .
                '''
            }
        }

        stage('Run Tests in Docker') {
            steps {
                sh '''
                docker run --rm \
                  -e DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY \
                  -e DATABASE_URL=sqlite:///test.db \
                  django-app sh -c "python manage.py test"
                '''
            }

        }
    stage('Deploy to Heroku') {
        steps {
            withCredentials([string(credentialsId: 'HEROKU_API', variable: 'HEROKU_API_KEY')]) {
                sh '''
                    echo "Logging into Heroku Container Registry..."
                    echo $HEROKU_API_KEY | docker login --username=_ --password-stdin registry.heroku.com

                    echo "Tagging Docker image..."
                    docker tag django-app registry.heroku.com/$HEROKU_APP_NAME/web

                    echo "Pushing Docker image..."
                    docker push registry.heroku.com/$HEROKU_APP_NAME/web

                    echo "Releasing on Heroku..."
                    heroku container:release web --app $HEROKU_APP_NAME
                '''
            }
        }
    }



        stage('Migrate & Collectstatic') {
            steps {
                sh '''
                heroku run python manage.py migrate --app $HEROKU_APP_NAME || true
                heroku run python manage.py collectstatic --noinput --app $HEROKU_APP_NAME || true
                '''
            }
        }
    }

    post {
        success { echo 'Pipeline succeeded!' }
        failure { echo 'Pipeline failed!' }
    }
}
