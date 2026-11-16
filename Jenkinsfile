pipeline {
    agent any

    environment {
        APP_NAME = "lab5-jenkins-app"
        STAGING_PORT = "8085"
        PROD_PORT = "8086"
    }

    stages {
        stage('1. Checkout SCM') {
            steps {
                echo "Pobieranie kodu z repozytorium (gałąź: ${env.BRANCH_NAME ?: 'main'})..."
                checkout scm
            }
        }

        stage('2. Static Code Analysis (Linting)') {
            steps {
                echo "Uruchamianie analizy statycznej kodu (flake8)..."
                sh 'flake8 app/ --max-line-length=100'
            }
        }

        stage('3. Build Docker Image') {
            steps {
                echo "Budowanie obrazu Docker dla wersji ${env.BUILD_NUMBER}..."
                sh "docker build -t ${APP_NAME}:${env.BUILD_NUMBER} -t ${APP_NAME}:latest ."
            }
        }

        stage('4. Unit & Integration Tests') {
            steps {
                echo "Uruchamianie testów jednostkowych (pytest)..."
                sh 'pytest -v'
            }
        }

        stage('5. Deploy to Staging') {
            steps {
                echo "Wdrażanie aplikacji na środowisko testowe (port ${STAGING_PORT})..."
                sh """
                    docker rm -f ${APP_NAME}-staging || true
                    docker run -d --name ${APP_NAME}-staging -p ${STAGING_PORT}:8000 -e DEPLOY_ENV=staging -e APP_VERSION=1.0.${BUILD_NUMBER} ${APP_NAME}:${BUILD_NUMBER}
                    sleep 3
                    curl -f http://localhost:${STAGING_PORT}/health
                """
            }
        }

        stage('6. Manual Approval for Production') {
            when {
                branch 'main'
            }
            steps {
                input message: 'Czy zatwierdzić wdrożenie tej wersji na środowisko PRODUKCYJNE?', ok: 'Zatwierdź i wdróż na PROD'
            }
        }

        stage('7. Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                echo "Wdrażanie aplikacji na środowisko PRODUKCYJNE (port ${PROD_PORT})..."
                sh """
                    docker rm -f ${APP_NAME}-prod || true
                    docker run -d --name ${APP_NAME}-prod -p ${PROD_PORT}:8000 -e DEPLOY_ENV=production -e APP_VERSION=1.0.${BUILD_NUMBER} ${APP_NAME}:${BUILD_NUMBER}
                    sleep 3
                    curl -f http://localhost:${PROD_PORT}/health
                """
            }
        }
    }

    post {
        success {
            echo "[POWIADOMIENIE CI/CD] SUCCEEDED: Pipeline #${env.BUILD_NUMBER} zakonczony powodzeniem! Wersja 1.0.${env.BUILD_NUMBER} zostala wdrożona."
        }
        failure {
            echo "[POWIADOMIENIE CI/CD] FAILED: Pipeline #${env.BUILD_NUMBER} zakonczony bledem! Sprawdz logi kompilacji."
        }
        always {
            echo "[POWIADOMIENIE CI/CD] Raport statusu wyslany do zespolu DevOps."
        }
    }
}
