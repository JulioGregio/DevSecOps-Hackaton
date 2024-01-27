pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "devsecopshackaton_flask-app:latest"
    }

    stages {
        stage('Clonar Repositório') {
            steps {
                // Utilizando branch e URL separados para maior clareza
                git branch: 'main', url: 'https://github.com/JulioGregio/DevSecOps-Hackaton.git'
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
                    echo "fazer"
                }
            }
        }

        stage('Análise de Vulnerabilidades') {
            steps {
                script {
                    sh "trivy image ${env.DOCKER_IMAGE}"
                }
            }
        }
    }

    post {
        always {
            script {
                echo 'In progress'
                docker.image(env.DOCKER_IMAGE).remove()
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
