
pipeline {
    agent any
    stages {
        stage("Test") {
            steps {
                sh 'docker-compose -f docker-compose-test.yml up --build'
            }
        }
    }
}