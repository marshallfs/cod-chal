from fastapi import FastAPI, UploadFile, File, HTTPException
from starlette.responses import FileResponse
from sqlalchemy import create_engine, text, select, func, and_
import pandas as pd
from typing import List
import uvicorn
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

app = FastAPI()
#engine = create_engine('mysql+pymysql://test_user:testuser@localhost/cod_chal')  # Conexion a Mysql
engine = create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')

@app.get("/test")
async def test():   #Funcion de prueba
    return {"message": "API activada"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    table_name = os.path.splitext(file.filename)[0]  #Obtener nombre de archivo, de ahi sale la tabla
    try:
        print(table_name)
        #Leemos el CSV
        df = pd.read_csv(file.file,header=None)
        #Elegimos a que tabla queremos insertar
        if table_name=='departments':
            print("Insercion de departamentos por archivo")            
            cols={df.columns[0]:'id',df.columns[1]:'department'} #Cambiamos nombre de columnas para que pueda ser leido por mysql
            df = df.rename(columns=cols)
        elif table_name=='jobs':
            print("Insercion de trabajos por archivo")            
            cols={df.columns[0]:'id',df.columns[1]:'job'} #Cambiamos nombre de columnas para que pueda ser leido por mysql
            df = df.rename(columns=cols)    
        elif table_name=='hired_employees':
            print("Insercion de empleados por archivo")            
            cols={df.columns[0]:'id',df.columns[1]:'name',df.columns[2]:'datetime',df.columns[3]:'department_id',df.columns[4]:'job_id'}                        
            df = df.rename(columns=cols) #Cambiamos nombre de columnas para que pueda ser leido por mysql, y ponemos la columna como datetime desde pandas
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
        #leemos el JSON que insertamos, la estructura es definida en el vinculo
        df = pd.DataFrame(data)
        #Elegimos a que tabla queremos insertar
        if table_destination=="departments":
            print("Insercion de departamentos por lotes")
            cols={df.columns[0]:'id',df.columns[1]:'department'} #Cambiamos nombre de columnas para que pueda ser leido por mysql
            df = df.rename(columns=cols)
        elif table_destination=="jobs":
            print("Insercion de trabajos por archivo")            
            cols={df.columns[0]:'id',df.columns[1]:'job'} #Cambiamos nombre de columnas para que pueda ser leido por mysql
            df = df.rename(columns=cols)    
            print("Insercion de trabajos por lotes")
        elif table_destination=="hired_employees":
            print("Insercion de empleados por lotes") 
            cols={df.columns[0]:'id',df.columns[1]:'name',df.columns[2]:'datetime',df.columns[3]:'department_id',df.columns[4]:'job_id'}                        
            df = df.rename(columns=cols) #Cambiamos nombre de columnas para que pueda ser leido por mysql, y ponemos la columna como datetime desde pandas
            df['datetime']=pd.to_datetime(df['datetime'])
        else:
            return {"message": "No corresponde a alguna tabla para completar"}
        df.to_sql(table_destination, engine, if_exists='append', index=False)  # Subir a tabla
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Inserción por lotes exitosa"}

#Para los endpoints de consulta, les hemos puesto el año como parametro para asegurar que puedan ser escogidos por el usuario

@app.get("/metrics1-json/{year}")
async def metrics1(year:int):
    #query a correr según requerimiento
    query = text("""
        SELECT d.department, j.job, QUARTER(e.datetime) as quarter, COUNT(*) as hires
        FROM hired_employees e
        JOIN departments d ON e.department_id = d.id
        JOIN jobs j ON e.job_id = j.id
        WHERE YEAR(e.datetime) = :year
        GROUP BY d.department, j.job, quarter
        ORDER BY d.department, j.job;
    """)
    #ejecutar query y emitir resultado como json
    with engine.connect() as connection:
        result = connection.execute(query, {"year":year})
        results_as_dict = result.mappings().all()        
        output = {}
        for row in results_as_dict:
            if row['department'] not in output:
                output[row['department']] = {}
            if row['job'] not in output[row['department']]:
                output[row['department']][row['job']] = {}
            output[row['department']][row['job']]['Q' + str(row['quarter'])] = row['hires']
        return output

@app.get("/metrics2-json/{year}")
async def metrics2(year:int):
    #query a correr según requerimiento
    query = text("""
        SELECT d.department, COUNT(*) as hires
        FROM hired_employees e
        JOIN departments d ON e.department_id = d.id
        WHERE YEAR(e.datetime) = :year
        GROUP BY d.department
        HAVING hires > (SELECT AVG(hires) FROM (SELECT COUNT(*) as hires FROM hired_employees WHERE YEAR(datetime) = :year GROUP BY department_id) as queryavg)
        ORDER BY hires DESC
    """)
    #ejecutar query y emitir resultado como json
    with engine.connect() as connection:
        result = connection.execute(query, {"year":year})
        results_as_dict = result.mappings().all()        
        output = {"year": year, "data": {}}
        for row in results_as_dict:
            output["data"][row['department']] = {'hires': row['hires']}
        return output
    
@app.get("/metrics1-tab/{year}")
async def metrics1(year:int):
    #query a correr según requerimiento
    query = text("""
        SELECT d.department, j.job, QUARTER(e.datetime) as quarter, COUNT(*) as hires
        FROM hired_employees e
        JOIN departments d ON e.department_id = d.id
        JOIN jobs j ON e.job_id = j.id
        WHERE YEAR(e.datetime) = :year
        GROUP BY d.department, j.job, quarter
        ORDER BY d.department, j.job;
    """)
    #ejecutar query y emitir resultado como csv
    with engine.connect() as connection:
        result = connection.execute(query, {"year":year})
        df = pd.DataFrame(result, columns=['Department', 'Job', 'Quarter', 'Hires'])        
        csv = df.to_csv('metrics1.csv',index=False)
        fr = FileResponse('metrics1.csv', media_type='text/csv', filename='metrics1.csv')         
        return fr   

@app.get("/metrics2-tab/{year}")
async def metrics2(year:int):
    #query a correr según requerimiento
    query = text("""
        SELECT d.department, COUNT(*) as hires
        FROM hired_employees e
        JOIN departments d ON e.department_id = d.id
        WHERE YEAR(e.datetime) = :year
        GROUP BY d.department
        HAVING hires > (SELECT AVG(hires) FROM (SELECT COUNT(*) as hires FROM hired_employees WHERE YEAR(datetime) = :year GROUP BY department_id) as queryavg)
        ORDER BY hires DESC
    """)
    #ejecutar query y emitir resultado como csv
    with engine.connect() as connection:
        result = connection.execute(query, {"year":year})
        df = pd.DataFrame(result, columns=['Department', 'Hires'])
        df.to_csv('metrics2.csv', index=False)
        fr = FileResponse('metrics2.csv', media_type='text/csv', filename='metrics2.csv')
        return fr
            

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, debug=True)