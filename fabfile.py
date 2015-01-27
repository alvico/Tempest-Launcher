import cuisine
from fabric.api import *
from fabric.colors import green, red, blue
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
env.user = "centos"
env.password = "gogomid0"
cuisine.select_package('apt')

def pre_req():
    cuisine.package_update_apt()
    sudo('apt-get -y upgrade')
    cuisine.package_ensure('wget')
    cuisine.package_ensure('gcc')
    cuisine.package_ensure('python-dev')
    cuisine.package_ensure('python-pip')
    cuisine.package_ensure('wget')
    cuisine.package_ensure('gcc')
    cuisine.package_ensure('libffi-dev')
    cuisine.package_ensure('libssl-dev')
    cuisine.package_ensure('libxml2-dev')
    cuisine.package_ensure('libxslt-dev')
    cuisine.package_ensure('git')

def set_up_key():
    run('ssh-keygen -t dsa -N "" -C "your_email@example.com" -f "id_rsa"')
    run('ssh-add ~/.ssh/id_rsa')
    run('cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys')

def clone_qa():
    # Make sure we hace git access rights
    run('git clone https://github.com/midokura/qa.git')
    with cd('~/qa'):
        run('git submodule update --init')

def execute_ansible():
    with cd('~/qa/tools/ansible'):
        run("ansible-playbook -vvvv -i hosts_localhost_allinone"
            "local-allinone.yml -e deploy=ubuntu14 -e midonet_version=2015.01"
            "-e openstack_version=juno")

def tempest_preliminars():
    cuisine.python_package_ensure_pip('virtualenv')
    cuisine.python_package_ensure_pip('virtualenvwrapper')
    run('echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc')
    
def tempest_setup():
    with cd('~'):
        run('git clone https://github.com/midokura/tempest.git')
    with cd('~/tempest'):
        sudo('cp /root/tempest.conf ~/tempest/etc/')
        sudo('chmod  a+rw ~/tempest/etc/tempest.conf')
        run('git fetch --all')
        run('git checkout development')
        with prefix('workon tempest'):
            cuisine.python_package_install_pip(r='requirements.txt')
            run('python mido-setup.py')

def restart():
    sudo("service midolman restart")

def run_tempest():
    with prefix('workon tempest'):
        with cd('~/tempest'):
            run('./run_tempest.sh tempest.api.network' 
                'tempest.scenario.test_network_basic_ops' 
                'tempest.scenario.test_network_advanced_server_ops') 
