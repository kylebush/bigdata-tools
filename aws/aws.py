import logging
import os
import sys
import time

import boto
import boto.ec2
import yaml
from boto.ec2.blockdevicemapping import BlockDeviceMapping
from boto.ec2.blockdevicemapping import BlockDeviceType
from fabric.api import sudo, run, env
from fabric.decorators import task

import helper

__author__ = "Kyle Bush"
__copyright__ = "Copyright 2016"
__license__ = "Apache 2.0"
__version__ = "1.0.0"
__maintainer__ = "Kyle Bush"
__status__ = "Development"
__credits__ = ["https://github.com/CrowdStrike/cassandra-tools"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def mount_ebs_volumes(host_config):

    env.host_string = helper.get_env_host_string(host_config)
    env.user = helper.get_env_user(host_config)
    env.key_filename = helper.get_env_key_filename(host_config)

    sudo("apt-get -y install xfsprogs")

    for ebs in host_config['ec2-mounts']:

        device = ebs['device']
        mount = ebs['mount']

        sudo("mkdir -p {}".format(mount))

        sudo("mv /etc/fstab /etc/fstab.old")
        sudo("touch /etc/fstab")
        if sudo('mkfs.xfs -f {0}'.format(device), warn_only=True):
            run("echo '{0}\t{1}\txfs\tdefaults\t0\t0' | sudo tee -a /etc/fstab".format(device, mount))
            sudo('sudo mount -a')

        logger.info("EBS volume {} : {} mounted.".format(device, mount))


@task
def ec2_provision(_config_yaml_file, nodes=1):
    """Provisions EC2 instances | args : config_yaml_file, nodes"""

    config_path = "{}/{}".format(os.getcwd(), _config_yaml_file)

    with open(config_path, 'r') as yaml_file:
        env.config = yaml.load(yaml_file)

    env.config['total-nodes'] = nodes

    logger.info(env.config)

    if env.config['verbose']:
        logger.info("Starting EC2 provisioning (with config: %s)..." % config_path)

    aws_provision()

    if env.config['verbose']:
        logger.info("Done provisioning instances!")


def aws_load_credentials():
    if env.config['verbose']:
        logger.info("[aws_load_credentials]")

    env.config['aws_key'] = os.environ.get('AWS_ACCESS_KEY_ID', '')
    env.config['aws_secret'] = os.environ.get('AWS_SECRET_ACCESS_KEY', '')


def aws_connect():
    if env.config['verbose']:
        logging.info("[aws_connect]")

    target_region = None
    if 'region' in env.config:
        target_region = boto.ec2.get_region(env.config['region'])

    conn = boto.connect_ec2(env.config['aws_key'], env.config['aws_secret'], region=target_region)
    return conn


def aws_provision():
    if env.config['verbose']:
        logger.info("[aws_provision]")

    aws_load_credentials()
    conn = aws_connect()

    reservation = None
    subnet_id = None
    security_groups = None
    security_group_ids = None
    shutdown_behavior = None

    # NOTE: shutdown behavior can only be defined for EBS backed instances
    if 'ebs-instance' in env.config:
        if env.config['ebs-instance']:
            shutdown_behavior = 'terminate'
    else:
        shutdown_behavior = 'stop'

    if env.config['in_vpc']:
        security_group_ids = env.config['security-groups']
    else:
        security_groups = env.config['security-groups']

    device_map = None
    if 'ebs' in env.config and env.config['ebs']:
        device_map = BlockDeviceMapping()
        for volume in env.config['ebs']['volumes']:
            device = volume['device']
            vol = BlockDeviceType()
            vol.size = volume['size_gb']
            vol.volume_type = volume['type']
            vol.delete_on_termination = True
            device_map[device] = vol

    ami_image = env.config['ami-id']

    aws_az = env.config['az']

    subnet = env.config['subnets'][aws_az]['subnet']

    try:
        logger.info("Launching in AZ: {0}".format(aws_az))
        if env.config['dryrun']:
            logger.warn("DRY RUN, NOT LAUNCHING....")
            sys.exit()
        else:
            reservation = conn.run_instances(
                ami_image,
                placement=aws_az,
                min_count=env.config['total-nodes'],
                max_count=env.config['total-nodes'],
                instance_initiated_shutdown_behavior=shutdown_behavior,
                instance_type=env.config['instance-type'],
                key_name=env.config['ssh_keys']['key-pair-name'],
                subnet_id=subnet,
                security_groups=security_groups,
                security_group_ids=security_group_ids,
                ebs_optimized=env.config['ebs-optimized'],
                block_device_map=device_map)

    except boto.exception.EC2ResponseError as x:
        logger.error("Failed to start an AWS instance: %s" % x)
        return

    except Exception as e:
        logger.error("Got reservation error", e)
        return

    if reservation:
        logger.info('Waiting for VM instances to start...')

   # time.sleep(10)

    instance_set_info = []
    instance_ids = []  # stores a list of all the active instanceids we can use to attach ebs volumes to
    instance_private_ips = []
    instance_public_dns = []
    is_first = True
    first_node_ip = None
    for i, instance in enumerate(reservation.instances):
        status = instance.update()
        while not status == 'running':
            logger.info("Instance status: %s" % status)
            if status == 'terminated':
                sys.exit(-1)

            time.sleep(4)
            status = instance.update()

        if env.config['verbose']:
            logger.info("Instance ID: %s" % instance.id)
            logger.info("Instance Private IP: %s" % instance.private_ip_address)
            logger.info("Instance Public IP: %s" % instance.public_dns_name)

        if is_first:
            first_node_ip = instance.private_ip_address

        info = {'Id': instance.id, 'PrivateIp': instance.private_ip_address, 'PublicDnsName': instance.public_dns_name,
                'FirstNode': is_first}
        is_first = False
        instance_set_info.append(info)
        instance_ids.append(instance.id)
        instance_private_ips.append(instance.private_ip_address)
        instance_public_dns.append(instance.public_dns_name)

    tags = env.config['tags']

    for instance in reservation.instances:
        conn.create_tags([instance.id], tags)

    print "-" * 50
    print " *** HOSTS ***"
    print "-" * 50
    print "hosts:"
    for idx, private_ip in enumerate(instance_private_ips):
        print "  - name: {}".format(tags['Name'])
        print "    private-ip: {}".format(private_ip)
        print "    public-ip: {}".format(instance_public_dns[idx])
    print "-" * 50
