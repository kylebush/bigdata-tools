import os
import yaml
import logging
from fabric.api import local
from fabric.decorators import task

__author__ = "Kyle Bush"
__copyright__ = "Copyright 2016"
__license__ = "Apache 2.0"
__version__ = "1.0.0"
__maintainer__ = "Kyle Bush"
__status__ = "Development"

@task
def up(machine=""):
    """Starts and provisions the machine"""
    local('vagrant up {}'.format(os.getcwd(), machine))
    print_hosts()


@task
def provision(machine=""):
    """Provisions the machines"""
    local('vagrant provision {}'.format(os.getcwd(), machine))
    print_hosts()

@task
def destroy(machine=""):
    """Destroys the machine and deletes all associated files"""
    local('vagrant destroy {}'.format(os.getcwd(), machine))


@task
def suspend(machine=""):
    """Suspends the machine and saves the current state"""
    local('vagrant suspend {}'.format(os.getcwd(), machine))


@task
def resume(machine=""):
    """Resumes a suspended machine"""
    local('vagrant resume {}'.format(os.getcwd(), machine))

@task
def print_hosts():
    """Prints the configured hosts"""
    config_file = "{}/config/vagrant.yml".format(os.getcwd())

    with open(config_file, 'r') as yaml_file:
        cfg = yaml.load(yaml_file)

    print "-" * 50
    print " *** HOSTS ***"
    print "-" * 50
    print "hosts:"

    for host in cfg['hosts']:
        print "  - name: {0}".format(host['name'])
        print "    private-ip: {}".format(host['ip'])
        print "    public-ip: {}".format(host['ip'])

    print "-" * 50
