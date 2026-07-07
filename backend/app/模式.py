# 模式.py — Pydantic 请求/响应模型（主要代码）
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ---------- 认证 ----------
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: str = "field_staff"


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut


class LoginRequest(BaseModel):
    username: str
    password: str


# ---------- 地块 ----------
class LandPlotCreate(BaseModel):
    cadastral_number: str
    name: str
    name_ru: Optional[str] = None
    area_ha: float
    soil_type: Optional[str] = None
    soil_type_ru: Optional[str] = None
    geometry: Optional[str] = None  # GeoJSON


class LandPlotUpdate(BaseModel):
    name: Optional[str] = None
    name_ru: Optional[str] = None
    area_ha: Optional[float] = None
    soil_type: Optional[str] = None
    soil_type_ru: Optional[str] = None
    geometry: Optional[str] = None
    status: Optional[str] = None


class LandPlotOut(BaseModel):
    id: int
    cadastral_number: str
    name: str
    area_ha: float
    soil_type: Optional[str] = None
    geometry: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ---------- 轮作 ----------
class CropRotationCreate(BaseModel):
    land_plot_id: int
    crop_name: str
    crop_name_ru: Optional[str] = None
    sowing_date: datetime
    harvest_date: Optional[datetime] = None
    yield_amount: Optional[float] = None
    notes: Optional[str] = None
    notes_ru: Optional[str] = None


class CropRotationOut(BaseModel):
    id: int
    land_plot_id: int
    crop_name: str
    sowing_date: datetime
    harvest_date: Optional[datetime] = None
    yield_amount: Optional[float] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


# ---------- 任务 ----------
class TaskCreate(BaseModel):
    title: str
    title_ru: Optional[str] = None
    description: Optional[str] = None
    description_ru: Optional[str] = None
    task_type: str = "other"
    land_plot_id: int
    assigned_to: Optional[int] = None
    planned_start: datetime
    planned_end: datetime
    priority: int = 1


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    title_ru: Optional[str] = None
    description: Optional[str] = None
    description_ru: Optional[str] = None
    task_type: Optional[str] = None
    assigned_to: Optional[int] = None
    planned_start: Optional[datetime] = None
    planned_end: Optional[datetime] = None
    status: Optional[str] = None
    priority: Optional[int] = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    task_type: str
    land_plot_id: int
    assigned_to: Optional[int] = None
    created_by: Optional[int] = None
    planned_start: datetime
    planned_end: datetime
    status: str
    priority: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ---------- 资源 ----------
class ResourceCreate(BaseModel):
    name: str
    name_ru: Optional[str] = None
    resource_type: str = "other"
    unit: str
    unit_ru: Optional[str] = None
    quantity: float = 0.0
    min_threshold: float = 0.0
    price_per_unit: float = 0.0
    supplier: Optional[str] = None
    supplier_ru: Optional[str] = None


class ResourceUpdate(BaseModel):
    name: Optional[str] = None
    name_ru: Optional[str] = None
    resource_type: Optional[str] = None
    unit: Optional[str] = None
    unit_ru: Optional[str] = None
    quantity: Optional[float] = None
    min_threshold: Optional[float] = None
    price_per_unit: Optional[float] = None
    supplier: Optional[str] = None
    supplier_ru: Optional[str] = None


class ResourceOut(BaseModel):
    id: int
    name: str
    resource_type: str
    unit: str
    quantity: float
    min_threshold: float
    price_per_unit: float
    supplier: Optional[str] = None

    class Config:
        from_attributes = True


# ---------- 物资消耗 ----------
class MaterialConsumptionCreate(BaseModel):
    task_id: int
    resource_id: int
    land_plot_id: int
    quantity_used: float
    notes: Optional[str] = None


class MaterialConsumptionOut(BaseModel):
    id: int
    task_id: int
    resource_id: int
    land_plot_id: int
    quantity_used: float
    used_at: Optional[datetime] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


# ---------- 工作报告 ----------
class WorkReportCreate(BaseModel):
    task_id: int
    progress_percent: float = 0.0
    report_text: Optional[str] = None
    report_text_ru: Optional[str] = None
    geo_latitude: Optional[float] = None
    geo_longitude: Optional[float] = None
    offline_synced: int = 0


class WorkReportOut(BaseModel):
    id: int
    task_id: int
    worker_id: int
    progress_percent: float
    report_text: Optional[str] = None
    geo_latitude: Optional[float] = None
    geo_longitude: Optional[float] = None
    reported_at: Optional[datetime] = None
    offline_synced: int = 0

    class Config:
        from_attributes = True


# ---------- 分析报告 ----------
class AnalyticsSummary(BaseModel):
    total_land_area: float
    total_plots: int
    active_tasks: int
    completed_tasks: int
    total_resources_value: float
    low_stock_resources: int
