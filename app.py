import uvicorn
from fastapi import FastAPI

from views import user, money, calorie

app = FastAPI(debug=True)

app.include_router(user.router)
app.include_router(money.router)
app.include_router(calorie.router)


if __name__ == '__main__':
    uvicorn.run(
        'app:app',
        host='0.0.0.0',
        port=8000,
        use_colors=True,
        reload=True
    )
