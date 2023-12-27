pipeline {
    agent any

    stages {
        stage('Build and Test') {
            steps {
                script {
                    // Commandes pour construire et tester votre application
                    sh 'echo "Building and Testing Application..."'
                }
            }
        }
        stage('Docker Build and Push') {
            steps {
                script {
                    // Construire et pousser l'image Docker pour cast-service
                    sh 'docker build -t patrick35/cast-service:20231226 ./cast-service'
                    sh 'docker push patrick35/cast-service:20231226'

                    // Construire et pousser l'image Docker pour movie-service
                    sh 'docker build -t patrick35/movie-service:20231226 ./movie-service'
                    sh 'docker push patrick35/movie-service:20231226'
                }
            }
        }

        stage('Deploy to Kubernetes with Helm') {
    steps {
        script {
            sh 'helm upgrade --install jenkins-devops-exams-release ./Chart-dev -f ./values-dev.yaml'
        }
    }
}

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Déployer dans l'environnement Kubernetes 
                    sh 'kubectl apply -f ./kubernetes/dev'
                    sh 'kubectl apply -f ./kubernetes/prod'      
                    sh 'kubectl apply -f ./kubernetes/staging' 
                    sh 'kubectl apply -f ./kubernetes/qa'    
                }

            }
        }
    }
}
