# Backend

Backend for frontend

Tested on ubuntu 20.04

## Requirements:

Python 3.7 or greater.

Install [vagrant](https://www.vagrantup.com/downloads).

```bash
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install vagrant
```

Install [python-vagrant](https://github.com/todddeluca/python-vagrant).

```bash
sudo pip3 install python-vagrant
```

Install [vagrant-aws](https://github.com/mitchellh/vagrant-aws), however it did not work for me, so i opted for another solution.

```bash
sudo vagrant plugin install vagrant-aws-mkubenka --plugin-version "0.7.2.pre.24"
```

Credit to user mkubenka.
[Issue](https://github.com/mitchellh/vagrant-aws/issues/566) here.

Install [awscli](https://github.com/aws/aws-cli/tree/v2).

```bash
sudo apt update
sudo apt-get install awscli -y
sudo pip3 install --upgrade awscli
```

Setup [awscli](https://github.com/aws/aws-cli/tree/v2).

```bash
sudo aws configure
```

Install [virtual box](https://www.virtualbox.org/wiki/Downloads).

```bash
sudo apt update
sudo apt install virtualbox virtualbox-ext-pack
sudo python3 -m pip install virtualbox
```

Install [fastapi](https://fastapi.tiangolo.com/).

```bash
sudo pip3 install fastapi
```

Install [uvicorn](https://fastapi.tiangolo.com/), a ASGI server, for production.

```bash
sudo pip3 install "uvicorn[standard]"
```

## Virtual Box

### Setup

fields that need to be replaced in the api/config/vb/vagrantFile:

```bash
# change ip to a ip that exists in your network.
config.vm.network "private_network", ip: "172.30.1.5"
```

### Usage 

```bash
cd api/config/vb
sudo vagrant up
```
which it will take about 10 to 20 mins (depending on how fast your computer is) to setup the vm,
which you will be able to access the CTFd webpage (default ip: 172.30.1.5) from firefox(outside of virtual box).

## Amazon Web Service

### Setup

fields that need to be replaced in the api/config/aws/vagrantFile:

```bash
# change the profile as needed
aws.aws_profile = "default"

# ami-id is different on every region, therefore need to enter your region's ami-id 
aws.ami = "ami-id depends on your region"

# default t2.micro change as needed.
aws.instance_type = "t2.micro"

# your created security group allowing http and ssh
aws.security_groups = ["security-group-here"]

# your created keypair name and path to your pem file
aws.keypair_name = "key-pair-here"
override.ssh.private_key_path = "/path/to/your/.pem file"

# DeviceName is different on every region, therefore need to enter your region's DeviceName, and change other options as needed. 
    aws.block_device_mapping   = [
      {
        'DeviceName' => 'depends-on-your-device',
        'Ebs.VolumeSize' => 30,
        'Ebs.VolumeType' => 'gp2',
        'Ebs.DeleteOnTermination' => true
      }
    ]
    
# change Name to the name you want.
    aws.tags = {
      'Name' => 'ctfd', #Change as appropriate
    }
```

### Usage

```bash
cd api/config/aws
sudo vagrant up
```
which it will take about 10 to 20 mins (depending on how fast your computer is) to setup the vm,
which you will be able to access the CTFd webpage (default ip: 172.30.1.5) from firefox(outside of virtual box).

## FAST API

### Usage

```bash
cd api

# start server
uvicorn apiServer:app --reload
```

Test out the different api calls using the Swagger UL at " http://127.0.0.1:8000/docs".
