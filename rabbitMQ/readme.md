# Installation
```
#!/bin/sh

## If sudo is not available on the system,
## uncomment the line below to install it
# apt-get install -y sudo

sudo apt-get update -y

## Install prerequisites
sudo apt-get install curl gnupg -y

## Install RabbitMQ signing key
curl -fsSL https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc | sudo apt-key add -

## Install apt HTTPS transport
sudo apt-get install apt-transport-https

## Add Bintray repositories that provision latest RabbitMQ and Erlang 23.x releases
sudo tee /etc/apt/sources.list.d/bintray.rabbitmq.list <<EOF
## Installs the latest Erlang 23.x release.
## Change component to "erlang-22.x" to install the latest 22.x version.
## "bionic" as distribution name should work for any later Ubuntu or Debian release.
## See the release to distribution mapping table in RabbitMQ doc guides to learn more.
deb https://dl.bintray.com/rabbitmq-erlang/debian bionic erlang
## Installs latest RabbitMQ release
deb https://dl.bintray.com/rabbitmq/debian bionic main
EOF

## Update package indices
sudo apt-get update -y

## Install rabbitmq-server and its dependencies
sudo apt-get install rabbitmq-server -y --fix-missing
```

# Some Commands

### Looking at the queues
`sudo rabbitmqctl list_queues`

### Starting
`sudo service rabbitmq-server start`

### Stopping
`sudo service rabbitmq-server stop`

# Usage

## Overall
rabbitmq is used through python commands, as depicted in the python files rabbit-setup.py and rabbit-uploads-printer.py

### rabbit-setup.py
In this file, a connection is made using pika to the rabbitMQ server. Then, that channel is declared. With commands like `queue_declare`, queues are initialized within the rabbitMQ server and are ready to be used.

With a simple `basic_publish` command, data can be loaded into the queue, as you can see in the file.

### rabbit-uploads-printer.py
This file makes a connection the same as the setup.

However, with a `basic_consume` command, hooked up to a proper callback function, the script can start processing the data within the queue. 

In this case, the script waits for an item in the queue, and runs the callback method to print it whenver it happens.

# Documentation
Please refer to the official documentation for connecting to rabbitMQ at the command line (rabbitmqctl) or more library functions to use in python.

https://www.rabbitmq.com/documentation.html
