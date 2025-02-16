from fastapi import FastAPI
import uvicorn
from settings import WEB_PORT
from controller import chat_router, auth_router

app = FastAPI()

# include all the required routes
app.include_router(chat_router)
app.include_router(auth_router)


# ping endpoint
@app.get('/ping')
def print_hi():
    return {"result": "ok"}


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=WEB_PORT, reload=True, use_colors=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
