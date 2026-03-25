# Screeps Moss 项目 - 详细设计文档 (v3.0)

## 📋 文档信息
- **项目名称**: Screeps Moss
- **文档类型**: 详细设计文档
- **版本**: v3.0
- **创建日期**: 2026-03-25
- **最后更新**: 2026-03-25
- **负责人**: Moss (OpenClaw AI)
- **状态**: 基于软件工程理论重新编制
- **关联文档**: 
  - `REQUIREMENTS_ANALYSIS.md` (v2.0) - 需求分析（已批准）
  - `SYSTEM_ANALYSIS.md` (v2.0) - 系统分析（已批准）
  - `ARCHITECTURE_DESIGN.md` (v1.2) - 架构设计（概要设计）
  - `docs/reviews/ARCHITECTURE_REVIEW_CHECKLIST.md` - 评审检查清单

## 📝 修改记录
| 版本 | 日期 | 修改内容 | 修改人 |
|------|------|----------|--------|
| v3.0 | 2026-03-25 | 基于软件工程理论重新编制详细设计文档：<br>1. 按照软件工程标准重新组织文档结构<br>2. 补充完整的模块详细设计<br>3. 完善接口详细定义<br>4. 补充算法详细设计<br>5. 完善数据结构设计<br>6. 补充错误处理机制<br>7. 完善性能优化策略<br>8. 补充测试策略 | Moss |

---

## 1. 设计概述

### 1.1 设计目标
基于需求分析文档和架构设计文档，按照软件工程标准设计满足以下目标的详细实现方案：

1. **模块化**: 功能解耦，支持独立开发、测试和维护
2. **高性能**: 在CPU/内存严格约束下实现最优性能
3. **可扩展性**: 支持从单房间到多房间平滑扩展
4. **高可靠性**: 容错设计，自动恢复，99.9%可用性
5. **可维护性**: 代码清晰，文档完整，易于维护和扩展
6. **可测试性**: 支持单元测试、集成测试和系统测试

### 1.2 设计原则
| 原则 | 描述 | 在详细设计中的应用 |
|------|------|----------------|
| **单一职责原则** | 每个类/模块只负责一个功能领域 | 类设计职责明确，方法功能单一 |
| **开闭原则** | 对扩展开放，对修改关闭 | 通过配置和插件扩展功能，不修改核心代码 |
| **里氏替换原则** | 子类可以替换父类而不影响程序 | 继承关系设计合理，接口定义清晰 |
| **接口隔离原则** | 客户端不应依赖不需要的接口 | 细粒度接口设计，避免接口污染 |
| **依赖倒置原则** | 依赖抽象而非具体实现 | 模块通过接口通信，降低耦合度 |
| **迪米特法则** | 最少知识原则 | 减少模块间直接依赖，通过接口通信 |

### 1.3 技术约束应对策略
| 约束 | 影响 | 详细设计应对策略 |
|------|------|----------------|
| **CPU限制** | 算法复杂度受限，每tick 20-100 CPU | 1. 分层计算：重计算分布到多个tick<br>2. 任务优先级：关键任务优先执行<br>3. 缓存机制：缓存路径计算结果<br>4. 算法优化：使用高效算法，避免O(n²)复杂度 |
| **内存限制** | 2MB内存限制，数据存储受限 | 1. 结构化存储：使用高效数据结构<br>2. 定期清理：定时清理无效数据<br>3. 数据压缩：压缩存储的历史数据<br>4. 按需加载：延迟加载非必要数据 |
| **API限制** | 游戏API调用次数和效率受限 | 1. 批量操作：批量API调用减少开销<br>2. 异步处理：非阻塞API调用<br>3. API优化：优化API使用模式<br>4. 错误重试：API失败时自动重试 |
| **实时性** | 必须在tick时限内完成所有计算 | 1. 任务调度：智能任务调度算法<br>2. 超时处理：计算超时自动终止<br>3. 降级策略：资源不足时降级运行<br>4. 状态保存：中断时保存状态以便恢复 |

### 1.4 版本与实现对应关系
基于架构设计文档的版本规划，详细设计支持渐进式实现：

#### v1.0 核心功能阶段详细设计
- **应用层**: RoomManager完整实现，GlobalCoordinator框架接口
- **业务层**: EnergyManager, CreepManager, RoleManager基础实现
- **服务层**: ConfigService, MemoryService, LogService基础实现
- **数据层**: GameState, ConfigData基础结构
- **实现重点**: 单房间基础自动化，能量采集和Creep管理

#### v1.5 功能完善阶段详细设计
- **业务层**: BuildingManager, DefenseManager详细实现
- **服务层**: MonitorService, ProfilerService详细实现
- **数据层**: HistoricalData, MonitorData详细结构
- **实现重点**: 建筑管理，防御系统，监控和性能分析

#### v2.0 多房间扩展阶段详细设计
- **应用层**: GlobalCoordinator完整功能实现
- **跨房间**: 资源协调、策略同步、全局监控
- **扩展性**: 插件化架构完整实现
- **实现重点**: 多房间管理，资源平衡，全局策略

#### v3.0 智能优化阶段详细设计
- **智能系统**: AIService智能优化服务
- **学习能力**: 行为模式学习，策略优化
- **预测分析**: 需求预测，资源规划
- **自动化部署**: DeploymentService自动化部署系统
- **实现重点**: 机器学习，自适应优化，自动化运维

---

## 2. 模块详细设计

### 2.1 应用层模块详细设计

#### 2.1.1 RoomManager 详细设计

**类图**:
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
│ - initialized: boolean              │
│ - lastTick: number                  │
│ - stats: RoomStats                  │
├─────────────────────────────────────┤
│ + initRoom(): boolean               │
│ + tickRoom(): RoomTickResult        │
│ - collectRoomState(): RoomState     │
│ - updateRoomMemory(): void          │
│ - monitorRoomPerformance(): void    │
│ - cleanup(): void                   │
│ - groupCreepsByRole(): object       │
│ - calculateCreepEfficiency(): number│
│ - countStructures(): number         │
│ - groupStructuresByType(): object   │
│ - calculateStructureHealth(): number│
└─────────────────────────────────────┘
```

**详细类定义**:
```javascript
/**
 * 房间管理器 - 负责协调房间内所有活动
 * @class RoomManager
 */
class RoomManager {
  /**
   * 构造函数
   * @param {string} roomName - 房间名称
   */
  constructor(roomName) {
    // 房间基本信息
    this.roomName = roomName;
    this.room = Game.rooms[roomName];
    
    // 业务管理器实例（依赖注入）
    this.energyManager = new EnergyManager(roomName);
    this.creepManager = new CreepManager(roomName);
    this.roleManager = new RoleManager(roomName);
    this.buildingManager = new BuildingManager(roomName);
    this.defenseManager = new DefenseManager(roomName);
    
    // 服务实例（单例模式）
    this.configService = ConfigService.getInstance();
    this.memoryService = MemoryService.getInstance();
    this.logService = LogService.getInstance();
    this.monitorService = MonitorService.getInstance();
    this.profilerService = ProfilerService.getInstance();
    
    // 状态管理
    this.initialized = false;
    this.lastTick = 0;
    this.stats = {
      totalTicks: 0,
      avgCpuUsage: 0,
      totalErrors: 0,
      lastError: null,
      performance: {
        minCpu: Infinity,
        maxCpu: 0,
        avgCpu: 0
      }
    };
    
    // 缓存管理
    this.cache = {
      roomState: null,
      lastUpdate: 0,
      ttl: 5 // 缓存有效期（tick）
    };
  }
  
  /**
   * 初始化房间
   * @returns {boolean} 初始化是否成功
   * @throws {Error} 初始化失败时抛出异常
   */
  initRoom() {
    const startCpu = Game.cpu.getUsed();
    
    try {
      // 1. 参数验证
      if (!this.roomName || typeof this.roomName !== 'string') {
        throw new Error(`无效的房间名称: ${this.roomName}`);
      }
      
      if (!this.room) {
        this.logService.warn(`RoomManager.initRoom: 房间不存在，等待加载 - ${this.roomName}`);
        return false;
      }
      
      // 2. 加载配置
      const config = this.configService.getRoomConfig(this.roomName);
      if (!config) {
        // 创建默认配置
        config = this.configService.createDefaultConfig(this.roomName);
        this.logService.info(`RoomManager.initRoom: 创建默认配置 - ${this.roomName}`);
      }
      
      // 3. 验证配置
      const validationResult = this.configService.validateConfig(config);
      if (!validationResult.valid) {
        throw new Error(`配置验证失败: ${validationResult.errors.join(', ')}`);
      }
      
      // 4. 初始化业务管理器（按依赖顺序）
      const initResults = {
        energy: this.energyManager.init(config.energy),
        creep: this.creepManager.init(config.creep),
        role: this.roleManager.init(config.role),
        building: this.buildingManager.init(config.building),
        defense: this.defenseManager.init(config.defense)
      };
      
      // 5. 检查初始化结果
      const failedModules = Object.entries(initResults)
        .filter(([_, success]) => !success)
        .map(([module]) => module);
      
      if (failedModules.length > 0) {
        throw new Error(`模块初始化失败: ${failedModules.join(', ')}`);
      }
      
      // 6. 初始化内存结构
      this.memoryService.initRoomMemory(this.roomName, config);
      
      // 7. 记录初始化日志
      const cpuUsed = Game.cpu.getUsed() - startCpu;
      this.logService.info(`RoomManager.initRoom: 房间初始化完成 - ${this.roomName}`, {
        rcl: this.room.controller?.level || 0,
        sources: this.room.find(FIND_SOURCES).length,
        spawns: this.room.find(FIND_MY_SPAWNS).length,
        cpuUsed: cpuUsed.toFixed(2),
        configVersion: config.version
      });
      
      this.initialized = true;
      this.stats.initializationTime = Game.time;
      
      return true;
      
    } catch (error) {
      const cpuUsed = Game.cpu.getUsed() - startCpu;
      this.logService.error(`RoomManager.initRoom: 初始化失败 - ${this.roomName}`, {
        error: error.message,
        stack: error.stack,
        cpuUsed: cpuUsed.toFixed(2),
        timestamp: Game.time
      });
      
      this.stats.totalErrors++;
      this.stats.lastError = {
        message: error.message,
        timestamp: Game.time
      };
      
      // 尝试降级初始化（仅核心模块）
      try {
        this.logService.warn(`RoomManager.initRoom: 尝试降级初始化 - ${this.roomName}`);
        this.energyManager.init(this.configService.getDefaultEnergyConfig());
        this.creepManager.init(this.configService.getDefaultCreepConfig());
        this.initialized = true;
        return true;
      } catch (fallbackError) {
        this.logService.error(`RoomManager.initRoom: 降级初始化也失败 - ${this.roomName}`, fallbackError);
        return false;
      }
    }
  }
  
  /**
   * 处理房间tick
   * @returns {RoomTickResult} tick处理结果
   */
  tickRoom() {
    // 性能监控开始
    const startCpu = Game.cpu.getUsed();
    const tickStart = Game.time;
    const profilerSession = this.profilerService.startSession(`room_tick_${this.roomName}_${tickStart}`);
    
    try {
      // 1. 检查初始化状态
      if (!this.initialized) {
        const success = this.initRoom();
        if (!success) {
          return {
            success: false,
            error: '初始化失败',
            cpuUsed: Game.cpu.getUsed() - startCpu,
            timestamp: tickStart,
            modules: {}
          };
        }
      }
      
      // 2. 检查房间是否存在
      if (!this.room) {
        this.room = Game.rooms[this.roomName];
        if (!this.room) {
          return {
            success: false,
            error: '房间不存在',
            cpuUsed: Game.cpu.getUsed() - startCpu,
            timestamp: tickStart,
            modules: {}
          };
        }
      }
      
      // 3. 收集游戏状态（使用缓存优化）
      const roomState = this.collectRoomStateWithCache();
      
      // 4. 执行业务逻辑（按优先级顺序）
      const moduleResults = {
        energy: this.executeWithProfiling('energy', () => 
          this.energyManager.tick(roomState)),
        creep: this.executeWithProfiling('creep', () => 
          this.creepManager.tick(roomState)),
        role: this.executeWithProfiling('role', () => 
          this.roleManager.tick(roomState)),
        building: this.executeWithProfiling('building', () => 
          this.buildingManager.tick(roomState)),
        defense: this.executeWithProfiling('defense', () => 
          this.defenseManager.tick(roomState))
      };
      
      // 5. 检查模块执行结果
      const failedModules = Object.entries(moduleResults)
        .filter(([_, result]) => !result.success)
        .map(([module]) => module);
      
      // 6. 更新内存状态
      if (failedModules.length === 0) {
        this.updateRoomMemory(roomState, moduleResults);
      }
      
      // 7. 监控和日志
      this.monitorRoomPerformance(startCpu, moduleResults, failedModules);
      
      // 8. 清理和优化（定期执行）
      this.periodicCleanup();
      
      // 9. 更新统计信息
      const cpuUsed = Game.cpu.getUsed() - startCpu;
      this.updateStats(cpuUsed, failedModules.length === 0);
      
      // 10. 性能监控结束
      this.profilerService.stopSession(profilerSession);
      
      return {
        success: failedModules.length === 0,
        cpuUsed,
        timestamp: tickStart,
        modules: moduleResults,
        failedModules: failedModules.length > 0 ? failedModules : undefined,
        warnings: this.collectWarnings(moduleResults)
      };
      
    } catch (error) {
      // 异常处理
      const cpuUsed = Game.cpu.getUsed() - startCpu;
      this.handleTickError(error, cpuUsed, tickStart);
      
      // 性能监控异常结束
      if (profilerSession) {
        this.profilerService.stopSession(profilerSession, { error: error.message });
      }
      
      return {
        success: false,
        error: error.message,
        cpuUsed,
        timestamp: tickStart,
        modules: {},
        isCritical: this.isCriticalError(error)
      };
    }
  }
  
  /**
   * 使用缓存收集房间状态
   * @private
   * @returns {RoomState} 房间状态
   */
  collectRoomStateWithCache() {
    const now = Game.time;
    
    // 检查缓存是否有效
    if (this.cache.roomState && 
        now - this.cache.lastUpdate < this.cache.ttl &&
        this.cache.roomState.timestamp === this.cache.lastUpdate) {
      return this.cache.roomState;
    }
    
    // 重新收集状态
    const roomState = this.collectRoomState();
    this.cache.roomState = roomState;
    this.cache.lastUpdate = now;
    
    return roomState;
  }
  
  /**
   * 收集房间状态（详细实现）
   * @private
   * @returns {RoomState} 房间状态
   */
  collectRoomState() {
    const room = this.room;
    if (!room) {
      throw new Error(`房间不存在: ${this.roomName}`);
    }
    
    const state = {
      // 基础信息
      metadata: {
        name: room.name,
        timestamp: Game.time,
        tickNumber: this.stats.totalTicks + 1,
        roomManagerVersion: '1.0.0'
      },
      
      // 控制器状态
      controller: room.controller ? {
        id: room.controller.id,
        level: room.controller.level,
        progress: room.controller.progress,
        progressTotal: room.controller.progressTotal,
        ticksToDowngrade: room.controller.ticksToDowngrade,
        upgradeBlocked: room.controller.upgradeBlocked,
        safeMode: room.controller.safeMode,
        safeModeAvailable: room.controller.safeModeAvailable,
        safeModeCooldown: room.controller.safeModeCooldown
      } : null,
      
      // 能量状态
      energy: {
        available: room.energyAvailable,
        capacity: room.energyCapacityAvailable,
        utilization: room.energyAvailable / room.energyCapacityAvailable || 0,
        sources: room.find(FIND_SOURCES).map(source => ({
          id: source.id,
          pos: { x: source.pos.x, y: source.pos.y, roomName: source.pos.roomName },
          energy: source.energy,
          energyCapacity: source.energyCapacity,
          ticksToRegeneration: source.ticksToRegeneration || 0,
          harvestableSpots: this.calculateHarvestableSpots(source)
        })),
        mineral: room.find(FIND_MINERALS).map(mineral => ({
          id: mineral.id,
          mineralType: mineral.mineralType,
          density: mineral.density,
          mineralAmount: mineral.mineralAmount
        })),
        deposits: room.find(FIND_DEPOSITS).map(deposit => ({
          id: deposit.id,
          depositType: deposit.depositType,
          cooldown: deposit.cooldown
        })),
        storages: room.find(FIND_MY_STRUCTURES, {
          filter: s => s.structureType === STRUCTURE_STORAGE || 
                      s.structureType === STRUCTURE_CONTAINER ||
                      s.structureType === STRUCTURE_TERMINAL
        }).map(storage => ({
          id: storage.id,
          type: storage.structureType,
          store: storage.store,
          storeCapacity: storage.storeCapacity,
          hits: storage.hits,
          hitsMax: storage.hitsMax,
          pos: { x: storage.pos.x, y: storage.pos.y, roomName: storage.pos.roomName }
        }))
      },
      
      // Creep状态
      creeps: {
        my: room.find(FIND_MY_CREEPS).map(creep => ({
          name: creep.name,
          role: creep.memory.role || 'unknown',
          body: creep.body.map(part => ({
            type: part.type,
            hits: part.hits,
            boost: part.boost
          })),
          store: creep.store,
          storeCapacity: creep.storeCapacity,
          hits: creep.hits,
          hitsMax: creep.hitsMax,
          ticksToLive: creep.ticksToLive,
          fatigue: creep.fatigue,
          spawning: creep.spawning,
          pos: { x: creep.pos.x, y: creep.pos.y, roomName: creep.pos.roomName },
          memory: creep.memory
        })),
        hostile: room.find(FIND_HOSTILE_CREEPS).map(creep => ({
          id: creep.id,
          owner: creep.owner.username,
          body: creep.body.map(part => part.type),
          hits: creep.hits,
          hitsMax: creep.hitsMax,
          pos: { x: creep.pos.x, y: creep.pos.y, roomName: creep.pos.roomName }
        })),
        total: room.find(FIND_CREEPS).length,
        byRole: this.groupCreepsByRole(room.find(FIND_MY_CREEPS))
      },
      
      // 建筑状态
      structures: {
        spawns: room.find(FIND_MY_SPAWNS).map(spawn => ({
          id: spawn.id,
          name: spawn.name,
          spawning: spawn.spawning ? {
            name: spawn.spawning.name,
            remainingTime: spawn.spawning.remainingTime,
            needTime: spawn.spawning.needTime,
            directions: spawn.spawning.directions
          } : null,
          store: spawn.store,
          storeCapacity: spawn.storeCapacity,
          hits: spawn.hits,
          hitsMax: spawn.hitsMax,
          pos: { x: spawn.pos.x, y: spawn.pos.y, roomName: spawn.pos.roomName }
        })),
        extensions: room.find(FIND_MY_STRUCTURES, {
          filter: s => s.structureType === STRUCTURE_EXTENSION
        }).map(extension => ({
          id: extension.id,
          store: extension.store,
          storeCapacity: extension.storeCapacity,
          hits: extension.hits,
          hitsMax: extension.hitsMax,
          pos: { x: extension.pos.x, y: extension.pos.y, roomName: extension.pos.roomName }
        })),
        towers: room.find(FIND_MY_STRUCTURES, {
          filter: s => s.structureType === STRUCTURE_TOWER
        }).map(tower => ({
          id: tower.id,
          store: tower.store,
          storeCapacity: tower.storeCapacity,
          hits: tower.hits,
          hitsMax: tower.hitsMax,
          energy: tower.energy,
          energyCapacity: tower.energyCapacity,
          pos: { x: tower.pos.x, y: tower.pos.y, roomName: tower.pos.roomName }
        })),
        labs: room.find(FIND_MY_STRUCTURES, {
          filter: s => s.structureType === STRUCTURE_LAB
        }).map(lab => ({
          id: lab.id,
          mineralType: lab.mineralType,
          mineralAmount: lab.mineralAmount,
          energy: lab.energy,
          cooldown: lab.cooldown,
          hits: lab.hits,
          hitsMax: lab.hitsMax,
          pos: { x: lab.pos.x, y: lab.pos.y, roomName: lab.pos.roomName }
        })),
        constructionSites: room.find(FIND_MY_CONSTRUCTION_SITES).map(site => ({
          id: site.id,
          structureType: site.structureType,
          progress: site.progress,
          progressTotal: site.progressTotal,
          pos: { x: site.pos.x, y: site.pos.y, roomName: site.pos.roomName }
        })),
        walls: room.find(FIND_STRUCTURES, {
          filter: s => s.structureType === STRUCTURE_WALL
        }).map(wall => ({
          id: wall.id,
          hits: wall.hits,
          hitsMax: wall.hitsMax,
          pos: { x: wall.pos.x, y: wall.pos.y, roomName: wall.pos.roomName }
        })),
        ramparts: room.find(FIND_STRUCTURES, {
          filter: s => s.structureType === STRUCTURE_RAMPART
        }).map(rampart => ({
          id: rampart.id,
          hits: rampart.hits,
          hitsMax: rampart.hitsMax,
          isPublic: rampart.isPublic,
          pos: { x: rampart.pos.x, y: rampart.pos.y, roomName: rampart.pos.roomName }
        }))
      },
      
      // 地形信息
      terrain: {
        walls: room.find(FIND_STRUCTURES, {
          filter: s => s.structureType === STRUCTURE_WALL
        }).length,
        ramparts: room.find(FIND_STRUCTURES, {
          filter: s => s.structureType === STRUCTURE_RAMPART
        }).length,
        roads: room.find(FIND_STRUCTURES, {
          filter: s => s.structureType === STRUCTURE_ROAD
        }).map(road => ({
          id: road.id,
          hits: road.hits,
          hitsMax: road.hitsMax,
          pos: { x: road.pos.x, y: road.pos.y, roomName: road.pos.roomName }
        })),
        terrainData: room.getTerrain().getRawBuffer()
      },
      
      // 资源状态
      resources: {
        dropped: room.find(FIND_DROPPED_RESOURCES).map(resource => ({
          id: resource.id,
          resourceType: resource.resourceType,
          amount: resource.amount,
          pos: { x: resource.pos.x, y: resource.pos.y, roomName: resource.pos.roomName }
        })),
        tombstones: room.find(FIND_TOMBSTONES).map(tombstone => ({
          id: tombstone.id,
          store: tombstone.store,
          deathTime: tombstone.deathTime,
          pos: { x: tombstone.pos.x, y: tombstone.pos.y, roomName: tombstone.pos.roomName }
        })),
        ruins: room.find(FIND_RUINS).map(ruin => ({
          id: ruin.id,
          store: ruin.store,
          structure: ruin.structure,
          destroyTime: ruin.destroyTime,
          pos: { x: ruin.pos.x, y: ruin.pos.y, roomName: ruin.pos.roomName }
        }))
      }
    };
    
    return state;
  }
  
  /**
   * 计算可采集点数量
   * @private
   * @param {Source} source - 能量源
   * @returns {number} 可采集点数量
   */
  calculateHarvestableSpots(source) {
    if (!source || !source.pos) return 0;
    
    const terrain = source.room.getTerrain();
    let count = 0;
    
    // 检查周围8个方向
    for (let dx = -1; dx <= 1; dx++) {
      for (let dy = -1; dy <= 1; dy++) {
        if (dx === 0 && dy === 0) continue;
        
        const x = source.pos.x + dx;
        const y = source.pos.y + dy;
        
        // 检查地形是否可通行
        const terrainType = terrain.get(x, y);
        if (terrainType !== TERRAIN_MASK_WALL) {
          count++;
        }
      }
    }
    
    return count;
  }
  
  /**
   * 执行带性能监控的函数
   * @private
   * @param {string} moduleName - 模块名称
   * @param {Function} func - 要执行的函数
   * @returns {any} 执行结果
   */
  executeWithProfiling(moduleName, func) {
    const startCpu = Game.cpu.getUsed();
    
    try {
      const result = func();
      const cpuUsed = Game.cpu.getUsed() - startCpu;
      
      // 记录性能数据
      this.profilerService.recordModulePerformance(moduleName, cpuUsed);
      
      // 添加CPU使用信息到结果
      if (result && typeof result === 'object') {
        result.cpuUsed = cpuUsed;
      }
      
      return result;
    } catch (error) {
      const cpuUsed = Game.cpu.getUsed() - startCpu;
      this.logService.error(`RoomManager.executeWithProfiling: 模块执行失败 - ${moduleName}`, {
        error: error.message,
        cpuUsed: cpuUsed.toFixed(2),
        timestamp: Game.time
      });
      
      return {
        success: false,
        error: error.message,
        cpuUsed,
        module: moduleName
      };
    }
  }
  
  /**
   * 更新房间内存
   * @private
   * @param {RoomState} roomState - 房间状态
   * @param {Object} moduleResults - 业务处理结果
   */
  updateRoomMemory(roomState, moduleResults) {
    try {
      // 1. 更新状态数据
      const stateUpdate = {
        energy: {
          available: roomState.energy.available,
          capacity: roomState.energy.capacity,
          utilization: roomState.energy.utilization,
          sourceCount: roomState.energy.sources.length,
          storageCount: roomState.energy.storages.length
        },
        creeps: {
          count: roomState.creeps.my.length,
          byRole: roomState.creeps.byRole,
          hostileCount: roomState.creeps.hostile.length,
          totalCount: roomState.creeps.total
        },
        structures: {
          spawnCount: roomState.structures.spawns.length,
          extensionCount: roomState.structures.extensions.length,
          towerCount: roomState.structures.towers.length,
          labCount: roomState.structures.labs.length,
          constructionSiteCount: roomState.structures.constructionSites.length,
          wallCount: roomState.structures.walls.length,
          rampartCount: roomState.structures.ramparts.length
        },
        controller: roomState.controller ? {
          level: roomState.controller.level,
          progress: roomState.controller.progress,
          progressTotal: roomState.controller.progressTotal,
          ticksToDowngrade: roomState.controller.ticksToDowngrade
        } : null,
        timestamp: Game.time
      };
      
      this.memoryService.updateRoomState(this.roomName, stateUpdate);
      
      // 2. 添加历史记录（采样，避免内存爆炸）
      if (Game.time % 10 === 0) { // 每10tick记录一次
        this.memoryService.addHistory(this.roomName, 'energy', {
          tick: Game.time,
          available: roomState.energy.available,
          capacity: roomState.energy.capacity,
          utilization: roomState.energy.utilization
        });
        
        this.memoryService.addHistory(this.roomName, 'creep', {
          tick: Game.time,
          count: roomState.creeps.my.length,
          roles: roomState.creeps.byRole,
          hostile: roomState.creeps.hostile.length
        });
      }
      
      // 3. 记录模块执行结果
      Object.entries(moduleResults).forEach(([module, result]) => {
        if (result && result.success !== undefined) {
          this.memoryService.addModuleResult(this.roomName, module, {
            tick: Game.time,
            success: result.success,
            cpuUsed: result.cpuUsed || 0,
            error: result.error
          });
        }
      });
      
    } catch (error) {
      this.logService.warn(`RoomManager.updateRoomMemory: 内存更新失败`, {
        error: error.message,
        room: this.roomName,
        timestamp: Game.time
      });
    }
  }
  
  /**
   * 监控房间性能
   * @private
   * @param {number} startCpu - 起始CPU使用量
   * @param {Object} moduleResults - 业务处理结果
   * @param {Array} failedModules - 失败的模块列表
   */
  monitorRoomPerformance(startCpu, moduleResults, failedModules) {
    const cpuUsed = Game.cpu.getUsed() - startCpu;
    const now = Game.time;
    
    // 1. 记录性能数据
    this.monitorService.recordPerformance(this.roomName, {
      tick: now,
      cpuUsed: cpuUsed.toFixed(2),
      memoryUsed: JSON.stringify(Memory).length,
      modulePerformance: Object.keys(moduleResults).reduce((acc, key) => {
        acc[key] = moduleResults[key]?.cpuUsed || 0;
        return acc;
      }, {}),
      failedModules: failedModules.length > 0 ? failedModules : undefined
    });
    
    // 2. CPU使用率告警
    if (cpuUsed > 15) { // 15 CPU阈值
      this.monitorService.alert('warning', `房间${this.roomName} CPU使用率过高: ${cpuUsed.toFixed(2)}`, {
        room: this.roomName,
        cpuUsed: cpuUsed.toFixed(2),
        timestamp: now,
        modules: Object.keys(moduleResults).map(key => ({
          name: key,
          cpu: moduleResults[key]?.cpuUsed || 0
        }))
      });
    }
    
    // 3. 内存使用告警
    const memorySize = JSON.stringify(Memory).length;
    if (memorySize > 500000) { // 500KB阈值
      this.monitorService.alert('warning', `房间${this.roomName} 内存使用过高: ${(memorySize / 1024).toFixed(2)}KB`, {
        room: this.roomName,
        memoryKB: (memorySize / 1024).toFixed(2),
        timestamp: now
      });
    }
    
    // 4. 模块错误监控
    failedModules.forEach(module => {
      const result = moduleResults[module];
      this.monitorService.alert('error', `模块${module}执行失败`, {
        room: this.roomName,
        module: module,
        error: result?.error || '未知错误',
        cpuUsed: result?.cpuUsed || 0,
        timestamp: now
      });
    });
    
    // 5. 性能趋势分析
    if (now % 100 === 0) { // 每100tick分析一次
      const trend = this.monitorService.analyzePerformanceTrend(this.roomName, 100);
      if (trend.cpuIncreasing && trend.cpuSlope > 0.1) {
        this.monitorService.alert('info', `房间${this.roomName} CPU使用率呈上升趋势`, {
          room: this.roomName,
          slope: trend.cpuSlope.toFixed(3),
          currentAvg: trend.currentAvg.toFixed(2),
          timestamp: now
        });
      }
    }
  }
  
  /**
   * 定期清理
   * @private
   */
  periodicCleanup() {
    const now = Game.time;
    
    // 1. 每100tick清理一次缓存
    if (now % 100 === 0) {
      this.cache.roomState = null;
      this.cache.lastUpdate = 0;
    }
    
    // 2. 每500tick清理一次内存
    if (now % 500 === 0) {
      this.memoryService.cleanupRoomMemory(this.roomName);
    }
    
    // 3. 每1000tick压缩一次内存
    if (now % 1000 === 0) {
      this.memoryService.compressRoomMemory(this.roomName);
    }
    
    // 4. 每10000tick重置统计
    if (now % 10000 === 0) {
      this.stats = {
        totalTicks: 0,
        avgCpuUsage: 0,
        totalErrors: 0,
        lastError: null,
        performance: {
          minCpu: Infinity,
          maxCpu: 0,
          avgCpu: 0
        }
      };
    }
  }
  
  /**
   * 更新统计信息
   * @private
   * @param {number} cpuUsed - 本次tick的CPU使用量
   * @param {boolean} success - 是否成功
   */
  updateStats(cpuUsed, success) {
    this.stats.totalTicks++;
    
    // 更新CPU统计
    this.stats.performance.minCpu = Math.min(this.stats.performance.minCpu, cpuUsed);
    this.stats.performance.maxCpu = Math.max(this.stats.performance.maxCpu, cpuUsed);
    this.stats.performance.avgCpu = 
      (this.stats.performance.avgCpu * (this.stats.totalTicks - 1) + cpuUsed) / this.stats.totalTicks;
    
    // 更新错误统计
    if (!success) {
      this.stats.totalErrors++;
    }
    
    // 更新平均CPU使用率
    this.stats.avgCpuUsage = 
      (this.stats.avgCpuUsage * (this.stats.totalTicks - 1) + cpuUsed) / this.stats.totalTicks;
  }
  
  /**
   * 收集警告信息
   * @private
   * @param {Object} moduleResults - 模块执行结果
   * @returns {Array} 警告列表
   */
  collectWarnings(moduleResults) {
    const warnings = [];
    
    Object.entries(moduleResults).forEach(([module, result]) => {
      if (result && result.warnings) {
        result.warnings.forEach(warning => {
          warnings.push({
            module,
            message: warning.message || warning,
            severity: warning.severity || 'warning',
            timestamp: Game.time
          });
        });
      }
      
      // CPU使用率警告
      if (result && result.cpuUsed > 5) {
        warnings.push({
          module,
          message: `CPU使用率较高: ${result.cpuUsed.toFixed(2)}`,
          severity: 'warning',
          timestamp: Game.time
        });
      }
    });
    
    return warnings.length > 0 ? warnings : undefined;
  }
  
  /**
   * 处理tick错误
   * @private
   * @param {Error} error - 错误对象
   * @param {number} cpuUsed - CPU使用量
   * @param {number} timestamp - 时间戳
   */
  handleTickError(error, cpuUsed, timestamp) {
    this.logService.error(`RoomManager.handleTickError: tick处理异常 - ${this.roomName}`, {
      error: error.message,
      stack: error.stack,
      cpuUsed: cpuUsed.toFixed(2),
      timestamp
    });
    
    this.stats.totalErrors++;
    this.stats.lastError = {
      message: error.message,
      stack: error.stack,
      cpuUsed,
      timestamp
    };
    
    // 错误恢复：根据错误类型采取不同策略
    if (this.isCriticalError(error)) {
      this.logService.warn(`RoomManager.handleTickError: 关键错误，尝试重新初始化 - ${this.roomName}`);
      this.initialized = false;
    } else if (this.isMemoryError(error)) {
      this.logService.warn(`RoomManager.handleTickError: 内存错误，尝试清理内存 - ${this.roomName}`);
      this.memoryService.emergencyCleanup(this.roomName);
    }
  }
  
  /**
   * 检查是否为关键错误
   * @private
   * @param {Error} error - 错误对象
   * @returns {boolean} 是否为关键错误
   */
  isCriticalError(error) {
    const criticalPatterns = [
      /内存/,
      /初始化/,
      /配置/,
      /房间不存在/,
      /无法访问/
    ];
    
    return criticalPatterns.some(pattern => 
      pattern.test(error.message) || (error.stack && pattern.test(error.stack))
    );
  }
  
  /**
   * 检查是否为内存错误
   * @private
   * @param {Error} error - 错误对象
   * @returns {boolean} 是否为内存错误
   */
  isMemoryError(error) {
    const memoryPatterns = [
      /内存不足/,
      /Memory/,
      /内存溢出/,
      /序列化/,
      /JSON/
    ];
    
    return memoryPatterns.some(pattern => 
      pattern.test(error.message) || (error.stack && pattern.test(error.stack))
    );
  }
  
  /**
   * 按角色分组Creep
   * @private
   * @param {Array} creeps - Creep数组
   * @returns {Object} 按角色分组的统计
   */
  groupCreepsByRole(creeps) {
    return creeps.reduce((acc, creep) => {
      const role = creep.memory?.role || 'unknown';
      if (!acc[role]) {
        acc[role] = {
          count: 0,
          totalHits: 0,
          totalHitsMax: 0,
          totalStore: 0,
          totalStoreCapacity: 0
        };
      }
      
      acc[role].count++;
      acc[role].totalHits += creep.hits || 0;
      acc[role].totalHitsMax += creep.hitsMax || 0;
      acc[role].totalStore += Object.values(creep.store || {}).reduce((sum, val) => sum + val, 0);
      acc[role].totalStoreCapacity += creep.storeCapacity || 0;
      
      return acc;
    }, {});
  }
  
  /**
   * 获取房间统计信息
   * @returns {RoomStats} 房间统计信息
   */
  getStats() {
    return {
      ...this.stats,
      roomName: this.roomName,
      initialized: this.initialized,
      lastTick: this.lastTick,
      currentTime: Game.time
    };
  }
  
  /**
   * 获取房间状态摘要
   * @returns {RoomSummary} 房间状态摘要
   */
  getSummary() {
    if (!this.room) {
      return {
        roomName: this.roomName,
        exists: false,
        initialized: this.initialized
      };
    }
    
    return {
      roomName: this.roomName,
      exists: true,
      initialized: this.initialized,
      controllerLevel: this.room.controller?.level || 0,
      energy: {
        available: this.room.energyAvailable,
        capacity: this.room.energyCapacityAvailable
      },
      creeps: {
        my: this.room.find(FIND_MY_CREEPS).length,
        hostile: this.room.find(FIND_HOSTILE_CREEPS).length
      },
      structures: {
        spawns: this.room.find(FIND_MY_SPAWNS).length,
        extensions: this.room.find(FIND_MY_STRUCTURES, {
          filter: s => s.structureType === STRUCTURE_EXTENSION
        }).length
      },
      stats: this.stats
    };
  }
  
  /**
   * 销毁房间管理器
   */
  destroy() {
    // 清理业务管理器
    if (this.energyManager && typeof this.energyManager.destroy === 'function') {
      this.energyManager.destroy();
    }
    if (this.creepManager && typeof this.creepManager.destroy === 'function') {
      this.creepManager.destroy();
    }
    if (this.roleManager && typeof this.roleManager.destroy === 'function') {
      this.roleManager.destroy();
    }
    if (this.buildingManager && typeof this.buildingManager.destroy === 'function') {
      this.buildingManager.destroy();
    }
    if (this.defenseManager && typeof this.defenseManager.destroy === 'function') {
      this.defenseManager.destroy();
    }
    
    // 清理缓存
    this.cache.roomState = null;
    this.cache.lastUpdate = 0;
    
    // 记录销毁日志
    this.logService.info(`RoomManager.destroy: 房间管理器已销毁 - ${this.roomName}`, {
      totalTicks: this.stats.totalTicks,
      avgCpuUsage: this.stats.avgCpuUsage.toFixed(2),
      totalErrors: this.stats.totalErrors,
      timestamp: Game.time
    });
    
    // 重置状态
    this.initialized = false;
    this.room = null;
  }
}

// RoomManager相关类型定义
/**
 * @typedef {Object} RoomTickResult
 * @property {boolean} success - 是否成功
 * @property {number} cpuUsed - CPU使用量
 * @property {number} timestamp - 时间戳
 * @property {Object} modules - 模块执行结果
 * @property {Array} [failedModules] - 失败的模块列表
 * @property {Array} [warnings] - 警告列表
 * @property {string} [error] - 错误信息
 * @property {boolean} [isCritical] - 是否为关键错误
 */

/**
 * @typedef {Object} RoomStats
 * @property {number} totalTicks - 总tick数
 * @property {number} avgCpuUsage - 平均CPU使用率
 * @property {number} totalErrors - 总错误数
 * @property {Object} [lastError] - 最后错误信息
 * @property {Object} performance - 性能统计
 * @property {number} performance.minCpu - 最小CPU使用量
 * @property {number} performance.maxCpu - 最大CPU使用量
 * @property {number} performance.avgCpu - 平均CPU使用量
 * @property {string} roomName - 房间名称
 * @property {boolean} initialized - 是否已初始化
 * @property {number} lastTick - 最后tick时间
 * @property {number} currentTime - 当前时间
 */

/**
 * @typedef {Object} RoomSummary
 * @property {string} roomName - 房间名称
 * @property {boolean} exists - 房间是否存在
 * @property {boolean} initialized - 是否已初始化
 * @property {number} [controllerLevel] - 控制器等级
 * @property {Object} [energy] - 能量信息
 * @property {number} energy.available - 可用能量
 * @property {number} energy.capacity - 能量容量
 * @property {Object} [creeps] - Creep信息
 * @property {number} creeps.my - 我的Creep数量
 * @property {number} creeps.hostile - 敌对Creep数量
 * @property {Object} [structures] - 建筑信息
 * @property {number} structures.spawns - Spawn数量
 * @property {number} structures.extensions - Extension数量
 * @property {RoomStats} [stats] - 统计信息
 */
```

### 2.1.2 GlobalCoordinator 详细设计（v2.0阶段）

**类图**:
```
┌─────────────────────────────────────┐
│        GlobalCoordinator            │
├─────────────────────────────────────┤
│ - roomManagers: Map<string, RoomManager>
│ - resourceBalancer: ResourceBalancer│
│ - strategyCoordinator: StrategyCoordinator
│ - defenseCoordinator: DefenseCoordinator
│ - configService: ConfigService      │
│ - logService: LogService            │
│ - monitorService: MonitorService    │
│ - initialized: boolean              │
│ - stats: GlobalStats                │
├─────────────────────────────────────┤
│ + init(): boolean                   │
│ + tick(): GlobalTickResult          │
│ + addRoom(roomName): boolean        │
│ + removeRoom(roomName): boolean     │
│ + getRoomStatus(roomName): RoomStatus│
│ + balanceResources(): BalanceResult │
│ + setGlobalStrategy(strategy): void │
│ + getGlobalStatus(): GlobalStatus   │
│ - coordinateRooms(): void           │
│ - monitorGlobalPerformance(): void  │
│ - handleGlobalErrors(): void        │
└─────────────────────────────────────┘
```

**详细类定义**:
```javascript
/**
 * 全局协调器 - 负责多房间协调和管理（v2.0阶段）
 * @class GlobalCoordinator
 */
class GlobalCoordinator {
  /**
   * 构造函数
   */
  constructor() {
    // 房间管理器映射
    this.roomManagers = new Map(); // roomName -> RoomManager
    
    // 协调器组件
    this.resourceBalancer = new ResourceBalancer();
    this.strategyCoordinator = new StrategyCoordinator();
    this.defenseCoordinator = new DefenseCoordinator();
    
    // 服务实例
    this.configService = ConfigService.getInstance();
    this.logService = LogService.getInstance();
    this.monitorService = MonitorService.getInstance();
    this.profilerService = ProfilerService.getInstance();
    
    // 状态管理
    this.initialized = false;
    this.stats = {
      totalTicks: 0,
      totalRooms: 0,
      avgCpuPerRoom: 0,
      totalErrors: 0,
      resourceTransfers: 0,
      strategyUpdates: 0
    };
    
    // 全局配置
    this.globalConfig = {
      maxRooms: 10,
      minCpuPerRoom: 5,
      maxCpuPerRoom: 20,
      resourceBalanceInterval: 100,
      strategyUpdateInterval: 1000
    };
  }
  
  /**
   * 初始化全局协调器
   * @returns {boolean} 初始化是否成功
   */
  init() {
    try {
      // 1. 加载全局配置
      const config = this.configService.getGlobalConfig();
      if (config) {
        this.globalConfig = { ...this.globalConfig, ...config };
      }
      
      // 2. 初始化协调器组件
      this.resourceBalancer.init();
      this.strategyCoordinator.init();
      this.defenseCoordinator.init();
      
      // 3. 加载已有房间
      const savedRooms = this.configService.getSavedRooms();
      savedRooms.forEach(roomName => {
        this.addRoom(roomName);
      });
      
      // 4. 记录初始化日志
      this.logService.info('GlobalCoordinator.init: 全局协调器初始化完成', {
        totalRooms: this.roomManagers.size,
        config: this.globalConfig,
        timestamp: Game.time
      });
      
      this.initialized = true;
      return true;
      
    } catch (error) {
      this.logService.error('GlobalCoordinator.init: 初始化失败', {
        error: error.message,
        stack: error.stack,
        timestamp: Game.time
      });
      return false;
    }
  }
  
  /**
   * 处理全局tick
   * @returns {GlobalTickResult} 全局tick处理结果
   */
  tick() {
    const startCpu = Game.cpu.getUsed();
    const tickStart = Game.time;
    
    try {
      // 1. 检查初始化状态
      if (!this.initialized) {
        const success = this.init();
        if (!success) {
          return {
            success: false,
            error: '全局协调器初始化失败',
            cpuUsed: Game.cpu.getUsed() - startCpu,
            timestamp: tickStart
          };
        }
      }
      
      // 2. 执行房间tick（并行处理，受CPU限制）
      const roomResults = this.executeRoomTicks();
      
      // 3. 协调房间间活动（定期执行）
      const coordinationResults = this.coordinateRooms();
      
      // 4. 监控全局性能
      this.monitorGlobalPerformance(startCpu, roomResults, coordinationResults);
      
      // 5. 更新统计信息
      const cpuUsed = Game.cpu.getUsed() - startCpu;
      this.updateGlobalStats(cpuUsed, roomResults, coordinationResults);
      
      return {
        success: true,
        cpuUsed,
        timestamp: tickStart,
        roomResults,
        coordinationResults,
        stats: this.getCurrentStats()
      };
      
    } catch (error) {
      const cpuUsed = Game.cpu.getUsed() - startCpu;
      this.handleGlobalError(error, cpuUsed, tickStart);
      
      return {
        success: false,
        error: error.message,
        cpuUsed,
        timestamp: tickStart,
        isCritical: this.isGlobalCriticalError(error)
      };
    }
  }
  
  /**
   * 添加房间到全局管理
   * @param {string} roomName - 房间名称
   * @returns {boolean} 是否添加成功
   */
  addRoom(roomName) {
    try {
      // 1. 参数验证
      if (!roomName || typeof roomName !== 'string') {
        throw new Error(`无效的房间名称: ${roomName}`);
      }
      
      // 2. 检查房间是否已存在
      if (this.roomManagers.has(roomName)) {
        this.logService.warn(`GlobalCoordinator.addRoom: 房间已存在 - ${roomName}`);
        return false;
      }
      
      // 3. 检查房间数量限制
      if (this.roomManagers.size >= this.globalConfig.maxRooms) {
        this.logService.warn(`GlobalCoordinator.addRoom: 达到最大房间数限制 - ${this.globalConfig.maxRooms}`);
        return false

