pipeline {
    agent any

    environment {
        FLASK_ENV = 'development' // or 'production'
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/ckongala/test-flask-app.git', branch: 'main'
            }
        }

        stage('Build') {
            steps {
                script {
                    // Create a virtual environment
                    sh 'python3 -m venv venv'
                    // Activate the virtual environment and install dependencies using bash
                    sh '''
                        bash -c "source venv/bin/activate && pip install -r requirements.txt"
                    '''
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Activate the virtual environment and run tests using bash
                    sh '''
                        bash -c "source venv/bin/activate && pytest test_app.py"
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Deployment logic here
                    echo 'Deploying the application...'
                    // Example: Starting the application with Gunicorn
                    sh '''
                        bash -c "source venv/bin/activate && gunicorn -w 4 -b 0.0.0.0:5000 app:app &"
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }

        success {
            echo 'The build was successful!'
        }

        failure {
            echo 'The build failed.'
        }
    }
}
