# MemoryService 详细设计文档

## 📋 文档信息
- **模块名称**: MemoryService（内存服务）
- **所属层级**: 服务层
- **文档版本**: v1.0.0
- **创建日期**: 2026-03-25
- **最后更新**: 2026-03-25
- **负责人**: Moss (OpenClaw AI)
- **状态**: [草案]
- **优先级**: P0 (v1.0核心模块)
- **关联文档**: 
  - `CONFIG_SERVICE.md` - 配置服务设计

## 🎯 设计目标

### 核心职责
1. **内存结构管理** - 统一管理游戏内存结构
2. **序列化和反序列化** - 高效的内存读写操作
3. **内存压缩和优化** - 减少内存使用量
4. **内存清理和维护** - 定期清理无效数据
5. **内存监控和告警** - 监控内存使用情况
6. **备份和恢复** - 内存数据的备份和恢复

### 质量目标
- **性能**: 内存操作延迟 < 2 ticks
- **效率**: 内存压缩率 > 30%
- **可靠性**: 数据一致性 100%
- **可用性**: 服务可用性 99.99%
- **安全性**: 数据完整性检查 100%

## 🏗️ 类图设计

### 类结构
```
┌─────────────────────────────────────┐
│          MemoryService              │
├─────────────────────────────────────┤
│ - memory: GameMemory                │
│ - structures: Map<string, MemoryStructure>
│ - compressors: Map<string, Compressor>
│ - cleaners: Map<string, Cleaner>    │
│ - monitors: Map<string, Monitor>    │
│ - config: MemoryConfig              │
│ - stats: MemoryStats                │
│ - cache: MemoryCache                │
├─────────────────────────────────────┤
│ + getInstance(): MemoryService      │
│ + get<T>(path: string): T           │
│ + set<T>(path: string, value: T): boolean
│ + delete(path: string): boolean     │
│ + compress(): CompressionResult     │
│ + clean(): CleanupResult            │
│ + backup(): BackupResult            │
│ + restore(backupId: string): RestoreResult
│ + monitor(): MonitoringReport       │
│ + getStats(): MemoryStats           │
│ + validate(): ValidationResult      │
│ - initializeStructures(): void      │
│ - updateCache(): void               │
│ - scheduleMaintenance(): void       │
│ - notifyMonitors(): void            │
│ - performGarbageCollection(): void  │
└─────────────────────────────────────┘
```

### 核心组件
```
MemoryService
    ├── MemoryManager      - 内存结构管理
    ├── Serializer         - 序列化和反序列化
    ├── Compressor         - 内存压缩优化
    ├── Cleaner            - 内存清理维护
    ├── Monitor            - 内存监控告警
    ├── BackupManager      - 备份和恢复
    └── CacheManager       - 缓存管理
```

## 📝 接口定义

### 公共接口

#### 1. 单例获取接口
```javascript
/**
 * 获取MemoryService单例实例
 * @returns {MemoryService} MemoryService实例
 */
static getInstance(): MemoryService
```

#### 2. 内存读写接口
```javascript
/**
 * 获取内存数据
 * @template T
 * @param {string} path - 内存路径
 * @param {T} [defaultValue] - 默认值
 * @returns {T} 内存数据
 */
get<T>(path: string, defaultValue?: T): T

/**
 * 设置内存数据
 * @template T
 * @param {string} path - 内存路径
 * @param {T} value - 要设置的值
 * @param {boolean} [compress=true] - 是否压缩
 * @returns {boolean} 设置是否成功
 */
set<T>(path: string, value: T, compress?: boolean): boolean

/**
 * 删除内存数据
 * @param {string} path - 内存路径
 * @returns {boolean} 删除是否成功
 */
delete(path: string): boolean

/**
 * 检查内存路径是否存在
 * @param {string} path - 内存路径
 * @returns {boolean} 是否存在
 */
has(path: string): boolean
```

#### 3. 内存维护接口
```javascript
/**
 * 压缩内存
 * @returns {CompressionResult} 压缩结果
 */
compress(): CompressionResult

/**
 * 清理内存
 * @returns {CleanupResult} 清理结果
 */
clean(): CleanupResult

/**
 * 执行垃圾回收
 * @returns {GarbageCollectionResult} 垃圾回收结果
 */
garbageCollect(): GarbageCollectionResult
```

#### 4. 备份恢复接口
```javascript
/**
 * 创建内存备份
 * @param {string} [name] - 备份名称
 * @returns {BackupResult} 备份结果
 */
backup(name?: string): BackupResult

/**
 * 恢复内存备份
 * @param {string} backupId - 备份ID
 * @returns {RestoreResult} 恢复结果
 */
restore(backupId: string): RestoreResult

/**
 * 列出所有备份
 * @returns {BackupInfo[]} 备份列表
 */
listBackups(): BackupInfo[]
```

#### 5. 监控接口
```javascript
/**
 * 监控内存状态
 * @returns {MonitoringReport} 监控报告
 */
monitor(): MonitoringReport

/**
 * 获取内存统计
 * @returns {MemoryStats} 内存统计
 */
getStats(): MemoryStats

/**
 * 验证内存完整性
 * @returns {ValidationResult} 验证结果
 */
validate(): ValidationResult
```

### 数据类型定义

#### MemoryConfig
```javascript
interface MemoryConfig {
  // 内存结构配置
  structures: {
    [path: string]: MemoryStructureConfig;
  };
  
  // 序列化配置
  serialization: {
    enabled: boolean;
    compressionLevel: 0 | 1 | 2 | 3; // 0: 无压缩, 3: 最大压缩
    maxDepth: number;                // 最大嵌套深度
    maxSize: number;                 // 最大序列化大小（字节）
    circularReference: 'error' | 'ignore' | 'handle'; // 循环引用处理
  };
  
  // 压缩配置
  compression: {
    enabled: boolean;
    algorithm: 'simple' | 'efficient' | 'aggressive'; // 压缩算法
    threshold: number;               // 压缩阈值（字节）
    minSavings: number;              // 最小节省比例（0-1）
    maxCompressionTime: number;      // 最大压缩时间（ticks）
  };
  
  // 清理配置
  cleanup: {
    enabled: boolean;
    interval: number;                // 清理间隔（ticks）
    strategies: CleanupStrategy[];   // 清理策略
    retention: {                     // 数据保留策略
      [dataType: string]: number;    // 数据类型 -> 保留时间（ticks）
    };
  };
  
  // 监控配置
  monitoring: {
    enabled: boolean;
    samplingInterval: number;        // 采样间隔（ticks）
    alertThresholds: {               // 告警阈值
      memoryUsage: number;           // 内存使用率阈值（0-1）
      fragmentation: number;         // 内存碎片化阈值（0-1）
      growthRate: number;            // 内存增长率阈值（每tick）
      errorRate: number;             // 错误率阈值（0-1）
    };
    metrics: string[];               // 监控指标
  };
  
  // 备份配置
  backup: {
    enabled: boolean;
    interval: number;                // 备份间隔（ticks）
    maxBackups: number;              // 最大备份数量
    retentionDays: number;           // 备份保留天数
    compression: boolean;            // 备份是否压缩
  };
  
  // 缓存配置
  cache: {
    enabled: boolean;
    ttl: number;                     // 缓存有效期（ticks）
    maxSize: number;                 // 最大缓存大小（字节）
    evictionPolicy: 'lru' | 'lfu' | 'fifo'; // 淘汰策略
  };
}
```

#### CompressionResult
```javascript
interface CompressionResult {
  success: boolean;                    // 是否成功
  originalSize: number;                // 原始大小（字节）
  compressedSize: number;              // 压缩后大小（字节）
  savings: number;                     // 节省空间（字节）
  savingsRatio: number;                // 节省比例（0-1）
  duration: number;                    // 压缩耗时（ticks）
  details: CompressionDetail[];        // 详细压缩信息
  warnings: CompressionWarning[];      // 压缩警告
}

interface CompressionDetail {
  path: string;                        // 内存路径
  originalSize: number;                // 原始大小
  compressedSize: number;              // 压缩后大小
  savings: number;                     // 节省空间
  algorithm: string;                   // 使用的算法
  compressionRatio: number;            // 压缩比
}
```

#### CleanupResult
```javascript
interface CleanupResult {
  success: boolean;                    // 是否成功
  cleaned: CleanedItem[];              // 清理的项目
  totalCleaned: number;                // 总清理数量
  totalSize: number;                   // 总清理大小（字节）
  duration: number;                    // 清理耗时（ticks）
  stats: CleanupStats;                 // 清理统计
  warnings: CleanupWarning[];          // 清理警告
}

interface CleanedItem {
  path: string;                        // 内存路径
  type: string;                        // 数据类型
  size: number;                        // 数据大小（字节）
  age: number;                         // 数据年龄（ticks）
  reason: string;                      // 清理原因
  timestamp: number;                   // 清理时间
}

interface CleanupStats {
  byType: { [type: string]: number };  // 按类型统计
  byAge: { [ageRange: string]: number }; // 按年龄统计
  bySize: { [sizeRange: string]: number }; // 按大小统计
  totalItems: number;                  // 总项目数
  totalSize: number;                   // 总大小
  fragmentation: number;               // 碎片化程度（0-1）
}
```

#### MonitoringReport
```javascript
interface MonitoringReport {
  timestamp: number;                   // 报告时间
  overall: {
    totalMemory: number;               // 总内存（字节）
    usedMemory: number;                // 已用内存（字节）
    freeMemory: number;                // 可用内存（字节）
    usageRatio: number;                // 使用率（0-1）
    fragmentation: number;             // 碎片化程度（0-1）
    growthRate: number;                // 增长率（字节/tick）
    errorRate: number;                 // 错误率（0-1）
  };
  
  byStructure: {
    [path: string]: StructureMetrics;
  };
  
  byType: {
    [type: string]: TypeMetrics;
  };
  
  performance: {
    readLatency: number;               // 读取延迟（ticks）
    writeLatency: number;              // 写入延迟（ticks）
    compressionTime: number;           // 压缩时间（ticks）
    cleanupTime: number;               // 清理时间（ticks）
    cacheHitRate: number;              // 缓存命中率（0-1）
  };
  
  alerts: Alert[];                     // 告警信息
  recommendations: Recommendation[];   // 建议信息
  trends: Trend[];                     // 趋势信息
}

interface StructureMetrics {
  path: string;                        // 内存路径
  size: number;                        // 大小（字节）
  itemCount: number;                   // 项目数量
  avgItemSize: number;                 // 平均项目大小
  maxItemSize: number;                 // 最大项目大小
  minItemSize: number;                 // 最小项目大小
  accessCount: number;                 // 访问次数
  lastAccess: number;                  // 最后访问时间
  age: number;                         // 数据年龄（ticks）
  compressionRatio: number;            // 压缩比
  fragmentation: number;               // 碎片化程度
}
```

#### MemoryStats
```javascript
interface MemoryStats {
  // 总体统计
  overall: {
    totalMemory: number;               // 总内存（字节）
    usedMemory: number;                // 已用内存（字节）
    freeMemory: number;                // 可用内存（字节）
    usageRatio: number;                // 使用率（0-1）
    fragmentation: number;             // 碎片化程度（0-1）
    itemCount: number;                 // 总项目数
    structureCount: number;            // 结构数量
  };
  
  // 性能统计
  performance: {
    totalReads: number;                // 总读取次数
    totalWrites: number;               // 总写入次数
    totalDeletes: number;              // 总删除次数
    avgReadLatency: number;            // 平均读取延迟（ticks）
    avgWriteLatency: number;           // 平均写入延迟（ticks）
    cacheHitRate: number;              // 缓存命中率（0-1）
    compressionCount: number;          // 压缩次数
    cleanupCount: number;              // 清理次数
    backupCount: number;               // 备份次数
  };
  
  // 效率统计
  efficiency: {
    totalCompressionSavings: number;   // 总压缩节省（字节）
    avgCompressionRatio: number;       // 平均压缩比
    totalCleanupSavings: number;       // 总清理节省（字节）
    avgCleanupEfficiency: number;      // 平均清理效率
    cacheEfficiency: number;           // 缓存效率（0-1）
    serializationEfficiency: number;   // 序列化效率（0-1）
  };
  
  // 可靠性统计
  reliability: {
    totalErrors: number;               // 总错误数
    errorRate: number;                 // 错误率（0-1）
    dataLossCount: number;             // 数据丢失次数
    corruptionCount: number;           // 数据损坏次数
    recoveryCount: number;             // 恢复次数
    uptime: number;                    // 运行时间（ticks）
  };
  
  // 历史趋势
  history: {
    memoryUsage: number[];             // 内存使用历史
    fragmentation: number[];           // 碎片化历史
    growthRate: number[];              // 增长率历史
    errorRate: number[];               // 错误率历史
    performance: number[];             // 性能历史
  };
  
  // 时间戳
  timestamp: number;                   // 统计时间
  collectionStart: number;             // 收集开始时间
  collectionDuration: number;          // 收集耗时
}
```

## 🔧 算法设计

### 1. 内存压缩算法

#### 分层压缩策略
```javascript
class MemoryCompressor {
  constructor() {
    this.compressors = new Map();
    this.initializeCompressors();
  }
  
  compress(memory, config) {
    const result = {
      success: true,
      originalSize: this.calculateSize(memory),
      compressedSize: 0,
      savings: 0,
      savingsRatio: 0,
      duration: 0,
      details: [],
      warnings: []
    };
    
    const startTime = Game.time;
    
    // 1. 选择压缩策略
    const strategy = this.selectCompressionStrategy(memory, config);
    
    // 2. 分层压缩
    const layers = this.splitIntoLayers(memory, strategy);
    
    layers.forEach((layer, index) => {
      const layerResult = this.compressLayer(layer, strategy);
      
      if (layerResult.success) {
        result.compressedSize += layerResult.compressedSize;
        result.details.push(layerResult);
      } else {
        result.success = false;
        result.warnings.push({
          layer: index,
          error: layerResult.error,
          message: `第${index}层压缩失败`
        });
      }
    });
    
    // 3. 计算压缩结果
    result.savings = result.originalSize - result.compressedSize;
    result.savingsRatio = result.originalSize > 0 
      ? result.savings / result.originalSize 
      : 0;
    result.duration = Game.time - startTime;
    
    // 4. 验证压缩有效性
    if (result.savingsRatio < config.compression.minSavings) {
      result.warnings.push({
        type: 'LOW_SAVINGS',
        message: `压缩节省比例过低: ${(result.savingsRatio * 100).toFixed(2)}%`,
        suggestion: '考虑使用不同的压缩策略或调整阈值'
      });
    }
    
    return result;
  }
  
  selectCompressionStrategy(memory, config) {
    const size = this.calculateSize(memory);
    const complexity = this.estimateComplexity(memory);
    
    // 基于大小和复杂度选择策略
    if (size < 1000) {
      return {
        algorithm: 'simple',
        level: 1,
        timeout: 5,
        minSavings: 0.1
      };
    } else if (size < 10000) {
      return {
        algorithm: 'efficient',
        level: 2,
        timeout: 10,
        minSavings: 0.2
      };
    } else {
      return {
        algorithm: 'aggressive',
        level: 3,
        timeout: 20,
