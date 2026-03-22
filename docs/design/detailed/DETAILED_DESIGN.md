# Screeps Moss 项目 - 技术设计文档 (v1.0)

## 1. 设计概述

### 1.1 设计目标
基于需求分析文档，设计满足以下目标的系统：
1. **模块化**: 功能解耦，独立开发测试
2. **高性能**: CPU/内存约束下优化
3. **可扩展**: 单房间→多房间平滑扩展
4. **可靠性**: 容错设计，自动恢复
5. **可维护**: 代码清晰，文档完整

### 1.2 设计原则
- 单一职责: 每个模块一个功能
- 开闭原则: 配置扩展，不改代码
- 依赖倒置: 依赖接口，不依赖实现
- 接口隔离: 细粒度接口
- 迪米特法则: 减少直接依赖

### 1.3 技术约束应对
- **CPU限制**: 算法优化，计算分布，缓存
- **内存限制**: 精细管理，定期清理，压缩
- **API限制**: 批量操作，异步处理
- **实时性**: 任务优先级，超时处理

## 2. 系统架构

### 2.1 总体架构
```
应用层: RoomManager, GlobalCoordinator(未来)
业务层: EnergyManager, CreepManager, RoleManager, BuildingManager
服务层: ConfigService, MemoryService, LogService, MonitorService
数据层: GameState, ConfigData, HistoricalData, MonitorData
```

### 2.2 模块职责
| 模块 | 职责 | 关键接口 |
|------|------|----------|
| RoomManager | 房间生命周期 | initRoom(), tickRoom() |
| EnergyManager | 能量管理 | analyze(), allocate(), monitor() |
| CreepManager | Creep管理 | analyzeNeeds(), spawn(), manageLifecycle() |
| RoleManager | 角色任务 | assignTasks(), monitorProgress() |
| BuildingManager | 建筑管理 | planLayout(), construct(), repair() |

### 2.3 数据流
```
正常流: API→采集→分析→决策→执行→反馈
异常流: 检测→分类→恢复→验证→恢复
```

### 2.4 扩展性设计
- **单房间**: RoomManager + 业务模块
- **多房间**: GlobalCoordinator + 多个RoomManager
- **插件化**: 插件接口 + 插件管理器

## 3. 详细设计

### 3.1 能量管理系统

#### 类设计
```javascript
class EnergyManager {
  constructor(roomName) {
    this.roomName = roomName;
    this.sources = [];    // EnergySource[]
    this.storages = [];   // EnergyStorage[]
    this.demands = [];    // EnergyDemand[]
  }
  
  analyze() { /* 分析能量状态 */ }
  allocate() { /* 分配能量 */ }
  monitor() { /* 监控能量流 */ }
}

class EnergySource {
  constructor(source) {
    this.id = source.id;
    this.pos = source.pos;
    this.energy = source.energy;
    this.capacity = source.energyCapacity;
  }
  
  getAvailableSpots() { /* 可用采集点 */ }
}

class EnergyDemand {
  constructor(type, priority, amount) {
    this.type = type;     // spawn|build|upgrade|repair|defense
    this.priority = priority; // 1-10
    this.amount = amount;
    this.allocated = 0;
  }
  
  isCritical() { return this.priority >= 8; }
  getRemaining() { return this.amount - this.allocated; }
}
```

#### 关键算法
1. **能量采集优化**
   ```javascript
   function optimizeHarvesterAllocation(sources, creeps) {
     // 按容量排序源
     const sorted = sources.sort((a,b) => b.capacity - a.capacity);
     const allocations = [];
     
     for (const source of sorted) {
       const optimal = source.calculateOptimalHarvesters();
       const available = source.getAvailableSpots();
       const count = Math.min(optimal, available);
       
       const assigned = assignCreeps(creeps, source, count);
       allocations.push({ source, assigned, count });
       
       creeps = creeps.filter(c => !assigned.includes(c));
     }
     
     return allocations;
   }
   ```

2. **能量分配**
   ```javascript
   function allocateEnergy(demands, available) {
     // 排序: 紧急 > 优先级
     const sorted = demands.sort((a,b) => {
       if (a.isCritical() !== b.isCritical())
         return b.isCritical() - a.isCritical();
       return b.priority - a.priority;
     });
     
     const allocations = [];
     let remaining = available;
     
     for (const demand of sorted) {
       if (remaining <= 0) break;
       
       const amount = Math.min(demand.getRemaining(), remaining);
       if (amount > 0) {
         demand.allocated += amount;
         remaining -= amount;
         allocations.push({ demand, amount });
       }
     }
     
     return { allocations, remaining };
   }
   ```

### 3.2 Creep管理系统

#### 类设计
```javascript
class CreepManager {
  constructor(roomName) {
    this.roomName = roomName;
    this.creeps = new Map();    // name -> CreepInfo
    this.roles = new Map();     // roleName -> CreepRole
    this.templates = new Map(); // roleName -> CreepTemplate
  }
  
  analyzeNeeds() { /* 分析需求 */ }
  spawnCreeps() { /* 生成Creep */ }
  manageLifecycle() { /* 生命周期管理 */ }
}

class CreepTemplate {
  constructor(role, config) {
    this.role = role;
    this.minRCL = config.minRCL || 1;
    this.maxRCL = config.maxRCL || 8;
    this.baseBody = config.body || [];
  }
  
  generateBody(energy, rcl) {
    if (rcl < this.minRCL || rcl > this.maxRCL) return null;
    
    let body = [...this.baseBody];
    let cost = calculateCost(body);
    
    // 能量充足优化
    if (energy > cost * 1.5) {
      body = optimizeBody(body, energy - cost);
      cost = calculateCost(body);
    }
    
    // 能量不足简化
    if (cost > energy) {
      body = simplifyBody(body, energy);
      cost = calculateCost(body);
    }
    
    return cost <= energy ? { body, cost } : null;
  }
}

class CreepRole {
  constructor(name, config) {
    this.name = name; // harvester|hauler|builder|upgrader
    this.minCount = config.minCount || 0;
    this.maxCount = config.maxCount || Infinity;
    this.priority = config.priority || 1;
  }
  
  calculateRequiredCount(roomState) {
    let count = this.minCount;
    
    switch (this.name) {
      case 'harvester':
        count = Math.max(count, (roomState.sources || []).length * 2);
        break;
      case 'builder':
        count = Math.max(count, Math.ceil((roomState.constructionSites || []).length / 3));
        break;
      case 'upgrader':
        count = Math.max(count, 2);
        break;
    }
    
    return Math.min(count, this.maxCount);
  }
}
```

#### 关键算法
1. **需求分析**
   ```javascript
   function analyzeCreepNeeds(roomState, roles) {
     const needs = {};
     
     for (const role of roles) {
       const required = role.calculateRequiredCount(roomState);
       const current = getCurrentCreepCount(role.name);
       const deficit = Math.max(0, required - current);
       
       needs[role.name] = { required, current, deficit };
     }
     
     return needs;
   }
   ```

2. **身体配置优化**
   ```javascript
   function optimizeCreepBody(role, energy, rcl) {
     const template = getTemplate(role);
     if (!template) return null;
     
     let body = template.baseBody;
     let cost = calculateCost(body);
     
     // 逐步增加工作部件
     while (cost + BODYPART_COST[WORK] <= energy) {
       body.push(WORK);
       cost += BODYPART_COST[WORK];
     }
     
     return { body, cost };
   }
   ```

### 3.3 角色行为系统

#### 状态机设计
```javascript
class BehaviorStateMachine {
  constructor(creep, role) {
    this.creep = creep;
    this.role = role;
    this.currentState = 'idle';
    this.states = {
      idle: this.handleIdle.bind(this),
      harvesting: this.handleHarvesting.bind(this),
      transporting: this.handleTransporting.bind(this),
      building: this.handleBuilding.bind(this),
      upgrading: this.handleUpgrading.bind(this)
    };
  }
  
  tick() {
    const handler = this.states[this.currentState];
    if (handler) {
      const nextState = handler();
      if (nextState && nextState !== this.currentState) {
        this.transitionTo(nextState);
      }
    }
  }
  
  handleIdle() {
    const task = this.findTask();
    return task ? task.type : 'idle';
  }
  
  handleHarvesting() {
    const creep = this.creep;
    
    if (creep.store.getFreeCapacity() === 0) {
      return 'transporting';
    }
    
    const source = this.getAssignedSource();
    if (source) {
      const result = creep.harvest(source);
      if (result === ERR_NOT_IN_RANGE) {
        creep.moveTo(source);
      }
    }
    
    return 'harvesting';
  }
  
  transitionTo(newState) {
    const oldState = this.currentState;
    this.currentState = newState;
    logStateTransition(this.creep.name, oldState, newState);
  }
}
```

#### 任务调度
```javascript
class TaskScheduler {
  constructor(roomName) {
    this.roomName = roomName;
    this.tasks = new Map();        // taskId -> Task
    this.assignments = new Map();  // creepName -> taskId
  }
  
  generateTasks(roomState) {
    const tasks = [];
    
    // 采集任务
    const sources = roomState.sources || [];
    for (const source of sources) {
      tasks.push(new Task('harvest', source.id, 10));
    }
    
    // 建造任务
    const sites = roomState.constructionSites || [];
    for (const site of sites) {
      tasks.push(new Task('build', site.id, getBuildPriority(site.structureType)));
    }
    
    // 升级任务
    if (roomState.controller) {
      tasks.push(new Task('upgrade', roomState.controller.id, 5));
    }
    
    return tasks;
  }
  
  assignTasks(creeps) {
    const assignments = [];
    const availableTasks = this.getAvailableTasks();
    
    // 按角色和能力分配任务
    for (const creep of creeps) {
      const suitableTasks = availableTasks.filter(task => 
        isCreepSuitableForTask(creep, task)
      );
      
      if (suitableTasks.length > 0) {
        const task = selectBestTask(creep, suitableTasks);
        this.assignments.set(creep.name, task.id);
        assignments.push({ creep: creep.name, task: task.id });
        
        // 从可用任务中移除
        availableTasks.splice(availableTasks.indexOf(task), 1);
      }
    }
    
    return assignments;
  }
}

class Task {
  constructor(type, targetId, priority) {
    this.id = generateId();
    this.type = type;       // harvest|build|upgrade|repair|transport
    this.targetId = targetId;
    this.priority = priority; // 1-10
    this.status = 'pending'; // pending|assigned|in_progress|completed|failed
    this.assignedTo = null;
    this.createdAt = Game.time;
  }
}
```

### 3.4 内存管理系统

#### 内存结构
```javascript
Memory.screepsMoss = {
  version: '1.0.0',
  rooms: {
    [roomName]: {
      // 状态数据
      state: {
        energy: { available: 0, capacity: 0 },
        creeps: { count: 0, byRole: {} },
        structures: { count: 0, byType: {} }
      },
      
      // 配置数据
      config: {
        creepTemplates: {},
        buildingLayout: {},
        energyPriorities: {}
      },
      
      // 历史数据
      history: {
        energyTrend: [],
        creepStats: [],
        performance: []
      }
    }
  },
  
  // 全局数据
  global: {
    stats: {
      uptime: 0,
      totalCreepsSpawned: 0,
      totalEnergyHarvested: 0
    },
    config: {
      loggingLevel: 'info',
      monitoringEnabled: true
    }
  }
};
```

#### 内存管理策略
1. **定期清理**
   ```javascript
   function cleanupMemory() {
     // 清理无效Creep内存
     for (const name in Memory.creeps) {
       if (!Game.creeps[name]) {
         delete Memory.creeps[name];
       }
     }
     
     // 清理过期数据
     const now = Game.time;
     for (const roomName in Memory.screepsMoss.rooms) {
       const room = Memory.screepsMoss.rooms[roomName];
       // 保留最近1000tick数据
       room.history.energyTrend = room.history.energyTrend.slice(-1000);
       room.history.creepStats = room.history.creepStats.slice(-1000);
     }
   }
   ```

2. **数据压缩**
   ```javascript
   function compressMemory() {
     // 压缩历史数据
     for (const roomName in Memory.screepsMoss.rooms) {
       const room = Memory.screepsMoss.rooms[roomName];
       
       // 采样压缩
       if (room.history.energyTrend.length > 100) {
         room.history.energyTrend = sampleData(room.history.energyTrend, 100);
       }
       
       // 删除冗余字段
       if (room.state.creeps.details) {
         delete room.state.creeps.details;
       }
     }
   }
   ```

## 4. 接口设计

### 4.1 模块接口规范

#### EnergyManager接口
```javascript
interface IEnergyManager {
  // 状态查询
  getEnergyStatus(roomName: string): EnergyStatus;
  getSourceUtilization(roomName: string): SourceUtilization[];
  
  // 能量分配
  allocateEnergy(roomName: string, purpose: string, amount: number): AllocationResult;
  getEnergyPriority(purpose: string): number;
  
  // 监控
  monitorEnergyFlow(roomName: string): EnergyFlowData;
  detectEnergyIssues(roomName: string): EnergyIssue[];
}
```

#### CreepManager接口
```javascript
interface ICreepManager {
  // Creep管理
  getCreepStats(roomName: string): CreepStats;
  spawnCreep(roomName: string, role: string): SpawnResult;
  
  // 配置管理
  getCreepTemplates(roomName: string): CreepTemplate[];
  updateCreepTemplate(roomName: string, role: string, template: CreepTemplate): void;
  
  // 生命周期
  manageCreepLifecycle(roomName: string): LifecycleReport;
}
```

### 4.2 数据接口规范

#### 响应格式
```javascript
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
  };
  timestamp: number;
}
```

#### 错误代码
```javascript
const ErrorCodes = {
  // 能量错误
  ENERGY_INSUFFICIENT: 'ENERGY_INSUFFICIENT',
  ENERGY_STORAGE_FULL: 'ENERGY_STORAGE_FULL',
  
  // Creep错误
  CREEP_SPAWN_FAILED: 'CREEP_SPAWN_FAILED',
  CREEP_NOT_FOUND: 'CREEP_NOT_FOUND',
  
  // 系统错误
  MEMORY_LIMIT_EXCEEDED: 'MEMORY_LIMIT_EXCEEDED',
  CPU_LIMIT_EXCEEDED: 'CPU_LIMIT_EXCEEDED'
};
```

## 5. 性能优化设计

### 5.1 CPU优化策略

#### 计算分布
```javascript
class ComputationScheduler {
  constructor() {
    this.heavyTasks = [];
    this.lightTasks = [];
  }
  
  scheduleTask(task, priority) {
    if (task.isHeavy()) {
      this.heavyTasks.push({ task, priority });
    } else {
      this.lightTasks.push({ task, priority });
    }
  }
  
  executeTasks(cpuBudget) {
    let cpuUsed = 0;
    
    // 先执行轻任务
    for (const { task } of this.lightTasks) {
      if (cpuUsed >= cpuBudget * 0.7) break;
      cpuUsed += task.execute();
    }
    
    // 执行重任务（如果还有CPU）
    for (const { task } of this.heavyTasks) {
      if (cpuUsed >= cpuBudget) break;
      cpuUsed += task.execute();
    }
    
    return cpuUsed;
  }
}
```

#### 缓存优化
```javascript
class CacheManager {
  constructor() {
    this.cache = new Map();
    this.ttl = 10; // 缓存有效期（tick）
  }
  
  get(key) {
    const entry = this.cache.get(key);
    if (entry && Game.time - entry.timestamp < this.ttl) {
      return entry.value;
    }
    return null;
  }
  
