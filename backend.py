import os
from dotenv import load_dotenv
load_dotenv()
from db import database_conn
from logging_config import logger
from fastapi import FastAPI,HTTPException,status,Path
from pydantic import BaseModel,Field
from typing import TypedDict,Annotated,Optional
import pandas as pd
import psycopg2

app=FastAPI(title="Endpoint Series :")

@app.get('/')
def status():
    return "Fastapi Endpoint"


@app.get('/view')
def view():
    try:
        logger.info("View Api EndPoint Working :")
        query='Select * From "Rudra"."Employee_Agent"'
        data=pd.read_sql_query(sql=query,con=database_conn())

        if data.empty:
            return "Records Not Present"
        
        else:
            return data.to_dict(orient="records")
    
    except Exception as e:
        return f"Connection Failed {e}"



@app.get('/fetch/{id}')
def fetch(id:int=Path(...,description="Id of the employee",ge=1,example=[1,2,3])):
    query='Select "id" from "Rudra"."Employee_Agent"'
    data=pd.read_sql_query(sql=query,
                           con=database_conn())
    ids=data["id"].to_list()
    if id not in ids:
        raise HTTPException(status_code=404,
                            detail="Record Not Found")
    
    else:
        query='Select * From "Rudra"."Employee_Agent" Where "id"=%s'
        data=pd.read_sql_query(sql=query,
                               con=database_conn(),
                               params=(id,))
        return data.to_dict(orient="records")
    

class Emp(BaseModel):
    id:int=Field(description="Id Of The Employee",ge=1)
    name:str=None
    age:int=Field(description="Age of The Employee",ge=18)
    dept:str
    salary:float

@app.post('/insert')
def insert(insert:Emp):
    query='Select "id" From "Rudra"."Employee_Agent"'
    data=pd.read_sql_query(sql=query,
                           con=database_conn())
    ids=data["id"].to_list()

    if insert.id in ids:
        return f"Employee id {insert.id} is already exist"
    
    else:
        query="""
               insert into "Rudra"."Employee_Agent" values
               (%s,%s,%s,%s,%s)"""
        
        conn=database_conn()
        c=conn.cursor()
        c.execute(query,(insert.id,insert.name,insert.age,insert.dept,insert.salary))

        conn.commit()
        conn.close()

        raise HTTPException(status_code=201,
                            detail="Resource Created Succesfully :")
    

@app.delete('/delete/{id}')
def delete(id:int=Path(...,title="Id Of The Employee",ge=1,example=[1,2,3])):
    query='Select "id" from "Rudra"."Employee_Agent"'
    data=pd.read_sql_query(sql=query,
                           con=database_conn())
    ids=data["id"].to_list()
    if id not in ids:
        raise HTTPException(status_code=404,
                            detail="Record Not Present")
    
    else:
        query='Delete From "Rudra"."Employee_Agent" Where "id"=%s'
        conn=database_conn()
        c=conn.cursor()
        c.execute(query,(id,))
        conn.commit()
        conn.close()

        raise HTTPException(status_code=204,
                            detail="Id Deleted Succesfully :")

class update(BaseModel):
   
   name: Optional[str] = None
   age: Optional[int] = None
   dept: Optional[str] = None
   salary: Optional[float] = None


@app.put('/update/{id}')
def update(update:update,id:int=Path(...,title="id of the employee to update",ge=1)):

    query='Select "id" From "Rudra"."Employee_Agent"'
    data=pd.read_sql_query(sql=query,
                           con=database_conn())
    ids=data["id"].to_list()
    if id not in ids:
        raise HTTPException(status_code=404,
                            detail="Records Not Found")
    

    conn = database_conn()
    cur = conn.cursor()

    fields = []
    values = []

    if update.name is not None:
        fields.append('"name"=%s')
        values.append(update.name)

    if update.age is not None:
        fields.append('"age"=%s')
        values.append(update.age)

    if update.dept is not None:
        fields.append('"dept"=%s')
        values.append(update.dept)

    if update.salary is not None:
        fields.append('"salary"=%s')
        values.append(update.salary)

    values.append(id)

    query = f'''
        UPDATE "Rudra"."Employee_Agent"
        SET {", ".join(fields)}
        WHERE "id"=%s
'''

    cur.execute(query, values)
    conn.commit()

    conn.close()

    return "updated succesfully"