import requests
import csv
import io
import pandas as pd
import json

def test_metrics1_json():
    response = requests.get("http://localhost:8000/metrics1-json/2021")
    assert response.status_code == 200
    data = json.loads(response.content)    
    assert str(data["Accounting"]["Account Representative IV"]) == "{'Q1': 1}"
    #assert "Accounting" in response.json()
    #assert "Programming Analyst IV" in response.json()
    
    
    

def test_metrics2_json():
    response = requests.get("http://localhost:8000/metrics2-json/2021")
    assert response.status_code == 200
    data = json.loads(response.content)
    print(data)
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