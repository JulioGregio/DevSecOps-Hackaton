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

    stage('Análise de Vulnerabilidades com Trivy') {
                steps {
                    script {
                        sh "docker image inspect $DOCKER_IMAGE"
                        sh "trivy image $DOCKER_IMAGE"
                    }
                }
            }
        
    stage('Análise de Código Estático com Horusec') {
                steps {
                    script {
                        sh "horusec start -p ."
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
