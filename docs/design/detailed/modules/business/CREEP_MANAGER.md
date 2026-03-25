# CreepManager 详细设计文档

## 📋 文档信息
- **模块名称**: CreepManager（Creep管理器）
- **所属层级**: 业务层
- **文档版本**: v1.0.0
- **创建日期**: 2026-03-25
- **最后更新**: 2026-03-25
- **负责人**: Moss (OpenClaw AI)
- **状态**: [草案]
- **优先级**: P0 (v1.0核心模块)
- **关联文档**: 
  - `ROOM_MANAGER.md` - 房间管理器设计
  - `ENERGY_MANAGER.md` - 能量管理器设计
  - `ROLE_MANAGER.md` - 角色管理器设计

## 🎯 设计目标

### 核心职责
1. **Creep生命周期管理** - 生成、维护、回收全周期
2. **身体配置优化** - 根据能量和需求优化身体部件
3. **生成队列管理** - 管理Spawn队列和优先级
4. **性能监控** - 监控Creep效率和健康状况
5. **内存管理** - 清理无效Creep内存

### 质量目标
- **性能**: 每tick CPU使用 < 3
- **效率**: Creep生成成功率 > 95%
- **优化**: 身体配置优化率 > 90%
- **可靠性**: 关键Creep中断时间 < 5 ticks

## 🏗️ 类图设计

### 类结构
```
┌─────────────────────────────────────┐
│          CreepManager               │
├─────────────────────────────────────┤
│ - roomName: string                  │
│ - creeps: Map<string, CreepInfo>    │
│ - roles: Map<string, CreepRole>     │
│ - templates: Map<string, CreepTemplate>
│ - spawnQueue: PriorityQueue<SpawnRequest>
│ - activeSpawns: Map<string, SpawnInfo>
│ - config: CreepConfig               │
│ - stats: CreepStats                 │
│ - cache: CreepCache                 │
├─────────────────────────────────────┤
│ + constructor(roomName: string)     │
│ + init(config: CreepConfig): boolean│
│ + tick(roomState: RoomState): CreepTickResult
│ + analyzeCreepNeeds(): CreepNeeds   │
│ + spawnCreep(role: string): SpawnResult
│ + manageLifecycle(): LifecycleReport│
│ + getCreepStats(): CreepStats       │
│ + getTemplate(role: string): CreepTemplate
│ + updateTemplate(role, template): void
│ - updateCreepRegistry(): void       │
│ - processSpawnQueue(): void         │
│ - optimizeBodyConfigs(): void       │
│ - cleanupDeadCreeps(): void         │
│ - monitorCreepHealth(): void        │
│ - balanceRoleDistribution(): void   │
└─────────────────────────────────────┘
```

### 核心组件
```
CreepManager
    ├── CreepRegistry        - Creep注册和跟踪
    ├── TemplateManager      - 身体模板管理
    ├── SpawnQueueManager    - 生成队列管理
    ├── BodyOptimizer        - 身体配置优化
    ├── LifecycleManager     - 生命周期管理
    └── HealthMonitor        - 健康状态监控
```

## 📝 接口定义

### 公共接口

#### 1. 初始化接口
```javascript
/**
 * 初始化Creep管理器
 * @param {CreepConfig} config - Creep配置
 * @returns {boolean} 初始化是否成功
 */
init(config: CreepConfig): boolean
```

#### 2. Tick处理接口
```javascript
/**
 * 处理Creep tick
 * @param {RoomState} roomState - 房间状态
 * @returns {CreepTickResult} tick处理结果
 */
tick(roomState: RoomState): CreepTickResult
```

#### 3. 需求分析接口
```javascript
/**
 * 分析Creep需求
 * @returns {CreepNeeds} Creep需求分析结果
 */
analyzeCreepNeeds(): CreepNeeds
```

#### 4. 生成接口
```javascript
/**
 * 生成Creep
 * @param {string} role - 角色名称
 * @param {CreepConfig} [config] - 可选配置
 * @returns {SpawnResult} 生成结果
 */
spawnCreep(role: string, config?: CreepConfig): SpawnResult
```

#### 5. 生命周期管理接口
```javascript
/**
 * 管理Creep生命周期
 * @returns {LifecycleReport} 生命周期管理报告
 */
manageLifecycle(): LifecycleReport
```

#### 6. 模板管理接口
```javascript
/**
 * 获取Creep模板
 * @param {string} role - 角色名称
 * @returns {CreepTemplate} Creep模板
 */
getTemplate(role: string): CreepTemplate

/**
 * 更新Creep模板
 * @param {string} role - 角色名称
 * @param {CreepTemplate} template - 新模板
 */
updateTemplate(role: string, template: CreepTemplate): void
```

### 数据类型定义

#### CreepConfig
```javascript
interface CreepConfig {
  // 角色配置
  roles: {
    [role: string]: RoleConfig;
  };
  
  // 生成配置
  spawning: {
    maxQueueSize: number;              // 最大队列大小
    priorityLevels: number;            // 优先级级别数量
    emergencySpawnThreshold: number;   // 紧急生成阈值
    preSpawnBuffer: number;            // 预生成缓冲时间（ticks）
  };
  
  // 身体配置
  body: {
    optimizationStrategy: 'balanced' | 'efficient' | 'durable';
    minBodyParts: number;              // 最小身体部件数
    maxBodyParts: number;              // 最大身体部件数
    upgradeThresholds: {               // 升级阈值（RCL）
      [rcl: number]: number;           // RCL -> 最大身体部件
    };
  };
  
  // 生命周期配置
  lifecycle: {
    renewalThreshold: number;          // 续命阈值（剩余ticks）
    emergencyRenewal: number;          // 紧急续命阈值
    recycleThreshold: number;          // 回收阈值（剩余ticks）
    cleanupInterval: number;           // 清理间隔（ticks）
  };
  
  // 监控配置
  monitoring: {
    enabled: boolean;
    healthCheckInterval: number;
    efficiencySampling: number;
    alertThresholds: {
      lowEfficiency: number;           // 低效率阈值
      highMortality: number;           // 高死亡率阈值
      spawnFailure: number;            // 生成失败阈值
    };
  };
}
```

#### CreepTickResult
```javascript
interface CreepTickResult {
  success: boolean;                    // 是否成功
  cpuUsed: number;                     // CPU使用量
  actions: {                           // 执行的动作
    spawned: SpawnedCreep[];           // 生成的Creep
    renewed: RenewedCreep[];           // 续命的Creep
    recycled: RecycledCreep[];         // 回收的Creep
    cleaned: CleanedCreep[];           // 清理的Creep
  };
  stats: CreepStats;                   // 当前统计
  needs: CreepNeeds;                   // 需求分析
  issues: CreepIssue[];                // 检测到的问题
  warnings: Warning[];                 // 警告信息
}
```

#### CreepNeeds
```javascript
interface CreepNeeds {
  // 按角色需求
  byRole: {
    [role: string]: {
      required: number;                // 需要数量
      current: number;                 // 当前数量
      deficit: number;                 // 缺口数量
      priority: number;                // 优先级（1-10）
      urgency: 'low' | 'medium' | 'high' | 'critical';
    };
  };
  
  // 总体需求
  overall: {
    totalRequired: number;             // 总需要数量
    totalCurrent: number;              // 总当前数量
    totalDeficit: number;              // 总缺口数量
    avgPriority: number;               // 平均优先级
    criticalRoles: string[];           // 关键角色列表
  };
  
  // 生成能力
  spawningCapacity: {
    availableSpawns: number;           // 可用Spawn数量
    queueLength: number;               // 队列长度
    estimatedTime: number;             // 预计完成时间（ticks）
    energyAvailable: number;           // 可用能量
    energyRequired: number;            // 需要能量
  };
  
  // 建议
  recommendations: {
    immediate: string[];               // 立即行动建议
    shortTerm: string[];               // 短期建议
    longTerm: string[];                // 长期建议
  };
}
```

#### SpawnResult
```javascript
interface SpawnResult {
  success: boolean;                    // 是否成功
  creepName?: string;                  // Creep名称（如果成功）
  body: BodyPartConstant[];            // 身体配置
  cost: number;                        // 能量成本
  spawnId?: string;                    // Spawn ID
  queuePosition?: number;              // 队列位置
  estimatedTime?: number;              // 预计时间（ticks）
  error?: string;                      // 错误信息
  warnings?: string[];                 // 警告信息
}
```

## 🔧 算法设计

### 1. 需求分析算法

#### 角色需求计算
```javascript
calculateRoleRequirements(roomState, rolesConfig) {
  const requirements = {};
  
  Object.entries(rolesConfig).forEach(([role, config]) => {
    let required = config.minCount || 0;
    
    // 根据房间状态动态计算需求
    switch (role) {
      case 'harvester':
        required = this.calculateHarvesterRequirement(roomState, config);
        break;
      case 'hauler':
        required = this.calculateHaulerRequirement(roomState, config);
        break;
      case 'builder':
        required = this.calculateBuilderRequirement(roomState, config);
        break;
      case 'upgrader':
        required = this.calculateUpgraderRequirement(roomState, config);
        break;
      case 'repairer':
        required = this.calculateRepairerRequirement(roomState, config);
        break;
      case 'defender':
        required = this.calculateDefenderRequirement(roomState, config);
        break;
      default:
        required = config.minCount || 1;
    }
    
    // 应用配置限制
    required = Math.max(config.minCount || 0, required);
    required = Math.min(config.maxCount || Infinity, required);
    
    // 获取当前数量
    const current = this.getCurrentCreepCount(role);
    const deficit = Math.max(0, required - current);
    
    // 计算紧急程度
    const urgency = this.calculateUrgency(role, deficit, config);
    
    requirements[role] = {
      required,
      current,
      deficit,
      priority: config.priority || 1,
      urgency,
      config
    };
  });
  
  return requirements;
}
```

#### Harvester需求计算
```javascript
calculateHarvesterRequirement(roomState, config) {
  let required = config.minCount || 2;
  
  // 1. 基于能量源数量
  const sources = roomState.energy.sources || [];
  required = Math.max(required, sources.length * 2); // 每个源2个Harvester
  
  // 2. 基于能量需求
  const energyDemand = this.estimateEnergyDemand(roomState);
  const harvesterOutput = this.estimateHarvesterOutput();
  const neededForDemand = Math.ceil(energyDemand / harvesterOutput);
  required = Math.max(required, neededForDemand);
  
  // 3. 基于房间等级
  const rcl = roomState.controller?.level || 1;
  required = Math.max(required, Math.floor(rcl * 1.5));
  
  // 4. 考虑效率因素
  const efficiency = this.getHarvesterEfficiency();
  if (efficiency < 0.8) {
    required = Math.ceil(required * (1 / efficiency));
  }
  
  return required;
}
```

#### 紧急程度计算
```javascript
calculateUrgency(role, deficit, config) {
  // 基础紧急程度
  let urgencyScore = 0;
  
  // 1. 缺口比例
  const deficitRatio = deficit / (config.minCount || 1);
  urgencyScore += deficitRatio * 40; // 最多40分
  
  // 2. 角色重要性
  const roleImportance = {
    harvester: 30,
    hauler: 25,
    upgrader: 20,
    builder: 15,
    repairer: 10,
    defender: 5
  };
  urgencyScore += roleImportance[role] || 10;
  
  // 3. 时间因素（如果已经缺了很久）
  const timeSinceDeficit = this.getTimeSinceDeficit(role);
  urgencyScore += Math.min(timeSinceDeficit / 10, 20); // 最多20分
  
  // 4. 房间状态影响
  const roomImpact = this.getRoomImpact(role);
  urgencyScore += roomImpact * 10;
  
  // 转换为紧急级别
  if (urgencyScore >= 70) return 'critical';
  if (urgencyScore >= 50) return 'high';
  if (urgencyScore >= 30) return 'medium';
  return 'low';
}
```

### 2. 身体配置优化算法

#### 智能身体生成
```javascript
optimizeCreepBody(role, availableEnergy, rcl, template) {
  // 1. 获取基础模板
  let body = [...template.baseBody];
  let cost = this.calculateBodyCost(body);
  
  // 2. 检查RCL限制
  const maxParts = this.getMaxBodyParts(rcl);
  if (body.length > maxParts) {
    body = body.slice(0, maxParts);
    cost = this.calculateBodyCost(body);
  }
  
  // 3. 能量充足优化
  if (availableEnergy > cost * 1.5) {
    body = this.enhanceBody(body, availableEnergy - cost, role);
    cost = this.calculateBodyCost(body);
  }
  
  // 4. 能量不足简化
  if (cost > availableEnergy) {
    body = this.simplifyBody(body, availableEnergy, role);
    cost = this.calculateBodyCost(body);
  }
  
  // 5. 验证和调整
  if (cost > availableEnergy) {
    // 如果还是太贵，使用最小配置
    body = this.getMinimalBody(role);
    cost = this.calculateBodyCost(body);
  }
  
  // 6. 确保有移动部件
  if (!body.includes(MOVE)) {
    // 在合适位置插入移动部件
    body = this.insertMoveParts(body, role);
    cost = this.calculateBodyCost(body);
    
    // 如果还是太贵，移除一些工作部件
    while (cost > availableEnergy && body.filter(p => p === WORK).length > 0) {
      const workIndex = body.lastIndexOf(WORK);
      if (workIndex !== -1) {
        body.splice(workIndex, 1);
        cost = this.calculateBodyCost(body);
      }
    }
  }
  
  return {
    body,
    cost,
    efficiency: this.calculateBodyEfficiency(body, role),
    durability: this.calculateBodyDurability(body)
  };
}
```

#### 身体增强策略
```javascript
enhanceBody(body, extraEnergy, role) {
  const enhanced = [...body];
  let remainingEnergy = extraEnergy;
  
  // 根据角色类型增强
  switch (role) {
    case 'harvester':
      // Harvester: 增加工作部件
      while (remainingEnergy >= BODYPART_COST[WORK] && 
             this.countParts(enhanced, WORK) < 5) {
        enhanced.push(WORK);
        remainingEnergy -= BODYPART_COST[WORK];
      }
      break;
      
    case 'hauler':
      // Hauler: 增加运输部件
      while (remainingEnergy >= BODYPART_COST[CARRY] && 
             this.countParts(enhanced, CARRY) < 10) {
        enhanced.push(CARRY);
        remainingEnergy -= BODYPART_COST[CARRY];
      }
      break;
      
    case 'builder':
    case 'upgrader':
      // Builder/Upgrader: 平衡增强
      const workCount = this.countParts(enhanced, WORK);
      const carryCount = this.countParts(enhanced, CARRY);
      
      // 确保工作部件和运输部件平衡
      while (remainingEnergy > 0) {
        if (workCount <= carryCount && remainingEnergy >= BODYPART_COST[WORK]) {
          enhanced.push(WORK);
          remainingEnergy -= BODYPART_COST[WORK];
        } else if (remainingEnergy >= BODYPART_COST[CARRY]) {
          enhanced.push(CARRY);
          remainingEnergy -= BODYPART_COST[CARRY];
        } else {
          break;
        }
      }
      break;
      
    case 'defender':
      // Defender: 增加攻击部件
      while (remainingEnergy >= BODYPART_COST[ATTACK] && 
             this.countParts(enhanced, ATTACK) < 5) {
        enhanced.push(ATTACK);
        remainingEnergy -= BODYPART_COST[ATTACK];
      }
      break;
  }
  
  // 如果还有剩余能量，增加移动部件
  while (remainingEnergy >= BODYPART_COST[MOVE]) {
    enhanced.push(MOVE);
    remainingEnergy -= BODYPART_COST[MOVE];
  }
  
  return enhanced;
}
```

#### 身体简化策略
```javascript
simplifyBody(body, availableEnergy, role) {
  const simplified = [...body];
  let cost = this.calculateBodyCost(simplified);
  
  // 简化策略：从最不重要的部件开始移除
  const removalPriority = this.getRemovalPriority(role);
  
  for (const partType of removalPriority) {
    while (cost > availableEnergy && simplified.includes(partType)) {
      const index = simplified.lastIndexOf(partType);
      if (index !== -1) {
        simplified.splice(index, 1);
        cost = this.calculateBodyCost(simplified);
      }
    }
    
    if (cost <= availableEnergy) break;
  }
  
  // 如果还是太贵，使用角色特定的最小配置
  if (cost > availableEnergy) {
    return this.getMinimalBody(role);
  }
  
  return simplified;
}

getRemovalPriority(role) {
  // 根据角色确定部件移除优先级（最后移除的最重要）
  const priorities = {
    harvester: [CARRY, MOVE, WORK],      // Harvester: 工作部件最重要
    hauler: [MOVE, CARRY],               // Hauler: 运输部件最重要
    builder: [MOVE, CARRY, WORK],        // Builder: 工作部件最重要
    upgrader: [MOVE, CARRY, WORK],       // Upgrader: 工作部件最重要
    defender: [MOVE, ATTACK, TOUGH]      // Defender: 攻击部件最重要
  };
  
  return priorities[role] || [MOVE, CARRY, WORK, ATTACK, RANGED_ATTACK, HEAL, CLAIM, TOUGH];
}
```

### 3. 生成队列管理算法

#### 优先级队列管理
```javascript
class SpawnPriorityQueue {
  constructor() {
    this.queue = [];
    this.maxSize = 10;
    this.priorityLevels = 5; // 1-5，5最高
  }
  
  addRequest(request) {
    // 计算请求的优先级分数
    const priorityScore = this.calculatePriorityScore(request);
    
    const queueItem = {
      ...request,
      priorityScore,
      addedAt: Game.time,
      estimatedCost: this.estimateSpawnCost(request)
    };
    
    // 插入到合适位置（按优先级降序）
    let inserted = false;
    for (let i = 0; i < this.queue.length; i++) {
      if (priorityScore > this.queue[i].priorityScore) {
        this.queue.splice(i, 0, queueItem);
        inserted = true;
        break;
      }
    }
    
    if (!inserted) {
      this.queue.push(queueItem);
    }
    
    // 保持队列大小
    if (this.queue.length > this.maxSize) {
      this.queue = this.queue.slice(0, this.maxSize);
    }
    
    return {
      position: this.queue.indexOf(queueItem) + 1,
      total: this.queue.length,
      estimatedWait: this.estimateWaitTime(queueItem)
    };
  }
  
  calculatePriorityScore(request) {
    let score = 0;
    
    // 1. 基础优先级（1-5映射到0-40分）
    score += (request.priority || 1) * 8;
    
    // 2. 紧急程度加成
    const urgencyBonus = {
      critical: 30,
      high: 20,
      medium: 10,
      low: 0
    };
    score += urgencyBonus[request.urgency] || 0;
    
    // 3. 等待时间加成（等待越久分数越高）
    if (request.waitTime) {
      score += Math.min(request.waitTime / 10, 20);
    }
    
    // 4. 角色重要性加成
    const roleBonus = {
      harvester: 25,
      hauler: 20,
      upgrader: 15,
      builder: 10,
      repairer: 5,
      defender: 5
    };
    score += roleBonus[request.role] || 0;
    
    // 5. 能量效率加成（成本低的优先）
    const estimatedCost = this.estimateSpawnCost(request);
    if (estimatedCost < 500) {
      score += 5;
    }
    
    return Math.min(score, 100); // 限制最大分数
  }
  
  getNextRequest(availableEnergy) {
    for (let i = 0; i < this.queue.length; i++) {
      const request = this.queue[i];
      
      // 检查是否有足够能量
      if (request.estimatedCost <= availableEnergy) {
        // 检查是否有可用Spawn
        const availableSpawn = this.findAvailableSpawn();
        if (availableSpawn) {
          return {
            request,
            spawn: availableSpawn,
            queuePosition: i + 1
          };
        }
      }
    }
    
    return null;
  }
  
  removeRequest(requestId) {
    const index = this.queue.findIndex(item => item.id === requestId);
    if (index !== -1) {
      this.queue.splice(index, 1);
      return true;
    }
    return false;
  }
  
  estimateWaitTime(request) {
    const position = this.queue.indexOf(request);
    if (position === -1) return 0;
    
    let totalTime = 0;
    
    // 计算前面所有请求的预计时间
    for (let i = 0; i < position; i++) {
      const item = this.queue[i];
      totalTime += this.estimateSpawnTime(item);
    }
    
    return totalTime;
  }
}
```

#### 生成调度算法
```javascript
processSpawnQueue() {
  const results = {
    spawned: [],
    failed: [],
    skipped: [],
    queueStatus: {}
  };
  
  // 获取当前能量状态
  const energyStatus = this.energyManager.getEnergyStatus();
  const availableEnergy = energyStatus.overall.available;
  
  // 获取可用Spawn
  const availableSpawns = this.getAvailableSpawns();
  
  if (availableSpawns.length === 0 || this.spawnQueue.length === 0) {
    return results;
  }
  
  // 处理每个可用Spawn
  availableSpawns.forEach(spawn => {
    if (this.spawnQueue.length === 0) return;
    
    // 获取下一个合适的请求
    const nextRequest = this.spawnQueue.getNextRequest(availableEnergy);
    if (!nextRequest) return;
    
    // 尝试生成
    const spawnResult = this.attemptSpawn(spawn, nextRequest.request);
    
    if (spawnResult.success) {
      // 生成成功，从队列移除
      this.spawnQueue.removeRequest(nextRequest.request.id);
      results.spawned.push(spawnResult);
      
      // 更新能量状态
      availableEnergy -= spawnResult.cost;
    } else {
      // 生成失败，处理失败
      this.handleSpawnFailure(spawnResult, nextRequest.request);
      results.failed.push({
        request: nextRequest.request,
        error: spawnResult.error,
        spawn: spawn.name
      });
    }
  });
  
  // 更新队列状态
  results.queueStatus = {
    length: this.spawnQueue.length,
    nextUrgent: this.getNextUrgentRequest(),
    estimatedCompletion: this.estimateQueueCompletionTime()
  };
  
  return results;
}

attemptSpawn(spawn, request) {
  try {
    // 1. 验证请求
    this.validateSpawnRequest(request);
    
    // 2. 优化身体配置
    const bodyConfig = this.optimizeCreepBody(
      request.role,
      request.maxCost || Infinity,
      this.room.controller.level,
      this.getTemplate(request.role)
    );
    
    // 3. 检查能量是否足够
    if (bodyConfig.cost > spawn.room.energyAvailable) {
      return {
        success: false,
        error: '能量不足',
        required: bodyConfig.cost,
        available: spawn.room.energyAvailable
      };
    }
    
    // 4. 执行生成
    const creepName = this.generateCreepName(request.role);
    const spawnResult = spawn.spawnCreep(
      bodyConfig.body,
      creepName,
      {
        memory: {
          role: request.role,
          born: Game.time,
          config: request.config || {},
          body: bodyConfig.body,
          cost: bodyConfig.cost
        }
      }
    );
    
    if (spawnResult === OK) {
      // 生成成功
      const spawning = spawn.spawning;
      
      return {
        success: true,
        creepName,
        body: bodyConfig.body,
        cost: bodyConfig.cost,
        spawn: spawn.name,
        spawning: {
          name: spawning.name,
          remainingTime: spawning.remainingTime,
          needTime: spawning.needTime
        },
        efficiency: bodyConfig.efficiency,
        estimatedLifespan: this.estimateCreepLifespan(bodyConfig.body)
      };
    } else {
      // 生成失败
      return {
        success: false,
        error: this.getSpawnErrorDescription(spawnResult),
        errorCode: spawnResult,
        spawn: spawn.name
      };
    }
    
  } catch (error) {
    return {
      success: false,
      error: error.message,
      spawn: spawn.name,
      stack: error.stack
    };
  }
}
```

### 4. 生命周期管理算法

#### Creep续命算法
```javascript
manageCreepRenewal() {
  const renewalCandidates = [];
  const renewalResults = [];
  
  // 1. 收集需要续命的Creep
  this.creeps.forEach((creep, creepName) => {
    if (this.shouldRenewCreep(creep)) {
      renewalCandidates.push({
        creep,
        creepName,
        priority: this.calculateRenewalPriority(creep)
      });
    }
  });
  
  // 2. 按优先级排序
  renewalCandidates.sort((a, b) => b.priority - a.priority);
  
  // 3. 处理续命
  renewalCandidates.forEach(candidate => {
    if (renewalResults.length >= this.config.lifecycle.maxRenewalsPerTick) {
      return; // 限制每tick续命数量
    }
    
    const renewalResult = this.attemptRenewal(candidate.creep, candidate.creepName);
    renewalResults.push(renewalResult);
    
    if (renewalResult.success) {
      // 更新Creep状态
      candidate.creep.renewedAt = Game.time;
      candidate.creep.renewalCount = (candidate.creep.renewalCount || 0) + 1;
    }
  });
  
  return {
    renewed: renewalResults.filter(r => r.success),
    failed: renewalResults.filter(r => !r.success),
    skipped: renewalCandidates.length - renewalResults.length,
    totalCandidates: renewalCandidates.length
  };
}

shouldRenewCreep(creep) {
  // 1. 检查是否还活着
  if (!creep || !creep.ticksToLive) return false;
  
  // 2. 检查续命阈值
  const renewalThreshold = creep.role === 'harvester' 
    ? this.config.lifecycle.emergencyRenewal
    : this.config.lifecycle.renewalThreshold;
  
  if (creep.ticksToLive > renewalThreshold) return false;
  
  // 3. 检查是否已经续命过多次
  const maxRenewals = this.getMaxRenewals(creep.role);
  if ((creep.renewalCount || 0) >= maxRenewals) return false;
  
  // 4. 检查Creep的价值（成本 vs 剩余价值）
  const creepValue = this.calculateCreepValue(creep);
  const renewalCost = this.estimateRenewalCost(creep);
  
  if (creepValue < renewalCost * 0.5) return false;
  
  // 5. 检查是否有可用Spawn
  const availableSpawn = this.findRenewalSpawn(creep);
  if (!availableSpawn) return false;
  
  return true;
}

calculateRenewalPriority(creep) {
  let priority = 0;
  
  // 1. 角色重要性
  const rolePriority = {
    harvester: 100,
    hauler: 80,
    upgrader: 60,
    builder: 40,
    repairer: 20,
    defender: 30
  };
  priority += rolePriority[creep.role] || 10;
  
  // 2. 剩余时间（越少越紧急）
  priority += (1500 - creep.ticksToLive) / 10; // 最多150分
  
  // 3. Creep效率（效率高的优先）
  const efficiency = this.getCreepEfficiency(creep.name);
  priority += efficiency * 50; // 最多50分
  
  // 4. 身体成本（成本高的优先）
  priority += Math.min(creep.bodyCost / 100, 30); // 最多30分
  
  // 5. 续命次数（续命次数少的优先）
  priority -= (creep.renewalCount || 0) * 10;
  
  return Math.max(0, priority);
}
```

#### Creep回收算法
```javascript
manageCreepRecycling() {
  const recycleCandidates = [];
  const recycleResults = [];
  
  // 1. 收集需要回收的Creep
  this.creeps.forEach((creep, creepName) => {
    if (this.shouldRecycleCreep(creep)) {
      recycleCandidates.push({
        creep,
        creepName,
        priority: this.calculateRecyclePriority(creep)
      });
    }
  });
  
  // 2. 按优先级排序（优先级高的先回收）
  recycleCandidates.sort((a, b) => b.priority - a.priority);
  
  // 3. 处理回收
  recycleCandidates.forEach(candidate => {
    const recycleResult = this.attemptRecycle(candidate.creep, candidate.creepName);
    recycleResults.push(recycleResult);
    
    if (recycleResult.success) {
      // 从注册表中移除
      this.creeps.delete(candidate.creepName);
      
      // 记录回收
      this.stats.totalRecycled++;
      this.stats.energyRecovered += recycleResult.energyRecovered;
    }
  });
  
  return {
    recycled: recycleResults.filter(r => r.success),
    failed: recycleResults.filter(r => !r.success),
    totalCandidates: recycleCandidates.length,
    totalEnergy: recycleResults.reduce((sum, r) => sum + (r.energyRecovered || 0), 0)
  };
}

shouldRecycleCreep(creep) {
  // 1. 检查是否还活着
  if (!creep || !creep.ticksToLive) return false;
  
  // 2. 检查回收阈值
  if (creep.ticksToLive > this.config.lifecycle.recycleThreshold) return false;
  
  // 3. 检查Creep是否在执行关键任务
  if (this.isCreepOnCriticalTask(creep.name)) return false;
  
  // 4. 检查回收的经济性
  const recycleValue = this.estimateRecycleValue(creep);
  const renewalCost = this.estimateRenewalCost(creep);
  
  // 如果续命成本高于回收价值，考虑回收
  if (renewalCost > recycleValue * 1.5) return true;
  
  // 5. 检查是否有更紧急的生成需求
  const urgentNeeds = this.getUrgentCreepNeeds();
  if (urgentNeeds.length > 0) {
    // 如果这个Creep的角色不是紧急需要的，可以回收
    if (!urgentNeeds.includes(creep.role)) return true;
  }
  
  return false;
}

calculateRecyclePriority(creep) {
  let priority = 0;
  
  // 1. 剩余时间（越少优先级越高）
  priority += (1500 - creep.ticksToLive) / 15; // 最多100分
  
  // 2. 角色重要性（不重要的优先回收）
  const roleImportance = {
    harvester: -50,
    hauler: -30,
    upgrader: -20,
    builder: -10,
    repairer: 0,
    defender: 0
  };
  priority += roleImportance[creep.role] || 10;
  
  // 3. Creep效率（效率低的优先回收）
  const efficiency = this.getCreepEfficiency(creep.name);
  priority += (1 - efficiency) * 40; // 最多40分
  
  // 4. 身体老化（续命次数多的优先回收）
  priority += (creep.renewalCount || 0) * 5;
  
  // 5. 能量回收价值（价值高的优先回收）
  const recycleValue = this.estimateRecycleValue(creep);
  priority += Math.min(recycleValue / 100, 20); // 最多20分
  
  return Math.max(0, priority);
}
```

## 🗃️ 数据结构

### 1. Creep信息数据结构
```javascript
class CreepInfo {
  constructor(creep) {
    this.name = creep.name;
    this.id = creep.id;
    this.role = creep.memory.role || 'unknown';
    this.body = creep.body.map(part => ({
      type: part.type,
      hits: part.hits,
      boost: part.boost
    }));
    this.bodyCost = this.calculateBodyCost
