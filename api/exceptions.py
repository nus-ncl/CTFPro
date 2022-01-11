# exceptions.py
class ComponentInfoException(Exception):
    ...


class ComponentInfoNotFoundError(ComponentInfoException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Component Info Not Found"


class ComponentInfoAlreadyExistError(ComponentInfoException):
    def __init__(self):
        self.status_code = 409
        self.detail = "Component Info Already Exists"

class NoComponentsSelected(ComponentInfoException):
    def __init__(self):
        self.status_code = 400
        self.detail = "No Component Selected"
        
