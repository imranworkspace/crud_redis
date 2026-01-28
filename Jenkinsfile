pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = "crud_redis_jen"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'master',
                credentialsId: 'fbc4daee-0fc0-4128-a7f4-ce51af0029dc', // docker username and password - imrandocker3656 and my pass
                    url: 'https://github.com/imranworkspace/crud_redis.git'
            }
        }

        stage('Build & Deploy') {
            steps {
                bat """
                docker-compose down
                docker-compose build
                docker-compose up -d
                """
            }
        }

        stage('Run Migrations') {
            steps {
                bat """
                docker-compose exec web python manage.py migrate
                """
            }
        }

        // stage('Collect Static') {
        //     steps {
        //         bat """
        //         docker-compose exec web python manage.py collectstatic --noinput
        //         """
        //     }
        // }
    }

    post {
        success {
            echo "🚀 Django deployed via Docker Compose"
        }
    }
}
