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

        stage('Análise de Vulnerabilidades com Bandit') {
            steps {
                script {
                    def banditOutput = sh(script: "bandit -r -f json -o bandit_results.json .", returnStdout: true).trim()

                    def vulnerabilities = readJSON text: banditOutput

                    vulnerabilities.results.each { result ->
                        echo "Vulnerabilidade: ${result.issue_text}"
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
