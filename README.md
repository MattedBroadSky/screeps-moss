# Screeps Moss 项目

## 项目概述
Screeps Moss 是一个基于软件工程方法重新规划的 Screeps AI 系统项目。

## 📁 项目文档结构

### 📋 需求文档 (`docs/requirements/`)
- `REQUIREMENTS_ANALYSIS.md` - 需求分析文档 (v2.0，已批准)

### 🔍 分析文档 (`docs/analysis/`)
- `SYSTEM_ANALYSIS.md` - 系统分析文档 (v2.0，已批准)

### 🏗️ 设计文档 (`docs/design/`)
#### 架构设计 (`docs/design/architecture/`)
- `ARCHITECTURE_DESIGN.md` - 架构设计文档 (v1.0，概要设计)

#### 详细设计 (`docs/design/detailed/`)
- `DETAILED_DESIGN.md` - 详细设计文档 (v1.0，进行中)

### 📊 规划文档 (`docs/planning/`)
- `PROJECT_BOARD.md` - 项目看板
- `STATUS_SNAPSHOT.md` - 项目状态快照

## 🔄 软件工程流程状态

```
✅ 需求分析 → ✅ 系统分析 → ✅ 概要设计 → ⏳ 详细设计 → ❌ 编码实现
```

## 🎯 项目里程碑

| 阶段 | 状态 | 完成时间 | 文档 |
|------|------|----------|------|
| 需求分析 | ✅ 已完成 | 2026-03-22 15:19 | `REQUIREMENTS_ANALYSIS.md` (v2.0) |
| 系统分析 | ✅ 已完成 | 2026-03-22 14:35 | `SYSTEM_ANALYSIS.md` (v2.0) |
| 概要设计 | ✅ 已完成 | 2026-03-22 16:00 | `ARCHITECTURE_DESIGN.md` (v1.0) |
| 详细设计 | ⏳ 进行中 | 预计 2026-03-23 | `DETAILED_DESIGN.md` (v1.0) |
| 编码实现 | ❌ 未开始 | 预计 2026-03-24 | - |

## 🏗️ 架构设计要点

### 四层架构
1. **应用层**: RoomManager, GlobalCoordinator
2. **业务层**: EnergyManager, CreepManager, RoleManager, BuildingManager, DefenseManager
3. **服务层**: ConfigService, MemoryService, LogService, MonitorService, ProfilerService
4. **数据层**: GameState, ConfigData, HistoricalData, MonitorData

### 核心模块
- **能量管理系统**: 能量采集、存储、分配优化
- **Creep管理系统**: 生命周期管理、需求分析、生成策略
- **角色行为系统**: 状态机设计、任务调度、效率优化
- **建筑管理系统**: 自动布局、优先级建造、维护管理

## 🚀 快速开始

### 开发环境
```bash
# 克隆项目
git clone https://github.com/MattedBroadSky/screeps-moss.git

# 进入项目目录
cd screeps-moss

# 查看项目状态
cat docs/planning/STATUS_SNAPSHOT.md
```

### 文档阅读顺序
1. 需求分析文档 (`docs/requirements/REQUIREMENTS_ANALYSIS.md`)
2. 系统分析文档 (`docs/analysis/SYSTEM_ANALYSIS.md`)
3. 架构设计文档 (`docs/design/architecture/ARCHITECTURE_DESIGN.md`)
4. 详细设计文档 (`docs/design/detailed/DETAILED_DESIGN.md`)

## 👥 项目团队

- **项目负责人**: Moss (OpenClaw AI)
- **架构设计师**: Moss
- **开发团队**: 待组建

## 📄 许可证

待定