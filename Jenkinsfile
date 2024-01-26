pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "DevSecTest/DevSecTest:latest"
        MAVEN_HOME = tool 'Maven' // Defina a instalação do Maven configurada no Jenkins
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
                    // Construir o projeto com Maven
                    sh "${MAVEN_HOME}/bin/mvn clean install"
                }
            }
        }

        stage('Construir Imagem Docker') {
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
                echo 'In progress'
            }
        }
        success {
            script {
                echo 'Success'
            }
        }
        failure {
            script {
                echo 'Fail'
            }
        }
    }
}
