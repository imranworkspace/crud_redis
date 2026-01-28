pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = "crud_redis_jen"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/imranworkspace/crud_redis.git'
            }
        }

        stage('Build & Deploy') {
            steps {
                sh """
                docker-compose down
                docker-compose build
                docker-compose up -d
                """
            }
        }

        stage('Run Migrations') {
            steps {
                sh """
                docker-compose exec web python manage.py migrate
                """
            }
        }

        stage('Collect Static') {
            steps {
                sh """
                docker-compose exec web python manage.py collectstatic --noinput
                """
            }
        }
    }

    post {
        success {
            echo "🚀 Django deployed via Docker Compose"
        }
    }
}
