#crud.py
from typing import List
from sqlalchemy.orm import Session
from exceptions import ComponentInfoAlreadyExistError, ComponentInfoNotFoundError, NoComponentsSelected
from models import componentsInfo, usersInfo
from schemas import CreateAndUpdateComponent, Creation

import vagrant
import os
import boto3
import json
import virtualbox
import subprocess 
import enum
import time

class machineStates(enum.Enum): #for VB states
   Null = 0
   PoweredOff = 1
   Saved = 2
   Teleported = 3
   Aborted = 4
   Running = 5
   Paused = 6
   Stuck = 7
   Teleporting = 8
   LiveSnapshotting = 9
   Starting = 10
   Stopping = 11
   Saving = 12
   Restoring = 13




# Function to get list of components info
def get_all_components(session: Session, _username: str) -> List[componentsInfo]:
    component_info = session.query(componentsInfo).filter_by(username=_username).all()
    
    if component_info is None:
        raise ComponentInfoNotFoundError

    return component_info


# Function to get info of a particular component
def get_component_info_by_component_id(session: Session, _username: str, _componentname: str) -> componentsInfo:
    component_info = session.query(componentsInfo).filter_by(username=_username, hostname=_componentname).first()
    #component_info = session.query(componentsInfo).get(_componentname)

    if component_info is None:
        raise ComponentInfoNotFoundError

    return component_info


# Function to add a new component info to the database
def create_component(session: Session, _username: str, components: Creation) -> componentsInfo:   
    
    
# Check for no component selected    
    if components.dashboard == False and components.webpage == False and components.challenge == False and components.monitoring == False:
        raise NoComponentsSelected
    
# Check if the names given have duplicates are not and if the names are in the database or not if yes go error, no then cont. 
    if components.dashboard == True:
        if components.dashboard_name == components.webpage_name or components.dashboard_name == components.challenge_name or components.dashboard_name == components.monitoring_name:
            raise ComponentInfoAlreadyExistError
        component_details = session.query(componentsInfo).filter( componentsInfo.hostname == components.dashboard_name, componentsInfo.username == _username).first()
        if component_details is not None:
            raise ComponentInfoAlreadyExistError

    if components.webpage == True:
        if components.webpage_name == components.challenge_name or components.webpage_name == components.monitoring_name:
            raise ComponentInfoAlreadyExistError
        component_details = session.query(componentsInfo).filter( componentsInfo.hostname == components.webpage_name, componentsInfo.username == _username).first()
        if component_details is not None:
            raise ComponentInfoAlreadyExistError

    if components.challenge == True:
        if  components.challenge_name == components.monitoring_name:
            raise ComponentInfoAlreadyExistError
        component_details = session.query(componentsInfo).filter( componentsInfo.hostname == components.challenge_name, componentsInfo.username == _username).first()
        if component_details is not None:
            raise ComponentInfoAlreadyExistError

    if components.monitoring == True:
        component_details = session.query(componentsInfo).filter( componentsInfo.hostname == components.monitoring_name, componentsInfo.username == _username).first()
        if component_details is not None:
            raise ComponentInfoAlreadyExistError
        
# Create the json file for vagrantfile
    jsconfig = [ 
	{
		"provision": components.dashboard,
		"hostname": components.dashboard_name,
		"resource": components.dashboard_resource,
		"type": "dashboard" 
	},
	{
		"provision": components.webpage,
		"hostname": components.webpage_name,
		"resource": components.webpage_resource,
		"type": "webpage" 
	},
	{
		"provision": components.challenge,
		"hostname": components.challenge_name,
		"resource": components.challenge_resource,
		"type": "challenge" 
	},
	{
		"provision": components.monitoring,
		"hostname": components.monitoring_name,
	        "resource": components.monitoring_resource,
	        "type": "monitoring" 
	}
	]
    
    # Serializing json 
    json_object = json.dumps(jsconfig, indent = 4)
  
    # Writing to sample.json
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)    
    
    # Vagrant up to create the machines 
    vagrantfilepath = os.path.join("config")
    v = vagrant.Vagrant(vagrantfilepath, quiet_stdout=False)
    v.up() # For creating an vb instance based on vagrantfile    
    
    
    
    # Connect to EC2
    ec2 = boto3.resource('ec2')
    
    # Connect to vbox
    vbox = virtualbox.VirtualBox()
    
# Get info into the database for each component accepted    
    if components.dashboard == True and components.dashboard_resource == "virtualbox":
        # Get the machine to receive the machine state and machine IPv4 and OS
        vm = vbox.find_machine(components.dashboard_name)
        dashboard_state = machineStates(vm.state).name
        
        time.sleep(30)
        dashboard_box = subprocess.run(["VBoxManage", "guestproperty", "get", components.dashboard_name, "/VirtualBox/HostInfo/VBoxVerExt"], capture_output=True, text=True).stdout
        dashboard_ip = subprocess.run(["VBoxManage", "guestproperty", "get", components.dashboard_name, "/VirtualBox/GuestInfo/Net/1/V4/IP"], capture_output=True, text=True).stdout
        dashboard_box = dashboard_box.split()
        dashboard_ip = dashboard_ip.split()
        dashboard_box = dashboard_box[1]
        dashboard_ip = dashboard_ip[1]
        
        #add the component into the database
        new_component_info = componentsInfo(username = _username, type = "dashboard", resource = components.dashboard_resource, hostname = components.dashboard_name, URL_access = dashboard_ip, state = dashboard_state)
        session.add(new_component_info)
        session.commit()
        session.refresh(new_component_info)
        
    elif components.dashboard == True and components.dashboard_resource == "aws":
        # Get the machine to receive the machine state and machine IPv4 and OS
        # Get information for specfic instance
        current_instances = ec2.instances.filter(Filters=[
          {"Name": "tag:Name",
           "Values":[components.dashboard_name]}])
        for instance in current_instances:
            for tag in instance.tags:
                if 'Name'in tag['Key']:
                   name = tag['Value']
            # Get the instance data
            dashboard_ip = instance.public_ip_address
            dashboard_storage = instance.instance_type
            dashboard_box = instance.platform_details
            dashboard_state = instance.state['Name']
               
        
        #add the component into the database
        new_component_info = componentsInfo(username = _username, type = "dashboard", resource = components.dashboard_resource, hostname = components.dashboard_name, URL_access = dashboard_ip, state = dashboard_state)
        session.add(new_component_info)
        session.commit()
        session.refresh(new_component_info)
        
        
        
        
    if components.webpage == True and components.webpage_resource == "virtualbox":
        
        # Get the machine to receive the machine state and machine IPv4 and OS
        vm = vbox.find_machine(components.webpage_name)
        webpage_state = machineStates(vm.state).name
        
        time.sleep(30)
        webpage_box = subprocess.run(["VBoxManage", "guestproperty", "get", components.webpage_name, "/VirtualBox/HostInfo/VBoxVerExt"], capture_output=True, text=True).stdout
        webpage_ip = subprocess.run(["VBoxManage", "guestproperty", "get", components.webpage_name, "/VirtualBox/GuestInfo/Net/1/V4/IP"], capture_output=True, text=True).stdout
        webpage_box = webpage_box.split()
        webpage_ip = webpage_ip.split()
        webpage_box = webpage_box[1]
        webpage_ip = webpage_ip[1]
        
        #add the component into the database
        new_component_info = componentsInfo(username = _username, type = "webpage", resource = components.webpage_resource, hostname = components.webpage_name, URL_access = webpage_ip, state = webpage_state)
        session.add(new_component_info)
        session.commit()
        session.refresh(new_component_info)
	        
    elif components.webpage == True and components.webpage_resource == "aws":
        # Get the machine to receive the machine state and machine IPv4 and OS
        # Get information for specfic instance
        current_instances = ec2.instances.filter(Filters=[
          {"Name": "tag:Name",
           "Values":[components.webpage_name]}])
        for instance in current_instances:
            for tag in instance.tags:
                if 'Name'in tag['Key']:
                   name = tag['Value']
            # Get the instance data
            webpage_ip = instance.public_ip_address
            webpage_storage = instance.instance_type
            webpage_box = instance.platform_details
            webpage_state = instance.state['Name']
               
        
        #add the component into the database
        new_component_info = componentsInfo(username = _username, type = "webpage", resource = components.webpage_resource, hostname = components.webpage_name, URL_access = webpage_ip, state = webpage_state)
        session.add(new_component_info)
        session.commit()
        session.refresh(new_component_info)
         
         
    if components.challenge == True and components.challenge_resource == "virtualbox":
        # Get the machine to receive the machine state and machine IPv4 and OS
        vm = vbox.find_machine(components.challenge_name)
        challenge_state = machineStates(vm.state).name
        
        time.sleep(30)
        challenge_box = subprocess.run(["VBoxManage", "guestproperty", "get", components.challenge_name, "/VirtualBox/HostInfo/VBoxVerExt"], capture_output=True, text=True).stdout
        challenge_ip = subprocess.run(["VBoxManage", "guestproperty", "get", components.challenge_name, "/VirtualBox/GuestInfo/Net/1/V4/IP"], capture_output=True, text=True).stdout
        challenge_box = challenge_box.split()
        challenge_ip = challenge_ip.split()
        challenge_box = challenge_box[1]
        challenge_ip = challenge_ip[1]
        
        #add the component into the database
        new_component_info = componentsInfo(username = _username, type = "challenge", resource = components.challenge_resource, hostname = components.challenge_name, URL_access = challenge_ip, state = challenge_state)
        session.add(new_component_info)
        session.commit()
        session.refresh(new_component_info)
        
        
    elif components.challenge == True and components.challenge_resource == "aws":
        # Get the machine to receive the machine state and machine IPv4 and OS
        # Get information for specfic instance
        current_instances = ec2.instances.filter(Filters=[
          {"Name": "tag:Name",
           "Values":[components.challenge_name]}])
        for instance in current_instances:
            for tag in instance.tags:
                if 'Name'in tag['Key']:
                   name = tag['Value']
            # Get the instance data
            challenge_ip = instance.public_ip_address
            challenge_storage = instance.instance_type
            challenge_box = instance.platform_details
            challenge_state = instance.state['Name']
               
        
        #add the component into the database
        new_component_info = componentsInfo(username = _username, type = "challenge", resource = components.challenge_resource, hostname = components.challenge_name, URL_access = challenge_ip, state = challenge_state)
        session.add(new_component_info)
        session.commit()
        session.refresh(new_component_info)
         

                
    if components.monitoring == True and components.monitoring_resource == "virtualbox":
        # Get the machine to receive the machine state and machine IPv4 and OS
        vm = vbox.find_machine(components.monitoring_name)
        monitoring_state = machineStates(vm.state).name
        
        time.sleep(30)
        monitoring_box = subprocess.run(["VBoxManage", "guestproperty", "get", components.monitoring_name, "/VirtualBox/HostInfo/VBoxVerExt"], capture_output=True, text=True).stdout
        monitoring_ip = subprocess.run(["VBoxManage", "guestproperty", "get", components.monitoring_name, "/VirtualBox/GuestInfo/Net/1/V4/IP"], capture_output=True, text=True).stdout
        monitoring_box = monitoring_box.split()
        monitoring_ip = monitoring_ip.split()
        monitoring_box = monitoring_box[1]
        monitoring_ip = monitoring_ip[1]
        
        #add the component into the database
        new_component_info = componentsInfo(username = _username, type = "monitoring", resource = components.monitoring_resource, hostname = components.monitoring_name, URL_access = monitoring_ip, state = monitoring_state)
        session.add(new_component_info)
        session.commit()
        session.refresh(new_component_info)
        
    elif components.monitoring == True and components.monitoring_resource == "aws":
        # Get the machine to receive the machine state and machine IPv4 and OS
        # Get information for specfic instance
        current_instances = ec2.instances.filter(Filters=[
          {"Name": "tag:Name",
           "Values":[components.monitoring_name]}])
        for instance in current_instances:
            for tag in instance.tags:
                if 'Name'in tag['Key']:
                   name = tag['Value']
            # Get the instance data
            monitoring_ip = instance.public_ip_address
            monitoring_storage = instance.instance_type
            monitoring_box = instance.platform_details
            monitoring_state = instance.state['Name']
               
        
        #add the component into the database
        new_component_info = componentsInfo(username = _username, type = "monitoring", resource = components.monitoring_resource, hostname = components.monitoring_name, URL_access = monitoring_ip, state = monitoring_state)
        session.add(new_component_info)
        session.commit()
        session.refresh(new_component_info)

    return {"message": "Provisoning Components"}


# Function to update details of the component
def update_component_info(session: Session, _username: str, _componentname: str, _getstate: str):
    component_info = get_component_info_by_component_id(session, _username, _componentname)

    if component_info is None:
        raise ComponentInfoNotFoundError
        
    # Connect to EC2
    ec2 = boto3.resource('ec2')
    
    # Connect to vbox
    vbox = virtualbox.VirtualBox()
        
    # Vb update for state 
    if component_info.resource == "virtualbox":
        # Check if stopping
        if _getstate == "stop":
            # Stop the vb machine
            subprocess.run(["VBoxManage", "controlvm", _componentname, "pause"], shell = False) # For stopping an vb instance
            # Get the machine to receive the new machine state
            vm = vbox.find_machine(_componentname)
            vbmachine_state = machineStates(vm.state).name
            component_info.state = vbmachine_state
            session.commit()
            session.refresh(component_info)
        
        # Check if starting
        elif _getstate == "start":
            #Start the vb machine
            subprocess.run(["VBoxManage", "controlvm", _componentname, "resume"], shell = False) # For starting an vb instance
            # Get the machine to receive the new machine state
            vm = vbox.find_machine(_componentname)
            vbmachine_state = machineStates(vm.state).name
            component_info.state = vbmachine_state
            session.commit()
            session.refresh(component_info)
           
    # Aws update for state
    elif component_info.resource == "aws":
        # Check if starting
        if _getstate == "stop":
            #Stop the aws machine
            ec2 = boto3.resource('ec2')
            ec2.instances.filter(Filters=[{
               "Name": "tag:Name",
               "Values": [_componentname]},
               ]).stop() # For halting an specfic ec2 instance
               
            time.sleep(40)   
            current_instances = ec2.instances.filter(Filters=[
              {"Name": "tag:Name",
               "Values":[_componentname]}])
            for instance in current_instances:
                for tag in instance.tags:
                    if 'Name'in tag['Key']:
                       name = tag['Value']
                # Get the instance state
                awsmachine_state = instance.state['Name']
            component_info.state = awsmachine_state
            session.commit()
            session.refresh(component_info)
            
        elif _getstate == "start":
            #Start the aws machine
            ec2 = boto3.resource('ec2')
            ec2.instances.filter(Filters=[{
               "Name": "tag:Name",
               "Values": [_componentname]},
               ]).start() # For starting an specfic ec2 instance
               
            time.sleep(40) 
            current_instances = ec2.instances.filter(Filters=[
              {"Name": "tag:Name",
               "Values":[_componentname]}])
            for instance in current_instances:
                for tag in instance.tags:
                    if 'Name'in tag['Key']:
                       name = tag['Value']
                # Get the instance state
                awsmachine_state = instance.state['Name']
            component_info.state = awsmachine_state
            session.commit()
            session.refresh(component_info)

    return component_info


# Function to delete a component info from the db
def delete_component_info(session: Session, _username: str, _componentname: str):
    component_info = get_component_info_by_component_id(session, _username, _componentname)

    if component_info is None:
        raise ComponentInfoNotFoundError
        
    # Connect to EC2
    ec2 = boto3.resource('ec2')
    
    # Connect to vbox
    vbox = virtualbox.VirtualBox()        
        
    # Delete for vb
    if component_info.resource == "virtualbox":
        vm = vbox.find_machine(_componentname)
        vm.remove(delete=True) # For destroying an vb instance
        session.delete(component_info)
        session.commit()
        message = {"message": "{} VB Instance Destroyed.".format(_componentname)}
    
    # Delete for aws
    elif component_info.resource == "aws":
        ec2.instances.filter(Filters=[{
           "Name": "tag:Name",
           "Values": [_componentname]}]).terminate() # For terminating an specfic ec2 instance
        session.delete(component_info)
        session.commit()
        message = {"message": "{} AWS Instance Destroyed.".format(_componentname)}

    return message
