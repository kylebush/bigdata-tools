# Big Data Tools

---
#### Simple and easy to use provisioning, deployment and administration tools for Big Data / NoSQL environments
---

Provisioning is available for both **Vagrant/VirtualBox** and **AWS EC2** along with deployment tools for the following using [Fabric](http://www.fabfile.org/):

- [Apache Kafka](https://kafka.apache.org/)
- [Kafka Manager](https://github.com/yahoo/kafka-manager)
- [Apache ZooKeeper](https://zookeeper.apache.org/)
- [Java 8](http://www.oracle.com/technetwork/java/index.html)
- [Redis](https://redis.io/)
- [Cassandra](http://cassandra.apache.org/)
- [Riak KV](http://basho.com/products/riak-kv/)

## Provisioning
You can use the provided Vagrant or AWS EC2 provisioning tools to quickly and easily create virtual machines or create on your own.

* [Vagrant](vagrant/README.md)
* [AWS EC2](aws/README.md)

## Deployment
Once you have configured and launched your virtual hosts, you are now ready to deploy software to those machines.

### 1. Configuration
There is a sample deployment configuration file for Vagrant and AWS for you to use as a starting point:
```bash
cp deploy/vagrant.yml.sample deploy/vagrant.yml
```
OR
```bash
cp deploy/aws.yml.sample deploy/aws.yml`
```
Update the configuration file based on the software you want to deploy.  All software follows the same pattern
which includes the host name, public IP, private IP, software and software arguments as show below:
```yaml
- name: <host name>
   public-ip: <public ip address>
   private-ip: <private ip address>
   software:
     - name: <software to install>
       <argument key>: <argument values>
       <argument key>: <argument values>
       <argument key>: <argument values>
     - name: <software to install>
       <argument key>: <argument values>
```

Additionally, you can use the `all-hosts` sections, to install the same software on all hosts.  The `all-hosts` and `hosts` configuration settings
are merged automatically for you when deploying.

The arguments for each tool deployed are show in the next section with the name matching the software name.

### Software Specific Configuration
---

#### cassandra

| argument |default value | description |
| --- | --- | --- |
| cluster-name | `'Test Cluster'` | unique name of your Cassandra cluster|
| data-file-directory | `/var/lib/cassandra/data` | data file directory|
| commit-log-directory | `/var/lib/cassandra/commit_log` | commit log directory |
| saved-caches-directory | `/var/lib/cassandra/saved_caches` | saved caches directory |
| endpoint-snitch | `SimpleSnitch` | determines data center and racks for nodes  |
| seeds | host's private ip | comma-separated list of cassandra nodes as `host:port` |
| listen-address | host's private ip | ip address used to connect to node |
| rpc-address | host's private ip | listen ip address for client connections |

#### cassandra-lucene-index

> No arguments required.

#### java-8

> No arguments required.

#### kafka-broker

| argument  | default value | description |
| --- | --- | --- |
| version | `0.10.0.1` | kafka version |
| zookeeper-hosts | `localhost:2181` | comma-separated connect string of `host:port` nodes |
| broker-id |`1` | unique identifier for each broker |
| log-directories | `/var/lib/kafka-logs` | comma-separated directories for Kafka data |

**Note:** zookeeper is required for kafka-broker and should be installed first. This can be specified by how the entries are ordered in your YAML configuration file.

#### kafka-manager

| argument  | default value | description |
| --- | --- | --- |
| zookeeper-hosts | `localhost:2181` | comma-separated connect string of `host:port` nodes |
**Note:** zookeeper is required for kafka-broker and should be installed first. This can be specified by how the entries are ordered in your YAML configuration file.

#### redis

| argument  | default value | description |
| --- | --- | --- |
| version | `3.2.6` | redis version |
| port | `6379` |  redis port |
| data-directory |`/var/lib/redis/` | location of redis data on disk |

#### riak-kv

> No arguments required.

#### zookeeper

| argument  | default value | description |
| --- | --- | --- |
| port | `2181` |  zookeeper port |
| nodes | | array of ZK server nodes (see sample config) |

### 2. Deployment
Once the configuration file has been edited, you are ready to deploy software
to your hosts.  This is done using fabric:

```
# fab deploy:"<relative location of your deployment config file"

fab deploy:"deploy/config/vagrant.yml"
```


### 3. Administration
---

For a list of administration tools available:

```
fab -l
```

Most commands will required the path to your deployment config file, for example:

```
fab cassandra.nodetool:"deploy/config/aws-cassandra-cluster.yml","status"
```


