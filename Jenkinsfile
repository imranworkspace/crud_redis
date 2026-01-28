pipeline{
    agent any
    environment {
        COMPOSE_PROJECT_NAME  = 'crud_redis_jen'
    }

    stages{
        stage("checkout code"){
            steps{
                git branch: 'master',
                url: 'https://github.com/imranworkspace/crud_redis'
            }
        }
        stage("Build & Deploy"){
            steps{
                sh """
                    docker compose down
                    docker compose build 
                    docker compose up -d
                """
            }
        }
        stage("Run Migration"){
            steps{
                sh """ docker compose exec web python manage.py migrate """
            }
        }
    }
    post{
        success{
            echo "django docker deployment successfully"
        }
        error{
            echo "failed docker deployment"
        }
    }

}