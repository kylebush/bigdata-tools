import os

from fabric.api import env, sudo, put
from fabric.decorators import task

import helper
from software import java


def broker_install(host_config):
    env.host_string = helper.get_env_host_string(host_config)
    env.user = helper.get_env_user(host_config)
    env.key_filename = helper.get_env_key_filename(host_config)

    java.v8_install(host_config)

    software_config = helper.get_software_config(host_config, 'kafka-broker')

    version = software_config.get('version', '0.10.0.1')

    put('{}/software/scripts/kafka-broker.sh'.format(os.getcwd()), '~/', use_sudo=True)
    sudo("chmod +x kafka-broker.sh")
    sudo(". ~/kafka-broker.sh {}".format(version))

    broker_id = software_config.get('broker-id', '0')
    zk_hosts = software_config.get('zookeeper-hosts', 'localhost:2181')
    log_directories = software_config.get('log-directories', '/var/lib/kafka-logs')

    tag = '## ---- CUSTOM CONFIGURATION ---'

    sudo('echo "{}" | sudo tee -a /srv/kafka/config/server.properties'.format(tag))
    sudo('echo "delete.topic.enable = true" | sudo tee -a /srv/kafka/config/server.properties')
    sudo('echo "broker.id={}" | sudo tee -a /srv/kafka/config/server.properties'.format(broker_id))
    sudo('echo "zookeeper.connect={}" | sudo tee -a /srv/kafka/config/server.properties'.format(zk_hosts))
    sudo('echo "log.dirs={}" | sudo tee -a /srv/kafka/config/server.properties'.format(log_directories))
    sudo('echo "listeners=PLAINTEXT://:9093" | sudo tee -a /srv/kafka/config/server.properties')
    sudo('echo "{}" | sudo tee -a /srv/kafka/config/server.properties'.format(tag))

    sudo("service kafka restart")


def manager_install(host_config):
    env.host_string = helper.get_env_host_string(host_config)
    env.user = helper.get_env_user(host_config)
    env.key_filename = helper.get_env_key_filename(host_config)

    software_config = helper.get_software_config(host_config, 'kafka-manager')
    zk_hosts = software_config.get('zookeeper-hosts', 'localhost:2181')

    put('{}/software/scripts/kafka-manager.sh'.format(os.getcwd()), '~/', use_sudo=True)
    sudo("chmod +x kafka-manager.sh")
    sudo(". ~/kafka-manager.sh {}".format(zk_hosts))


@task
def create_topic(config_file, topic, replication_factor=1, partitions=1):
    """Creates a Kafka topic | args: config_file, topic name, replication factor, partitions"""
    cfg = helper.get_config(config_file)
    host_config = get_kafka_host_cfg(cfg)

    cmd = "/srv/kafka/bin/kafka-topics.sh --create --zookeeper {} " \
          "--replication-factor {} --partitions {} --topic {}".format(get_zk_host(cfg),
                                                                      replication_factor,
                                                                      partitions,
                                                                      topic)
    env.host_string = helper.get_env_host_string(host_config)
    env.user = helper.get_env_user(host_config)
    env.key_filename = helper.get_env_key_filename(host_config)

    sudo(cmd)


@task
def delete_topic(config_file, topic):
    """Deletes a Kafka topic | args: config_file, topic name"""
    cfg = helper.get_config(config_file)
    host_config = get_kafka_host_cfg(cfg)

    cmd = "/srv/kafka/bin/kafka-topics.sh --delete --zookeeper {} --topic {}".format(get_zk_host(cfg), topic)

    env.host_string = helper.get_env_host_string(host_config)
    env.user = helper.get_env_user(host_config)
    env.key_filename = helper.get_env_key_filename(host_config)

    sudo(cmd)


def get_kafka_host_cfg(cfg):
    for host_config in cfg['hosts']:
        for software in host_config['software']:
            if software['name'] == 'kafka-broker':
                return host_config
    return None


def get_zk_host(cfg):
    for host_config in cfg['hosts']:
        for software in host_config['software']:
            if software['name'] == 'kafka-broker':
                zk_host = software.get('zookeeper-hosts')
                if zk_host:
                    return zk_host.split(",")[0]
    return None
