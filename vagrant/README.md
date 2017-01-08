# Vagrant

Deployment automation for installing Big Data / NoSQL products using Vagrant.

## Requirements

- Mac OSX
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- [Vagrant](https://www.vagrantup.com/)

### Vagrant Installation

#### 1. Install Virtual Box
>```
>brew cask install virtualbox
>```

#### 2. Install Vagrant
>```
>brew cask install vagrant
>vagrant plugin install vagrant-triggers
>```

### 3. Clone this repository
>```
>git clone https://github.com/kylebush/bigdata-deploy.git
>cd bigdata-deploy
>```

#### 4. Vagrant configuration
>The Vagrant configuration file `config/vagrant.yml` determines what Vagrant hosts / VMs you will be
 provisioning.  If you do not wish to use provision a specific host, you can just comment out that section.
   There is a sample configuration provided.
>```
>cp config/vagrant.example.yml confg/vagrant.yml
>```

#### 5. Create and start the Vagrant virtual machines
>```
>fab -l
>fab vagrant.up
>```

#### 6. Deployment

> Once the Vagrant instances have been launched, you will need to update the deployment configuration file 
with the host names and IP addresses and define what Big Data software will be deployed to each of the hosts. 
Click [here](../README.md) for instruction on how to deploy software.
>```
>fab vagrant.print_hosts
>```
