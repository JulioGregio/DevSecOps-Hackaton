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
        
stage('Análise de Código Estático com Bandit') {
    steps {
        script {
            try {
                def banditOutput = sh(script: "bandit -r -f json -o bandit_results.json .", returnStdout: true).trim()

                def vulnerabilities = readJSON text: banditOutput

                vulnerabilities.results.each { result ->
                    echo "Vulnerabilidade: ${result.issue_text}" // Corrigir para o campo correto, se necessário
                }
            } catch (Exception e) {
                echo "Erro ao executar o Bandit: ${e.message}"
                
                // Adicionar a seguinte linha para imprimir a saída padrão de erro do Bandit
                def banditErrorOutput = sh(script: "bandit -r -f json -o bandit_results.json .", returnStatus: true, returnStdout: true).err
                echo "Saída de erro do Bandit: ${banditErrorOutput}"
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
