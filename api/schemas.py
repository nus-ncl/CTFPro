#schemas
from pydantic import BaseModel
from typing import Optional, List

    
# TO support creation and update APIs
class CreateAndUpdateComponent(BaseModel):
    type: str
    hostname: str
    URL_access: str
    username: str
    
# TO create components
class Creation(BaseModel):
    dashboard: bool
    dashboard_resource: str
    dashboard_name: str
    webpage: bool
    webpage_resource: str
    webpage_name: str
    challenge: bool
    challenge_resource: str
    challenge_name: str
    monitoring: bool
    monitoring_resource: str
    monitoring_name: str
