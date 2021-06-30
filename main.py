import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles

app = fastapi.FastAPI()

def configure_routing():
    app.mount('/static', StaticFiles(directory='static'), name='static')
    app.include_router(home.router)

def configure():
    configure_routing()

if __name__ == '__main__':
    configure()
    uvicorn.run(app)
else:
    configure()