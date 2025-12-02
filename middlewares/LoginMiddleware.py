from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger
from starlette.responses import JSONResponse

class LoginMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        logger.info('中间件接收到请求')
        if request.url.path in ['/user/login','/test','/']:
            response = await call_next(request)
            logger.info('中间件接收到答复')
            return response
        userid = request.session.get('userid')
        if userid is None:
            return JSONResponse(content={'code':999,'msg':'未登录或登录过期，请重新登录'})
        response = await call_next(request)
        logger.info('中间件接收到答复')
        return response