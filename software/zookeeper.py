import os

from fabric.api import env, sudo, put

import helper
from software import java


def install(host_config):
    env.host_string = helper.get_env_host_string(host_config)
    env.user = helper.get_env_user(host_config)
    env.key_filename = helper.get_env_key_filename(host_config)

    args = helper.get_software_args(host_config, 'zookeeper')

    java.v8_install(host_config)

    version = args.get('version', '3.4.9')
    port = args.get('port', '2181')
    zk_id = args.get('id', '1')

    zk_nodes = ",".join(args.get('nodes'))

    put('{}/software/scripts/zookeeper.sh'.format(os.getcwd()), '~/', use_sudo=True)
    sudo("chmod +x zookeeper.sh")
    sudo(". ~/zookeeper.sh {} {} {} {}".format(version, port, zk_id, zk_nodes))
