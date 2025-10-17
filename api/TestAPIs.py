from fastapi import APIRouter,Request
from pydantic import BaseModel
import pyodbc

TestRouter = APIRouter(prefix='/test',tags=['测试'])

@TestRouter.get('/testSQL')
async def testSQL():
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=127.0.0.1;'
        'DATABASE=MyTEST;'
        'UID=sa;'
        'PWD=123456'
    )
    cursor = conn.cursor()

    sql = '''
        select 1 第一列, 'hello' 第二列
        union
        select 342,'hi'
        union 
        select 5645,'hey'
    '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    cols = [col[0] for col in cursor.description]
    cursor.close()
    conn.close()
    data = [dict(zip(cols,row)) for row in rows ]
    return {'code':0,'data':data}


    
@TestRouter.get('/getUserInfo')
async def getUserInfo(request:Request):
    if request.session.get('userid') is None:
        return {'code':1,'msg':'未登录'}
    return {
        'code':0,
        'userInfo':{
            'age':18,
            'gender':'男',
            'phone':'12345678910',
            'address':'中国'
        }
    }

@TestRouter.get('/autoLogin')
async def autoLogin(request:Request):
    if request.session.get('userid') is None:
        return {'code':1,'msg':'未登录'}
    else:
        return {'code':0,'msg':'已登录','nickname':'顶顶顶顶'}

@TestRouter.get('/logout')
async def logout(request:Request):
    if request.session.get('userid') is None:
        return {'code':1,'msg':'未登录'}
    else:
        request.session.clear()
        return {'code':0,'msg':'退出登录成功'}
