# 主要.py — FastAPI 主入口（主要代码）
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .数据库 import engine, Base
from .routers import 认证, 地块, 任务, 资源, 报告

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="智慧农业 API",
    description="农业综合信息管理系统",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 路由
app.include_router(认证.router)
app.include_router(地块.router)
app.include_router(任务.router)
app.include_router(资源.router)
app.include_router(报告.router)

# 前端静态文件
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "frontend", "dist")
if os.path.isdir(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{path:path}")
    async def serve_spa(path: str):
        file_path = os.path.join(frontend_dist, path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))

    @app.get("/")
    async def root_spa():
        return FileResponse(os.path.join(frontend_dist, "index.html"))
else:
    @app.get("/")
    def root():
        return {"message": "Frontend not built. Run: cd frontend && npm run build"}
