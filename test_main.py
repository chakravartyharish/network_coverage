from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Network Coverage API"}

def test_get_coverage_valid():
    response = client.get("/get_coverage?address=42+rue+du+Chemin+Vert+75011+Paris")
    assert response.status_code == 200
    expected_response ={
        "SFR":{"2G":True,"3G":True,"4G":True},
        "Orange":{"2G":True,"3G":True,"4G":True},
        "Bouygues":{"2G":True,"3G":True,"4G":True},
        "Free":{"2G":False,"3G":True,"4G":True}}
    assert response.json() == expected_response

def test_get_coverage_invalid():
    response = client.get("/get_coverage?address=Invalid Address")
    assert response.status_code == 404
    assert response.json() == {"detail": "Address not found"}
