from fastapi import FastAPI, UploadFile, File
from sqlalchemy import create_engine
import pandas as pd
from typing import List
import uvicorn
import pymysql

app = FastAPI()
engine = create_engine('mysql+pymysql://root:testroot@localhost/cod_chal')  # Cambia esto por tu base de datos

@app.get("/test")
async def test():   
    return {"message": "API activada"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    data = pd.read_csv(file.file)
    data.to_sql('table_name', engine, if_exists='append')  # Cambia 'table_name' por el nombre de tu tabla
    return {"message": "Datos subidos con éxito"}

@app.post("/batch_insert")
async def batch_insert(data: List[dict]):
    df = pd.DataFrame(data)
    df.to_sql('table_name', engine, if_exists='append')  # Cambia 'table_name' por el nombre de tu tabla
    return {"message": "Inserción por lotes exitosa"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)