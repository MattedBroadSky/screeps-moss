# EnergyManager 详细设计文档

## 📋 文档信息
- **模块名称**: EnergyManager（能量管理器）
- **所属层级**: 业务层
- **文档版本**: v1.0.0
- **创建日期**: 2026-03-25
- **最后更新**: 2026-03-25
- **负责人**: Moss (OpenClaw AI)
- **状态**: [草案]
- **优先级**: P0 (v1.0核心模块)
- **关联文档**: 
  - `ROOM_MANAGER.md` - 房间管理器设计
  - `CREEP_MANAGER.md` - Creep管理器设计

## 🎯 设计目标

### 核心职责
1. **能量状态监控** - 实时监控能量采集、存储、消耗
2. **能量分配优化** - 智能分配能量到不同用途
3. **采集效率优化** - 优化Harvester分配和路径
4. **供应链管理** - 管理能量从采集到消耗的全流程

### 质量目标
- **性能**: 每tick CPU使用 < 3
- **准确性**: 能量预测准确率 > 90%
- **效率**: 能量采集效率 > 80%
- **可靠性**: 能量中断恢复时间 < 10 ticks

## 🏗️ 类图设计

### 类结构
```
┌─────────────────────────────────────┐
│          EnergyManager              │
├─────────────────────────────────────┤
│ - roomName: string                  │
│ - sources: Map<string, EnergySource>│
│ - storages: Map<string, EnergyStorage>
│ - demands: PriorityQueue<EnergyDemand>
│ - allocations: Map<string, Allocation>
│ - config: EnergyConfig              │
│ - stats: EnergyStats                │
│ - cache: EnergyCache                │
├─────────────────────────────────────┤
│ + constructor(roomName: string)     │
│ + init(config: EnergyConfig): boolean
│ + tick(roomState: RoomState): EnergyTickResult
│ + analyzeEnergyStatus(): EnergyStatus│
│ + allocateEnergy(purpose, amount): AllocationResult
│ + monitorEnergyFlow(): EnergyFlowData│
│ + getSourceUtilization(): SourceUtilization[]
│ + detectEnergyIssues(): EnergyIssue[]│
│ - updateSources(): void             │
│ - updateStorages(): void            │
│ - analyzeDemands(): void            │
│ - optimizeAllocations(): void       │
│ - executeTransfers(): void          │
│ - recordMetrics(): void             │
└─────────────────────────────────────┘
```

### 核心组件
```
EnergyManager
    ├── EnergySourceManager    - 能量源管理
    ├── EnergyStorageManager   - 能量存储管理
    ├── EnergyDemandAnalyzer   - 需求分析
    ├── EnergyAllocator        - 能量分配器
    ├── EnergyTransferExecutor - 转移执行器
    └── EnergyMonitor          - 能量监控
```

## 📝 接口定义

### 公共接口

#### 1. 初始化接口
```javascript
/**
 * 初始化能量管理器
 * @param {EnergyConfig} config - 能量配置
 * @returns {boolean} 初始化是否成功
 */
init(config: EnergyConfig): boolean
```

#### 2. Tick处理接口
```javascript
/**
 * 处理能量tick
 * @param {RoomState} roomState - 房间状态
 * @returns {EnergyTickResult} tick处理结果
 */
tick(roomState: RoomState): EnergyTickResult
```

#### 3. 状态查询接口
```javascript
/**
 * 分析能量状态
 * @returns {EnergyStatus} 能量状态
 */
analyzeEnergyStatus(): EnergyStatus

/**
 * 获取能量源利用率
 * @returns {SourceUtilization[]} 能量源利用率数据
 */
getSourceUtilization(): SourceUtilization[]

/**
 * 检测能量问题
 * @returns {EnergyIssue[]} 检测到的问题
 */
detectEnergyIssues(): EnergyIssue[]
```

#### 4. 能量分配接口
```javascript
/**
 * 分配能量
 * @param {string} purpose - 用途（spawn/build/upgrade/repair/defense）
 * @param {number} amount - 请求数量
 * @returns {AllocationResult} 分配结果
 */
allocateEnergy(purpose: string, amount: number): AllocationResult
```

#### 5. 监控接口
```javascript
/**
 * 监控能量流
 * @returns {EnergyFlowData} 能量流数据
 */
monitorEnergyFlow(): EnergyFlowData
```

### 数据类型定义

#### EnergyConfig
```javascript
interface EnergyConfig {
  // 采集配置
  harvesting: {
    minHarvesterPerSource: number;    // 每个源最少Harvester
    maxHarvesterPerSource: number;    // 每个源最多Harvester
    optimalUtilization: number;       // 最优利用率（0-1）
    emergencyThreshold: number;       // 紧急阈值（0-1）
  };
  
  // 分配配置
  allocation: {
    strategy: 'balanced' | 'emergency' | 'growth'; // 分配策略
    priorities: {                   // 优先级配置（1-10）
      spawn: number;
      build: number;
      upgrade: number;
      repair: number;
      defense: number;
    };
    emergencyLevels: {              // 紧急级别配置
      critical: number;             // 临界值（能量比例）
      warning: number;              // 警告值
      normal: number;               // 正常值
    };
  };
  
  // 存储配置
  storage: {
    minReserve: number;             // 最小储备量
    transferBatchSize: number;      // 转移批量大小
    balanceInterval: number;        // 平衡间隔（ticks）
  };
  
  // 监控配置
  monitoring: {
    enabled: boolean;
    samplingInterval: number;
    alertThresholds: {
      lowEnergy: number;
      inefficientHarvesting: number;
      unbalancedStorage: number;
    };
  };
}
```

#### EnergyTickResult
```javascript
interface EnergyTickResult {
  success: boolean;                    // 是否成功
  cpuUsed: number;                     // CPU使用量
  actions: {                           // 执行的动作
    harvesting: HarvestingAction[];
    transfers: TransferAction[];
    allocations: AllocationAction[];
  };
  status: EnergyStatus;                // 当前状态
  issues: EnergyIssue[];               // 检测到的问题
  warnings: Warning[];                 // 警告信息
  predictions: EnergyPredictions;      // 能量预测
}
```

#### EnergyStatus
```javascript
interface EnergyStatus {
  // 总体状态
  overall: {
    available: number;                 // 可用能量
    capacity: number;                  // 总容量
    utilization: number;               // 利用率（0-1）
    trend: 'increasing' | 'decreasing' | 'stable';
    emergencyLevel: 'normal' | 'warning' | 'critical';
  };
  
  // 采集状态
  harvesting: {
    sources: SourceStatus[];           // 能量源状态
    totalHarvested: number;            // 本tick采集总量
    efficiency: number;                // 采集效率（0-1）
    assignedHarvesters: number;        // 分配的Harvester数量
    optimalHarvesters: number;         // 最优Harvester数量
  };
  
  // 存储状态
  storage: {
    storages: StorageStatus[];         // 存储设施状态
    totalStored: number;               // 存储总量
    distribution: {                    // 能量分布
      spawns: number;
      extensions: number;
      storage: number;
      other: number;
    };
    balanceScore: number;              // 平衡度评分（0-1）
  };
  
  // 需求状态
  demands: {
    active: DemandStatus[];            // 活跃需求
    totalRequested: number;            // 总请求量
    totalAllocated: number;            // 总分配量
    satisfactionRate: number;          // 满足率（0-1）
    waitingTime: number;               // 平均等待时间（ticks）
  };
  
  // 时间信息
  timestamp: number;
  tickNumber: number;
}
```

#### AllocationResult
```javascript
interface AllocationResult {
  success: boolean;                    // 是否成功
  allocated: number;                   // 实际分配量
  requested: number;                   // 请求量
  remaining: number;                   // 剩余可用量
  priority: number;                    // 分配优先级
  waitTime: number;                    // 预计等待时间
  reason?: string;                     // 失败原因
  suggestions?: AllocationSuggestion[]; // 优化建议
}
```

## 🔧 算法设计

### 1. 能量采集优化算法

#### Harvester分配算法
```javascript
optimizeHarvesterAllocation(sources, availableHarvesters) {
  // 1. 计算每个源的最优Harvester数量
  const sourceNeeds = sources.map(source => ({
    source,
    optimal: this.calculateOptimalHarvesters(source),
    current: this.getAssignedHarvesters(source),
    deficit: 0
  }));
  
  // 2. 计算总需求和缺口
  let totalOptimal = sourceNeeds.reduce((sum, need) => sum + need.optimal, 0);
  let totalCurrent = sourceNeeds.reduce((sum, need) => sum + need.current, 0);
  let totalDeficit = Math.max(0, totalOptimal - totalCurrent);
  
  // 3. 如果有缺口，重新分配
  if (totalDeficit > 0 && availableHarvesters > 0) {
    // 按优先级分配（利用率高的源优先）
    sourceNeeds.sort((a, b) => 
      b.source.utilization - a.source.utilization
    );
    
    let remainingHarvesters = Math.min(availableHarvesters, totalDeficit);
    
    for (const need of sourceNeeds) {
      if (remainingHarvesters <= 0) break;
      
      const additional = Math.min(
        need.optimal - need.current,
        remainingHarvesters
      );
      
      if (additional > 0) {
        need.deficit = additional;
        remainingHarvesters -= additional;
      }
    }
  }
  
  // 4. 生成分配计划
  return sourceNeeds.map(need => ({
    sourceId: need.source.id,
    current: need.current,
    optimal: need.optimal,
    deficit: need.deficit,
    priority: need.source.utilization
  }));
}
```

#### 最优Harvester计算
```javascript
calculateOptimalHarvesters(source) {
  // 基础因素
  const energyRate = source.energy / source.energyCapacity;
  const harvestableSpots = this.calculateHarvestableSpots(source);
  
  // 计算公式：考虑能量率、可采集点、房间等级
  const base = Math.ceil(harvestableSpots * 0.5); // 每个可采集点0.5个Harvester
  const energyFactor = 1 + (energyRate * 0.5);    // 能量率影响
  const rclFactor = 1 + (this.room.controller.level * 0.1); // 房间等级影响
  
  let optimal = Math.floor(base * energyFactor * rclFactor);
  
  // 限制范围
  optimal = Math.max(
    this.config.harvesting.minHarvesterPerSource,
    Math.min(
      optimal,
      this.config.harvesting.maxHarvesterPerSource,
      harvestableSpots // 不能超过可采集点
    )
  );
  
  return optimal;
}
```

### 2. 能量分配算法

#### 优先级分配算法
```javascript
allocateEnergyByPriority(demands, availableEnergy) {
  // 1. 按紧急程度和优先级排序
  const sortedDemands = demands.sort((a, b) => {
    // 首先按紧急程度
    if (a.isCritical !== b.isCritical) {
      return b.isCritical - a.isCritical;
    }
    
    // 然后按配置的优先级
    const priorityA = this.config.allocation.priorities[a.purpose] || 1;
    const priorityB = this.config.allocation.priorities[b.purpose] || 1;
    
    if (priorityA !== priorityB) {
      return priorityB - priorityA;
    }
    
    // 最后按等待时间
    return b.waitTime - a.waitTime;
  });
  
  // 2. 分配能量
  const allocations = [];
  let remaining = availableEnergy;
  
  for (const demand of sortedDemands) {
    if (remaining <= 0) break;
    
    // 计算本次分配量
    let amount = Math.min(
      demand.remaining,
      remaining,
      this.calculateMaxAllocation(demand)
    );
    
    if (amount > 0) {
      // 执行分配
      const allocation = this.executeAllocation(demand, amount);
      allocations.push(allocation);
      
      // 更新需求状态
      demand.allocated += amount;
      demand.remaining -= amount;
      remaining -= amount;
      
      // 记录分配时间
      demand.lastAllocationTime = Game.time;
    }
  }
  
  // 3. 返回分配结果
  return {
    allocations,
    remaining,
    totalAllocated: availableEnergy - remaining,
    satisfactionRate: this.calculateSatisfactionRate(demands)
  };
}
```

#### 紧急程度判断
```javascript
calculateEmergencyLevel(energyStatus) {
  const utilization = energyStatus.overall.utilization;
  const config = this.config.allocation.emergencyLevels;
  
  if (utilization <= config.critical) {
    return 'critical';
  } else if (utilization <= config.warning) {
    return 'warning';
  } else {
    return 'normal';
  }
}

isDemandCritical(demand, emergencyLevel) {
  // 基础判断
  if (emergencyLevel === 'critical') {
    // 关键时期，只有核心需求是关键的
    return ['spawn', 'defense'].includes(demand.purpose);
  } else if (emergencyLevel === 'warning') {
    // 警告时期，重要需求是关键
    return ['spawn', 'defense', 'upgrade'].includes(demand.purpose);
  } else {
    // 正常时期，所有需求都不是关键（按优先级）
    return false;
  }
}
```

### 3. 能量预测算法

#### 短期预测（未来100ticks）
```javascript
predictShortTermEnergy(history, currentStatus) {
  // 使用时间序列分析
  const predictions = [];
  const horizon = 100; // 预测100ticks
  
  // 1. 计算趋势
  const trend = this.calculateEnergyTrend(history);
  
  // 2. 考虑周期性（采集周期）
  const periodicity = this.analyzePeriodicity(history);
  
  // 3. 生成预测
  for (let i = 1; i <= horizon; i++) {
    // 基础预测 = 当前值 + 趋势
    let prediction = currentStatus.available + (trend.slope * i);
    
    // 考虑周期性
    if (periodicity.detected) {
      const phase = (currentStatus.tickNumber + i) % periodicity.period;
      prediction += periodicity.amplitude * Math.sin(2 * Math.PI * phase / periodicity.period);
    }
    
    // 考虑随机波动
    prediction += this.generateRandomNoise(trend.variance);
    
    // 限制范围
    prediction = Math.max(0, Math.min(prediction, currentStatus.capacity));
    
    predictions.push({
      tick: currentStatus.tickNumber + i,
      predicted: prediction,
      confidence: this.calculateConfidence(i, trend, periodicity)
    });
  }
  
  return predictions;
}
```

#### 需求预测
```javascript
predictEnergyDemands(roomState, history) {
  const predictions = {
    spawn: this.predictSpawnDemand(roomState),
    build: this.predictBuildDemand(roomState),
    upgrade: this.predictUpgradeDemand(roomState),
    repair: this.predictRepairDemand(roomState),
    defense: this.predictDefenseDemand(roomState)
  };
  
  // 汇总预测
  const total = Object.values(predictions).reduce((sum, p) => sum + p.amount, 0);
  
  return {
    byPurpose: predictions,
    total,
    timestamp: Game.time,
    confidence: this.calculateDemandConfidence(roomState, history)
  };
}
```

## 🗃️ 数据结构

### 1. 能量源数据结构
```javascript
class EnergySource {
  constructor(source) {
    this.id = source.id;
    this.pos = source.pos;
    this.energy = source.energy;
    this.energyCapacity = source.energyCapacity;
    this.ticksToRegeneration = source.ticksToRegeneration || 0;
    
    // 计算属性
    this.utilization = this.energy / this.energyCapacity;
    this.harvestableSpots = this.calculateHarvestableSpots();
    this.assignedHarvesters = 0;
    
    // 历史数据
    this.harvestHistory = []; // 最近N次采集记录
    this.efficiencyHistory = []; // 效率历史
  }
  
  calculateHarvestableSpots() {
    // 计算周围可通行位置数量
    let count = 0;
    const terrain = this.pos.room.getTerrain();
    
    for (let dx = -1; dx <= 1; dx++) {
      for (let dy = -1; dy <= 1; dy++) {
        if (dx === 0 && dy === 0) continue;
        
        const x = this.pos.x + dx;
        const y = this.pos.y + dy;
        const terrainType = terrain.get(x, y);
        
        if (terrainType !== TERRAIN_MASK_WALL) {
          count++;
        }
      }
    }
    
    return count;
  }
  
  recordHarvest(amount, harvesterId) {
    const record = {
      tick: Game.time,
      amount,
      harvesterId,
      sourceUtilization: this.utilization
    };
    
    this.harvestHistory.push(record);
    
    // 保持历史记录大小
    if (this.harvestHistory.length > 100) {
      this.harvestHistory.shift();
    }
    
    // 计算效率
    const efficiency = this.calculateHarvestEfficiency();
    this.efficiencyHistory.push({
      tick: Game.time,
      efficiency
    });
    
    if (this.efficiencyHistory.length > 50) {
      this.efficiencyHistory.shift();
    }
  }
  
  calculateHarvestEfficiency() {
    if (this.harvestHistory.length < 10) return 0;
    
    const recent = this.harvestHistory.slice(-10);
    const totalHarvested = recent.reduce((sum, r) => sum + r.amount, 0);
    const maxPossible = 10 * 2 * 5; // 10ticks * 2能量/tick * 5工作部件
    
    return totalHarvested / maxPossible;
  }
  
  getAverageEfficiency(window = 50) {
    if (this.efficiencyHistory.length === 0) return 0;
    
    const samples = this.efficiencyHistory.slice(-window);
    const sum = samples.reduce((total, record) => total + record.efficiency, 0);
    return sum / samples.length;
  }
}
```

### 2. 能量存储数据结构
```javascript
class EnergyStorage {
  constructor(storage) {
    this.id = storage.id;
    this.type = storage.structureType;
    this.pos = storage.pos;
    this.store = storage.store;
    this.storeCapacity = storage.storeCapacity;
    this.hits = storage.hits;
    this.hitsMax = storage.hitsMax;
    
    // 计算属性
    this.utilization = this.store[RESOURCE_ENERGY] / this.storeCapacity || 0;
    this.fillRate = 0; // 填充率（能量/tick）
    this.drainRate = 0; // 消耗率（能量/tick）
    
    // 历史数据
    this.levelHistory = []; // 能量水平历史
    this.transferHistory = []; // 转移历史
  }
  
  recordLevel(energy) {
    this.levelHistory.push({
      tick: Game.time,
      energy,
      capacity: this.storeCapacity
    });
    
    if (this.levelHistory.length > 200) {
      this.levelHistory.shift();
    }
    
    // 更新填充/消耗率
    if (this.levelHistory.length >= 2) {
      const current = this.levelHistory[this.levelHistory.length - 1];
      const previous = this.levelHistory[this.levelHistory.length - 2];
      const delta = current.energy - previous.energy;
      const ticks = current.tick - previous.tick;
      
      if (delta > 0) {
        this.fillRate = delta / ticks;
      } else if (delta < 0) {
        this.drainRate = -delta / ticks;
      }
    }
  }
  
  recordTransfer(amount, destinationId, type) {
    this.transferHistory.push({
      tick: Game.time,
      amount,
      destinationId,
      type, // 'in' or 'out'
      sourceLevel: this.store[RESOURCE_ENERGY]
    });
    
    if (this.transferHistory.length > 100) {
      this.transferHistory.shift();
    }
  }
  
  getTransferStats(window = 100) {
    const recent = this.transferHistory.slice(-window);
    const stats = {
      totalIn: 0,
      totalOut: 0,
      countIn: 0,
      countOut: 0,
      avgIn: 0,
      avgOut: 0
    };
    
    recent.forEach(transfer => {
      if (transfer.type === 'in') {
        stats.totalIn += transfer.amount;
        stats.countIn++;
      } else {
        stats.totalOut += transfer.amount;
        stats.countOut++;
      }
    });
    
    if (stats.countIn > 0) stats.avgIn = stats.totalIn / stats.countIn;
    if (stats.countOut > 0) stats.avgOut = stats.totalOut / stats.countOut;
    
    return stats;
  }
}
```

### 3. 能量需求数据结构
```javascript
class EnergyDemand {
  constructor(purpose, amount, priority = 1) {
    this.id = `demand_${Game.time}_${Math.random().toString(36).substr(2, 9)}`;
    this.purpose = purpose; // spawn/build/upgrade/repair/defense
    this.requestedAmount = amount;
    this.allocatedAmount = 0;
    this.remainingAmount = amount;
    this.priority = priority; // 1-10
    this.emergencyLevel = 'normal'; // normal/warning/critical
    this.createdAt = Game.time;
    this.lastAllocationTime = null;
    this.waitTime = 0;
    this.requesterId = null; // 请求者ID（Creep/建筑等）
    
    // 历史分配记录
    this.allocationHistory = [];
  }
  
  get isCritical() {
    return this.emergencyLevel === 'critical';
  }
  
  get isSatisfied() {
    return this.remainingAmount <= 0;
  }
  
  get satisfactionRate() {
    return this.allocatedAmount / this.requestedAmount;
  }
  
  updateWaitTime() {
    this.waitTime = Game.time - this.createdAt;
  }
  
  recordAllocation(amount, sourceId) {
    const allocation = {
      tick: Game.time,
      amount,
      sourceId,
      remaining: this.remainingAmount - amount
    };
    
    this.allocationHistory.push(allocation);
    this.allocatedAmount += amount;
    this.remainingAmount -= amount;
    this.lastAllocationTime = Game.time;
    
    // 更新紧急程度
    this.updateEmergencyLevel();
    
    return allocation;
  }
  
  updateEmergencyLevel() {
    const waitThresholds = {
      normal: 100,
      warning: 50,
      critical: 20
    };
    
    this.waitTime = Game.time - this.createdAt;
    
    if (this.waitTime > waitThresholds.normal) {
      this.emergencyLevel = 'critical';
    } else if (this.waitTime > waitThresholds.warning) {
      this.emergencyLevel = 'warning';
    } else {
      this.emergencyLevel = 'normal';
    }
    
    // 如果需求即将过期，提高紧急程度
    if (this.requesterId) {
      const requester = Game.getObjectById(this.requesterId);
      if (requester) {
        if (requester.ticksToLive && requester.ticksToLive < 100) {
          this.emergencyLevel = 'critical';
        }
      }
    }
  }
  
  getUrgencyScore() {
    // 紧急程度评分 = 基础优先级 + 等待时间因子 + 紧急级别因子
    let score = this.priority * 10;
    
    // 等待时间因子（等待越久分数越高）
    score += Math.min(this.waitTime / 10, 20);
    
    // 紧急级别因子
    const emergencyFactors = {
      critical: 30,
      warning: 15,
      normal: 0
    };
    score += emergencyFactors[this.emergencyLevel];
    
    // 满足率因子（越不满足分数越高）
    score += (1 - this.satisfactionRate) * 20;
    
    return score;
  }
}
```

## 🚨 错误处理

### 错误分类和处理

#### 1. 采集错误
```javascript
class HarvestingError extends Error {
  constructor(sourceId, harvesterId, reason) {
    super(`采集错误: 能量源 ${sourceId}, Harvester ${harvesterId}, 原因: ${reason}`);
    this.name = 'HarvestingError';
    this.sourceId = sourceId;
    this.harvesterId = harvesterId;
    this.reason = reason;
    this.timestamp = Game.time;
  }
  
  static createBlockedError(sourceId, harvesterId) {
    return new HarvestingError(sourceId, harvesterId, '路径被阻挡');
  }
  
  static createNoEnergyError(sourceId, harvesterId) {
    return new HarvestingError(sourceId, harvesterId, '能量源枯竭');
  }
  
  static createRangeError(sourceId, harvesterId) {
    return new HarvestingError(sourceId, harvesterId, '超出采集范围');
  }
}

handleHarvestingError(error) {
  switch (error.reason) {
    case '路径被阻挡':
      this.logService.warn('采集路径被阻挡，尝试重新规划', error);
      this.replanHarvesterPath(error.sourceId, error.harvesterId);
      break;
      
    case '能量源枯竭':
      this.logService.info('能量源枯竭，等待再生', error);
      this.scheduleHarvesterForLater(error.sourceId, error.harvesterId);
      break;
      
    case '超出采集范围':
      this.logService.warn('Harvester超出采集范围，重新分配', error);
      this.reassignHarvester(error.harvesterId);
      break;
      
    default:
      this.logService.error('未知采集错误', error);
      this.disableSourceTemporarily(error.sourceId);
  }
}
```

#### 2. 分配错误
```javascript
class AllocationError extends Error {
  constructor(demandId, requested, available, reason) {
    super(`分配错误: 需求 ${demandId}, 请求 ${requested}, 可用 ${available}, 原因: ${reason}`);
    this.name = 'AllocationError';
    this.demandId = demandId;
    this.requested = requested;
    this.available = available;
    this.reason = reason;
    this.timestamp = Game.time;
  }
  
  static createInsufficientError(demandId, requested, available) {
    return new AllocationError(demandId, requested, available, '能量不足');
  }
  
  static createStorageFullError(demandId, requested) {
    return new AllocationError(demandId, requested, 0, '存储已满');
  }
  
  static createTransferError(demandId, requested, available) {
    return new AllocationError(demandId, requested, available, '转移失败');
  }
}

handleAllocationError(error) {
  switch (error.reason) {
    case '能量不足':
      this.logService.warn('能量不足，降低分配或等待', error);
      this.handleInsufficientEnergy(error.demandId, error.requested, error.available);
      break;
      
    case '存储已满':
      this.logService.warn('目标存储已满，寻找其他存储', error);
      this.findAlternativeStorage(error.demandId);
      break;
      
    case '转移失败':
      this.logService.warn('能量转移失败，重试或取消', error);
      this.retryOrCancelTransfer(error.demandId);
      break;
      
    default:
      this.logService.error('未知分配错误', error);
      this.cancelDemand(error.demandId);
  }
}
```

#### 3. 监控错误
```javascript
class MonitoringError extends Error {
  constructor(metric, expected, actual, threshold) {
    super(`监控错误: 指标 ${metric}, 期望 ${expected}, 实际 ${actual}, 阈值 ${threshold}`);
    this.name = 'MonitoringError';
    this.metric = metric;
    this.expected = expected;
    this.actual = actual;
    this.threshold = threshold;
    this.timestamp = Game.time;
  }
  
  static createLowEfficiencyError(expected, actual) {
    return new MonitoringError('采集效率', expected, actual, '低于80%');
  }
  
  static createHighWasteError(expected, actual) {
    return new MonitoringError('能量浪费', expected, actual, '高于10%');
  }
  
  static createUnbalancedError(expected, actual) {
    return new MonitoringError('存储平衡', expected, actual, '偏差大于20%');
  }
}

handleMonitoringError(error) {
  // 记录告警
  this.monitorService.alert('warning', `能量监控异常: ${error.metric}`, {
    metric: error.metric,
    expected: error.expected,
    actual: error.actual,
    threshold: error.threshold,
    timestamp: error.timestamp
  });
  
  // 根据指标类型采取行动
  switch (error.metric) {
    case '采集效率':
      this.optimizeHarvestingStrategy();
      break;
      
    case '能量浪费':
      this.reduceEnergyWaste();
      break;
      
    case '存储平衡':
      this.balanceStorageDistribution();
      break;
  }
}
```

### 错误恢复策略

#### 1. 渐进式恢复
```javascript
class ProgressiveRecovery {
  constructor() {
    this.recoveryLevel = 0; // 0-正常, 1-轻度, 2-中度, 3-重度
    this.recoverySteps = [
      { level: 1, actions: ['优化分配', '调整优先级'] },
      { level: 2, actions: ['减少非核心需求', '启用备用方案'] },
      { level: 3, actions: ['暂停非关键操作', '紧急采集', '请求外部帮助'] }
    ];
  }
  
  escalateRecovery(errorSeverity) {
    // 根据错误严重程度升级恢复级别
    if (errorSeverity >= 0.8 && this.recoveryLevel < 3) {
      this.recoveryLevel = 3;
    } else if (errorSeverity >= 0.6 && this.recoveryLevel < 2) {
      this.recoveryLevel = 2;
    } else if (errorSeverity >= 0.4 && this.recoveryLevel < 1) {
      this.recoveryLevel = 1;
    }
    
    return this.executeRecoveryActions();
  }
  
  executeRecoveryActions() {
    const actions = [];
    
    // 执行当前级别及以下的所有恢复动作
    for (let i = 0; i <= this.recoveryLevel; i++) {
      actions.push(...this.recoverySteps[i].actions);
    }
    
    // 执行恢复动作
    actions.forEach(action => {
      this.executeRecoveryAction(action);
    });
    
    return actions;
  }
  
  executeRecoveryAction(action) {
    switch (action) {
      case '优化分配':
        this.optimizeEnergyAllocation();
        break;
      case '调整优先级':
        this.adjustDemandPriorities();
        break;
      case '减少非核心需求':
        this.reduceNonCriticalDemands();
        break;
      case '启用备用方案':
        this.activateBackupPlan();
        break;
      case '暂停非关键操作':
        this.pauseNonCriticalOperations();
        break;
      case '紧急采集':
        this.emergencyHarvesting();
        break;
      case '请求外部帮助':
        this.requestExternalAssistance();
        break;
    }
  }
  
  deescalateRecovery() {
    // 当系统稳定时，逐步降低恢复级别
    if (this.recoveryLevel > 0 && this.isSystemStable()) {
      this.recoveryLevel--;
      this.logService.info(`恢复级别降低到 ${this.recoveryLevel}`);
    }
  }
}
```

#### 2. 备用方案管理
```javascript
class BackupPlanManager {
  constructor() {
    this.backupPlans = new Map();
    this.activeBackupPlan = null;
  }
  
  registerBackupPlan(name, plan) {
    this.backupPlans.set(name, {
      name,
      plan,
      priority: plan.priority || 1,
      conditions: plan.conditions || [],
      lastUsed: null,
      successRate: 1.0
    });
  }
  
  activateBackupPlan(condition) {
    // 查找符合条件的备用方案
    const suitablePlans = [];
    
    for (const [name, backup] of this.backupPlans) {
      if (this.checkConditions(backup.conditions, condition)) {
        suitablePlans.push(backup);
      }
    }
    
    // 按优先级和成功率排序
    suitablePlans.sort((a, b) => {
      if (a.priority !== b.priority) {
        return b.priority - a.priority;
      }
      return b.successRate - a.successRate;
    });
    
    if (suitablePlans.length > 0) {
      const selectedPlan = suitablePlans[0];
      this.activeBackupPlan = selectedPlan.name;
      this.logService.info(`激活备用方案: ${selectedPlan.name}`);
      
      // 执行备用方案
      return this.executeBackupPlan(selectedPlan);
    }
    
    return null;
  }
  
  executeBackupPlan(backup) {
    try {
      const result = backup.plan.execute();
      backup.lastUsed = Game.time;
      
      // 更新成功率
      if (result.success) {
        backup.successRate = Math.min(1.0, backup.successRate + 0.05);
      } else {
        backup.successRate = Math.max(0.0, backup.successRate - 0.1);
      }
      
      return result;
    } catch (error) {
      this.logService.error(`备用方案执行失败: ${backup.name}`, error);
      backup.successRate = Math.max(0.0, backup.successRate - 0.2);
      return { success: false, error: error.message };
    }
  }
  
  de