from fastapi.testclient import TestClient
import sys
sys.path.append("../")
from main import app

client = TestClient(app)

def test_get_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'message': 'Welcome to CTFPro'}