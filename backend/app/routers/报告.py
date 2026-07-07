# 报告.py — 分析报告 API（主要代码）
import io
import xlsxwriter
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..数据库 import get_db
from ..模型 import WorkReport, LandPlot, Task, Resource, MaterialConsumption
from ..模式 import WorkReportCreate, WorkReportOut, AnalyticsSummary
from ..工具 import tr, tr_dict

router = APIRouter(prefix="/api/reports", tags=["reports"])

REPORT_MAP = {"report_text": "report_text_ru"}
LAND_MAP = {"name": "name_ru"}


@router.post("/work", response_model=WorkReportOut)
def create_work_report(data: WorkReportCreate, db: Session = Depends(get_db)):
    report = WorkReport(**data.model_dump(), worker_id=1)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


@router.get("/work", response_model=list[WorkReportOut])
def list_work_reports(lang: str = Query("zh"), task_id: int = None, db: Session = Depends(get_db)):
    q = db.query(WorkReport)
    if task_id:
        q = q.filter(WorkReport.task_id == task_id)
    reports = q.all()
    for r in reports:
        tr(r, lang, REPORT_MAP)
    return reports


@router.get("/analytics", response_model=AnalyticsSummary)
def get_analytics(db: Session = Depends(get_db)):
    total_area = db.query(func.sum(LandPlot.area_ha)).scalar() or 0
    total_plots = db.query(func.count(LandPlot.id)).scalar() or 0
    active_tasks = db.query(func.count(Task.id)).filter(
        Task.status.in_(["pending", "in_progress"])
    ).scalar() or 0
    completed_tasks = db.query(func.count(Task.id)).filter(
        Task.status == "completed"
    ).scalar() or 0
    total_value = db.query(
        func.sum(Resource.quantity * Resource.price_per_unit)
    ).scalar() or 0
    low_stock = db.query(func.count(Resource.id)).filter(
        Resource.quantity <= Resource.min_threshold
    ).scalar() or 0

    return AnalyticsSummary(
        total_land_area=round(total_area, 2),
        total_plots=total_plots,
        active_tasks=active_tasks,
        completed_tasks=completed_tasks,
        total_resources_value=round(total_value, 2),
        low_stock_resources=low_stock,
    )


@router.get("/profitability")
def profitability_by_field(lang: str = Query("zh"), db: Session = Depends(get_db)):
    results = []
    plots = db.query(LandPlot).all()
    for plot in plots:
        consumptions = db.query(MaterialConsumption).filter(
            MaterialConsumption.land_plot_id == plot.id
        ).all()
        total_cost = 0.0
        for c in consumptions:
            resource = db.query(Resource).filter(Resource.id == c.resource_id).first()
            if resource:
                total_cost += c.quantity_used * resource.price_per_unit
        name = plot.name_ru if lang == "ru" and plot.name_ru else plot.name
        results.append({
            "plot_id": plot.id,
            "plot_name": name,
            "area_ha": plot.area_ha,
            "total_material_cost": round(total_cost, 2),
            "cost_per_ha": round(total_cost / plot.area_ha, 2) if plot.area_ha > 0 else 0,
        })
    return results


@router.get("/profitability/excel")
def export_profitability_excel(lang: str = Query("zh"), db: Session = Depends(get_db)):
    """导出 profitability 报表为 Excel (.xlsx) 文件"""
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})

    # 根据语言选择列标题
    if lang == "ru":
        headers = ["ID участка", "Название участка", "Площадь (га)", "Общая стоимость (¥)", "Себестоимость (¥/га)"]
        sheet_name = "Рентабельность"
    else:
        headers = ["地块ID", "地块名称", "面积(ha)", "总成本(¥)", "每公顷成本(¥/ha)"]
        sheet_name = "收益率分析"

    worksheet = workbook.add_worksheet(sheet_name)

    # 标题格式
    header_fmt = workbook.add_format({
        'bold': True, 'bg_color': '#2d6a4f', 'font_color': '#ffffff',
        'border': 1, 'align': 'center', 'valign': 'vcenter',
        'font_size': 12, 'font_name': 'Arial'
    })
    # 数据格式
    cell_fmt = workbook.add_format({
        'border': 1, 'align': 'center', 'valign': 'vcenter',
        'font_size': 11, 'font_name': 'Arial'
    })
    num_fmt = workbook.add_format({
        'border': 1, 'align': 'right', 'valign': 'vcenter',
        'font_size': 11, 'font_name': 'Arial', 'num_format': '#,##0.00'
    })

    # 设置列宽
    worksheet.set_column(0, 0, 12)
    worksheet.set_column(1, 1, 30)
    worksheet.set_column(2, 4, 18)

    # 写标题行
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, header_fmt)
    worksheet.set_row(0, 30)

    # 获取数据
    plots = db.query(LandPlot).all()
    row = 1
    total_cost_all = 0
    total_area_all = 0

    for plot in plots:
        consumptions = db.query(MaterialConsumption).filter(
            MaterialConsumption.land_plot_id == plot.id
        ).all()
        total_cost = 0.0
        for c in consumptions:
            resource = db.query(Resource).filter(Resource.id == c.resource_id).first()
            if resource:
                total_cost += c.quantity_used * resource.price_per_unit
        name = plot.name_ru if lang == "ru" and plot.name_ru else plot.name
        cost_per_ha = round(total_cost / plot.area_ha, 2) if plot.area_ha > 0 else 0

        worksheet.write(row, 0, plot.id, cell_fmt)
        worksheet.write(row, 1, name, cell_fmt)
        worksheet.write_number(row, 2, plot.area_ha or 0, num_fmt)
        worksheet.write_number(row, 3, round(total_cost, 2), num_fmt)
        worksheet.write_number(row, 4, cost_per_ha, num_fmt)

        total_cost_all += total_cost
        total_area_all += plot.area_ha or 0
        row += 1

    # 汇总行
    sum_fmt = workbook.add_format({
        'bold': True, 'bg_color': '#e8f5e9', 'border': 1, 'align': 'right',
        'valign': 'vcenter', 'font_size': 11, 'font_name': 'Arial', 'num_format': '#,##0.00'
    })
    sum_label_fmt = workbook.add_format({
        'bold': True, 'bg_color': '#e8f5e9', 'border': 1, 'align': 'center',
        'valign': 'vcenter', 'font_size': 11, 'font_name': 'Arial'
    })

    label_text = "ИТОГО" if lang == "ru" else "合计"
    worksheet.write(row, 0, '', sum_label_fmt)
    worksheet.write(row, 1, label_text, sum_label_fmt)
    worksheet.write_number(row, 2, round(total_area_all, 2), sum_fmt)
    worksheet.write_number(row, 3, round(total_cost_all, 2), sum_fmt)
    avg_cost = round(total_cost_all / total_area_all, 2) if total_area_all > 0 else 0
    worksheet.write_number(row, 4, avg_cost, sum_fmt)

    workbook.close()
    output.seek(0)

    filename = "rentabelnost.xlsx" if lang == "ru" else "profitability.xlsx"
    headers_resp = {
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }
    return StreamingResponse(output, headers=headers_resp)
