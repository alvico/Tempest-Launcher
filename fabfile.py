import cuisine
from fabric.api import *
from fabric.colors import green, red, blue
import logging
from pprint import pprint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
env.user = "root"
env.password = "gogomid0"
cuisine.select_package('yum')


def setup_tempest():
    """
    change tempest fork
    checkout tempest branch
    pull code
    """
    with cd('/var/lib/tempest/'):
        run('git remote add mine git@github.com:alvico/tempest.git ')
        run('git fetch mine')
        run('git checkout albert')
        #RHEL git branch --set-upstream foo upstream/foo
        run('git branch -u mine/albert')
        run('git pull')


def pull_tempest():
    """
    TODO: Check git is on the correct tempest branch
    pull the code
    """
    with cd('/var/lib/tempest/'):
        run('git pull')


def switch_branch():
    with cd('/var/lib/tempest/'):
        run('git checkout albert')


def run_tempest():
    if cuisine.dir_exists("~/tempest/bin/"):
     run("source tempest/bin/activate")
    pull_tempest()
    tests = "test_network_basic_inter_vmconnectivity"
    try:
        with cd('/var/lib/tempest/tempest/scenario/midokura/'):
           run('nosetests -q {0} --logging-level=INFO'.format(tests))
    except ValueError:
        print "Oops!  That was a FAIL.  Try again..."

def run_all_custom():
    tests = "test_network_basic_adminstateup " \
            "test_network_basic_multisubnet " \
            "test_network_basic_metadata " \
            "test_network_basic_vmconnectivity " \
            "test_network_basic_inter_vmconnectivity "
    try:
        run("source /root/tempest/bin/activate")
        with cd('/var/lib/tempest/tempest/scenario/midokura/'):
           run('nosetests -q {0} --logging-level=INFO'.format(tests))
    except ValueError:
        print "Oops!  That was a FAIL.  Try again..."