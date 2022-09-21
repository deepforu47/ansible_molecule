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
  agent {
    label 'Molecule_Slave'
  }
    options {
        ansiColor('xterm')
    }
    environment{
        ANSIBLE_CONFIG = "$HOME/.ansible.cfg"
        PATH = "$PATH:/usr/local/bin"
        MOLECULE_SCENARIO_NAME = "podman"
        VERIFIER_NAME = "testinfra"
        
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
            molecule -c .config/molecule/config.yml cleanup -s $MOLECULE_SCENARIO_NAME ;\
            molecule -c .config/molecule/config.yml destroy -s $MOLECULE_SCENARIO_NAME
        '''
      }
    }
    stage ('Molecule: Test all the matrix') {
      steps {
        sh '''
            molecule -c .config/molecule/config.yml test --destroy=never -s $MOLECULE_SCENARIO_NAME
        '''
      }
    }

  }
  post{ 
        always{
            publishHTML([allowMissing: false, alwaysLinkToLastBuild: true, keepAll: true, reportDir: './', reportFiles: 'report.html', reportName: 'Molecule Test Report', reportTitles: 'Molecule Test Report'])       }
  }
}
