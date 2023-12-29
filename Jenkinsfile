pipeline {
    environment { 
        DOCKER_ID = "patrick35"
        DOCKER_IMAGE_CAST = "castserviceapi"
        DOCKER_IMAGE_MOVIE = "movieserviceapi"
        KUBECONFIG = credentials("config")
    }
    agent any 

    stages {
        stage('Build and Test cast-service') { 
            steps {
                script {
                    dir('cast-service') {
                        sh 'docker build -t $DOCKER_ID/$DOCKER_IMAGE_CAST:v.${BUILD_ID}.0 .'
                        sh 'docker run -d -p 8000:8000 --name cast-service-test $DOCKER_ID/$DOCKER_IMAGE_CAST:v.${BUILD_ID}.0'
                        sh 'sleep 10'
                        sh 'curl localhost:8000/api/v1/casts'
                        sh 'docker rm -f cast-service-test'
                    }
                }
            }
        }

        stage('Build and Test movie-service') { 
            steps {
                script {
                    dir('movie-service') {
                        sh 'docker build -t $DOCKER_ID/$DOCKER_IMAGE_MOVIE:v.${BUILD_ID}.0 .'
                        sh 'docker run -d -p 8000:8000 --name movie-service-test $DOCKER_ID/$DOCKER_IMAGE_MOVIE:v.${BUILD_ID}.0'
                        sh 'sleep 10'
                        sh 'curl localhost:8000/api/v1/movies'
                        sh 'docker rm -f movie-service-test'
                    }
                }
            }
        }

        stage('Docker Push cast-service') { 
            environment {
                DOCKER_PASS = credentials("DOCKER_HUB_PASS")
            }
            steps {
                script {
                    sh 'docker login -u $DOCKER_ID -p $DOCKER_PASS'
                    sh 'docker push $DOCKER_ID/$DOCKER_IMAGE_CAST:v.${BUILD_ID}.0'
                }
            }
        }

        stage('Docker Push movie-service') { 
            environment {
                DOCKER_PASS = credentials("DOCKER_HUB_PASS")
            }
            steps {
                script {
                    sh 'docker login -u $DOCKER_ID -p $DOCKER_PASS'
                    sh 'docker push $DOCKER_ID/$DOCKER_IMAGE_MOVIE:v.${BUILD_ID}.0'
                }
            }
        }

        stage('Deployment in dev') {
            steps {
                script {
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    echo $KUBECONFIG > .kube/config
                    cp cast-service/values.yaml cast-values.yml
                    cp movie-service/values.yaml movie-values.yml
                    sed -i "s+tag.*+tag: v.${BUILD_ID}.0+g" cast-values.yml
                    sed -i "s+tag.*+tag: v.${BUILD_ID}.0+g" movie-values.yml
                    helm upgrade --install cast-service cast-service --values=cast-values.yml --namespace dev
                    helm upgrade --install movie-service movie-service --values=movie-values.yml --namespace dev
                    '''
                }
            }
        }

        stage('Deployment in staging') {
            steps {
                script {
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    echo $KUBECONFIG > .kube/config
                    cp cast-service/values.yaml cast-values.yml
                    cp movie-service/values.yaml movie-values.yml
                    sed -i "s+tag.*+tag: v.${BUILD_ID}.0+g" cast-values.yml
                    sed -i "s+tag.*+tag: v.${BUILD_ID}.0+g" movie-values.yml
                    helm upgrade --install cast-service cast-service --values=cast-values.yml --namespace staging
                    helm upgrade --install movie-service movie-service --values=movie-values.yml --namespace staging
                    '''
                }
            }
        }

        stage('Deployment in prod') {
            steps {
                script {
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    echo $KUBECONFIG > .kube/config
                    cp cast-service/values.yaml cast-values.yml
                    cp movie-service/values.yaml movie-values.yml
                    sed -i "s+tag.*+tag: v.${BUILD_ID}.0+g" cast-values.yml
                    sed -i "s+tag.*+tag: v.${BUILD_ID}.0+g" movie-values.yml
                    helm upgrade --install cast-service cast-service --values=cast-values.yml --namespace prod
                    helm upgrade --install movie-service movie-service --values=movie-values.yml --namespace prod
                    '''
                }
            }
        }
    }
}
