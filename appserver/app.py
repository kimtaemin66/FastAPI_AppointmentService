from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from appserver.apps.account.endpoints import router as account_router
from appserver.apps.calendar.endpoints import router as calendar_router
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine
from sqladmin import Admin
from .db import engine
from appserver.admin import include_admin_views

app = FastAPI()

def include_routers(_app: FastAPI):
    _app.include_router(account_router)
    _app.include_router(calendar_router)

include_routers(app)

def init_admin(_app: FastAPI, _engine: AsyncEngine):
    return Admin(_app, _engine)

admin = init_admin(app, engine)
include_admin_views(admin)
    
#     # /static 경로로 요청이 들어오면, StaticFIles 앱으로 처리
#     _app.mount("/static", StaticFiles(directory="static"), name="static")
#     # /uploads 경로로 요청이 들어오면, StaticFIles 앱으로 처리
#     _app.mount("uploads", StaticFiles(directory="uploads"), name="uploads")

# def init_middleware(_app: FastAPI):
#     _app.add_middleware(
#         CORSMiddleware,
#         allow_origins=["*"],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )

# init_middleware(app)