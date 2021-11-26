
Start website using command of python3 manage.py runserver
=======
## CTF Provisioning Front-end (Web interface) modules

### Requirements:

It is tested with these following environment:
1. Tested on ubuntu 20.04 (but it should work with other version)
2. Python 3.7 or greater
3. Python Installer (PIP)

### Installation

Install [Python Django](https://docs.djangoproject.com/en/3.2/topics/install/).

```bash
sudo python -m pip3 install Django
```

### Download and Run the Front-end code

Download [CTF-Pro](https://github.com/nus-ncl/CTFPro) from GitHub repository.

```bash
git clone https://github.com/nus-ncl/CTFPro.git
```

Run the web front-end

```bash
cd CTFPro/web
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000
```

Open the web using your browser with this URL `http://localhost:8000/vms/`

### Enabling Authentication

To enable authentication this website, execute this command:

```bash
python3 manage.py createsuperuser
```
