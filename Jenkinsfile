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

        stage('Análise Estática de Código') {
            steps {
                script {
                    echo "Realizar análise estática de código aqui"
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
    }

    post {
        always {
            script {
                echo 'Finalizando'
                if (docker.image.exists(env.DOCKER_IMAGE)) {
                    docker.image(env.DOCKER_IMAGE).remove()
                } else {
                    echo "A imagem ${env.DOCKER_IMAGE} não existe."
                }
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
