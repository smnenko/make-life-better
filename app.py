import uvicorn
from fastapi import FastAPI

from routers import user_router, money_router

app = FastAPI(debug=True)

app.include_router(user_router.router)
app.include_router(money_router.router)


if __name__ == '__main__':
    uvicorn.run(
        'app:app',
        host='0.0.0.0',
        port=8000,
        use_colors=True,
        reload=True
    )
