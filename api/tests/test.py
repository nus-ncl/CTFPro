from multiprocessing import Process

import pytest
import requests
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


def run_server():
    uvicorn.run(app)


@pytest.fixture 
def server():
    proc = Process(target=run_server, args=(), daemon=True)
    proc.start() 
    yield
    proc.kill() # Cleanup after testdef test_read_main(server):
    response = requests.get("http://localhost:8000/")
    assert response.status_code == 200 
    assert response.json() == {"msg": "Hello World"}
    
