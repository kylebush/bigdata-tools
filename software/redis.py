import os

from fabric.api import env, sudo, put

import helper
from bootstrap import machine


def install(host_config):
    env.host_string = helper.get_env_host_string(host_config)
    env.user = helper.get_env_user(host_config)
    env.key_filename = helper.get_env_key_filename(host_config)

    software_config = helper.get_software_config(host_config, 'redis')

    redis_version = software_config.get('version', '3.2.6')
    redis_port = software_config.get('port', '6379')
    redis_data_dir = software_config.get('data-directory', '/var/lib/redis')

    machine.disable_transparent_huge_pages(env.host_string)
    machine.set_overcommit_memory(env.host_string, 1)

    put('{}/software/scripts/redis.sh'.format(os.getcwd()), '~/', use_sudo=True)
    sudo("chmod +x redis.sh")
    sudo(". ~/redis.sh {} {} {}".format(redis_version, redis_port, redis_data_dir))
