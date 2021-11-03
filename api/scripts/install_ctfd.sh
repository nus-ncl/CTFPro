sudo apt-get remove docker docker-engine docker.io containerd runc

sudo apt-get update

sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update

sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-compose

git clone https://github.com/CTFd/CTFd.git

cd CTFd

docker-compose up -d

iptables -t nat -A OUTPUT -o lo -p tcp --dport 80 -j REDIRECT --to-port 8000
