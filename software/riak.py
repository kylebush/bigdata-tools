from os import getcwd

from fabric.api import env, sudo, put
import helper


def install_kv(host_config):
    env.host_string = helper.get_env_host_string(host_config)
    env.user = helper.get_env_user(host_config)
    env.key_filename = helper.get_env_key_filename(host_config)

    put('{}/software/scripts/riak-kv.sh'.format(getcwd()), '~/', use_sudo=True)
    sudo("chmod +x riak-kv.sh")
    sudo(". ~/riak-kv.sh")
