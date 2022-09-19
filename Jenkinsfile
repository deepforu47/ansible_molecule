properties([
    parameters([
        string(name: 'MOLECULE_SCENARIO_NAME', defaultValue: 'podman', description: 'Please Provide the molecule scenario to execute', ),
        string(name: 'VERIFIER_NAME', defaultValue: 'testinfra', description: 'Please Provide the molecule verifier you want to use', ),
    ])
])
environment{
    ANSIBLE_CONFIG = "$HOME/.ansible.cfg"
    PATH = "$PATH:/usr/local/bin"
}
pipeline {
    scm {
        git {
            remote {
                github('test-owner/test-project')
                refspec('+refs/pull/*:refs/remotes/origin/pr/*')
            }
            branch('${sha1}')
        }
    }
    triggers {
        githubPullRequest {
            admin('user_1')
            admins(['user_2', 'user_3'])
            userWhitelist('you@you.com')
            userWhitelist(['me@me.com', 'they@they.com'])
            orgWhitelist('my_github_org')
            orgWhitelist(['your_github_org', 'another_org'])
            cron('H/5 * * * *')
            triggerPhrase('OK to test')
            onlyTriggerPhrase()
            useGitHubHooks()
            permitAll()
            autoCloseFailedPullRequests()
            allowMembersOfWhitelistedOrgsAsAdmin()
            extensions {
                commitStatus {
                    context('deploy to staging site')
                    triggeredStatus('starting deployment to staging site...')
                    startedStatus('deploying to staging site...')
                    statusUrl('http://mystatussite.com/prs')
                    completedStatus('SUCCESS', 'All is well')
                    completedStatus('FAILURE', 'Something went wrong. Investigate!')
                    completedStatus('PENDING', 'still in progress...')
                    completedStatus('ERROR', 'Something went really wrong. Investigate!')
                }
            }
        }
    }
  agent {
    // Node setup : minimal centos7, plugged into Jenkins, and
    // git config --global http.sslVerify false
    // sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
    // sudo yum -y install python36u python36u-pip python36u-devel git curl gcc
    // git config --global http.sslVerify false
    // sudo curl -fsSL get.docker.com | bash
    label 'Molecule_Slave'
  }
    options {
        ansiColor('xterm')
    }
    environment{
        ANSIBLE_CONFIG = "$HOME/.ansible.cfg"
        PATH = "$PATH:/usr/local/bin"
    }
  stages {

    // stage ('Get latest code') {
    //   steps {
    //     checkout scm
    //   }
    // }

    // stage ('Setup Python virtual environment') {
    //   steps {
    //     // sh '''
    //     //   //python3 -m pip install virtualenv
    //     //   //virtualenv virtenv
    //     //   //source virtenv/bin/activate
    //     //   //python3 -m pip install --upgrade ansible molecule docker
    //     // '''
    //   }
    // }

    stage ('Display versions') {
      steps {
        sh '''   
          /usr/local/bin/podman -v
          /Users/kulsharm2/sandbox/PythonCrashCourse/bin/python -V
          /usr/local/bin/ansible  --version
          molecule --version
        '''
      }
    }
    stage ('Molecule: Clean up environment') {
      steps {
        sh '''
            cd /Users/kulsharm2/.ansible/collections/ansible_collections/confluent/platform/  && \
            molecule -c .config/molecule/config.yml cleanup -s $MOLECULE_SCENARIO_NAME ;\
            molecule -c .config/molecule/config.yml destroy -s $MOLECULE_SCENARIO_NAME
        '''
      }
    }
    stage ('Molecule: Test all the matrix') {
      steps {
        sh '''
            cd /Users/kulsharm2/ansible/molecule_demo
            just test
        '''
      }
    }

  }
  post{ 
        always{
            publishHTML([allowMissing: false, alwaysLinkToLastBuild: true, keepAll: true, reportDir: './', reportFiles: 'report.html', reportName: 'Molecule Test Report', reportTitles: 'Molecule Test Report'])       }
  }
}
