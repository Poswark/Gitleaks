pipeline {
    agent any

    environment {
        PROJECT_DIR = 'app'                      
        REPORT_JSON = 'gitleaks-report.json'
        REPORT_HTML = 'gitleaks-report.html'
        GITLEAKS_IMAGE = 'zricethezav/gitleaks:latest'
    }

    stages {
        stage('Preparar entorno') {
            steps {
                echo "🛠️ Preparando entorno..."
                sh 'rm -f ${REPORT_JSON} ${REPORT_HTML}'
            }
        }

        stage('Escanear secretos con Gitleaks') {
            steps {
                echo "🔍 Ejecutando Gitleaks..."
                sh """
                docker run --rm \
                    -v "\$PWD":/repo \
                    \$GITLEAKS_IMAGE \
                    detect \
                    --no-git \
                    --source=/repo/\$PROJECT_DIR \
                    --report-format=json \
                    --report-path=/repo/\$REPORT_JSON \
                    --config=/repo/.gitleaks.toml \
                    --verbose || true
                """
            }
        }

        stage('Generar reporte HTML') {
            steps {
                echo "📝 Generando reporte HTML..."
                sh 'python3 generar_html_gitleaks.py'
            }
        }

        stage('Publicar HTML') {
            steps {
                echo "🌐 Publicando reporte..."
                publishHTML(target: [
                    allowMissing: false,
                    keepAll: true,
                    alwaysLinkToLastBuild: true,
                    reportDir: '.',
                    reportFiles: "${REPORT_HTML}",
                    reportName: 'Gitleaks Secret Report'
                ])
            }
        }

        stage('Evaluar resultados') {
            steps {
                script {
                    def json = readJSON file: "${REPORT_JSON}"
                    if (json && json.size() > 0) {
                        echo "⚠️ Se detectaron secretos: ${json.size()} hallazgos"
                        currentBuild.result = 'UNSTABLE'
                    } else {
                        echo "✅ No se detectaron secretos."
                    }
                }
            }
        }
    }

    post {
        failure {
            echo "🚨 El pipeline falló"
        }
        unstable {
            echo "⚠️ Se marcará el build como UNSTABLE por secretos encontrados"
        }
        success {
            echo "🎉 Pipeline finalizado exitosamente"
        }
    }
}