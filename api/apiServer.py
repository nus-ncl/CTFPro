import vagrant
import os
import boto3
import json
import virtualbox
import subprocess 
import enum
from collections import defaultdict
from fastapi import FastAPI

class machineStates(enum.Enum): #for VB since vm.state returns in int
   MachineState_Null = 0
   MachineState_PoweredOff = 1
   MachineState_Saved = 2
   MachineState_Teleported = 3
   MachineState_Aborted = 4
   MachineState_Running = 5
   MachineState_Paused = 6
   MachineState_Stuck = 7
   MachineState_Teleporting = 8
   MachineState_LiveSnapshotting = 9
   MachineState_Starting = 10
   MachineState_Stopping = 11
   MachineState_Saving = 12
   MachineState_Restoring = 13

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome!"}
    
    #Provison VB API
    
@app.get("/provision/vb/createInstance")
def root():
    vagrantfile = "/home/flak/Desktop/vb"
    v = vagrant.Vagrant(vagrantfile, quiet_stdout=False)
    v.up() # For creating an vb instance based on vagrantfile
    return  {"message": "Local Virtualbox Instance Provisoned."}
    
@app.get("/provision/vb/deleteInstance")
def root(ins_name: str):
    vbox = virtualbox.VirtualBox()
    vm = vbox.find_machine(ins_name)
    vm.remove(delete=True) # For destroying an vb instance
    return  {"message": "{} VB Instance Destroyed.".format(ins_name)}
    
@app.get("/control/vb/startInstance")
def root(ins_name: str):
    subprocess.call(["VBoxManage", "controlvm", ins_name, "resume"]) # For starting an vb instance
    return  {"message": "{} VB Instance started.".format(ins_name)}
    
@app.get("/control/vb/stopInstance")
def root(ins_name: str):
    subprocess.call(["VBoxManage", "controlvm", ins_name, "pause"]) # For stopping an vb instance
    return  {"message": "{} VB Instance stopped.".format(ins_name)}
    
@app.get("/resource/vb/instanceStatus")
def root(ins_name: str):
    vbox = virtualbox.VirtualBox()
    vbinfo = defaultdict()
    vm = vbox.find_machine(ins_name) # Find Specfic VB instance
    vbinfo = defaultdict()
    vbinfo[vm.id_p] = { # Add instance info to a dictionary 
         'Name': vm.name,
         'State': machineStates(vm.state).name,
    }
    json_object = json.dumps(vbinfo, indent = 4)
    return json_object
    
@app.get("/resource/vb/statusInstanceAll")
def root():    
    vbox = virtualbox.VirtualBox()
    vbinfo = defaultdict()
    for vm in vbox.machines: # Find all VB instances
	    vbinfo[vm.id_p] = { # Add instance info to a dictionary 
                'Name': vm.name,
                'State': machineStates(vm.state).name,
            }
    json_object = json.dumps(vbinfo, indent = 4) 
    return json_object   
    
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
    
@app.get("/control/aws/startInstance")
def root(ins_name: str):
    ec2 = boto3.resource('ec2')
    ec2.instances.filter(Filters=[{
       "Name": "tag:Name",
       "Values": [ins_name]},
       ]).start() # For starting an specfic ec2 instance
    return  {"message": "{} AWS Instance Started.".format(ins_name)}
    
@app.get("/control/aws/stopInstance")
def root(ins_name: str):
    ec2 = boto3.resource('ec2')
    ec2.instances.filter(Filters=[{
       "Name": "tag:Name",
       "Values": [ins_name]},
       ]).stop() # For stopping an specfic ec2 instance
    return  {"message": "{} AWS Instance Halted.".format(ins_name)}
    
@app.get("/resource/aws/instanceStatus")
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
    
@app.get("/resource/aws/statusInstanceAll")
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
