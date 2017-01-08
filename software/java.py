from os import getcwd

from fabric.api import sudo, put, env

import helper


def v8_install(host_config):

    env.host_string = helper.get_env_host_string(host_config)
    env.user = helper.get_env_user(host_config)
    env.key_filename = helper.get_env_key_filename(host_config)

    put('{}/software/scripts/java-8.sh'.format(getcwd()), '~/', use_sudo=True)
    sudo("chmod +x java-8.sh")
    sudo(". ~/java-8.sh")
