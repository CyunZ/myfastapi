from fastapi import APIRouter,Request
from pydantic import BaseModel
import pyodbc
import DBTool
import bcrypt
import api.UserSQLs as UserSQLs

UserRouter = APIRouter(prefix='/user',tags=['用户'])



class SignUpInfo(BaseModel):
    username:str = ''
    pwd:str = ''
    nickname:str = ''

@UserRouter.post('/signup')
async def signup(request:Request, signupInfo : SignUpInfo):
    
    if signupInfo.username == '':
        return {'code':1,'msg':'用户名不能为空'}
    if signupInfo.pwd == '':
        return {'code':1,'msg':'密码不能为空'}
    if signupInfo.nickname == '':
        return {'code':1,'msg':'昵称不能为空'}

    rows,cols = DBTool.selectSQL(UserSQLs.selectUserByUsernameSQL,(signupInfo.username))
    if len(rows) > 0:
        return {'code':1,'msg':'该用户已注册'}
    
    hashPwd = bcrypt.hashpw(signupInfo.pwd.encode('utf-8'),bcrypt.gensalt())

    successFlag = DBTool.insertSQL(UserSQLs.insertUserSQL,(signupInfo.username,hashPwd,signupInfo.nickname))

    if successFlag:
        return  {'code':0,'msg':'注册成功'}
    else:
        return  {'code':1,'msg':'注册失败，请联系管理员'}

class LoginInfo(BaseModel):
    uname:str =''
    pwd:str = ''

@UserRouter.post('/login')
async def login(request:Request, loInfo : LoginInfo):
    if loInfo.uname == '':
        return {'code':1,'msg':'用户名不能为空'}
    if loInfo.pwd == '':
        return {'code':1,'msg':'密码不能为空'}
    

    rows,cols = DBTool.selectSQL(UserSQLs.selectLoginUserSQL,(loInfo.uname))
    if len(rows) == 0:
        return {'code':1,'msg':'用户名或密码错误'}
    row = rows[0]

    flag = bcrypt.checkpw(loInfo.pwd.encode('utf-8'),row[1])
    if flag:
        request.session['userid'] = row[0]
        return {'code':0,'msg':'登录成功','nickname':row[2]}

    return {'code':1,'msg':'用户名或密码错误'}