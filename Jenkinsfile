pipeline {
    environment {
        DOCKER_ID = "patrick35"
        DOCKER_IMAGE = "datascientestapi"
        DOCKER_TAG = "v.${BUILD_ID}.0"
    }
    agent any

    stages {
        stage('Docker Build and Test') {
            steps {
                script {
                    sh 'docker rm -f jenkins || true'
                    sh "docker build -t $DOCKER_ID/$DOCKER_IMAGE:$DOCKER_TAG ."
                }
            }
        }

        stage('Docker Run') {
            steps {
                script {
                    sh "docker run -d -p 8000:8000 --name jenkins $DOCKER_ID/$DOCKER_IMAGE:$DOCKER_TAG"
                    sleep 10
                }
            }
        }

        stage('Test Acceptance') {
            steps {
                script {
                    sh 'curl localhost:8080/api/v1/casts'
                    sh 'curl localhost:8080/api/v1/movies'
                }
            }
        }

        stage('Docker Push') {
            environment {
                DOCKER_PASS = credentials("DOCKER_HUB_PASS")
            }
            steps {
                script {
                    sh "docker login -u $DOCKER_ID -p $DOCKER_PASS"
                    sh "docker push $DOCKER_ID/$DOCKER_IMAGE:$DOCKER_TAG"
                }
            }
        }

        stage('Deploiement en dev/staging/prod') {
            environment {
                KUBECONFIG = credentials("config")
            }
            steps {
                script {
                    sh 'rm -Rf .kube || true'
                    sh 'mkdir .kube'
                    sh 'cat $KUBECONFIG > .kube/config'
                    sh 'cp fastapi/values.yaml values.yml'
                    sh "sed -i 's+tag.*+tag: ${DOCKER_TAG}+g' values.yml"
                    sh 'helm upgrade --install app fastapi --values=values.yml --namespace dev'
                    sh 'helm upgrade --install app fastapi --values=values.yml --namespace staging'
                    sh 'helm upgrade --install app fastapi --values=values.yml --namespace prod'
                }
            }
        }
    }
}
