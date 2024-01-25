pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "DevSecTest/DevSecTest:latest"
    }

    stages {
        stage('Clonar Repositório') {
            steps {
                script {
                    // Clonar do branch principal (mude para 'main' se estiver usando 'main' como branch principal)
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
                // Lógica que será executada independentemente do resultado
                // Exemplo: Remover recursos temporários, gerar relatórios, etc.
            }
        }
        success {
            script {
                // Lógica executada apenas se a pipeline for bem-sucedida
                // Exemplo: Notificar equipes, gerar relatórios de sucesso, etc.
            }
        }
        failure {
            script {
                // Lógica executada apenas se a pipeline falhar
                // Exemplo: Notificar equipes, executar ações corretivas, etc.
            }
        }
    }
}
