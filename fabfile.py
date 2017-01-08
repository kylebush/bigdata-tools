import logging

from fabric.api import task

import helper
from aws import aws
from software import cassandra, java, kafka, redis, riak, zookeeper
from vagrant import vagrant

aws
vagrant

__author__ = "Kyle Bush"
__copyright__ = "Copyright 2016"
__license__ = "Apache 2.0"
__version__ = "1.0.0"
__maintainer__ = "Kyle Bush"
__status__ = "Development"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@task
def deploy(config_file):
    """Deploys software per config file | config_file: location of the deploy config file"""

    cfg = helper.get_config(config_file)

    for host_config in cfg['hosts']:
        if 'aws-ebs' in host_config:
            aws.mount_ebs_volumes(host_config)

        for software in host_config['software']:
            install(software['name'], host_config)


def install(_software, _config):
    if _software == 'cassandra':
        java.v8_install(_config)
        cassandra.install(_config)

    elif _software == 'cassandra-lucene-index':
        cassandra.lucene_index_install(_config)

    elif _software == 'java-8':
        java.v8_install(_config)

    elif _software == 'kafka-broker':
        java.v8_install(_config)
        kafka.broker_install(_config)

    elif _software == 'kafka-manager':
        kafka.manager_install(_config)

    elif _software == 'redis':
        redis.install(_config)

    elif _software == 'riak-kv':
        riak.install_kv(_config)

    elif _software == 'zookeeper':
        zookeeper.install(_config)

    else:
        logger.error("Error: {} is not defined as software".format(_software))
