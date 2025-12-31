from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from appserver.apps.account.endpoints import router as account_router
from appserver.apps.calendar.endpoints import router as calendar_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

def include_routers(_app: FastAPI):
    _app.include_router(account_router)
    _app.include_router(calendar_router)
    
    # /static 경로로 요청이 들어오면, StaticFIles 앱으로 처리
    _app.mount("/static", StaticFiles(directory="static"), name="static")
    # /uploads 경로로 요청이 들어오면, StaticFIles 앱으로 처리
    _app.mount("uploads", StaticFiles(directory="uploads"), name="uploads")

def init_middleware(_app: FastAPI):
    _app.add_middleware(
        CORSMiddleware,
        allow_orgins=["*"],
        allow_credentals=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

init_middleware(app)

