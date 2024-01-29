pipeline {
    agent any

    tools {
        maven 'Maven3'
    }

    environment {
        DOCKER_IMAGE = "devsecopshackaton_flask-app:latest"
        SONARQUBE_URL = "http://your-sonarqube-server:9000"
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
                script {
                    withMaven(
                        maven: 'Maven3', 
                        mavenSettingsConfig: 'your-maven-settings-id'
                    ) {
                        sh "mvn clean verify sonar:sonar -Dsonar.projectKey=teste -Dsonar.projectName='teste' -Dsonar.host.url=$SONARQUBE_URL"
                    }
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
