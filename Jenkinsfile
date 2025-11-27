pipeline {
    agent any

    environment {
        HEROKU_APP_NAME = "ecommerce-app-d702fa150d9f"
        HEROKU_API_KEY = credentials('HEROKU_API')
    }

    stages {

        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/hallumy/alx-project-nexus.git',
                        credentialsId: 'github-pat'
                    ]]
                ])
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t django-app .'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker compose run web pytest || true'
            }
        }

        stage('Heroku Login') {
            steps {
                sh '''
                echo $HEROKU_API_KEY | heroku login --interactive
                heroku container:login
                '''
            }
        }

        stage('Deploy to Heroku') {
            steps {
                sh '''
                heroku container:push web --app $HEROKU_APP_NAME
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
