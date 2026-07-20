# SmartAgro 智慧农业综合管理系统

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)](https://fastapi.tiangolo.com)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.0+-brightgreen)](https://vuejs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

乌拉尔联邦大学 2026 届毕业设计 | 独立全栈开发

🌾 **中俄双语**农场管理系统，电脑端和手机端均可使用。

## 项目背景

针对中小农场用 Excel 手工管理效率低、ERP 成本过高的痛点，设计并开发了一套中俄双语农场管理网页系统。

## 功能模块

| 模块 | 说明 |
|------|------|
| 🗺️ **土地管理** | 地块 GIS 可视化，地图绘制多边形添加地块，自动计算面积、检测重叠 |
| 📋 **任务调度** | 耕地、播种、收割、施肥、灌溉任务分配与状态追踪 |
| 📦 **资源追踪** | 种子、肥料、燃油、农药库存管理，消耗关联到具体任务 |
| 📊 **数据报表** | 工作量统计、资源消耗分析、轮作记录 |
| 🔐 **用户认证** | 4 种角色权限（管理员/调度员/田间人员/仓库管理员） |

## 技术栈

**后端**
- Python + FastAPI — REST API
- SQLAlchemy ORM + SQLite
- GeoJSON 地理数据存储与 hash 校验
- JWT 用户认证

**前端**
- Vue.js 3 (Composition API)
- Leaflet 开源地图集成
- vue-i18n 中俄双语一键切换
- Pinia 状态管理

**部署**
- Docker 一键部署
- PWA 支持（手机可添加到桌面当 App 使用）
- 离线数据查看

## 项目结构

```
├── backend/
│   └── app/
│       ├── 主要.py          # FastAPI 入口
│       ├── 数据库.py        # 数据库连接
│       ├── 模型.py          # 7 张数据表模型
│       ├── 模式.py          # Pydantic 验证模式
│       ├── 安全.py          # JWT 认证
│       ├── 工具.py          # 双语翻译工具
│       └── routers/
│           ├── 认证.py      # 登录/注册 API
│           ├── 地块.py      # 地块管理 API
│           ├── 任务.py      # 任务调度 API
│           ├── 资源.py      # 资源追踪 API
│           └── 报告.py      # 数据报表 API
├── frontend/
│   └── src/
│       ├── views/           # 页面组件
│       ├── stores/          # Pinia 状态管理
│       ├── router/          # 路由配置
│       └── i18n.js          # 中俄双语
├── docker-compose.yml       # Docker 一键部署
└── 代码说明/                # 系统说明文档
```

## 项目数据

- **25+** API 接口
- **7** 张数据表
- **4** 种角色权限
- **中俄双语** 完整支持
- **Docker** 一键部署
- 毕设已通过答辩 ✅

## 快速启动

### Docker（推荐）

```bash
docker-compose up -d
```

浏览器访问 `http://localhost:8000`

### 手动启动

```bash
# 后端
cd backend
pip install -r requirements.txt
python 运行.py

# 前端
cd frontend
npm install
npm run dev
```

## 作者

xxx | 2026
