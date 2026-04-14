from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from api.TestAPIs import TestRouter
from starlette.middleware.sessions import SessionMiddleware
from api.HIS.ClinicAPIs import ClinicRouter
from api.UserAPIs import UserRouter
from loguru import logger
import sys
# from api.AIChatAPIs import AIChatRouter,loadAIModel
from contextlib import asynccontextmanager
from middlewares.LoginMiddleware import LoginMiddleware
from pydantic import BaseModel


@asynccontextmanager
async def lifespan(app:FastAPI):
    logger.remove()
    logger.add('mylogs/mylog{time:YYYY-MM-DD}.log',rotation='00:00')
    logger.add(sys.stderr)
    # loadAIModel()

    yield
    logger.info('项目关闭')


app = FastAPI(lifespan=lifespan)
# app.add_middleware(LoginMiddleware)
app.add_middleware(
    SessionMiddleware,
    secret_key='jio3424fdsfoijo',
    session_cookie = "goodcookie",
    max_age = 24*60*60,  
    same_site = "none",
    https_only = True,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True,
)





app.include_router(TestRouter)
app.include_router(ClinicRouter)
app.include_router(UserRouter)
# app.include_router(AIChatRouter)




@app.get('/')
async def root():
    logger.info('测试')
    return '你好'


@app.get('/test')
async def test():
    return '测试'


@app.get('/music')
async def music():
    return 'I am the storm that is approaching!'



class Something(BaseModel):
    what : str = ''

@app.post('/giveme')
async def giveme(some : Something):
    print('对方想要：'+ some.what)
    if some.what == 'Yamato':
        return 'If you want it,then you\'ll have to take it.'
    else :
        return 'OK'

if __name__ == '__main__':
    uvicorn.run('main:app',host='192.168.31.216',port=12345,reload=True)