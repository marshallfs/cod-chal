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
        df = pd.read_csv(file.file,header=None)
        if table_name=='departments':
            print("Insercion de departamentos por archivo")            
            cols={df.columns[0]:'id',df.columns[1]:'department'}
            df = df.rename(columns=cols)
        elif table_name=='jobs':
            print("Insercion de trabajos por archivo")            
            cols={df.columns[0]:'id',df.columns[1]:'job'}
            df = df.rename(columns=cols)    
        elif table_name=='hired_employees':
            print("Insercion de empleados por archivo")            
            cols={df.columns[0]:'id',df.columns[1]:'name',df.columns[2]:'datetime',df.columns[3]:'department_id',df.columns[4]:'job_id'}                        
            df = df.rename(columns=cols)
            df['datetime']=pd.to_datetime(df['datetime'])
        else:
            return {"message": "No corresponde a algun archivo indicado"}
        df.to_sql(table_name, engine, if_exists='append', index=False)  # Subir a tabla  
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Datos subidos con éxito para "+table_name}

@app.post("/batch_insert/{table_destination}")
async def batch_insert(data: List[dict], table_destination: str):
    try:
        df = pd.DataFrame(data)
        if table_destination=="departments":
            print("Insercion de departamentos por lotes")
            cols={df.columns[0]:'id',df.columns[1]:'department'}
            df = df.rename(columns=cols)
        elif table_destination=="jobs":
            print("Insercion de trabajos por archivo")            
            cols={df.columns[0]:'id',df.columns[1]:'job'}
            df = df.rename(columns=cols)    
            print("Insercion de trabajos por lotes")
        elif table_destination=="hired_employees":
            print("Insercion de empleados por lotes") 
            cols={df.columns[0]:'id',df.columns[1]:'name',df.columns[2]:'datetime',df.columns[3]:'department_id',df.columns[4]:'job_id'}                        
            df = df.rename(columns=cols)
            df['datetime']=pd.to_datetime(df['datetime'])
        else:
            return {"message": "No corresponde a alguna tabla para completar"}
        df.to_sql(table_destination, engine, if_exists='append', index=False)  # Subir a tabla
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Inserción por lotes exitosa"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
