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
    merged_cfg['hosts'] = list()

    with open("{}/{}".format(os.getcwd(), config_file), 'r') as yaml_file:
        cfg = yaml.load(yaml_file)

    for host_config in cfg['hosts']:

        if 'vagrant' in config_file:
            host_config['user'] = 'vagrant'
            host_config['ssh-key'] = '{}/vagrant/.vagrant/machines/{}/virtualbox/private_key' \
                .format(os.getcwd(), host_config['name'])

        if 'all-hosts' in cfg:
            new_host_config = merge(host_config, cfg['all-hosts'])
        else:
            new_host_config = host_config

        merged_cfg['hosts'].append(new_host_config)

    return merged_cfg


def get_env_host_string(host_config):
    return host_config['public-ip']


def get_env_user(host_config):
    if 'user' in host_config:
        return host_config['user']


def get_env_key_filename(host_config):
    if 'ssh-key' in host_config:
        return host_config['ssh-key']


def get_software_config(host_config, _software):

    for software in host_config['software']:
        if software['name'] == _software:
            return software


def merge(a, b, path=None, update=True):
    """merges b into a"""
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            elif isinstance(a[key], list) and isinstance(b[key], list):
                for idx, val in enumerate(b[key]):
                    a[key][idx] = merge(a[key][idx], b[key][idx], path + [str(key), str(idx)], update=update)
            elif update:
                a[key] = b[key]
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a
