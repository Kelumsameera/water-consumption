pipeline {
  agent any

  environment {
    DOCKER = "C:\\Program Files\\Docker\\docker\\docker.exe"
    IMAGE_NAME = "fy600-python-api"
    CONTAINER_NAME = "fy600-api"
    PORT = "3000"
  }

  stages {

    stage('Build Docker Image') {
      steps {
        bat '''
        call "%DOCKER%" build -t %IMAGE_NAME%:latest .
        '''
      }
    }

    stage('Deploy Container') {
      steps {
        bat '''
        call "%DOCKER%" stop %CONTAINER_NAME% || exit 0
        call "%DOCKER%" rm %CONTAINER_NAME% || exit 0
        call "%DOCKER%" run -d ^
          --restart always ^
          -p %PORT%:%PORT% ^
          --name %CONTAINER_NAME% ^
          %IMAGE_NAME%:latest
        '''
      }
    }
  }
}
