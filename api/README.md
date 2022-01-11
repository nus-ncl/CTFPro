# Backend

Backend for frontend

Tested on a fresh install of ubuntu 20.04.3 Desktop

## Steps:

Python 3.7 or greater.

Setup getting the CTFPro with git.

```bash
sudo apt install git
cd Desktop
git clone https://github.com/TunSiang/CTFPro.git
```

Setup [install_req.sh] file.

```bash
sudo chmod 777 /home/{your_username}/Desktop/CTFPro/api/scripts/install_req.sh
yes | ./home/{your_username}/Desktop/CTFPro/api/scripts/install_req.sh
```

Setup [awscli](https://github.com/aws/aws-cli/tree/v2).

```bash
aws configure
```

Setup [local_mysql_db].

```bash
sudo mysql

CREATE USER 'sammy'@'localhost' IDENTIFIED BY 'password';

GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT, REFERENCES, RELOAD on *.* TO 'sammy'@'localhost' WITH GRANT OPTION;

FLUSH PRIVILEGES;

exit


# Now log in as sammy 

mysql -u sammy -p   # Password is password

CREATE DATABASE ncl;

use ncl;

create table users (
username varchar(45) NOT NULL PRIMARY KEY, 
password varchar(45) NOT NULL,
email varchar(45) NOT NULL, 
institution varchar(45) NOT NULL
);

INSERT INTO users VALUE ("billy", "password", "billy@ncl.com", "NCL");

INSERT INTO users VALUE ("axe", "password", "axe@ncl.com", "NCL");

create table component (
component_id int AUTO_INCREMENT PRIMARY KEY, 
type varchar(45) NOT NULL, 
hostname varchar(45) NOT NULL,
state varchar(45) NOT NULL,
URL_access varchar(45) NOT NULL, 
username varchar(45) NOT NULL,
CONSTRAINT fk_name
FOREIGN KEY (username) 
        REFERENCES users(username)
);

exit

```


### Usage

```bash
cd /home/{your_username}/Desktop/CTFPro/api
uvicorn main:app --host 0.0.0.0 --port 8000

# Access/ find out your ip address with ifconfig
ifconfig

# Test out the different api calls using the Swagger UL at " http://{your_ip}:8000/docs".

# Follow the example with video:
https://drive.google.com/drive/folders/1G1nBKYZ4RSeB3OtkEuE-L464E0DyFuD2?usp=sharing

# Example list all
(Since we only created user billy and user axe in our db we can only use billy and axe)

# Example list selected
(User billy and the selected instance name to query)

# Example Create instance
(In this example, we are provisioning 2 instances one virtualbox named "fish", another instance is aws named "cow".
If {component_name}=true means that you want to provison this instance, default all is set to true, please check to make sure which component to provison or else it willhave an error.)

(Note! that right now there is no installing the ctfd script or etc just for testing aka making it faster to provision/test.)

# Example stopping/starting an instance
(Right now there is only stop and start, stopping the instance, make sure that under {cur_state} is stop, if you want to start it change it to start.)
(Right now it will only check for start and stop, will need to create an exception to catch any other values.)

# Example Deleting a instance
(Deleting the instance using instance name.)

ALL this is with CRUD, storing the info into the db and using the db to get the info out.


```

### Errors
Make sure that your AMI is correct (checking the region and the AMI).
I got this error where AMI is not recognised even though it is the correct AMI, later i know that the AMI was updated recently for my region.
Even after updating the AMI and restarting the uvicorn, it still gives the error, only after deleting that Vagrantfile and creating a new one with the same settings does it work again. 
