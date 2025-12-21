pipeline {
    agent any

    tools {
        allure 'allure'
    }

    environment {
        TELEGRAM_BOT_TOKEN = credentials('telegram-bot-token')
        TELEGRAM_CHAT_ID = '584328610'
    }

    stages {
        stage('Run Tests in Docker') {
            steps {
                script {
                    // docker.image('python:3.13.9-slim').inside("--network jenkins-network") {
                        stage('Install Dependencies') {
                            sh '''
                                docker exec python-runner bash -c "
                                    pip install -r /var/jenkins_home/workspace/autotest_py/requirements.txt
                                "
                            '''
                        }
                        
                        stage('Run Tests') {
                            sh '''
                                docker exec python-runner bash -c "pytest /var/jenkins_home/workspace/autotest_py/tc_products.py \
                                -v --alluredir=/var/jenkins_home/workspace/autotest_py/allure-results"
                            '''
                        }
                    // }
                }
            }
        }
    }
    
    post {
        always {

            // 1️⃣ Publish Allure (cukup SATU KALI, di post)
            allure includeProperties: false,
                   jdk: '',
                   results: [[path: 'allure-results']]

            // 2️⃣ Kirim notifikasi Telegram (AMAN)
            withCredentials([
                string(credentialsId: 'telegram-bot-token', variable: 'TELEGRAM_BOT_TOKEN')
            ]) {

                script {
                    def status   = currentBuild.currentResult
                    def jobName  = env.JOB_NAME
                    def buildNum = env.BUILD_NUMBER
                    def buildUrl = env.BUILD_URL

                    def message = """
Test Automation Result

Job: ${jobName}
Build: #${buildNum}
Status: ${status}
Time: ${new Date().format('dd-MM-yyyy HH:mm')}

Allure Report:
${buildUrl}allure/

Jenkins Console:
${buildUrl}
"""
                .trim()

                    withEnv(["MESSAGE=${message}"]) {
                        sh '''
                            curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
                              -d chat_id=$TELEGRAM_CHAT_ID \
                              -d disable_web_page_preview=false \
                              -d text="$MESSAGE"
                        '''
                    }
                }
            }
        }
    }
}