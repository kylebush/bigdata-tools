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


def install(software, config):
    if software == 'cassandra':
        cassandra.install(config)

    elif software == 'cassandra-lucene-index':
        cassandra.lucene_index_install(config)

    elif software == 'java-8':
        java.v8_install(config)

    elif software == 'kafka-broker':
        kafka.broker_install(config)

    elif software == 'kafka-manager':
        kafka.manager_install(config)

    elif software == 'redis':
        redis.install(config)

    elif software == 'riak-kv':
        riak.install_kv(config)

    elif software == 'zookeeper':
        zookeeper.install(config)

    else:
        logger.error("Error: {} is not defined as software".format(software))
