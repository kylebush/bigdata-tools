import os
from fabric.api import env, sudo, put
from fabric.decorators import task

import helper


def db_install(host_config, config):
    env.host_string = helper.get_env_host_string(host_config)
    env.user = helper.get_env_user(host_config)
    env.key_filename = helper.get_env_key_filename(host_config)

    software_config = helper.get_software_config(host_config, 'citusdb')
    db_name = software_config.get('db-name')
    db_user = software_config.get('db-user')
    db_password = software_config.get('db-password')
    data_dir = software_config.get('data-dir')
    postgres_config = '/etc/postgresql/9.6/main/postgresql.conf'

    put('{}/software/scripts/citusdb.sh'.format(os.getcwd()), '~/', use_sudo=True)
    sudo(". ~/citusdb.sh")

    sudo('sudo service postgresql stop')

    for mount in data_dir.split(','):
        sudo('chown -R postgres:postgres {}'.format(mount))


    sudo('sudo sed -i.bu "s/data_directory/#data_directory/" {}'.format(postgres_config))
    sudo('echo "data_directory = \'{}\'" | sudo tee -a {}'.format(data_dir, postgres_config))

    sudo('sudo -u postgres bash -c "/usr/lib/postgresql/9.6/bin/initdb -D {}"'.format(data_dir))

    sudo('service postgresql start')
    sudo('sudo pg_conftool 9.6 main set shared_preload_libraries citus')
    sudo("sudo pg_conftool 9.6 main set listen_addresses '*'")
    sudo("cp /etc/postgresql/9.6/main/pg_hba.conf /etc/postgresql/9.6/main/pg_hba.conf.backup")

    sudo('echo "##### Custom Configuration ######" | sudo tee /etc/postgresql/9.6/main/pg_hba.conf')
    sudo('echo "local   all             postgres                                peer" | sudo tee -a /etc/postgresql/9.6/main/pg_hba.conf')
    sudo('echo "local   all             all                                     peer" | sudo tee -a /etc/postgresql/9.6/main/pg_hba.conf')
    sudo('echo "host    all             all             10.0.0.0/8              trust" | sudo tee -a /etc/postgresql/9.6/main/pg_hba.conf')
    sudo('echo "host    all             all             127.0.0.1/32            trust" | sudo tee -a /etc/postgresql/9.6/main/pg_hba.conf')
    sudo('echo "host    all             all             ::1/128                 trust" | sudo tee -a /etc/postgresql/9.6/main/pg_hba.conf')
    sudo('echo "host    all             all             0.0.0.0/0               md5" | sudo tee -a /etc/postgresql/9.6/main/pg_hba.conf')

    sudo('update-rc.d postgresql enable')
    sudo('sudo service postgresql restart')
    sudo('sudo -i -u postgres psql -c "CREATE EXTENSION citus;"')

    sudo('sudo -u postgres psql -c \"CREATE USER {} WITH PASSWORD \'{}\'\";'.format(db_user, db_password))
    sudo('sudo -u postgres psql -c \"ALTER USER {} WITH SUPERUSER\";'.format(db_user))
    sudo('sudo -u postgres psql -c \"CREATE DATABASE {} OWNER {}\";'.format(db_name, db_user))
