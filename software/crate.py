import os
from fabric.api import env, sudo, put
from fabric.decorators import task

import helper


def db_install(host_config, config):
    env.host_string = helper.get_env_host_string(host_config)
    env.user = helper.get_env_user(host_config)
    env.key_filename = helper.get_env_key_filename(host_config)

    software_config = helper.get_software_config(host_config, 'crate')

    sudo("sysctl -w vm.max_map_count=262144")

    put('{}/software/scripts/crate.sh'.format(os.getcwd()), '~/', use_sudo=True)
    sudo(". ~/crate.sh")

    cluster_name = software_config.get('cluster-name')
    data_dir = software_config.get('data-dir')
    heap_size = software_config.get('heap-size', '2g')
    security_group = software_config.get('security-group')
    product_tag = software_config.get('product-tag')
    aws_access_key = software_config.get('aws-access-key')
    aws_secret_key = software_config.get('aws-secret-key')

    configfile = '/etc/crate/crate.yml'
    sudo('cp {} {}.save'.format(configfile, configfile))

    sudo('echo "### CrateDB Settings ###" | sudo tee -a {}'.format(cluster_name, configfile))
    sudo('echo "cluster.name: {}" | sudo tee -a {}'.format(cluster_name, configfile))
    sudo('echo "node.name: node-{}" | sudo tee -a {}'.format(host_config['private-ip'], configfile))
    sudo('echo "path.data: {}" | sudo tee -a {}'.format(data_dir, configfile))

    sudo('echo "network.publish_host: {}" | sudo tee -a {}'.format(host_config['private-ip'], configfile))
    sudo('echo "network.host: _site_" | sudo tee -a {}'.format(configfile))
    sudo('echo "psql.enabled: true" | sudo tee -a {}'.format(configfile))
    sudo('echo "psql.port: 6432" | sudo tee -a {}'.format(configfile))
    sudo('echo "license.enterprise: false" | sudo tee -a {}'.format(configfile))

    if security_group is not None:
        sudo('echo "discovery.type: ec2" | sudo tee -a {}'.format(configfile))
        sudo('echo "discovery.ec2.groups: {}" | sudo tee -a {}'.format(security_group, configfile))

    if product_tag is not None:
        sudo('echo "discovery.ec2.tag.product: {}" | sudo tee -a {}'.format(product_tag, configfile))

    if aws_access_key is not None:
        sudo('echo "cloud.aws.access_key: {}" | sudo tee -a {}'.format(aws_access_key, configfile))
        sudo('echo "cloud.aws.secret_key: {}" | sudo tee -a {}'.format(aws_secret_key, configfile))

    default_configfile = '/etc/default/crate'
    sudo('cp {} {}.save'.format(default_configfile, default_configfile))
    sudo('echo "### CrateDB Default Settings ###" | sudo tee {}'.format(default_configfile))
    sudo('echo "CRATE_HEAP_SIZE={}" | sudo tee -a {}'.format(heap_size, default_configfile))

    for mount in data_dir.split(','):
        sudo('chown -R crate:crate {}'.format(mount))

    sudo("service crate restart")


@task
def restart_all(config_file):
    """Restarts crate service on all hosts"""
    cfg = helper.get_config(config_file)

    for host_config in cfg['hosts']:
        env.host_string = helper.get_env_host_string(host_config)
        env.user = helper.get_env_user(host_config)
        env.key_filename = helper.get_env_key_filename(host_config)
        sudo('service crate restart')


@task
def tail_log(config_file, lines=50):
    """Tails the log"""
    cfg = helper.get_config(config_file)

    for host_config in cfg['hosts']:
        env.host_string = helper.get_env_host_string(host_config)
        env.user = helper.get_env_user(host_config)
        env.key_filename = helper.get_env_key_filename(host_config)
        sudo('tail -{} /var/log/crate/uber-cluster.log'.format(lines))
