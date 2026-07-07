# 地块.py — 地块管理与轮作 API（主要代码）
import hashlib
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..数据库 import get_db
from ..模型 import LandPlot, CropRotation
from ..模式 import LandPlotCreate, LandPlotUpdate, LandPlotOut, CropRotationCreate, CropRotationOut
from ..工具 import tr

router = APIRouter(prefix="/api/lands", tags=["lands"])


def compute_hash(geometry: str) -> str:
    return hashlib.sha256(geometry.encode()).hexdigest()


LAND_MAP = {"name": "name_ru", "soil_type": "soil_type_ru"}
ROT_MAP = {"crop_name": "crop_name_ru", "notes": "notes_ru"}


@router.get("/", response_model=list[LandPlotOut])
def list_lands(lang: str = Query("zh"), db: Session = Depends(get_db)):
    plots = db.query(LandPlot).all()
    for p in plots:
        tr(p, lang, LAND_MAP)
    return plots


@router.get("/{plot_id}", response_model=LandPlotOut)
def get_land(plot_id: int, lang: str = Query("zh"), db: Session = Depends(get_db)):
    plot = db.query(LandPlot).filter(LandPlot.id == plot_id).first()
    if not plot:
        raise HTTPException(status_code=404, detail="Land plot not found")
    tr(plot, lang, LAND_MAP)
    return plot


@router.post("/", response_model=LandPlotOut)
def create_land(data: LandPlotCreate, db: Session = Depends(get_db)):
    existing = db.query(LandPlot).filter(LandPlot.cadastral_number == data.cadastral_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Cadastral number already exists")
    plot = LandPlot(
        cadastral_number=data.cadastral_number,
        name=data.name, name_ru=data.name_ru,
        area_ha=data.area_ha,
        soil_type=data.soil_type, soil_type_ru=data.soil_type_ru,
        geometry=data.geometry,
        hash_sum=compute_hash(data.geometry) if data.geometry else None,
    )
    db.add(plot)
    db.commit()
    db.refresh(plot)
    return plot


@router.put("/{plot_id}", response_model=LandPlotOut)
def update_land(plot_id: int, data: LandPlotUpdate, db: Session = Depends(get_db)):
    plot = db.query(LandPlot).filter(LandPlot.id == plot_id).first()
    if not plot:
        raise HTTPException(status_code=404, detail="Land plot not found")
    update_data = data.model_dump(exclude_unset=True)
    if update_data.get("geometry"):
        update_data["hash_sum"] = compute_hash(update_data["geometry"])
    for key, val in update_data.items():
        setattr(plot, key, val)
    db.commit()
    db.refresh(plot)
    return plot


@router.delete("/{plot_id}")
def delete_land(plot_id: int, db: Session = Depends(get_db)):
    plot = db.query(LandPlot).filter(LandPlot.id == plot_id).first()
    if not plot:
        raise HTTPException(status_code=404, detail="Land plot not found")
    db.delete(plot)
    db.commit()
    return {"message": "Deleted"}


@router.get("/{plot_id}/rotations", response_model=list[CropRotationOut])
def list_rotations(plot_id: int, lang: str = Query("zh"), db: Session = Depends(get_db)):
    rots = db.query(CropRotation).filter(CropRotation.land_plot_id == plot_id).all()
    for r in rots:
        tr(r, lang, ROT_MAP)
    return rots


@router.post("/rotations", response_model=CropRotationOut)
def create_rotation(data: CropRotationCreate, db: Session = Depends(get_db)):
    rot = CropRotation(**data.model_dump())
    db.add(rot)
    db.commit()
    db.refresh(rot)
    return rot
