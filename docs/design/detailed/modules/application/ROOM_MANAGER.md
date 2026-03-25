# RoomManager 详细设计文档

## 📋 文档信息
- **模块名称**: RoomManager（房间管理器）
- **所属层级**: 应用层
- **文档版本**: v1.0.0
- **创建日期**: 2026-03-25
- **最后更新**: 2026-03-25
- **负责人**: Moss (OpenClaw AI)
- **状态**: [草案]
- **关联文档**: 
  - `ARCHITECTURE_DESIGN.md` - 架构设计文档
  - `ENERGY_MANAGER.md` - 能量管理器设计
  - `CREEP_MANAGER.md` - Creep管理器设计

## 🎯 设计目标

### 核心职责
1. **房间生命周期管理** - 初始化、运行、清理
2. **业务模块协调** - 协调能量、Creep、角色等模块
3. **状态监控** - 监控房间状态和性能
4. **错误处理** - 处理房间级别的错误和恢复

### 质量目标
- **性能**: 每tick CPU使用 < 10
- **可靠性**: 99.9% uptime，自动恢复
- **可维护性**: 清晰的接口，完整的日志
- **可扩展性**: 支持未来多房间扩展

## 🏗️ 类图设计

### 类结构
```
┌─────────────────────────────────────┐
│           RoomManager               │
├─────────────────────────────────────┤
│ - roomName: string                  │
│ - room: Room                        │
│ - energyManager: EnergyManager      │
│ - creepManager: CreepManager        │
│ - roleManager: RoleManager          │
│ - buildingManager: BuildingManager  │
│ - defenseManager: DefenseManager    │
│ - configService: ConfigService      │
│ - memoryService: MemoryService      │
│ - logService: LogService            │
│ - monitorService: MonitorService    │
│ - profilerService: ProfilerService  │
│ - initialized: boolean              │
│ - lastTick: number                  │
│ - stats: RoomStats                  │
│ - cache: RoomCache                  │
├─────────────────────────────────────┤
│ + constructor(roomName: string)     │
│ + initRoom(): boolean               │
│ + tickRoom(): RoomTickResult        │
│ + getStats(): RoomStats             │
│ + getSummary(): RoomSummary         │
│ + destroy(): void                   │
│ - collectRoomStateWithCache(): RoomState
│ - collectRoomState(): RoomState     │
│ - updateRoomMemory(): void          │
│ - monitorRoomPerformance(): void    │
│ - periodicCleanup(): void           │
│ - handleTickError(): void           │
│ - isCriticalError(): boolean        │
│ - isMemoryError(): boolean          │
└─────────────────────────────────────┘
```

### 依赖关系
```
RoomManager
    ├── 依赖业务层模块
    │   ├── EnergyManager
    │   ├── CreepManager
    │   ├── RoleManager
    │   ├── BuildingManager
    │   └── DefenseManager
    │
    ├── 依赖服务层模块
    │   ├── ConfigService
    │   ├── MemoryService
    │   ├── LogService
    │   ├── MonitorService
    │   └── ProfilerService
    │
    └── 依赖游戏API
        ├── Game.rooms
        ├── Game.time
        └── Game.cpu
```

## 📝 接口定义

### 公共接口

#### 1. 构造函数
```javascript
/**
 * RoomManager 构造函数
 * @param {string} roomName - 房间名称
 */
constructor(roomName: string): RoomManager
```

#### 2. 初始化接口
```javascript
/**
 * 初始化房间
 * @returns {boolean} 初始化是否成功
 * @throws {Error} 初始化失败时抛出异常
 */
initRoom(): boolean
```

#### 3. Tick处理接口
```javascript
/**
 * 处理房间tick
 * @returns {RoomTickResult} tick处理结果
 */
tickRoom(): RoomTickResult
```

#### 4. 状态查询接口
```javascript
/**
 * 获取房间统计信息
 * @returns {RoomStats} 房间统计信息
 */
getStats(): RoomStats

/**
 * 获取房间状态摘要
 * @returns {RoomSummary} 房间状态摘要
 */
getSummary(): RoomSummary
```

#### 5. 资源清理接口
```javascript
/**
 * 销毁房间管理器
 */
destroy(): void
```

### 数据类型定义

#### RoomTickResult
```javascript
interface RoomTickResult {
  success: boolean;                    // 是否成功
  cpuUsed: number;                     // CPU使用量
  timestamp: number;                   // 时间戳
  modules: {                           // 模块执行结果
    energy?: ModuleResult;
    creep?: ModuleResult;
    role?: ModuleResult;
    building?: ModuleResult;
    defense?: ModuleResult;
  };
  failedModules?: string[];            // 失败的模块列表
  warnings?: Warning[];                // 警告列表
  error?: string;                      // 错误信息
  isCritical?: boolean;                // 是否为关键错误
}

interface ModuleResult {
  success: boolean;
  cpuUsed: number;
  error?: string;
  warnings?: Warning[];
}

interface Warning {
  module: string;
  message: string;
  severity: 'info' | 'warning' | 'error';
  timestamp: number;
}
```

#### RoomStats
```javascript
interface RoomStats {
  totalTicks: number;                  // 总tick数
  avgCpuUsage: number;                 // 平均CPU使用率
  totalErrors: number;                 // 总错误数
  lastError?: {                       // 最后错误信息
    message: string;
    stack?: string;
    cpuUsed: number;
    timestamp: number;
  };
  performance: {                      // 性能统计
    minCpu: number;
    maxCpu: number;
    avgCpu: number;
  };
  roomName: string;                   // 房间名称
  initialized: boolean;               // 是否已初始化
  lastTick: number;                   // 最后tick时间
  currentTime: number;                // 当前时间
}
```

#### RoomSummary
```javascript
interface RoomSummary {
  roomName: string;                   // 房间名称
  exists: boolean;                    // 房间是否存在
  initialized: boolean;               // 是否已初始化
  controllerLevel?: number;           // 控制器等级
  energy?: {                         // 能量信息
    available: number;
    capacity: number;
  };
  creeps?: {                         // Creep信息
    my: number;
    hostile: number;
  };
  structures?: {                     // 建筑信息
    spawns: number;
    extensions: number;
  };
  stats?: RoomStats;                 // 统计信息
}
```

## 🔧 算法设计

### 1. Tick处理算法

#### 算法流程
```
开始tick
    ↓
检查初始化状态 → 失败 → 尝试初始化 → 失败 → 返回错误
    ↓ 成功
检查房间是否存在 → 不存在 → 返回错误
    ↓ 存在
收集房间状态（使用缓存）
    ↓
按优先级执行业务模块：
    1. EnergyManager.tick()
    2. CreepManager.tick()
    3. RoleManager.tick()
    4. BuildingManager.tick()
    5. DefenseManager.tick()
    ↓
检查模块执行结果
    ↓
更新内存状态
    ↓
监控性能并记录日志
    ↓
定期清理资源
    ↓
更新统计信息
    ↓
返回处理结果
```

#### 伪代码实现
```javascript
tickRoom() {
  const startCpu = Game.cpu.getUsed();
  const tickStart = Game.time;
  
  try {
    // 1. 检查初始化
    if (!this.initialized && !this.initRoom()) {
      return errorResult('初始化失败', startCpu, tickStart);
    }
    
    // 2. 检查房间
    if (!this.room) {
      return errorResult('房间不存在', startCpu, tickStart);
    }
    
    // 3. 收集状态（带缓存）
    const roomState = this.collectRoomStateWithCache();
    
    // 4. 执行业务模块
    const moduleResults = this.executeModules(roomState);
    
    // 5. 检查结果
    const failedModules = this.checkModuleResults(moduleResults);
    
    // 6. 更新内存
    if (failedModules.length === 0) {
      this.updateRoomMemory(roomState, moduleResults);
    }
    
    // 7. 监控性能
    this.monitorPerformance(startCpu, moduleResults, failedModules);
    
    // 8. 定期清理
    this.periodicCleanup();
    
    // 9. 更新统计
    const cpuUsed = Game.cpu.getUsed() - startCpu;
    this.updateStats(cpuUsed, failedModules.length === 0);
    
    return successResult(cpuUsed, tickStart, moduleResults, failedModules);
    
  } catch (error) {
    return this.handleTickError(error, startCpu, tickStart);
  }
}
```

### 2. 状态收集算法（带缓存）

#### 缓存策略
```javascript
collectRoomStateWithCache() {
  const now = Game.time;
  
  // 检查缓存有效性
  if (this.cache.roomState && 
      now - this.cache.lastUpdate < this.cache.ttl &&
      this.cache.roomState.timestamp === this.cache.lastUpdate) {
    return this.cache.roomState;
  }
  
  // 重新收集
  const roomState = this.collectRoomState();
  this.cache.roomState = roomState;
  this.cache.lastUpdate = now;
  
  return roomState;
}
```

#### 状态收集优化
```javascript
collectRoomState() {
  // 使用批量API调用优化性能
  const room = this.room;
  
  return {
    metadata: { /* 基础信息 */ },
    controller: this.collectControllerState(room),
    energy: this.collectEnergyState(room),
    creeps: this.collectCreepState(room),
    structures: this.collectStructureState(room),
    terrain: this.collectTerrainState(room),
    resources: this.collectResourceState(room)
  };
}
```

### 3. 错误处理算法

#### 错误分类
```javascript
class ErrorClassifier {
  static classify(error) {
    if (this.isCriticalError(error)) {
      return 'critical';
    } else if (this.isMemoryError(error)) {
      return 'memory';
    } else if (this.isApiError(error)) {
      return 'api';
    } else if (this.isLogicError(error)) {
      return 'logic';
    } else {
      return 'unknown';
    }
  }
  
  static isCriticalError(error) {
    const patterns = [/内存/, /初始化/, /配置/, /房间不存在/, /无法访问/];
    return patterns.some(p => p.test(error.message));
  }
  
  static isMemoryError(error) {
    const patterns = [/内存不足/, /Memory/, /内存溢出/, /序列化/, /JSON/];
    return patterns.some(p => p.test(error.message));
  }
}
```

#### 恢复策略
```javascript
handleError(error, errorType) {
  switch (errorType) {
    case 'critical':
      this.logService.warn('关键错误，尝试重新初始化');
      this.initialized = false;
      break;
      
    case 'memory':
      this.logService.warn('内存错误，尝试清理内存');
      this.memoryService.emergencyCleanup(this.roomName);
      break;
      
    case 'api':
      this.logService.warn('API错误，使用缓存数据');
      this.useCachedData();
      break;
      
    case 'logic':
      this.logService.warn('逻辑错误，使用备用算法');
      this.useFallbackAlgorithm();
      break;
      
    default:
      this.logService.error('未知错误类型', error);
  }
}
```

## 🗃️ 数据结构

### 1. 缓存数据结构
```javascript
class RoomCache {
  constructor() {
    this.roomState = null;      // 缓存的房间状态
    this.lastUpdate = 0;        // 最后更新时间
    this.ttl = 5;              // 缓存有效期（tick）
    this.hits = 0;             // 缓存命中次数
    this.misses = 0;           // 缓存未命中次数
  }
  
  get hitRate() {
    const total = this.hits + this.misses;
    return total > 0 ? this.hits / total : 0;
  }
}
```

### 2. 统计数据结构
```javascript
class RoomStats {
  constructor() {
    this.totalTicks = 0;
    this.avgCpuUsage = 0;
    this.totalErrors = 0;
    this.lastError = null;
    this.performance = {
      minCpu: Infinity,
      maxCpu: 0,
      avgCpu: 0,
      samples: []  // 最近N个样本用于计算趋势
    };
    this.moduleStats = new Map(); // 模块性能统计
  }
  
  addTickResult(cpuUsed, success) {
    this.totalTicks++;
    
    // 更新CPU统计
    this.performance.minCpu = Math.min(this.performance.minCpu, cpuUsed);
    this.performance.maxCpu = Math.max(this.performance.maxCpu, cpuUsed);
    
    // 滑动平均
    this.performance.avgCpu = 
      (this.performance.avgCpu * (this.totalTicks - 1) + cpuUsed) / this.totalTicks;
    
    // 记录样本（用于趋势分析）
    this.performance.samples.push(cpuUsed);
    if (this.performance.samples.length > 100) {
      this.performance.samples.shift();
    }
    
    // 错误统计
    if (!success) {
      this.totalErrors++;
    }
    
    // 更新平均CPU使用率
    this.avgCpuUsage = 
      (this.avgCpuUsage * (this.totalTicks - 1) + cpuUsed) / this.totalTicks;
  }
}
```

### 3. 房间状态数据结构
```javascript
class RoomState {
  constructor(room) {
    this.metadata = {
      name: room.name,
      timestamp: Game.time,
      roomManagerVersion: '1.0.0'
    };
    
    this.controller = this.extractControllerState(room);
    this.energy = this.extractEnergyState(room);
    this.creeps = this.extractCreepState(room);
    this.structures = this.extractStructureState(room);
    this.terrain = this.extractTerrainState(room);
    this.resources = this.extractResourceState(room);
  }
  
  // 提取器方法省略...
}
```

## 🚨 错误处理

### 错误分类体系

#### 1. 初始化错误
- **原因**: 配置错误、房间不存在、API访问失败
- **处理**: 记录日志，返回初始化失败
- **恢复**: 尝试使用默认配置重新初始化

#### 2. 运行时错误
- **内存错误**: 内存不足、序列化失败
- **API错误**: API调用失败、权限不足
- **逻辑错误**: 算法错误、数据不一致
- **资源错误**: 能量不足、Creep死亡

#### 3. 性能错误
- **CPU超限**: 计算超时、循环过深
- **内存超限**: 内存使用超过阈值
- **API限制**: API调用次数超限

### 错误处理策略

#### 防御性编程
```javascript
// 参数验证
validateRoomName(roomName) {
  if (!roomName || typeof roomName !== 'string') {
    throw new Error(`无效的房间名称: ${roomName}`);
  }
  if (!Game.rooms[roomName]) {
    throw new Error(`房间不存在: ${roomName}`);
  }
  return true;
}

// 空值检查
safeGetRoom() {
  if (!this.room) {
    this.room = Game.rooms[this.roomName];
    if (!this.room) {
      throw new Error(`房间已消失: ${this.roomName}`);
    }
  }
  return this.room;
}
```

#### 优雅降级
```javascript
executeWithFallback(primaryFunc, fallbackFunc) {
  try {
    return primaryFunc();
  } catch (error) {
    this.logService.warn('主函数执行失败，使用备用函数', error);
    try {
      return fallbackFunc();
    } catch (fallbackError) {
      this.logService.error('备用函数也失败', fallbackError);
      throw new Error(`所有恢复尝试都失败: ${error.message}`);
    }
  }
}
```

#### 自动恢复
```javascript
autoRecovery(error) {
  const errorType = ErrorClassifier.classify(error);
  
  switch (errorType) {
    case 'critical':
      // 重新初始化
      this.initialized = false;
      this.initRoom();
      break;
      
    case 'memory':
      // 清理内存
      this.memoryService.emergencyCleanup(this.roomName);
      break;
      
    case 'api':
      // 使用缓存
      this.useCachedState();
      break;
      
    default:
      // 记录错误，继续运行
      this.logService.error('无法自动恢复的错误', error);
  }
}
```

## ⚡ 性能优化

### CPU优化策略

#### 1. 计算分布
```javascript
// 重计算分布到多个tick
distributeHeavyComputation(computation, chunkSize) {
  const results = [];
  let remaining = computation.data.length;
  let offset = 0;
  
  while (remaining > 0 && Game.cpu.getUsed() < this.cpuBudget) {
    const chunk = computation.data.slice(offset, offset + chunkSize);
    results.push(computation.process(chunk));
    offset += chunkSize;
    remaining -= chunkSize;
  }
  
  // 保存状态以便下次继续
  if (remaining > 0) {
    this.memoryService.saveComputationState({
      computationId: computation.id,
      offset,
      remaining,
      results
    });
  }
  
  return results;
}
```

#### 2. 缓存优化
```javascript
// 智能缓存管理
class SmartCache {
  constructor() {
    this.cache = new Map();
    this.accessCount = new Map();
    this.sizeLimit = 100; // 缓存项数量限制
  }
  
  get(key) {
    const entry = this.cache.get(key);
    if (entry) {
      // 更新访问计数
      this.accessCount.set(key, (this.accessCount.get(key) || 0) + 1);
      
      // 检查缓存有效期
      if (Game.time - entry.timestamp < entry.ttl) {
        return entry.value;
      } else {
        // 缓存过期，删除
        this.cache.delete(key);
        this.accessCount.delete(key);
      }
    }
    return null;
  }
  
  set(key, value, ttl = 10) {
    // 如果缓存已满，删除最少使用的项
    if (this.cache.size >= this.sizeLimit) {
      this.evictLeastUsed();
    }
    
    this.cache.set(key, {
      value,
      timestamp: Game.time,
      ttl
    });
    this.accessCount.set(key, 1);
  }
  
  evictLeastUsed() {
    let minKey = null;
    let minCount = Infinity;
    
    for (const [key, count] of this.accessCount) {
      if (count < minCount) {
        minCount = count;
        minKey = key;
      }
    }
    
    if (minKey) {
      this.cache.delete(minKey);
      this.accessCount.delete(minKey);
    }
  }
}
```

#### 3. 条件执行
```javascript
// 非必要计算跳过
conditionalExecute(condition, func) {
  if (condition()) {
    return func();
  }
  return null;
}

// 示例：只在能量变化时重新计算
recalculateEnergyAllocation() {
  return this.conditionalExecute(
    () => this.energyChangedSinceLastTick(),
    () => this.energyManager.optimizeAllocations()
  );
}
```

### 内存优化策略

#### 1. 结构化存储
```javascript
// 使用高效的数据结构
class CompactRoomState {
  constructor(room) {
    // 使用数组而不是对象存储位置数据
    this.sourcePositions = room.find(FIND_SOURCES).map(s => [s.pos.x, s.pos.y]);
    this.creepCounts = new Uint8Array(10); // 使用类型化数组
    this.energyLevels = new Float32Array(5);
  }
  
  // 序列化时压缩数据
  serialize() {
    return {
      s: this.sourcePositions,
      c: Array.from(this.creepCounts),
      e: Array.from(this.energyLevels)
    };
  }
}
```

#### 2. 定期清理
```javascript
// 定时清理无效数据
scheduleCleanup() {
  const cleanupIntervals = {
    memory: 100,    // 每100tick清理内存
    cache: 500,     // 每500tick清理缓存
    logs: 1000,     // 每1000tick清理日志
    stats: 10000    // 每10000tick重置统计
  };
  
  Object.entries(cleanupIntervals).forEach(([type, interval]) => {
    if (Game.time % interval === 0) {
      this.cleanupType(type);
    }
  });
}

cleanupType(type) {
  switch (type) {
    case 'memory':
      this.memoryService.cleanup();
      break;
    case 'cache':
      this.cache.clear();
      break;
    case 'logs':
      this.logService.rotateLogs();
      break;
    case 'stats':
      this.resetOldStats();
      break;
  }
}
```

#### 3. 数据压缩
```javascript
// 压缩历史数据
compressHistoricalData(data, maxPoints = 100) {
  if (data.length <= maxPoints) {
    return data;
  }
  
  // 采样压缩：保留头尾和关键点
  const compressed = [];
  const step = Math.ceil(data.length / maxPoints);
  
  // 保留开头
  compressed.push(data[0]);
  
  // 采样中间数据
  for (let i = step; i < data.length - step; i += step) {
    compressed.push(data[i]);
  }
  
  // 保留结尾
  compressed.push(data[data.length - 1]);
  
  return compressed;
}
```

### API优化策略

#### 1. 批量操作
```javascript
// 批量API调用
batchApiCalls(operations) {
  const results = [];
  let batch = [];
  
  for (const op of operations) {
    batch.push(op);
    
    // 每10个操作批量执行一次
    if (batch.length >= 10) {
      results.push(...this.executeBatch(batch));
      batch = [];
      
      // 检查CPU使用
      if (Game.cpu.getUsed() > this.cpuBudget * 0.8) {
        break;
      }
    }
  }
  
  // 执行剩余操作
  if (batch.length > 0) {
    results.push(...this.executeBatch(batch));
  }
  
  return results;
}
```

#### 2. 异步处理
```javascript
// 非阻塞操作
asyncProcess(operation, callback) {
  // 将重操作分布到多个tick
  const state = this.memoryService.getAsyncState(operation.id);
  
  if (!state) {
    // 第一次执行，初始化状态
    this.memoryService.setAsyncState(operation.id, {
      step: 0,
      totalSteps: operation.steps,
      results: []
    });
    return { status: 'started' };
  }
  
  // 继续执行
  if (state.step < state.totalSteps) {
    const result = operation.executeStep(state.step);
    state.results.push(result);
    state.step++;
    
    this.memoryService.setAsyncState(operation.id, state);
    
    if (state.step >= state.totalSteps) {
      // 完成，执行回调
      callback(state.results);
      this.memoryService.deleteAsyncState(operation.id);
      return { status: 'completed', results: state.results };
    }
    
    return { status: 'in_progress', progress: state.step / state.totalSteps };
  }
}
```

## 🧪 测试策略

### 单元测试设计

#### 1. 构造函数测试
```javascript
describe('RoomManager Constructor', () => {
  test('should create instance with valid room name', () => {
    const manager = new RoomManager('E15S17');
    expect(manager.roomName).toBe('E15S17');
    expect(manager.initialized).toBe(false);
  });
  
  test('should throw error with invalid room name', () => {
    expect(() => new RoomManager(null)).toThrow('无效的房间名称');
    expect(() => new RoomManager('')).toThrow('无效的房间名称');
  });
});
```

#### 2. 初始化测试
```javascript
describe('RoomManager Initialization', () => {
  let manager;
  
  beforeEach(() => {
    manager = new RoomManager('E15S17');
  });
  
  test('should initialize successfully with valid room', () => {
    mockGameRoom('E15S17', { controller: { level: 1 } });
    const result = manager.initRoom();
    expect(result).toBe(true);
    expect(manager.initialized).toBe(true);
  });
  
  test('should fail initialization with non-existent room', () => {
    mockGameRoom('E15S17', null);
    const result = manager.initRoom();
    expect(result).toBe(false);
    expect(manager.initialized).toBe(false);
  });
});
```

#### 3. Tick处理测试
```javascript
describe('RoomManager Tick Processing', () => {
  let manager;
  
  beforeEach(() => {
    manager = new RoomManager('E15S17');
    mockGameRoom('E15S17', { 
      controller: { level: 1 },
      energyAvailable: 1000,
      energyCapacityAvailable: 1500
    });
    manager.initRoom();
  });
  
  test('should process tick successfully', () => {
    const result = manager.tickRoom();
    expect(result.success).toBe(true);
    expect(result.cpuUsed).toBeGreaterThan(0);
    expect(result.timestamp).toBe(Game.time);
  });
  
  test('should handle errors gracefully', () => {
    // 模拟模块失败
    mockModuleFailure('energyManager');
    const result = manager.tickRoom();
    expect(result.success).toBe(false);
    expect(result.failedModules).toContain('energy');
    expect(result.error).toBeDefined();
  });
});
```

### 集成测试设计

#### 1. 模块集成测试
```javascript
describe('RoomManager Module Integration', () => {
  test('should coordinate all modules correctly', async () => {
    const manager = new RoomManager('E15S17');
    await manager.initRoom();
    
    // 模拟完整的游戏状态
    const mockState = createMockRoomState();
    
    // 执行tick
    const result = manager.tickRoom();
    
    // 验证所有模块都被调用
    expect(result.modules.energy).toBeDefined();
    expect(result.modules.creep).toBeDefined();
    expect(result.modules.role).toBeDefined();
    expect(result.modules.building).toBeDefined();
    expect(result.modules.defense).toBeDefined();
    
    // 验证内存更新
    const memoryState = Memory.screepsMoss.rooms['E15S17'];
    expect(memoryState).toBeDefined();
    expect(memoryState.state.energy.available).toBe(mockState.energy.available);
  });
});
```

#### 2. 性能测试
```javascript
describe('RoomManager Performance', () => {
  test('should stay within CPU limits', () => {
    const manager = new RoomManager('E15S17');
    manager.initRoom();
    
    const iterations = 100;
    let totalCpu = 0;
    let maxCpu = 0;
    
    for (let i = 0; i < iterations; i++) {
      const result = manager.tickRoom();
      totalCpu += result.cpuUsed;
      maxCpu = Math.max(maxCpu, result.cpuUsed);
      
      // 每tick CPU应该小于10
      expect(result.cpuUsed).toBeLessThan(10);
    }
    
    const avgCpu = totalCpu / iterations;
    console.log(`平均CPU: ${avgCpu.toFixed(2)}, 最大CPU: ${maxCpu.toFixed(2)}`);
    
    // 平均CPU应该小于5
    expect(avgCpu).toBeLessThan(5);
  });
});
```

### 验收测试设计

#### 1. 功能验收测试
```javascript
describe('RoomManager Acceptance Tests', () => {
  test('should manage room for 24 hours without critical errors', async () => {
    const manager = new RoomManager('E15S17');
    const startTime = Game.time;
    const duration = 24 * 3600; // 24小时（游戏时间）
    let errorCount = 0;
    
    for (let tick = 0; tick < duration; tick++) {
      const result = manager.tickRoom();
      
      if (!result.success && result.isCritical) {
        errorCount++;
        console.error(`关键错误 at tick ${tick}:`, result.error);
      }
      
      // 每1000tick检查一次
      if (tick % 1000 === 0) {
        const stats = manager.getStats();
        console.log(`Progress: ${tick}/${duration}, Errors: ${errorCount}, Avg CPU: ${stats.avgCpuUsage.toFixed(2)}`);
      }
    }
    
    // 验收标准：24小时内关键错误少于10次
    expect(errorCount).toBeLessThan(10);
    
    const finalStats = manager.getStats();
    console.log(`Final stats: ${finalStats.totalTicks} ticks, ${errorCount} errors, avg CPU: ${finalStats.avgCpuUsage.toFixed(2)}`);
  });
});
```

## 🔗 依赖关系

### 依赖模块

#### 必需依赖（v1.0）
1. **EnergyManager** - 能量管理
   - 版本要求：v1.0.0+
   - 接口：`tick(roomState)`, `analyzeEnergyStatus()`
   
2. **CreepManager** - Creep管理
   - 版本要求：v1.0.0+
   - 接口：`tick(roomState)`, `analyzeCreepNeeds()`
   
3. **RoleManager** - 角色管理
   - 版本要求：v1.0.0+
   - 接口：`tick(roomState)`, `assignTasks()`
   
4. **ConfigService** - 配置服务
   - 版本要求：v1.0.0+
   - 接口：`getRoomConfig()`, `getDefaultConfig()`
   
5. **MemoryService** - 内存服务
   - 版本要求：v1.0.0+
   - 接口：`initRoomMemory()`, `updateRoomState()`
   
6. **LogService** - 日志服务
   - 版本要求：v1.0.0+
   - 接口：`info()`, `error()`, `warn()`

#### 可选依赖（v1.5+）
1. **BuildingManager** - 建筑管理
   - 版本要求：v1.5.0+
   - 接口：`tick(roomState)`, `planLayout()`
   
2. **DefenseManager** - 防御管理
   - 版本要求：v1.5.0+
   - 接口：`tick(roomState)`, `assessThreats()`
   
3. **MonitorService** - 监控服务
   - 版本要求：v1.5.0+
   - 接口：`recordPerformance()`, `alert()`
   
4. **ProfilerService** - 性能服务
   - 版本要求：v1.5.0+
   - 接口：`startSession()`, `stopSession()`

### 接口兼容性

#### 向后兼容保证
1. **公共接口稳定** - 主要公共方法签名不变
2. **数据类型扩展** - 新字段可选，旧字段保留
3. **错误处理增强** - 新错误类型不影响现有处理

#### 版本升级策略
```javascript
// 版本检测和适配
checkCompatibility(module, requiredVersion) {
  const actualVersion = module.getVersion();
  
  if (this.compareVersions(actualVersion, requiredVersion) < 0) {
    throw new Error(`模块 ${module.name} 版本过低: ${actualVersion} < ${requiredVersion}`);
  }
  
  // 检查接口兼容性
  const missingInterfaces = this.checkInterfaces(module, requiredInterfaces);
  if (missingInterfaces.length > 0) {
    throw new Error(`模块 ${module.name} 缺少接口: ${missingInterfaces.join(', ')}`);
  }
  
  return true;
}
```

## 📊 性能指标

### 关键性能指标（KPI）

#### 1. CPU使用指标
- **目标**: 每tick平均CPU < 5
- **警告阈值**: 单次tick CPU > 10
- **严重阈值**: 连续3次tick CPU > 15

#### 2. 内存使用指标
- **目标**: 内存增长 < 1KB/tick
- **警告阈值**: 内存使用 > 500KB
- **严重阈值**: 内存使用 > 1.5MB

#### 3. 可靠性指标
- **成功率**: > 99.9%
- **平均无故障时间**: > 10000 ticks
- **恢复时间**: < 10 ticks

#### 4. 业务指标
- **能量采集效率**: > 80%
- **Creep生成成功率**: > 95%
- **任务完成率**: > 90%

### 监控和告警

#### 监控配置
```javascript
const monitoringConfig = {
  cpu: {
    enabled: true,
    samplingInterval: 10, // 每10tick采样一次
    alertThreshold: 10,
    criticalThreshold: 15
  },
  memory: {
    enabled: true,
    samplingInterval: 100,
    alertThreshold: 500000, // 500KB
    criticalThreshold: 1500000 // 1.5MB
  },
  errors: {
    enabled: true,
    alertThreshold: 5, // 每100tick错误数
    criticalThreshold: 10
  }
};
```

#### 告警规则
```javascript
class AlertRules {
  static checkRoomManagerAlerts(stats, config) {
    const alerts = [];
    
    // CPU告警
    if (stats.performance.avgCpu > config.cpu.alertThreshold) {
      alerts.push({
        level: 'warning',
        type: 'cpu_high',
        message: `CPU使用率过高: ${stats.performance.avgCpu.toFixed(2)}`,
        data: stats
      });
    }
    
    // 错误率告警
    const errorRate = stats.totalErrors / Math.max(stats.totalTicks, 1);
    if (errorRate > config.errors.alertThreshold / 100) {
      alerts.push({
        level: 'error',
        type: 'error_rate_high',
        message: `错误率过高: ${(errorRate * 100).toFixed(2)}%`,
        data: stats
      });
    }
    
    return alerts;
  }
}
```

## 📈 扩展点设计

### 插件扩展点

####