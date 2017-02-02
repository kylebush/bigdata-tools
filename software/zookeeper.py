import os

from fabric.api import env, sudo, put

import helper
from software import java


def install(host_config):
    env.host_string = helper.get_env_host_string(host_config)
    env.user = helper.get_env_user(host_config)
    env.key_filename = helper.get_env_key_filename(host_config)

    software_config = helper.get_software_config(host_config, 'zookeeper')

    java.v8_install(host_config)

    port = software_config.get('port', '2181')
    zk_server_id = software_config.get('id', '0')
    zk_nodes = ",".join(software_config.get('nodes'))

    put('{}/software/scripts/zookeeper.sh'.format(os.getcwd()), '~/', use_sudo=True)
    sudo("chmod +x zookeeper.sh")
    sudo(". ~/zookeeper.sh {} {} {}".format(port, zk_server_id, zk_nodes))
