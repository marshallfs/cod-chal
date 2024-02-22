from fastapi.testclient import TestClient
from coding_challenge_api import app
import requests
import csv
import io
import pandas as pd
import json
import pytest
import uvicorn
import httpx

client = TestClient(app)

def test_upload_file_departments():
    # Asegúrate de tener un archivo de prueba en el directorio correcto
    file_path = "departments.csv"
    with open(file_path, "rb") as f:
        response = client.post("/upload", files={"file": ("departments.csv", f, "text/csv")})
    assert response.status_code == 200
    assert response.json() == {"message": "Datos subidos con éxito para departments"}

def test_upload_file_jobs():
    # Asegúrate de tener un archivo de prueba en el directorio correcto
    file_path = "jobs.csv"
    with open(file_path, "rb") as f:
        response = client.post("/upload", files={"file": ("jobs.csv", f, "text/csv")})
    assert response.status_code == 200
    assert response.json() == {"message": "Datos subidos con éxito para jobs"}    

def test_upload_file_hired_employees():
    # Asegúrate de tener un archivo de prueba en el directorio correcto
    file_path = "hired_employees.csv"
    with open(file_path, "rb") as f:
        response = client.post("/upload", files={"file": ("hired_employees.csv", f, "text/csv")})
    assert response.status_code == 200
    assert response.json() == {"message": "Datos subidos con éxito para hired_employees"}        


@pytest.mark.parametrize("table_destination,data", [("departments", [{"id": 300, "department": "testdep"}])])
def test_batch_insert_departments(table_destination, data):
    response = client.post(f"/batch_insert/{table_destination}", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Inserción por lotes exitosa"}

@pytest.mark.parametrize("table_destination,data", [("jobs", [{"id": 300, "job": "testjob"}])])
def test_batch_insert_jobs(table_destination, data):
    response = client.post(f"/batch_insert/{table_destination}", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Inserción por lotes exitosa"}

@pytest.mark.parametrize("table_destination,data", [("hired_employees", [{"id": "3000", "name": "Prueba EmpleadoAuto", "datetime": "2023-01-02T13:00:05Z", "department_id": "300", "job_id": "300"}])])
def test_batch_insert_hired_employees(table_destination, data):
    response = client.post(f"/batch_insert/{table_destination}", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Inserción por lotes exitosa"}        
   

def test_metrics1_json():
    response = requests.get("http://localhost:8000/metrics1-json/2021")
    assert response.status_code == 200
    data = json.loads(response.content)    
    assert str(data["Accounting"]["Account Representative IV"]) == "{'Q1': 1}"
  
def test_metrics2_json():
    response = requests.get("http://localhost:8000/metrics2-json/2021")
    assert response.status_code == 200
    data = json.loads(response.content)    
    assert str(data["data"]["Business Development"]) == "{'hires': 187}"



def test_metrics1_tab():
    response = requests.get("http://localhost:8000/metrics1-tab/2021")
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/csv; charset=utf-8'
    content = response.content.decode('utf-8')
    cr = csv.reader(io.StringIO(content))
    data = list(cr)
    assert len(data) == 1378  # Reemplaza 'expected_rows' con el número esperado de filas

def test_metrics2_tab():
    response = requests.get("http://localhost:8000/metrics2-tab/2021")
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/csv; charset=utf-8'
    content = response.content.decode('utf-8')
    cr = csv.reader(io.StringIO(content))
    data = list(cr)
    assert len(data) == 8  # Reemplaza 'expected_rows' con el número esperado de filas