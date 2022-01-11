# api.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from crud import get_all_components, get_component_info_by_component_id, create_component, update_component_info, delete_component_info
from database import get_db
from exceptions import ComponentInfoException
from schemas import CreateAndUpdateComponent, Creation

from fastapi import FastAPI

router = APIRouter()

@router.get("/list/{username}")
def list_components(username: str, session: Session = Depends(get_db)):

    try:
        components_list = get_all_components(session, username)
        return components_list
    except ComponentInfoException as cie:
        raise HTTPException(**cie.__dict__)

# API endpoint to create an particular component
@router.post("/create")
def add_component(username: str,components: Creation, session: Session = Depends(get_db)):        

    try:
        component_info = create_component(session, username, components)
        return component_info
    except ComponentInfoException as cie:
        raise HTTPException(**cie.__dict__)
        
# API endpoint to get info of a particular component
@router.get("/{username}/{component_name}")
def get_component_info(username: str, component_name: str, session: Session = Depends(get_db)):

    try:
        component_info = get_component_info_by_component_id(session, username, component_name)
        return component_info
    except ComponentInfoException as cie:
        raise HTTPException(**cie.__dict__)


# API to update a existing component info after stopping or starting the component
@router.put("/{username}/{component_name}/{cur_state}")
def update_component(username: str, component_name: str, get_state: str, session: Session = Depends(get_db)):

    try:
        component_info = update_component_info(session, username, component_name, get_state)
        return component_info
    except ComponentInfoException as cie:
        raise HTTPException(**cie.__dict__)


# API to delete a component info from the data base and the component
@router.delete("/{username}/{component_name}")
def delete_component(username: str, component_name: str, session: Session = Depends(get_db)):

    try:
        messageb = delete_component_info(session, username, component_name)
        return messageb
    except ComponentInfoException as cie:
        raise HTTPException(**cie.__dict__)
        
