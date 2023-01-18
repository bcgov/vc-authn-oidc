#!groovy

// --------------------
// Declarative Pipeline
// --------------------
pipeline {
  agent any

  environment {
    // Enable pipeline verbose debug output if greater than 0
    DEBUG_OUTPUT = 'false'

    // Get projects/namespaces from config maps
    DEV_PROJECT = new File('/var/run/configs/ns/project.dev').getText('UTF-8').trim()
    TEST_PROJECT = new File('/var/run/configs/ns/project.test').getText('UTF-8').trim()
    PROD_PROJECT = new File('/var/run/configs/ns/project.prod').getText('UTF-8').trim()
    TOOLS_PROJECT = new File('/var/run/configs/ns/project.tools').getText('UTF-8').trim()

    // Get application config from config maps
    REPO_OWNER = new File('/var/run/configs/jobs/repo.owner').getText('UTF-8').trim()
    REPO_NAME = new File('/var/run/configs/jobs/repo.name').getText('UTF-8').trim()
    APP_NAME = new File('/var/run/configs/jobs/app.name').getText('UTF-8').trim()
    APP_DOMAIN = new File('/var/run/configs/jobs/app.domain').getText('UTF-8').trim()

    // JOB_NAME should be the pull request/branch identifier (i.e. 'pr-5')
    JOB_NAME = JOB_BASE_NAME.toLowerCase()

    // SOURCE_REPO_* references git repository resources
    SOURCE_REPO_RAW = "https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/${JOB_NAME}"
    SOURCE_REPO_REF = "${JOB_NAME}"
    SOURCE_REPO_URL = "https://github.com/${REPO_OWNER}/${REPO_NAME}.git"

    // ENV_HOST is the full domain without the path (ie. 'appname-dev.pathfinder.gov.bc.ca')
    DEV_HOST = "${REPO_NAME}-dev.${APP_DOMAIN}"
    TEST_HOST = "${REPO_NAME}-test.${APP_DOMAIN}"
    PROD_HOST = "${REPO_NAME}.${APP_DOMAIN}"
    // PATH_ROOT will be appended to ENV_HOST
    PATH_ROOT = "/${JOB_NAME.equalsIgnoreCase('master') ? 'app' : JOB_NAME}"
  }

  options {
    parallelsAlwaysFailFast()
  }

  stages {
    stage('Initialize') {
      agent any
      steps {
        // Cancel any running builds in progress
        timeout(time: 10, unit: 'MINUTES') {
          echo "Cancelling previous ${APP_NAME}-${JOB_NAME} builds in progress..."
          abortAllPreviousBuildInProgress(currentBuild)
        }

        script {
          if(DEBUG_OUTPUT.equalsIgnoreCase('true')) {
            // Force OpenShift Plugin directives to be verbose
            openshift.logLevel(1)

            // Print all environment variables
            echo 'DEBUG - All pipeline environment variables:'
            echo sh(returnStdout: true, script: 'env')
          }

          loadCommonPipeline()
        }
      }
    }

    stage('Build') {
      agent any
      steps {
        script {
          loadCommonPipeline()
          commonPipeline.runStageBuild()
        }
      }
      post {
        success {
          echo 'Cleanup App BuildConfigs...'
          script {
            openshift.withCluster() {
              openshift.withProject(TOOLS_PROJECT) {
                if(DEBUG_OUTPUT.equalsIgnoreCase('true')) {
                  echo "DEBUG - Using project: ${openshift.project()}"
                } else {
                  def bcApp = openshift.selector('bc', "${REPO_NAME}-app-${JOB_NAME}")

                  if(bcApp.exists()) {
                    echo "Removing BuildConfig ${REPO_NAME}-app-${JOB_NAME}..."
                    bcApp.delete()
                  }
                }
              }
            }
          }
        }
      }
    }

    stage('Deploy - Dev') {
      agent any
      steps {
        script {
          loadCommonPipeline()
          commonPipeline.runStageDeploy('Dev', DEV_PROJECT, DEV_HOST, PATH_ROOT)
        }
      }
      post {
        success {
          script {
            commonPipeline.createDeploymentStatus(DEV_PROJECT, 'SUCCESS', JOB_NAME, DEV_HOST, PATH_ROOT)
            commonPipeline.notifyStageStatus('Deploy - Dev', 'SUCCESS')
          }
        }
        unsuccessful {
          script {
            commonPipeline.createDeploymentStatus(DEV_PROJECT, 'FAILURE', JOB_NAME, DEV_HOST, PATH_ROOT)
            commonPipeline.notifyStageStatus('Deploy - Dev', 'FAILURE')
          }
        }
      }
    }

    stage('Deploy - Test') {
      agent any
      steps {
        script {
          loadCommonPipeline()
          commonPipeline.runStageDeploy('Test', TEST_PROJECT, TEST_HOST, PATH_ROOT)
        }
      }
      post {
        success {
          script {
            commonPipeline.createDeploymentStatus(TEST_PROJECT, 'SUCCESS', JOB_NAME, TEST_HOST, PATH_ROOT)
            commonPipeline.notifyStageStatus('Deploy - Test', 'SUCCESS')
          }
        }
        unsuccessful {
          script {
            commonPipeline.createDeploymentStatus(TEST_PROJECT, 'FAILURE', JOB_NAME, TEST_HOST, PATH_ROOT)
            commonPipeline.notifyStageStatus('Deploy - Test', 'FAILURE')
          }
        }
      }
    }

    stage('Deploy - Prod') {
      agent any
      steps {
        script {
          loadCommonPipeline()
          commonPipeline.runStageDeploy('Prod', PROD_PROJECT, PROD_HOST, PATH_ROOT)
        }
      }
      post {
        success {
          script {
            commonPipeline.createDeploymentStatus(PROD_PROJECT, 'SUCCESS', JOB_NAME, PROD_HOST, PATH_ROOT)
            commonPipeline.notifyStageStatus('Deploy - Prod', 'SUCCESS')
          }
        }
        unsuccessful {
          script {
            commonPipeline.createDeploymentStatus(PROD_PROJECT, 'FAILURE', JOB_NAME, PROD_HOST, PATH_ROOT)
            commonPipeline.notifyStageStatus('Deploy - Prod', 'FAILURE')
          }
        }
      }
    }
  }
}

// --------------------
// Supporting Functions
// --------------------

// Load Common Code as Global Variable
def loadCommonPipeline() {
  if (!binding.hasVariable('commonPipeline')) {
    commonPipeline = load "${WORKSPACE}/openshift/commonPipeline.groovy"
  }
}
