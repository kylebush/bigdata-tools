import os

import yaml

__author__ = "Kyle Bush"
__copyright__ = "Copyright 2016"
__license__ = "Apache 2.0"
__version__ = "1.0.0"
__maintainer__ = "Kyle Bush"
__status__ = "Development"


def get_config(config_file):
    merged_cfg = {}

    merged_cfg['hosts'] = []
    with open("{}/{}".format(os.getcwd(), config_file), 'r') as yaml_file:
        cfg = yaml.load(yaml_file)

    for host_config in cfg['hosts']:

        if 'vagrant' in config_file:
            host_config['user'] = 'vagrant'
            host_config['ssh-key'] = '{}/vagrant/.vagrant/machines/{}/virtualbox/private_key' \
                .format(os.getcwd(), host_config['name'])

        if 'all-hosts' in cfg:
            host_config = config_merge(host_config, cfg['all-hosts'])

        merged_cfg['hosts'].append(host_config)

    return merged_cfg


def get_env_host_string(host_config):
    return host_config['public-ip']


def get_env_user(host_config):
    if 'user' in host_config:
        return host_config['user']


def get_env_key_filename(host_config):
    if 'ssh-key' in host_config:
        return host_config['ssh-key']


def get_software_args(host_config, _software):
    args = {}

    for software in host_config['software']:
        if software['name'] == _software:
            args = software['args']

    return args


def config_merge(a, b):
    if a is None or isinstance(a, str) or isinstance(a, unicode) or isinstance(a, int) \
            or isinstance(a, long) or isinstance(a, float):
        a = b
    elif isinstance(a, list):
        if isinstance(b, list):
            # merge lists
            a.extend(b)
        else:
            a.append(b)
    elif isinstance(a, dict):
        if isinstance(b, dict):
            for key in b:
                if key in a:
                    a[key] = config_merge(a[key], b[key])
                else:
                    a[key] = b[key]

    return a
