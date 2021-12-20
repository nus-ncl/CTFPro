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
    ctfd: bool
    ctfd_type: str
    ctfd_name: str
    dashboard: bool
    dashboard_type: str
    dashboard_name: str
    landing_page: bool
    landing_page_type: str
    landing_page_name: str
    database: bool
    database_type: str
    database_name: str
      
