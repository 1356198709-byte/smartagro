# 任务.py — 任务调度 API（主要代码）
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..数据库 import get_db
from ..模型 import Task
from ..模式 import TaskCreate, TaskUpdate, TaskOut
from ..工具 import tr

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

TASK_MAP = {"title": "title_ru", "description": "description_ru"}


@router.get("/", response_model=list[TaskOut])
def list_tasks(lang: str = Query("zh"), status: str = None, db: Session = Depends(get_db)):
    q = db.query(Task)
    if status:
        q = q.filter(Task.status == status)
    tasks = q.all()
    for t in tasks:
        tr(t, lang, TASK_MAP)
    return tasks


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, lang: str = Query("zh"), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    tr(task, lang, TASK_MAP)
    return task


@router.post("/", response_model=TaskOut)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    task = Task(**data.model_dump(), created_by=1)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, val in update_data.items():
        setattr(task, key, val)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Deleted"}
