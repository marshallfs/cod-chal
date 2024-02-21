from fastapi import FastAPI, UploadFile, File, HTTPException
from sqlalchemy import create_engine
import pandas as pd
from typing import List
import uvicorn
import pymysql
import os

app = FastAPI()
engine = create_engine('mysql+pymysql://root:testroot@localhost/cod_chal')  # Cambia esto por tu base de datos

@app.get("/test")
async def test():   
    return {"message": "API activada"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    table_name = os.path.splitext(file.filename)[0]
    try:
        print(table_name)
        data = pd.read_csv(file.file,header=None)
        if table_name=='departments':
            print("Insercion de departamentos por archivo")            
            cols={data.columns[0]:'id',data.columns[1]:'department'}
            data = data.rename(columns=cols)
        elif table_name=='jobs':
            print("Insercion de trabajos por archivo")            
            cols={data.columns[0]:'id',data.columns[1]:'job'}
            data = data.rename(columns=cols)    
        elif table_name=='hired_employees':
            print("Insercion de empleados por archivo")            
            cols={data.columns[0]:'id',data.columns[1]:'name',data.columns[2]:'datetime',data.columns[3]:'department_id',data.columns[4]:'job_id'}
            data = data.rename(columns=cols)   
        data.to_sql(table_name, engine, if_exists='append', index=False)  # Cambia 'table_name' por el nombre de tu tabla        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Datos subidos con éxito para "+table_name}

@app.post("/batch_insert")
async def batch_insert(data: List[dict]):
    df = pd.DataFrame(data)
    table_name = os.path.splitext(file.filename)[0]
    df.to_sql(table_name, engine, if_exists='append', index=False)  # Cambia 'table_name' por el nombre de tu tabla
    return {"message": "Inserción por lotes exitosa"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
