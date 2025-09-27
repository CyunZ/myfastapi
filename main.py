from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from api.TestAPIs import TestRouter
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True,
)

app.add_middleware(
    SessionMiddleware,
    secret_key='jio3424fdsfoijo',
    session_cookie = "goodcookie",
    max_age = 24*60*60,  
    same_site = "none",
    https_only = True,
)

app.include_router(TestRouter)



@app.get('/')
async def root():
    return '你好'


@app.get('/test')
async def test():
    return '测试'

if __name__ == '__main__':
    uvicorn.run('main:app',host='127.0.0.1',port=12345,reload=True)