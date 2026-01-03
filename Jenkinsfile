pipeline {
    agent any

    environment {
        DOCKER = "C:\\Program Files\\Docker\\docker\\docker.exe"
        IMAGE_NAME = "fy600-python-api"
        CONTAINER_NAME = "fy600-api"
        PORT = "3000"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'master',
                    url: 'https://github.com/Kelumsameera/water-consumption.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'call "%DOCKER%" build -t %IMAGE_NAME%:latest .'
            }
        }

        stage('Deploy Container') {
            steps {
                bat '''
                call "%DOCKER%" stop %CONTAINER_NAME% || echo Container not running
                call "%DOCKER%" rm %CONTAINER_NAME% || echo Container not found

                call "%DOCKER%" run -d ^
                  --restart always ^
                  -p %PORT%:%PORT% ^
                  --name %CONTAINER_NAME% ^
                  %IMAGE_NAME%:latest
                '''
            }
        }

        stage('Wait for API') {
            steps {
                bat '''
                echo Waiting for API to start...

                for /L %%i in (1,1,10) do (
                    curl -f http://localhost:%PORT%/fy600 && exit /b 0
                    echo API not ready yet... retry %%i
                    ping 127.0.0.1 -n 6 > nul
                )

                echo API failed to start
                exit /b 1
                '''
            }
        }
    }

    post {
        always {
            bat 'call "%DOCKER%" image prune -f'
        }
    }
}
