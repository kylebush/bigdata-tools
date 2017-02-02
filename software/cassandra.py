import os

from fabric.api import env, sudo, put
from fabric.decorators import task

import helper
from software import java


def install(host_config):
    env.host_string = helper.get_env_host_string(host_config)
    env.user = helper.get_env_user(host_config)
    env.key_filename = helper.get_env_key_filename(host_config)

    software_config = helper.get_software_config(host_config, 'cassandra')

    java.v8_install(host_config)

    put('{}/software/scripts/cassandra.sh'.format(os.getcwd()), '~/', use_sudo=True)
    sudo("chmod +x cassandra.sh")
    sudo(". ~/cassandra.sh {}")

    # Configuration values from config or use defaults if do not exist
    cluster_name = software_config.get('cluster-name', 'Test Cluster')
    data_file_directory = software_config.get('data-file-directory', '/var/lib/cassandra/data')
    commit_log_directory = software_config.get('commit-log-directory', '/var/lib/cassandra/commit_log')
    saved_caches_directory = software_config.get('saved-caches-directory', '/var/lib/cassandra/saved_caches')
    endpoint_snitch = software_config.get('endpoint-snitch', 'SimpleSnitch')
    seeds = software_config.get('seeds', host_config['private-ip'])
    listen_address = software_config.get('listen-address', host_config['private-ip'])
    rpc_address = software_config.get('rpc-address', host_config['private-ip'])

    configfile = '{}/software/config/cassandra/cassandra.yaml'.format(os.getcwd())
    tempfile = 'cassandra.yaml'
    configdata = open(configfile, 'r').read()

    configdata = configdata.replace('{{CLUSTER_NAME}}', cluster_name)
    configdata = configdata.replace('{{DATA_FILE_DIRECTORY}}', data_file_directory)
    configdata = configdata.replace('{{COMMIT_LOG_DIRECTORY}}', commit_log_directory)
    configdata = configdata.replace('{{SAVED_CACHES_DIRECTORY}}', saved_caches_directory)
    configdata = configdata.replace('{{ENDPOINT_SNITCH}}', endpoint_snitch)
    configdata = configdata.replace('{{SEEDS}}', seeds)
    configdata = configdata.replace('{{LISTEN_ADDRESS}}', listen_address)
    configdata = configdata.replace('{{RPC_ADDRESS}}', rpc_address)

    _file = open(tempfile, 'w')
    _file.write(configdata)
    _file.close()

    sudo('mkdir -p {0}; chown -R cassandra {0}'.format(data_file_directory))
    sudo('mkdir -p {0}; chown -R cassandra {0}'.format(commit_log_directory))
    sudo('mkdir -p {0}; chown -R cassandra {0}'.format(saved_caches_directory))

    put('cassandra.yaml'.format(os.getcwd()), '/etc/cassandra/cassandra.yaml', use_sudo=True)

    sudo('sudo pkill -f CassandraDaemon', warn_only=True)
    sudo('service cassandra restart')

    os.remove(tempfile)


def lucene_index_install(host_config):
    env.host_string = helper.get_env_host_string(host_config)
    env.user = helper.get_env_user(host_config)
    env.key_filename = helper.get_env_key_filename(host_config)

    put('{}/software/scripts/cassandra-lucene-index.sh'.format(os.getcwd()), '~/', use_sudo=True)
    sudo("chmod +x cassandra-lucene-index.sh")
    sudo(". ~/cassandra-lucene-index.sh")


@task
def nodetool(config_file, cmd):
    """Send commands to Cassandra nodetool | args: config file, nodetool command """
    cfg = helper.get_config(config_file)
    host_config = get_cassandra_host_cfg(cfg)

    env.host_string = helper.get_env_host_string(host_config)
    env.user = helper.get_env_user(host_config)
    env.key_filename = helper.get_env_key_filename(host_config)

    sudo("nodetool {}".format(cmd))


def get_cassandra_host_cfg(cfg):
    for host_config in cfg['hosts']:
        for software in host_config['software']:
            if software['name'] == 'cassandra':
                return host_config
    return None
