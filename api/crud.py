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
def create_component(session: Session, _username: str, components: Creation) -> componentsInfo:    ##################################################
    
    
# Check for no component selected    
    if components.ctfd == False and components.dashboard == False and components.landing_page == False and components.database == False:
        raise NoComponentsSelected
    

#Check if the names are in the database or not if yes go error, no then cont. 
    if components.ctfd == True:
        component_details = session.query(componentsInfo).filter( componentsInfo.hostname == components.ctfd_name, componentsInfo.username == _username).first()
        if component_details is not None:
            raise ComponentInfoAlreadyExistError

    if components.dashboard == True:
        component_details = session.query(componentsInfo).filter( componentsInfo.hostname == components.dashboard_name, componentsInfo.username == _username).first()
        if component_details is not None:
            raise ComponentInfoAlreadyExistError

    if components.landing_page == True:
        component_details = session.query(componentsInfo).filter( componentsInfo.hostname == components.landing_page_name, componentsInfo.username == _username).first()
        if component_details is not None:
            raise ComponentInfoAlreadyExistError

    if components.database == True:
        component_details = session.query(componentsInfo).filter( componentsInfo.hostname == components.database_name, componentsInfo.username == _username).first()
        if component_details is not None:
            raise ComponentInfoAlreadyExistError
        
# Create the json file for vagrantfile
    jsconfig = [ 
	{
		"provision": components.ctfd,
		"hostname": components.ctfd_name,
		"type": components.ctfd_type
	},
	{
		"provision": components.dashboard,
		"hostname": components.dashboard_name,
		"type": components.dashboard_type
	},
	{
		"provision": components.landing_page,
		"hostname": components.landing_page_name,
		"type": components.landing_page_type
	},
	{
		"provision": components.database,
		"hostname": components.database_name,
	        "type": components.database_type
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
    if components.ctfd == True and components.ctfd_type == "virtualbox":
        # Get the machine to receive the machine state and machine IPv4 and OS
        vm = vbox.find_machine(components.ctfd_name)
        ctfd_state = machineStates(vm.state).name
        
        ctfd_box = subprocess.run(["VBoxManage", "guestproperty", "get", components.ctfd_name, "/VirtualBox/HostInfo/VBoxVerExt"], capture_output=True, text=True).stdout
        ctfd_ip = subprocess.run(["VBoxManage", "guestproperty", "get", components.ctfd_name, "/VirtualBox/GuestInfo/Net/1/V4/Broadcast"], capture_output=True, text=True).stdout
        ctfd_box = ctfd_box.split()
        ctfd_ip = ctfd_ip.split()
        ctfd_box = ctfd_box[1]
        ctfd_ip = ctfd_ip[1]
        
        #add the component into the database
        new_component_info = componentsInfo(username = _username, type = components.ctfd_type, hostname = components.ctfd_name, URL_access = ctfd_ip, state = ctfd_state)
        session.add(new_component_info)
        session.commit()
        session.refresh(new_component_info)
        
    elif components.ctfd == True and components.ctfd_type == "aws":
        # Get the machine to receive the machine state and machine IPv4 and OS
        # Get information for specfic instance
        current_instances = ec2.instances.filter(Filters=[
          {"Name": "tag:Name",
           "Values":[components.ctfd_name]}])
        for instance in current_instances:
            for tag in instance.tags:
                if 'Name'in tag['Key']:
                   name = tag['Value']
            # Get the instance data
            ctfd_ip = instance.public_ip_address
            ctfd_storage = instance.instance_type
            ctfd_box = instance.platform_details
            ctfd_state = instance.state['Name']
               
        
        #add the component into the database
        new_component_info = componentsInfo(username = _username, type = components.ctfd_type, hostname = components.ctfd_name, URL_access = ctfd_ip, state = ctfd_state)
        session.add(new_component_info)
        session.commit()
        session.refresh(new_component_info)
        
        
        
        
    if components.dashboard == True and components.dashboard_type == "virtualbox":
        
        # Get the machine to receive the machine state and machine IPv4 and OS
        vm = vbox.find_machine(components.dashboard_name)
        dashboard_state = machineStates(vm.state).name
        
        dashboard_box = subprocess.run(["VBoxManage", "guestproperty", "get", components.dashboard_name, "/VirtualBox/HostInfo/VBoxVerExt"], capture_output=True, text=True).stdout
        dashboard_ip = subprocess.run(["VBoxManage", "guestproperty", "get", components.dashboard_name, "/VirtualBox/GuestInfo/Net/1/V4/Broadcast"], capture_output=True, text=True).stdout
        dashboard_box = dashboard_box.split()
        dashboard_ip = dashboard_ip.split()
        dashboard_box = dashboard_box[1]
        dashboard_ip = dashboard_ip[1]
        
        #add the component into the database
        new_component_info = componentsInfo(username = _username, type = components.dashboard_type, hostname = components.dashboard_name, URL_access = dashboard_ip, state = dashboard_state)
        session.add(new_component_info)
        session.commit()
        session.refresh(new_component_info)
	        
    elif components.dashboard == True and components.dashboard_type == "aws":
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
        new_component_info = componentsInfo(username = _username, type = components.dashboard_type, hostname = components.dashboard_name, URL_access = dashboard_ip, state = dashboard_state)
        session.add(new_component_info)
        session.commit()
        session.refresh(new_component_info)
         
         
    if components.landing_page == True and components.landing_page_type == "virtualbox":
        # Get the machine to receive the machine state and machine IPv4 and OS
        vm = vbox.find_machine(components.landing_page_name)
        landing_page_state = machineStates(vm.state).name
        
        landing_page_box = subprocess.run(["VBoxManage", "guestproperty", "get", components.landing_page_name, "/VirtualBox/HostInfo/VBoxVerExt"], capture_output=True, text=True).stdout
        landing_page_ip = subprocess.run(["VBoxManage", "guestproperty", "get", components.landing_page_name, "/VirtualBox/GuestInfo/Net/1/V4/Broadcast"], capture_output=True, text=True).stdout
        landing_page_box = landing_page_box.split()
        landing_page_ip = landing_page_ip.split()
        landing_page_box = landing_page_box[1]
        landing_page_ip = landing_page_ip[1]
        
        #add the component into the database
        new_component_info = componentsInfo(username = _username, type = components.landing_page_type, hostname = components.landing_page_name, URL_access = landing_page_ip, state = landing_page_state)
        session.add(new_component_info)
        session.commit()
        session.refresh(new_component_info)
        
        
    elif components.landing_page == True and components.landng_page_type == "aws":
        # Get the machine to receive the machine state and machine IPv4 and OS
        # Get information for specfic instance
        current_instances = ec2.instances.filter(Filters=[
          {"Name": "tag:Name",
           "Values":[components.landing_page_name]}])
        for instance in current_instances:
            for tag in instance.tags:
                if 'Name'in tag['Key']:
                   name = tag['Value']
            # Get the instance data
            landing_page_ip = instance.public_ip_address
            landing_page_storage = instance.instance_type
            landing_page_box = instance.platform_details
            landing_page_state = instance.state['Name']
               
        
        #add the component into the database
        new_component_info = componentsInfo(username = _username, type = components.landing_page_type, hostname = components.landing_page_name, URL_access = landing_page_ip, state = landing_page_state)
        session.add(new_component_info)
        session.commit()
        session.refresh(new_component_info)
         

                
    if components.database == True and components.database_type == "virtualbox":
        # Get the machine to receive the machine state and machine IPv4 and OS
        vm = vbox.find_machine(components.database_name)
        database_state = machineStates(vm.state).name
        
        database_box = subprocess.run(["VBoxManage", "guestproperty", "get", components.database_name, "/VirtualBox/HostInfo/VBoxVerExt"], capture_output=True, text=True).stdout
        database_ip = subprocess.run(["VBoxManage", "guestproperty", "get", components.database_name, "/VirtualBox/GuestInfo/Net/1/V4/Broadcast"], capture_output=True, text=True).stdout
        database_box = database_box.split()
        database_ip = database_ip.split()
        database_box = database_box[1]
        database_ip = database_ip[1]
        
        #add the component into the database
        new_component_info = componentsInfo(username = _username, type = components.database_type, hostname = components.database_name, URL_access = database_ip, state = database_state)
        session.add(new_component_info)
        session.commit()
        session.refresh(new_component_info)
        
    elif components.database == True and components.database_type == "aws":
        # Get the machine to receive the machine state and machine IPv4 and OS
        # Get information for specfic instance
        current_instances = ec2.instances.filter(Filters=[
          {"Name": "tag:Name",
           "Values":[components.database_name]}])
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
        new_component_info = componentsInfo(username = _username, type = components.dashboard_type, hostname = components.dashboard_name, URL_access = dashboard_ip, state = database_state)
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
    if component_info.type == "virtualbox":
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
    elif component_info.type == "aws":
        # Check if starting
        if _getstate == "stop":
            #Stop the aws machine
            ec2 = boto3.resource('ec2')
            ec2.instances.filter(Filters=[{
               "Name": "tag:Name",
               "Values": [_componentname]},
               ]).stop() # For halting an specfic ec2 instance
               
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
    if component_info.type == "virtualbox":
        vm = vbox.find_machine(_componentname)
        vm.remove(delete=True) # For destroying an vb instance
        session.delete(component_info)
        session.commit()
        message = {"message": "{} VB Instance Destroyed.".format(_componentname)}
    
    # Delete for aws
    elif component_info.type == "aws":
        ec2.instances.filter(Filters=[{
           "Name": "tag:Name",
           "Values": [_componentname]}]).terminate() # For terminating an specfic ec2 instance
        session.delete(component_info)
        session.commit()
        message = {"message": "{} AWS Instance Destroyed.".format(_componentname)}

    return message
  
