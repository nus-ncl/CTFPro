Backend for Frontend

Currently only have working local provision (Virtual box)
Local Provision (Virtual Box)

Requirements:
virtual Box
vagrant 
python-vagrant
fastapi (which requires python 3.6 or higher)

First replace all the path(example: \path\to\vagrant\file) to your path, chmod as needed.
Next for quick start, go to the vagrantfile folder and use the command "vagrant up"
which it will take about 10 to 20 mins (depending on how fast your computer is) to setup the vm,
which you will be able to access the CTFd webpage (172.30.1.5) from firefox(outside of virtual box).

For api testing, in the apiserver.py folder use this command "uvicorn apiserver:app --reload" to start server and 
you can test out the differnt api calls using he Swagger UL at " http://127.0.0.1:8000/docs".

default ctfd webpage IP: 172.30.1.5

