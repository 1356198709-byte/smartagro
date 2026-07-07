# 模型.py — 数据库表结构（主要代码）
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .数据库 import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    DISPATCHER = "dispatcher"
    FIELD_STAFF = "field_staff"
    STOREKEEPER = "storekeeper"


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskType(str, enum.Enum):
    PLOWING = "plowing"
    SOWING = "sowing"
    HARVESTING = "harvesting"
    FERTILIZING = "fertilizing"
    IRRIGATION = "irrigation"
    OTHER = "other"


class ResourceType(str, enum.Enum):
    SEEDS = "seeds"
    FERTILIZER = "fertilizer"
    FUEL = "fuel"
    PESTICIDE = "pesticide"
    OTHER = "other"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    full_name = Column(String(100))
    phone = Column(String(30))
    role = Column(String(20), default=UserRole.FIELD_STAFF.value)
    created_at = Column(DateTime, default=datetime.utcnow)

    tasks = relationship("Task", foreign_keys="Task.assigned_to", back_populates="assignee")
    work_reports = relationship("WorkReport", back_populates="worker")


class LandPlot(Base):
    __tablename__ = "land_plots"

    id = Column(Integer, primary_key=True, index=True)
    cadastral_number = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    name_ru = Column(String(100))
    area_ha = Column(Float, nullable=False)
    soil_type = Column(String(100))
    soil_type_ru = Column(String(100))
    geometry = Column(Text)
    hash_sum = Column(String(64))
    status = Column(String(20), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    crop_rotations = relationship("CropRotation", back_populates="land_plot")
    tasks = relationship("Task", back_populates="land_plot")
    material_consumptions = relationship("MaterialConsumption", back_populates="land_plot")


class CropRotation(Base):
    __tablename__ = "crop_rotation"

    id = Column(Integer, primary_key=True, index=True)
    land_plot_id = Column(Integer, ForeignKey("land_plots.id"), nullable=False)
    crop_name = Column(String(100), nullable=False)
    crop_name_ru = Column(String(100))
    sowing_date = Column(DateTime, nullable=False)
    harvest_date = Column(DateTime)
    yield_amount = Column(Float)
    notes = Column(Text)
    notes_ru = Column(Text)

    land_plot = relationship("LandPlot", back_populates="crop_rotations")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    title_ru = Column(String(200))
    description = Column(Text)
    description_ru = Column(Text)
    task_type = Column(String(30), default=TaskType.OTHER.value)
    land_plot_id = Column(Integer, ForeignKey("land_plots.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"))
    created_by = Column(Integer, ForeignKey("users.id"))
    planned_start = Column(DateTime, nullable=False)
    planned_end = Column(DateTime, nullable=False)
    status = Column(String(20), default=TaskStatus.PENDING.value)
    priority = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    land_plot = relationship("LandPlot", back_populates="tasks")
    assignee = relationship("User", foreign_keys=[assigned_to], back_populates="tasks")
    material_consumptions = relationship("MaterialConsumption", back_populates="task")
    work_reports = relationship("WorkReport", back_populates="task")


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    name_ru = Column(String(100))
    resource_type = Column(String(30), default=ResourceType.OTHER.value)
    unit = Column(String(20), nullable=False)
    unit_ru = Column(String(20))
    quantity = Column(Float, default=0.0)
    min_threshold = Column(Float, default=0.0)
    price_per_unit = Column(Float, default=0.0)
    supplier = Column(String(100))
    supplier_ru = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    material_consumptions = relationship("MaterialConsumption", back_populates="resource")


class MaterialConsumption(Base):
    __tablename__ = "material_consumption"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    land_plot_id = Column(Integer, ForeignKey("land_plots.id"), nullable=False)
    quantity_used = Column(Float, nullable=False)
    used_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)

    task = relationship("Task", back_populates="material_consumptions")
    resource = relationship("Resource", back_populates="material_consumptions")
    land_plot = relationship("LandPlot", back_populates="material_consumptions")


class WorkReport(Base):
    __tablename__ = "work_reports"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    worker_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    progress_percent = Column(Float, default=0.0)
    report_text = Column(Text)
    report_text_ru = Column(Text)
    geo_latitude = Column(Float)
    geo_longitude = Column(Float)
    reported_at = Column(DateTime, default=datetime.utcnow)
    offline_synced = Column(Integer, default=0)

    task = relationship("Task", back_populates="work_reports")
    worker = relationship("User", back_populates="work_reports")
