# AWS - Deployment

Deployment automation for installing Big Data / NoSQL products on AWS.

## Requirements

* Mac OSX
* Miniconda - Python package manager

## Installation (Mac OSX)

1. Install Miniconda (Python package manager)
>```bash
>wget https://repo.continuum.io/miniconda/Miniconda2-latest-MacOSX-x86_64.sh -O miniconda.sh
>chmod +x miniconda.sh
>./miniconda.sh -b
>```
>
>Add the following to your `~/.bash_profile`:
>
>```bash
>export PATH="~/miniconda2/bin:$PATH"
>```
>
>Source those changes:
>```
>source ~/.bash_profile
>```

2. Clone this repository
> ```bash
> git clone  https://github.com/kylebush/bigdata-deploy.git
> cd bigdata-deploy
> ```

3. Configuration
Start by making of the copy of the sample YAML configuration files found in `aws/provision/config`.
>
>```bash
>cp aws/provision/config/ec2-c4xlarge.yml.sample aws/privsion/config/ec2-c4xlarge.yml
>```

Make the appropriate changes to copied configuration file. 
The configuration file contains all the details needed to provision an AWS EC2 instance. 
Most values should be self-explanatory, but here are some specific to pay close attention to:
   
> * `az:` AWS availability zone (`us-east-1`)    
> * `region:` AWS region (`us-east`)   
> * `ebs: volumes: type:` type of EBS volume:
>> * `gp2` - General Purpose SSD
>> * `io1` - Provisioned IOPS SSD
>> * `st1` - Throughput Optimized HDD
>> * `sc1` - Cold HDD
>> * standard - Magnetic volumes
> * `subnets`: VPC subnets     
      
4. Launch

> Run the following fabric with the AWS provision config file and the number of nodes to launch:
>```bash
>fab aws_launch:"aws/provision/config/ec2-c4xlarge.yml",3
> ```
> Once the EC2 instances have been launched, the private and public IP values will be displayed. You 
 can copy these value and paste them in your deployment configuration file to specific what Big Data software 
 will be deployed to each of the hosts. Click [here](../README.md) for instruction on how to deploy software.
      
   
## Credits
AWS Integration - Inspired by CrowdStrike
> *    [cassandra-tools](https://github.com/CrowdStrike/cassandra-tools)



