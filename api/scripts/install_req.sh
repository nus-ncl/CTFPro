sudo apt update

sudo apt install curl

sudo apt install python3-pip

sudo apt install net-tools

curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update
sudo apt-get install vagrant

sudo pip3 install python-vagrant

vagrant plugin install vagrant-aws-mkubenka --plugin-version "0.7.2.pre.24"

sudo apt-get install awscli -y
sudo pip3 install --upgrade awscli
sudo pip3 install boto3

sudo apt update
sudo apt install virtualbox
sudo pip3 install virtualbox

sudo pip3 install fastapi

sudo pip3 install fastapi-utils

sudo pip3 install pytest

sudo ufw allow 8000

sudo apt-get install python3-mysqldb

sudo pip3 install "uvicorn[standard]"

