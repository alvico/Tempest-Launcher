import cuisine
from fabric.api import *
from fabric.colors import green, red, blue
import logging
from pprint import pprint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
env.user = "root"
env.password = ""
cuisine.select_package('yum')


def setup_tempest():
    """
    change tempest fork
    checkout tempest branch
    pull code
    """
    with cd('/var/lib/tempest/'):
        run('git remote add midokura git@github.com:midokura/tempest.git ')
        run('git fetch midokura')
        run('git checkout albert')
        run('git branch --set-upstream albert midokura/albert')
        run('git pull')


def pull_tempest():
    """
    TODO: Check git is on the correct tempest branch
    pull the code
    """
    with cd('/var/lib/tempest/'):
        run('git pull')


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
