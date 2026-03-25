# RoleManager 详细设计文档

## 📋 文档信息
- **模块名称**: RoleManager（角色管理器）
- **所属层级**: 业务层
- **文档版本**: v1.0.0
- **创建日期**: 2026-03-25
- **最后更新**: 2026-03-25
- **负责人**: Moss (OpenClaw AI)
- **状态**: [草案]
- **优先级**: P0 (v1.0核心模块)
- **关联文档**: 
  - `CREEP_MANAGER.md` - Creep管理器设计
  - `ENERGY_MANAGER.md` - 能量管理器设计

## 🎯 设计目标

### 核心职责
1. **角色行为管理** - 定义和执行各角色行为逻辑
2. **任务分配优化** - 智能分配任务给合适Creep
3. **状态机管理** - 管理Creep行为状态转换
4. **效率监控** - 监控角色执行效率和任务完成率
5. **行为优化** - 根据历史数据优化行为策略

### 质量目标
- **性能**: 每tick CPU使用 < 4
- **效率**: 任务分配准确率 > 90%
- **响应**: 任务分配延迟 < 5 ticks
- **可靠性**: 关键任务中断时间 < 3 ticks

## 🏗️ 类图设计

### 类结构
```
┌─────────────────────────────────────┐
│          RoleManager                │
├─────────────────────────────────────┤
│ - roomName: string                  │
│ - roles: Map<string, RoleBehavior>  │
│ - tasks: Map<string, Task>          │
│ - assignments: Map<string, string>  │
│ - stateMachines: Map<string, BehaviorStateMachine>
│ - config: RoleConfig                │
│ - stats: RoleStats                  │
│ - cache: RoleCache                  │
├─────────────────────────────────────┤
│ + constructor(roomName: string)     │
│ + init(config: RoleConfig): boolean │
│ + tick(roomState: RoomState): RoleTickResult
│ + assignTasks(creeps: Creep[]): AssignmentResult
│ + monitorRolePerformance(): RolePerformance[]
│ + optimizeBehaviors(): OptimizationResult
│ + getRoleStats(role: string): RoleStat
│ + updateBehavior(role, behavior): void
│ - generateTasks(roomState): Task[]  │
│ - matchCreepsToTasks(): Assignment[]│
│ - executeBehaviors(): void          │
│ - updateStateMachines(): void       │
│ - recordMetrics(): void             │
│ - cleanupCompletedTasks(): void     │
└─────────────────────────────────────┘
```

### 核心组件
```
RoleManager
    ├── TaskGenerator      - 任务生成器
    ├── TaskAssigner       - 任务分配器
    ├── BehaviorExecutor   - 行为执行器
    ├── StateMachineManager - 状态机管理
    ├── PerformanceMonitor - 性能监控
    └── BehaviorOptimizer  - 行为优化器
```

## 📝 接口定义

### 公共接口

#### 1. 初始化接口
```javascript
/**
 * 初始化角色管理器
 * @param {RoleConfig} config - 角色配置
 * @returns {boolean} 初始化是否成功
 */
init(config: RoleConfig): boolean
```

#### 2. Tick处理接口
```javascript
/**
 * 处理角色tick
 * @param {RoomState} roomState - 房间状态
 * @returns {RoleTickResult} tick处理结果
 */
tick(roomState: RoomState): RoleTickResult
```

#### 3. 任务分配接口
```javascript
/**
 * 分配任务给Creep
 * @param {Creep[]} creeps - Creep数组
 * @returns {AssignmentResult} 分配结果
 */
assignTasks(creeps: Creep[]): AssignmentResult
```

#### 4. 性能监控接口
```javascript
/**
 * 监控角色性能
 * @returns {RolePerformance[]} 角色性能数据
 */
monitorRolePerformance(): RolePerformance[]
```

#### 5. 行为优化接口
```javascript
/**
 * 优化角色行为
 * @returns {OptimizationResult} 优化结果
 */
optimizeBehaviors(): OptimizationResult
```

#### 6. 状态查询接口
```javascript
/**
 * 获取角色统计
 * @param {string} role - 角色名称
 * @returns {RoleStat} 角色统计
 */
getRoleStats(role: string): RoleStat
```

### 数据类型定义

#### RoleConfig
```javascript
interface RoleConfig {
  // 角色行为配置
  behaviors: {
    [role: string]: RoleBehaviorConfig;
  };
  
  // 任务分配配置
  taskAssignment: {
    strategy: 'greedy' | 'balanced' | 'efficient'; // 分配策略
    maxAssignmentsPerTick: number;                 // 每tick最大分配数
    reassignmentThreshold: number;                 // 重新分配阈值
    priorityWeights: {                             // 优先级权重
      distance: number;    // 距离权重
      efficiency: number;  // 效率权重
      urgency: number;     // 紧急程度权重
      specialization: number; // 专业化权重
    };
  };
  
  // 状态机配置
  stateMachine: {
    defaultState: string;                         // 默认状态
    transitionRules: TransitionRule[];            // 状态转换规则
    timeoutThresholds: {                          // 超时阈值
      [state: string]: number;
    };
  };
  
  // 性能监控配置
  monitoring: {
    enabled: boolean;
    samplingInterval: number;
    efficiencyThresholds: {                       // 效率阈值
      optimal: number;    // 最优
      acceptable: number; // 可接受
      poor: number;       // 差
    };
    alertThresholds: {
      lowEfficiency: number;   // 低效率告警
      highIdleRate: number;    // 高闲置率告警
      taskFailure: number;     // 任务失败告警
    };
  };
  
  // 优化配置
  optimization: {
    enabled: boolean;
    learningRate: number;      // 学习率
    explorationRate: number;   // 探索率
    historyWindow: number;     // 历史窗口大小
    improvementThreshold: number; // 改进阈值
  };
}
```

#### RoleTickResult
```javascript
interface RoleTickResult {
  success: boolean;                    // 是否成功
  cpuUsed: number;                     // CPU使用量
  actions: {                           // 执行的动作
    tasksGenerated: number;            // 生成的任务数
    tasksAssigned: number;             // 分配的任务数
    behaviorsExecuted: number;         // 执行的行为数
    stateTransitions: number;          // 状态转换数
  };
  performance: RolePerformance[];      // 性能数据
  assignments: AssignmentSummary;      // 分配摘要
  issues: RoleIssue[];                 // 检测到的问题
  optimizations: OptimizationSuggestion[]; // 优化建议
}
```

#### AssignmentResult
```javascript
interface AssignmentResult {
  success: boolean;                    // 是否成功
  assignments: Assignment[];           // 分配结果
  unassignedCreeps: string[];          // 未分配的Creep
  unassignedTasks: string[];           // 未分配的任务
  efficiency: number;                  // 分配效率（0-1）
  stats: {
    totalCreeps: number;               // 总Creep数
    totalTasks: number;                // 总任务数
    assignmentRate: number;            // 分配率
    avgDistance: number;               // 平均距离
    avgEfficiency: number;             // 平均效率
  };
}
```

#### RolePerformance
```javascript
interface RolePerformance {
  role: string;                        // 角色名称
  metrics: {
    efficiency: number;                // 效率（0-1）
    utilization: number;               // 利用率（0-1）
    taskCompletion: number;            // 任务完成率（0-1）
    idleRate: number;                  // 闲置率（0-1）
    errorRate: number;                 // 错误率（0-1）
  };
  tasks: {
    active: number;                    // 活跃任务数
    completed: number;                 // 完成的任务数
    failed: number;                    // 失败的任务数
    avgDuration: number;               // 平均持续时间
    successRate: number;               // 成功率
  };
  creeps: {
    total: number;                     // 总Creep数
    assigned: number;                  // 已分配的Creep数
    idle: number;                      // 闲置的Creep数
    avgEfficiency: number;             // 平均效率
  };
  timestamp: number;                   // 时间戳
}
```

## 🔧 算法设计

### 1. 任务生成算法

#### 智能任务生成
```javascript
generateTasks(roomState) {
  const tasks = [];
  
  // 1. 采集任务（基于能量源）
  const harvestTasks = this.generateHarvestTasks(roomState);
  tasks.push(...harvestTasks);
  
  // 2. 运输任务（基于能量存储）
  const haulTasks = this.generateHaulTasks(roomState);
  tasks.push(...haulTasks);
  
  // 3. 建造任务（基于建筑工地）
  const buildTasks = this.generateBuildTasks(roomState);
  tasks.push(...buildTasks);
  
  // 4. 升级任务（基于控制器）
  const upgradeTasks = this.generateUpgradeTasks(roomState);
  tasks.push(...upgradeTasks);
  
  // 5. 维修任务（基于受损建筑）
  const repairTasks = this.generateRepairTasks(roomState);
  tasks.push(...repairTasks);
  
  // 6. 防御任务（基于威胁）
  const defenseTasks = this.generateDefenseTasks(roomState);
  tasks.push(...defenseTasks);
  
  // 7. 清理任务（基于死亡Creep和废墟）
  const cleanupTasks = this.generateCleanupTasks(roomState);
  tasks.push(...cleanupTasks);
  
  // 8. 自定义任务（基于特殊需求）
  const customTasks = this.generateCustomTasks(roomState);
  tasks.push(...customTasks);
  
  // 计算任务优先级
  tasks.forEach(task => {
    task.priority = this.calculateTaskPriority(task, roomState);
  });
  
  return tasks;
}
```

#### 任务优先级计算
```javascript
calculateTaskPriority(task, roomState) {
  let priority = 1; // 基础优先级
  
  // 1. 任务类型权重
  const typeWeights = {
    harvest: 10,     // 采集：最高优先级
    haul: 9,         // 运输：高优先级
    upgrade: 8,      // 升级：重要
    build: 7,        // 建造：重要
    repair: 6,       // 维修：中等
    defense: 9,      // 防御：高优先级（紧急时更高）
    cleanup: 3,      // 清理：低优先级
    custom: 5        // 自定义：中等
  };
  priority *= (typeWeights[task.type] || 5);
  
  // 2. 紧急程度
  if (task.emergency) {
    priority *= 2;
  }
  
  // 3. 资源重要性
  if (task.resourceType === RESOURCE_ENERGY) {
    priority *= 1.5;
  }
  
  // 4. 目标状态（例如：建筑损坏程度）
  if (task.target) {
    const target = Game.getObjectById(task.target);
    if (target) {
      if (target.hits && target.hitsMax) {
        const healthRatio = target.hits / target.hitsMax;
        if (healthRatio < 0.3) priority *= 2;
        else if (healthRatio < 0.5) priority *= 1.5;
      }
    }
  }
  
  // 5. 时间因素（任务存在时间越长优先级越高）
  if (task.createdAt) {
    const age = Game.time - task.createdAt;
    priority *= (1 + Math.min(age / 100, 1)); // 最多翻倍
  }
  
  // 6. 房间状态影响
  const energyRatio = roomState.energy.available / roomState.energy.capacity;
  if (energyRatio < 0.3 && task.type === 'harvest') {
    priority *= 2; // 能量低时采集任务更重要
  }
  
  // 限制范围
  return Math.max(1, Math.min(priority, 100));
}
```

### 2. 任务分配算法

#### 基于多因素匹配的分配
```javascript
matchCreepsToTasks(creeps, tasks) {
  const assignments = [];
  const assignedCreeps = new Set();
  const assignedTasks = new Set();
  
  // 1. 准备匹配数据
  const creepProfiles = this.createCreepProfiles(creeps);
  const taskProfiles = this.createTaskProfiles(tasks);
  
  // 2. 构建匹配矩阵
  const matchMatrix = this.buildMatchMatrix(creepProfiles, taskProfiles);
  
  // 3. 使用匹配算法（匈牙利算法或贪心算法）
  const matching = this.findOptimalMatching(matchMatrix);
  
  // 4. 生成分配结果
  matching.forEach(({ creepIndex, taskIndex, score }) => {
    if (score > this.config.taskAssignment.minMatchScore) {
      const creep = creeps[creepIndex];
      const task = tasks[taskIndex];
      
      assignments.push({
        creepId: creep.id,
        creepName: creep.name,
        taskId: task.id,
        taskType: task.type,
        score,
        estimatedEfficiency: this.estimateAssignmentEfficiency(creep, task)
      });
      
      assignedCreeps.add(creep.id);
      assignedTasks.add(task.id);
    }
  });
  
  // 5. 处理未分配的Creep和任务
  const unassignedCreeps = creeps
    .filter(c => !assignedCreeps.has(c.id))
    .map(c => c.name);
    
  const unassignedTasks = tasks
    .filter(t => !assignedTasks.has(t.id))
    .map(t => t.id);
  
  return {
    assignments,
    unassignedCreeps,
    unassignedTasks,
    matchQuality: this.calculateMatchQuality(assignments)
  };
}
```

#### Creep能力分析
```javascript
createCreepProfiles(creeps) {
  return creeps.map(creep => {
    const profile = {
      id: creep.id,
      name: creep.name,
      role: creep.memory.role,
      body: this.analyzeCreepBody(creep.body),
      position: creep.pos,
      store: creep.store,
      fatigue: creep.fatigue,
      ticksToLive: creep.ticksToLive,
      currentTask: creep.memory.taskId,
      efficiencyHistory: this.getCreepEfficiencyHistory(creep.name),
      specialization: this.calculateCreepSpecialization(creep)
    };
    
    // 计算能力分数
    profile.capabilities = {
      harvest: this.calculateHarvestCapability(creep),
      haul: this.calculateHaulCapability(creep),
      build: this.calculateBuildCapability(creep),
      upgrade: this.calculateUpgradeCapability(creep),
      repair: this.calculateRepairCapability(creep),
      attack: this.calculateAttackCapability(creep),
      heal: this.calculateHealCapability(creep)
    };
    
    return profile;
  });
}
```

#### 任务需求分析
```javascript
createTaskProfiles(tasks) {
  return tasks.map(task => {
    const profile = {
      id: task.id,
      type: task.type,
      priority: task.priority,
      position: task.position,
      targetId: task.target,
      resourceType: task.resourceType,
      amount: task.amount,
      emergency: task.emergency || false,
      createdAt: task.createdAt || Game.time,
      requirements: this.analyzeTaskRequirements(task)
    };
    
    // 计算需求向量
    profile.requirements = {
      harvest: task.type === 'harvest' ? 1 : 0,
      haul: task.type === 'haul' ? 1 : 0,
      build: task.type === 'build' ? 1 : 0,
      upgrade: task.type === 'upgrade' ? 1 : 0,
      repair: task.type === 'repair' ? 1 : 0,
      attack: task.type === 'defense' ? 1 : 0,
      heal: task.type === 'defense' ? 0.5 : 0,
      distanceWeight: this.calculateDistanceWeight(task),
      urgencyWeight: task.emergency ? 2 : 1
    };
    
    return profile;
  });
}
```

#### 匹配分数计算
```javascript
calculateMatchScore(creepProfile, taskProfile) {
  let score = 0;
  
  // 1. 角色匹配（基础分）
  const roleMatch = this.checkRoleMatch(creepProfile.role, taskProfile.type);
  score += roleMatch * 30; // 最多30分
  
  // 2. 能力匹配
  const capabilityMatch = this.calculateCapabilityMatch(
    creepProfile.capabilities,
    taskProfile.requirements
  );
  score += capabilityMatch * 40; // 最多40分
  
  // 3. 距离因素
  const distance = this.calculateDistance(
    creepProfile.position,
    taskProfile.position
  );
  const distanceScore = Math.max(0, 20 - distance / 5); // 最多20分
  score += distanceScore;
  
  // 4. 效率历史
  const efficiencyBonus = creepProfile.efficiencyHistory * 10; // 最多10分
