from fastapi import APIRouter,Request
from pydantic import BaseModel
import pyodbc
import api.HIS.ClinicSQLs as ClinicSQLs
import DBTool 

ClinicRouter = APIRouter(prefix='/clinic',tags=['门诊'])

@ClinicRouter.get('/getHouZhenList')
async def getHouZhenList():
    rows,cols = DBTool.selectSQL(ClinicSQLs.getHouZhenListSQL)
    if len(rows) == 0:
        return {'code': 1,'msg':'没有找到数据'}
    
    data = [dict(zip(cols,row)) for row in rows ]
    return {'code':0,'data':data}