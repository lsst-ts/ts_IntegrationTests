pipeline{
    agent{
        docker {
            alwaysPull true
            image 'lsstts/develop-env:develop'
            args "-u root --entrypoint=''"
        }
    }
    environment {
        user_ci = credentials('lsst-io')
        LTD_USERNAME="${user_ci_USR}"
        LTD_PASSWORD="${user_ci_PSW}"
    }
    stages{
        stage("Run the Unit Tests") {
            steps {
                 withEnv(["HOME=/home/saluser"]) {
                    sh """
                    source $HOME/.setup_dev.sh
                    pip install . 
                    pytest -ra -o junit_family=xunit2 --junitxml=tests/results/results.xml
                    echo "====== Unit testing complete ======"
                    """ 
                }
            }   
        }
        stage('Build and Upload Documentation') {
            steps {
                withEnv(["HOME=/home/saluser"]) {
                    sh """
                    source $HOME/.setup_dev.sh
                    pip install -r doc/requirements.txt
                    package-docs build
                    ltd upload --product ts-integrationtests --git-ref ${GIT_BRANCH} --dir doc/_build/html
                    """
                }
            }
        }
    }
    post{
       always {
            withEnv(["HOME=${env.WORKSPACE}"]) {
                sh 'chown -R 1003:1003 ${HOME}/'
            }
       }
       cleanup {
            deleteDir()
        }
    }
}
