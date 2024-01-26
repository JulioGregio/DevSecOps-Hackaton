pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "DevSecTest/DevSecTest:latest"
    }

    stages {
        stage('Clonar Repositório') {
            steps {
                script {
                    git 'https://github.com/JulioGregio/DevSecOps-Hackaton.git'
                }
            }
        }

        stage('Construir e Testar') {
            steps {
                script {
                    sh "docker build -t $DOCKER_IMAGE ."
                }
            }
        }

        stage('Análise Estática de Código') {
            steps {
                script {
                    sh "bandit -r ."
                }
            }
        }

        stage('Análise de Vulnerabilidades') {
            steps {
                script {
                    sh "trivy $DOCKER_IMAGE"
                }
            }
        }
    }

    post {
        always {
            script {
                echo 'In progess'
            }
        }
        success {
            script {
               echo 'Sucess'
            }
        }
        failure {
            script {
                echo 'Fail'
            }
        }
    }
}
