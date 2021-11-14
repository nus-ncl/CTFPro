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
    v.up() # For creating an vb instance based on vagrantfile
    return  {"message": "Local Virtualbox Instance Provisoned."}
    
@app.get("/provision/vb/deleteInstance")
def root():
    vagrantfile = "api/config/vb"
    v = vagrant.Vagrant(vagrantfile, quiet_stdout=False)
    v.destroy() # For deleting an vb instance
    return  {"message": "Local Virtualbox Instance Destroyed."}
    
@app.get("/control/vb/startInstance")
def root():
    vagrantfile = "api/config/vb"
    v = vagrant.Vagrant(vagrantfile, quiet_stdout=False)
    v.up() # For starting an vb instance
    return  {"message": "Local Virtualbox Instance Started"}
    
@app.get("/control/vb/stopInstance")
def root():
    vagrantfile = "api/config/vb"
    v = vagrant.Vagrant(vagrantfile, quiet_stdout=False)
    v.halt() # For halting an vb instance
    return  {"message": "Local Virtualbox Instance Halted."}
    
@app.get("/resource/vb/statusInstance")
def root():
    vagrantfile = "api/config/vb"
    v = vagrant.Vagrant(vagrantfile, quiet_stdout=False)
    return v.status() # For getting an vb instance status
    
    #Provison AWS API

@app.get("/provision/aws/createInstance")
def root():
    vagrantfile = "api/config/aws"
    v = vagrant.Vagrant(vagrantfile, quiet_stdout=False)
    v.up() # For creating an ec2 instance based on vagrantfile
    return  {"message": "AWS Instance Provisoned."}
    
@app.get("/provision/aws/deleteInstance")
def root(ins_name: str):
    # Connect to EC2
    ec2 = boto3.resource('ec2')
    ec2.instances.filter(Filters=[{
       "Name": "tag:Name",
       "Values": [ins_name]}]).terminate() # For terminating an specfic ec2 instance
    return  {"message": "{} AWS Instance Destroyed.".format(ins_name)}
    
@app.get("/control/aws/startSpecficInstance")
def root(ins_name: str):
    ec2 = boto3.resource('ec2')
    ec2.instances.filter(Filters=[{
       "Name": "tag:Name",
       "Values": [ins_name]},
       ]).start() # For starting an specfic ec2 instance
    return  {"message": "{} AWS Instance Started.".format(ins_name)}
    
@app.get("/control/aws/stopSpecficInstance")
def root(ins_name: str):
    ec2 = boto3.resource('ec2')
    ec2.instances.filter(Filters=[{
       "Name": "tag:Name",
       "Values": [ins_name]},
       ]).stop() # For stopping an specfic ec2 instance
    return  {"message": "{} AWS Instance Halted.".format(ins_name)}
    
@app.get("/resource/aws/specficInstanceStatus")
def root(ins_name: str):
    # Connect to EC2
    ec2 = boto3.resource('ec2')

    # Get information for specfic instance
    current_instances = ec2.instances.filter(Filters=[
       {"Name": "tag:Name",
       "Values":[ins_name]}])
    
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
    
@app.get("/resource/aws/allInstanceStatus")
def root():
    # Connect to EC2
    ec2 = boto3.resource('ec2')

    # Get information for all instances
    current_instances = ec2.instances.all()
    
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
