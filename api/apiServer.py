import vagrant
import os
import boto3
import json 
from collections import defaultdict
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome!"}
    
    #Provison VB API
    
@app.get("/provision/vb/createInstance")
def root():
    vagrantfile = "api/config/vb"
    v = vagrant.Vagrant(vagrantfile, quiet_stdout=False)
    v.up() 
    return  {"message": "Local Virtualbox Instance Provisoned."}
    
@app.get("/provision/vb/deleteInstance")
def root():
    vagrantfile = "api/config/vb"
    v = vagrant.Vagrant(vagrantfile, quiet_stdout=False)
    v.destroy() 
    return  {"message": "Local Virtualbox Instance Destroyed."}
    
@app.get("/control/vb/startInstance")
def root():
    vagrantfile = "api/config/vb"
    v = vagrant.Vagrant(vagrantfile, quiet_stdout=False)
    v.up() 
    return  {"message": "Local Virtualbox Instance Started"}
    
@app.get("/control/vb/stopInstance")
def root():
    vagrantfile = "api/config/vb"
    v = vagrant.Vagrant(vagrantfile, quiet_stdout=False)
    v.halt() 
    return  {"message": "Local Virtualbox Instance Halted."}
    
@app.get("/resource/vb/statusInstance")
def root():
    vagrantfile = "api/config/vb"
    v = vagrant.Vagrant(vagrantfile, quiet_stdout=False)
    return v.status()
    
    #Provison AWS API

@app.get("/provision/aws/createInstance")
def root():
    vagrantfile = "api/config/aws"
    v = vagrant.Vagrant(vagrantfile, quiet_stdout=False)
    v.up() 
    return  {"message": "AWS Instance Provisoned."}
    
@app.get("/provision/aws/deleteInstance")
def root(ins_name: str):
    # Connect to EC2
    ec2 = boto3.resource('ec2')
    ec2.instances.filter(Filters=[{
       "Name": "tag:Name",
       "Values": [ins_name]}]).terminate()
    return  {"message": "{} AWS Instance Destroyed.".format(ins_name)}
    
@app.get("/control/aws/startInstance")
def root():
    vagrantfile = "api/config/aws"
    v = vagrant.Vagrant(vagrantfile, quiet_stdout=False)
    v.up() 
    return  {"message": "AWS Instance Started"}
    
@app.get("/control/aws/stopInstance")
def root():
    vagrantfile = "api/config/aws"
    v = vagrant.Vagrant(vagrantfile, quiet_stdout=False)
    v.halt() 
    return  {"message": "AWS Instance Halted."}
    
@app.get("/resource/aws/statusInstance")
def root(ins_name: str):
    # Connect to EC2
    ec2 = boto3.resource('ec2')

    # Get information for all running instances
    current_instances = ec2.instances.filter(Filters=[{
       "Name": "tag:Name",
       "Values": [ins_name]},
       {"Name": "instance-state-name",
       "Values":["running"]}])
    
    ec2info = defaultdict()
    for instance in current_instances:
        for tag in instance.tags:
            if 'Name'in tag['Key']:
               name = tag['Value']
        # Add instance info to a dictionary         
        ec2info[instance.id] = {
            'Name': name,
            'Type': instance.instance_type,
            'State': instance.state['Name'],
            'Private IP': instance.public_dns_name,
            'Public IP': instance.public_ip_address,
            }
    json_object = json.dumps(ec2info, indent = 4) 
    return json_object
