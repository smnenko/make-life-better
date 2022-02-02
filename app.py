import uvicorn
from fastapi import FastAPI

from views import auth, user, money, calorie

app = FastAPI(debug=True)

app.include_router(router=auth.router, prefix='/api/v1')
app.include_router(router=user.router, prefix='/api/v1')
app.include_router(router=money.router, prefix='/api/v1')
app.include_router(router=calorie.router, prefix='/api/v1')


if __name__ == '__main__':
    uvicorn.run(
        'app:app',
        host='0.0.0.0',
        port=8000,
        use_colors=True,
        reload=True
    )
