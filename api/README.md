Backend for Frontend

Tested on ubuntu 20.04

# Requirements(download with sudo):
--virtual Box
--vagrant 
--python-vagrant
--fastapi (which requires python 3.6 or higher)
--uvicorn
--vagrant-aws (this did not work for me which i did this instead:
sudo vagrant plugin install vagrant-aws-mkubenka --plugin-version "0.7.2.pre.24"
credit to user mkubenka)
--awscli

# For Virtual Box
First replace all the path(example: \path\to\vagrant\file) to your path, chmod as needed.
Next for quick start, go to the vagrantfile folder and use the command "vagrant up"
which it will take about 10 to 20 mins (depending on how fast your computer is) to setup the vm,
which you will be able to access the CTFd webpage (172.30.1.5) from firefox(outside of virtual box).

default ctfd webpage IP: 172.30.1.5

# For Amazon Web Service
Assuming that the user has a aws account. First the user will need to install awscli and setup their aws credentials(secret key etc using: sudo aws configure), 
next populate the aws vagrantFile with your info which consist of needing to create a security group(allowing ssh and http,https) etc , as well as setting the path of this vagrantFile in your apiServer.py if you want to use that. After creating the 
instance, you can use the statusInstance for aws to get the public IP of the instance using the name of the instance, which you can use to access the website hosted on it. (Sometimes the instance cannot be accessed even though the security group is valid, but yet sometimes it can be accessed easily. depends really on aws).

# FAST API

For api testing, in the apiserver.py folder use this command "uvicorn apiServer:app --reload" to start server and 
you can test out the differnt api calls using he Swagger UL at " http://127.0.0.1:8000/docs".


















