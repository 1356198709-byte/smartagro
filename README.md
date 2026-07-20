# SmartAgro — 智慧农业管理系统

> 毕业设计项目 | 乌拉尔联邦大学 信息学与计算机技术

## 作者

**xxx** | 2026

## 项目简介

SmartAgro 是一套面向中型农场的轻量级 Web 管理系统，解决中小农场用 Excel 手工管理效率低、ERP 成本过高的痛点。

- **技术栈**：FastAPI + Vue 3 + PostgreSQL/PostGIS + Docker
- **6 大模块**：仪表盘、土地 GIS 管理、任务调度、资源核算、分析报表、PWA 移动端
- **中俄双语**：vue-i18n 一键切换
- **离线可用**：PWA + Service Worker + IndexedDB
- **空间数据**：Leaflet 地图 + PostGIS 空间引擎

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/1356198709-byte/smartagro.git

# 启动后端
cd backend
pip install -r requirements.txt
python 运行.py

# 启动前端（开发模式）
cd frontend
npm install
npm run dev
```

## 在线演示

👉 [https://1356198709-byte.github.io/smartagro](https://1356198709-byte.github.io/smartagro)

## 许可证

MIT License
