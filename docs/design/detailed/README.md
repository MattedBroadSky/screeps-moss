# Screeps Moss 项目 - 详细设计文档目录

## 📁 文档结构

### 1. 总体设计文档
- `OVERVIEW.md` - 详细设计概述和设计原则
- `ARCHITECTURE_REVIEW.md` - 架构设计评审要点
- `VERSION_PLAN.md` - 版本实现计划

### 2. 应用层模块设计
- `modules/application/ROOM_MANAGER.md` - 房间管理器详细设计
- `modules/application/GLOBAL_COORDINATOR.md` - 全局协调器详细设计（v2.0）

### 3. 业务层模块设计
- `modules/business/ENERGY_MANAGER.md` - 能量管理器详细设计
- `modules/business/CREEP_MANAGER.md` - Creep管理器详细设计
- `modules/business/ROLE_MANAGER.md` - 角色管理器详细设计
- `modules/business/BUILDING_MANAGER.md` - 建筑管理器详细设计
- `modules/business/DEFENSE_MANAGER.md` - 防御管理器详细设计

### 4. 服务层模块设计
- `modules/service/CONFIG_SERVICE.md` - 配置服务详细设计
- `modules/service/MEMORY_SERVICE.md` - 内存服务详细设计
- `modules/service/LOG_SERVICE.md` - 日志服务详细设计
- `modules/service/MONITOR_SERVICE.md` - 监控服务详细设计
- `modules/service/PROFILER_SERVICE.md` - 性能服务详细设计
- `modules/service/AI_SERVICE.md` - 智能服务详细设计（v3.0）
- `modules/service/DEPLOYMENT_SERVICE.md` - 部署服务详细设计（v3.0）

### 5. 数据层模块设计
- `modules/data/GAME_STATE.md` - 游戏状态数据结构
- `modules/data/CONFIG_DATA.md` - 配置数据结构
- `modules/data/HISTORICAL_DATA.md` - 历史数据结构
- `modules/data/MONITOR_DATA.md` - 监控数据结构

### 6. 通用设计文档
- `common/INTERFACE_DEFINITIONS.md` - 接口定义规范
- `common/ALGORITHM_DESIGN.md` - 算法设计文档
- `common/ERROR_HANDLING.md` - 错误处理机制
- `common/PERFORMANCE_OPTIMIZATION.md` - 性能优化策略
- `common/TEST_STRATEGY.md` - 测试策略设计
- `common/DEPLOYMENT_OPS.md` - 部署和运维设计
- `common/SECURITY_DESIGN.md` - 安全设计

## 🎯 开发流程

### 阶段1：v1.0 核心功能设计（当前阶段）
1. **优先级1** - 完成基础模块设计：
   - `ROOM_MANAGER.md`
   - `ENERGY_MANAGER.md`
   - `CREEP_MANAGER.md`
   - `ROLE_MANAGER.md`
   - `CONFIG_SERVICE.md`
   - `MEMORY_SERVICE.md`
   - `LOG_SERVICE.md`

2. **优先级2** - 完成通用设计：
   - `INTERFACE_DEFINITIONS.md`
   - `ALGORITHM_DESIGN.md`
   - `ERROR_HANDLING.md`

### 阶段2：v1.5 功能完善设计
1. **业务层完善**：
   - `BUILDING_MANAGER.md`
   - `DEFENSE_MANAGER.md`

2. **服务层完善**：
   - `MONITOR_SERVICE.md`
   - `PROFILER_SERVICE.md`

### 阶段3：v2.0+ 扩展功能设计
1. **多房间扩展**：
   - `GLOBAL_COORDINATOR.md`

2. **智能优化**：
   - `AI_SERVICE.md`
   - `DEPLOYMENT_SERVICE.md`

## 📝 文档规范

### 每个模块文档应包含：
1. **文档信息** - 版本、负责人、状态等
2. **设计目标** - 模块的设计目标
3. **类图设计** - UML类图或类似设计图
4. **接口定义** - 完整的接口定义
5. **算法设计** - 关键算法的详细设计
6. **数据结构** - 使用的数据结构
7. **错误处理** - 错误分类和处理策略
8. **性能考虑** - 性能优化策略
9. **测试策略** - 单元测试和集成测试设计
10. **依赖关系** - 与其他模块的依赖关系

### 评审流程：
1. **模块设计完成** → 提交评审
2. **技术评审** → 架构师评审
3. **修改完善** → 根据评审意见修改
4. **批准通过** → 标记为已批准状态
5. **编码实现** → 基于批准的设计编码

## 🔄 版本管理

### 文档版本规则：
- 主版本.次版本.修订版本（如：v1.0.0）
- 重大变更 → 主版本+1
- 功能增加 → 次版本+1
- 错误修正 → 修订版本+1

### 状态标记：
- `[草案]` - 设计进行中
- `[评审中]` - 提交评审
- `[已批准]` - 评审通过
- `[已实现]` - 编码完成
- `[已废弃]` - 不再使用

## 👥 分工建议

### 建议分工方式：
1. **架构师** - 负责总体设计和接口规范
2. **模块负责人** - 负责具体模块的详细设计
3. **评审委员会** - 跨模块设计评审
4. **文档维护者** - 维护文档一致性和完整性

### 协作工具：
- GitHub Issues - 任务跟踪
- GitHub Projects - 项目管理
- Pull Requests - 设计评审
- Markdown文档 - 设计文档

---

## 📅 当前任务

### 立即开始：
1. 创建模块化文档结构
2. 将现有RoomManager设计迁移到模块文档
3. 开始EnergyManager模块设计
4. 建立接口定义规范

### 本周目标：
完成v1.0核心功能的所有模块设计文档初稿。

---

*最后更新：2026-03-25*