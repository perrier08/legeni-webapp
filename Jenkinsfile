// TP 3.6 : pipeline multibranch -> seule la branche main publie une image
pipeline {
    agent any

    parameters {
        string(name: 'DOCKERHUB_ID', defaultValue: 'perrier08', description: 'Votre identifiant Docker Hub')
    }

    environment {
        IMAGE          = "${params.DOCKERHUB_ID}/legeni-webapp"
        // Nom de branche utilisable dans un nom de conteneur / de réseau Docker
        SAFE_BRANCH    = "${env.BRANCH_NAME.replaceAll('[^a-zA-Z0-9]', '-')}"
        // main -> 1.0.<n> ; autre branche -> <branche>-<n>
        VERSION        = "${env.BRANCH_NAME == 'main' ? '1.0.' + env.BUILD_NUMBER : env.BRANCH_NAME.replaceAll('[^a-zA-Z0-9.-]', '-') + '-' + env.BUILD_NUMBER}"
        // Noms uniques par branche : deux branches peuvent avoir le même numéro de build en même temps
        TEST_CONTAINER = "webapp-ci-${SAFE_BRANCH}-${env.BUILD_NUMBER}"
        CI_NETWORK     = "ci-net-${SAFE_BRANCH}-${env.BUILD_NUMBER}"
    }

    options {
        timestamps()
        timeout(time: 20, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Tests unitaires') {
            steps {
                sh 'docker build --target test -t legeni-webapp:test .'
            }
        }

        stage('Build image') {
            steps {
                sh 'docker build --build-arg APP_VERSION=$VERSION -t $IMAGE:$VERSION .'
            }
        }

        stage("Test d'acceptance") {
            steps {
                sh '''
                    docker network create $CI_NETWORK
                    docker run -d --name $TEST_CONTAINER --network $CI_NETWORK $IMAGE:$VERSION
                    docker run --rm --network $CI_NETWORK curlimages/curl:8.11.1 \
                        -sf --retry 10 --retry-connrefused --retry-delay 1 http://$TEST_CONTAINER:5000/health
                    docker run --rm --network $CI_NETWORK curlimages/curl:8.11.1 \
                        -sf http://$TEST_CONTAINER:5000/ | grep -q "Version $VERSION"
                '''
            }
        }

        stage('Push Docker Hub') {
            when { branch 'main' }
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub',
                                                  usernameVariable: 'DH_USER',
                                                  passwordVariable: 'DH_TOKEN')]) {
                    retry(3) {
                        sh '''
                            echo "$DH_TOKEN" | docker login -u "$DH_USER" --password-stdin
                            docker push $IMAGE:$VERSION
                            docker tag $IMAGE:$VERSION $IMAGE:latest
                            docker push $IMAGE:latest
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            sh 'docker rm -f $TEST_CONTAINER || true; docker network rm $CI_NETWORK || true'
        }
        success {
            echo "Image ${IMAGE}:${VERSION} construite et validée (branche ${env.BRANCH_NAME})"
        }
        failure {
            echo "Échec du pipeline : consultez la console de l'étape en rouge"
        }
    }
}
