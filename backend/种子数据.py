# 种子数据.py — 填充中俄双语演示数据（主要代码）
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app.数据库 import engine, Base, SessionLocal
from app.模型 import User, LandPlot, CropRotation, Task, Resource, MaterialConsumption, WorkReport
from app.安全 import hash_password
from datetime import datetime, timedelta

Base.metadata.create_all(bind=engine)
db = SessionLocal()

for tbl in [WorkReport, MaterialConsumption, Task, CropRotation, Resource, LandPlot, User]:
    db.query(tbl).delete()
db.commit()

# 用户
users = [
    User(username="admin", email="admin@zhny.ru", hashed_password=hash_password("admin123"),
         full_name="系统管理员", role="admin"),
    User(username="dispatcher", email="disp@zhny.ru", hashed_password=hash_password("disp123"),
         full_name="调度员张三", role="dispatcher"),
    User(username="worker1", email="worker1@zhny.ru", hashed_password=hash_password("work123"),
         full_name="田间工人李四", role="field_staff"),
    User(username="storekeeper", email="store@zhny.ru", hashed_password=hash_password("store123"),
         full_name="库管员王五", role="storekeeper"),
]
db.add_all(users)
db.commit()

# 地块（中俄双语）— 新疆伊犁
plots = [
    LandPlot(cadastral_number="XJ-001",
             name="伊犁麦田", name_ru="Илийское пшеничное поле",
             area_ha=120.5, soil_type="黑土", soil_type_ru="Чернозём",
             geometry='{"type":"Polygon","coordinates":[[[81.28,43.93],[81.30,43.93],[81.30,43.95],[81.28,43.95],[81.28,43.93]]]}',
             hash_sum="abc001"),
    LandPlot(cadastral_number="XJ-002",
             name="伊犁玉米地", name_ru="Илийское кукурузное поле",
             area_ha=85.3, soil_type="褐土", soil_type_ru="Бурая почва",
             geometry='{"type":"Polygon","coordinates":[[[81.32,43.91],[81.34,43.91],[81.34,43.93],[81.32,43.93],[81.32,43.91]]]}',
             hash_sum="def002"),
    LandPlot(cadastral_number="XJ-003",
             name="伊犁大豆田", name_ru="Илийское соевое поле",
             area_ha=200.0, soil_type="栗钙土", soil_type_ru="Каштановая почва",
             geometry='{"type":"Polygon","coordinates":[[[81.23,43.92],[81.26,43.92],[81.26,43.94],[81.23,43.94],[81.23,43.92]]]}',
             hash_sum="ghi003"),
]
db.add_all(plots)
db.commit()

# 轮作
rots = [
    CropRotation(land_plot_id=1,
                 crop_name="冬小麦", crop_name_ru="Озимая пшеница",
                 sowing_date=datetime(2025, 10, 15), harvest_date=datetime(2026, 6, 20),
                 yield_amount=5250, notes="亩产350公斤", notes_ru="350 кг/му"),
    CropRotation(land_plot_id=1,
                 crop_name="夏玉米", crop_name_ru="Яровая кукуруза",
                 sowing_date=datetime(2026, 6, 25), harvest_date=datetime(2026, 10, 10),
                 yield_amount=6000),
    CropRotation(land_plot_id=2,
                 crop_name="春玉米", crop_name_ru="Яровая кукуруза",
                 sowing_date=datetime(2026, 4, 20), harvest_date=None,
                 notes="青贮饲料", notes_ru="На силос"),
]
db.add_all(rots)
db.commit()

# 任务
now = datetime.utcnow()
tasks = [
    Task(title="伊犁麦田深耕", title_ru="Глубокая вспашка пшеничного поля",
         description="冬小麦播种前深耕作业", description_ru="Подготовка почвы под озимую пшеницу",
         task_type="plowing", land_plot_id=1, assigned_to=3, created_by=2,
         planned_start=now, planned_end=now + timedelta(days=5),
         status="in_progress", priority=2),
    Task(title="伊犁玉米播种", title_ru="Посев кукурузы на южном поле",
         description="春玉米播种，品种：郑单958", description_ru="Посев кукурузы, сорт Чжэндань 958",
         task_type="sowing", land_plot_id=2, assigned_to=3, created_by=2,
         planned_start=now + timedelta(days=7), planned_end=now + timedelta(days=10),
         status="pending", priority=3),
    Task(title="伊犁大豆收割", title_ru="Уборка сои на западном поле",
         description="大豆联合收割作业", description_ru="Комбайновая уборка сои",
         task_type="harvesting", land_plot_id=3, assigned_to=3, created_by=2,
         planned_start=now - timedelta(days=10), planned_end=now - timedelta(days=3),
         status="completed", priority=2),
    Task(title="伊犁施肥", title_ru="Внесение удобрений на западном поле",
         description="施用复合肥 50公斤/亩", description_ru="Внесение комплексных удобрений 50 кг/му",
         task_type="fertilizing", land_plot_id=3, assigned_to=3, created_by=2,
         planned_start=now + timedelta(days=14), planned_end=now + timedelta(days=16),
         status="pending", priority=1),
]
db.add_all(tasks)
db.commit()

# 资源
resources = [
    Resource(name="冬小麦种子（郑麦366）", name_ru="Семена озимой пшеницы (Чжэнмай 366)",
             resource_type="seeds", unit="公斤", unit_ru="кг",
             quantity=5000, min_threshold=500, price_per_unit=4.2,
             supplier="中农种业", supplier_ru="Чжуннун Семена"),
    Resource(name="复合肥（15-15-15）", name_ru="Комплексные удобрения (15-15-15)",
             resource_type="fertilizer", unit="公斤", unit_ru="кг",
             quantity=2000, min_threshold=300, price_per_unit=3.5,
             supplier="云天化集团", supplier_ru="Юньтяньхуа Групп"),
    Resource(name="柴油", name_ru="Дизельное топливо",
             resource_type="fuel", unit="升", unit_ru="л",
             quantity=1500, min_threshold=200, price_per_unit=7.8,
             supplier="中石油", supplier_ru="ПетроЧайна"),
    Resource(name="除草剂（草甘膦）", name_ru="Гербицид (Глифосат)",
             resource_type="pesticide", unit="升", unit_ru="л",
             quantity=80, min_threshold=100, price_per_unit=45.0,
             supplier="先正达", supplier_ru="Сингента"),
    Resource(name="春玉米种子（郑单958）", name_ru="Семена кукурузы (Чжэндань 958)",
             resource_type="seeds", unit="公斤", unit_ru="кг",
             quantity=200, min_threshold=50, price_per_unit=18.0,
             supplier="中农种业", supplier_ru="Чжуннун Семена"),
]
db.add_all(resources)
db.commit()

# 消耗
cons = [
    MaterialConsumption(task_id=1, resource_id=3, land_plot_id=1, quantity_used=120, notes="拖拉机用油"),
    MaterialConsumption(task_id=3, resource_id=3, land_plot_id=3, quantity_used=200),
]
db.add_all(cons)
db.commit()

# 报告
reports = [
    WorkReport(task_id=1, worker_id=3, progress_percent=60,
               report_text="伊犁麦田已完成60%深耕", report_text_ru="Вспахано 60% пшеничного поля",
               geo_latitude=43.94, geo_longitude=81.29),
    WorkReport(task_id=3, worker_id=3, progress_percent=100,
               report_text="大豆收割完成，入库3号仓库", report_text_ru="Уборка сои завершена, принято на склад №3",
               geo_latitude=43.92, geo_longitude=81.25),
]
db.add_all(reports)
db.commit()

db.close()
print("种子数据填充完成！(中俄双语)")
