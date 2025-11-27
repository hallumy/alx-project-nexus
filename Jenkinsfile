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
                  -w /app \
                  django-app sh -c "python manage.py test"
                '''
            }

        }

        stage('Heroku Login') {
            steps {
                sh '''
                echo $HEROKU_API_KEY | heroku container:login
                '''
            }
        }

        stage('Deploy to Heroku') {
            steps {
                sh '''
                docker tag django-app registry.heroku.com/$HEROKU_APP_NAME/web
                docker push registry.heroku.com/$HEROKU_APP_NAME/web
                heroku container:release web --app $HEROKU_APP_NAME
                '''
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
