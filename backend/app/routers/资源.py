# 资源.py — 资源与消耗管理 API（主要代码）
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..数据库 import get_db
from ..模型 import Resource, MaterialConsumption
from ..模式 import (
    ResourceCreate, ResourceUpdate, ResourceOut,
    MaterialConsumptionCreate, MaterialConsumptionOut,
)
from ..工具 import tr

router = APIRouter(prefix="/api/resources", tags=["resources"])

RES_MAP = {"name": "name_ru", "unit": "unit_ru", "supplier": "supplier_ru"}


@router.get("/", response_model=list[ResourceOut])
def list_resources(lang: str = Query("zh"), db: Session = Depends(get_db)):
    resources = db.query(Resource).all()
    for r in resources:
        tr(r, lang, RES_MAP)
    return resources


@router.get("/low-stock", response_model=list[ResourceOut])
def low_stock_resources(lang: str = Query("zh"), db: Session = Depends(get_db)):
    resources = db.query(Resource).filter(Resource.quantity <= Resource.min_threshold).all()
    for r in resources:
        tr(r, lang, RES_MAP)
    return resources


@router.post("/", response_model=ResourceOut)
def create_resource(data: ResourceCreate, db: Session = Depends(get_db)):
    res = Resource(**data.model_dump())
    db.add(res)
    db.commit()
    db.refresh(res)
    return res


@router.put("/{resource_id}", response_model=ResourceOut)
def update_resource(resource_id: int, data: ResourceUpdate, db: Session = Depends(get_db)):
    res = db.query(Resource).filter(Resource.id == resource_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Resource not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, val in update_data.items():
        setattr(res, key, val)
    db.commit()
    db.refresh(res)
    return res


@router.delete("/{resource_id}")
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    res = db.query(Resource).filter(Resource.id == resource_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Resource not found")
    db.delete(res)
    db.commit()
    return {"message": "Deleted"}


@router.post("/consumption", response_model=MaterialConsumptionOut)
def add_consumption(data: MaterialConsumptionCreate, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == data.resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    if resource.quantity < data.quantity_used:
        raise HTTPException(status_code=400, detail="Insufficient resource quantity")
    resource.quantity -= data.quantity_used
    cons = MaterialConsumption(**data.model_dump())
    db.add(cons)
    db.commit()
    db.refresh(cons)
    return cons


@router.get("/consumption", response_model=list[MaterialConsumptionOut])
def list_consumptions(db: Session = Depends(get_db)):
    return db.query(MaterialConsumption).all()
