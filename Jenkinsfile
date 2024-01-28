pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "devsecopshackaton_flask-app:latest"
    }

    stages {
        stage('Clonar Repositório') {
            steps {
                git branch: 'main', url: 'https://github.com/JulioGregio/DevSecOps-Hackaton.git'
            }
        }

        stage('Construir e Testar') {
            steps {
                script {
                    sh "docker build -t $DOCKER_IMAGE ."
                    sh "docker image inspect $DOCKER_IMAGE"
                }
            }
        }

        stage('Análise de Vulnerabilidades') {
            steps {
                script {
                    sh "docker image inspect $DOCKER_IMAGE"
                    sh "trivy image $DOCKER_IMAGE"
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withMaven(
                    maven: 'Default Maven', 
                    mavenSettingsConfig: 'your-maven-settings-id'
                ) {
                    sh "mvn clean verify sonar:sonar -Dsonar.projectKey=teste -Dsonar.projectName='teste'"
                }
            }
        }
    }

    post {
        always {
            script {
                echo 'Finalizando'
            }
        }
        success {
            script {
                echo 'Sucesso'
            }
        }
        failure {
            script {
                echo 'Falha'
            }
        }
    }
}
