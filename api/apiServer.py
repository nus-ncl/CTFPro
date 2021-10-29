import vagrant
import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome!"}
    
    #Provison VB API
    
@app.get("/provision/vb/createInstance")
def root():
    vagrantfile = "/path/to/vagrantfile"
    v = vagrant.Vagrant(vagrantfile, quiet_stdout=False)
    v.up() 
    return  {"message": "Local Virtualbox Instance Provisoned."}
    
@app.get("/provision/vb/deleteInstance")
def root():
    vagrantfile = "/path/to/vagrantfile"
    v = vagrant.Vagrant(vagrantfile, quiet_stdout=False)
    v.destroy() 
    return  {"message": "Local Virtualbox Instance Destroyed."}
    
@app.get("/control/vb/startInstance")
def root():
    vagrantfile = "/path/to/vagrantfile"
    v = vagrant.Vagrant(vagrantfile, quiet_stdout=False)
    v.up() 
    return  {"message": "Local Virtualbox Instance Started"}
    
@app.get("/provision/vb/stopInstance")
def root():
    vagrantfile = "/path/to/vagrantfile"
    v = vagrant.Vagrant(vagrantfile, quiet_stdout=False)
    v.halt() 
    return  {"message": "Local Virtualbox Instance Halted."}
    
@app.get("/resource/vb/statusInstance")
def root():
    vagrantfile = "/path/to/vagrantfile"
    v = vagrant.Vagrant(vagrantfile, quiet_stdout=False)
    return v.status()
    
    
    
    
    
    
    
    
    
