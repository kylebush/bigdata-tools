import os

from fabric.api import env, put, sudo, run

__author__ = "Kyle Bush"
__copyright__ = "Copyright 2016"
__license__ = "Apache 2.0"
__version__ = "1.0.0"
__maintainer__ = "Kyle Bush"
__status__ = "Development"


def disable_transparent_huge_pages(_host):
    env.host_string = _host

    run('echo "never" | sudo tee /sys/kernel/mm/transparent_hugepage/enabled')
    put('{}/bootstrap/scripts/disable-thp.sh'.format(os.getcwd()), '~/', use_sudo=True)
    sudo("chmod +x disable-thp.sh")
    sudo(". ~/disable-thp.sh")


def set_swapiness(_host, _swap_percent):
    env.host_string = _host
    sudo('sudo sysctl vm.swappiness={}'.format(_swap_percent))
    run('echo "vm.swappiness = {}" | sudo tee -a /etc/sysctl.conf'.format(_swap_percent))


def set_overcommit_memory(_host, _value):
    env.host_string = _host
    sudo('sysctl vm.overcommit_memory={}'.format(_value))
    run('echo "vm.overcommit_memory = {}" | sudo tee -a /etc/sysctl.conf'.format(_value))

