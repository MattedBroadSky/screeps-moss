# LogService 详细设计文档

## 📋 文档信息
- **模块名称**: LogService（日志服务）
- **所属层级**: 服务层
- **文档版本**: v1.0.0
- **创建日期**: 2026-03-25
- **最后更新**: 2026-03-25
- **负责人**: Moss (OpenClaw AI)
- **状态**: [草案]
- **优先级**: P0 (v1.0核心模块)
- **关联文档**: 
  - `MEMORY_SERVICE.md` - 内存服务设计
  - `CONFIG_SERVICE.md` - 配置服务设计

## 🎯 设计目标

### 核心职责
1. **日志记录** - 统一记录系统日志
2. **日志分级** - 支持多级日志（DEBUG, INFO, WARN, ERROR, FATAL）
3. **日志格式化** - 统一的日志格式和输出
4. **日志存储** - 高效存储和检索日志
5. **日志轮转** - 自动日志轮转和清理
6. **日志分析** - 日志分析和统计
7. **日志告警** - 基于日志的实时告警

### 质量目标
- **性能**: 日志记录延迟 < 1 tick
- **可靠性**: 日志完整性 100%
- **可用性**: 服务可用性 99.99%
- **存储效率**: 日志压缩率 > 50%
- **查询性能**: 日志查询响应 < 5 ticks

## 🏗️ 类图设计

### 类结构
```
┌─────────────────────────────────────┐
│          LogService                 │
├─────────────────────────────────────┤
│ - loggers: Map<string, Logger>      │
│ - appenders: Map<string, Appender>  │
│ - filters: Map<string, Filter>      │
│ - formatters: Map<string, Formatter>│
│ - config: LogConfig                 │
│ - stats: LogStats                   │
│ - cache: LogCache                   │
├─────────────────────────────────────┤
│ + getInstance(): LogService         │
│ + debug(message: string, ...data): void
│ + info(message: string, ...data): void
│ + warn(message: string, ...data): void
│ + error(message: string, ...data): void
│ + fatal(message: string, ...data): void
│ + log(level, message, ...data): void│
│ + query(filter: LogFilter): LogEntry[]
│ + analyze(analysis: AnalysisConfig): AnalysisResult
│ + rotate(): RotationResult          │
│ + cleanup(): CleanupResult          │
│ + getStats(): LogStats              │
│ + monitor(): MonitoringReport       │
│ - initializeLoggers(): void         │
│ - processLogEntry(): void           │
│ - scheduleRotation(): void          │
│ - notifyListeners(): void           │
│ - updateCache(): void               │
└─────────────────────────────────────┘
```

### 核心组件
```
LogService
    ├── LoggerManager     - 日志记录器管理
    ├── AppenderManager   - 日志输出器管理
    ├── FilterManager     - 日志过滤器管理
    ├── FormatterManager  - 日志格式化器管理
    ├── StorageManager    - 日志存储管理
    ├── RotationManager   - 日志轮转管理
    ├── AnalysisManager   - 日志分析管理
    └── AlertManager      - 日志告警管理
```

## 📝 接口定义

### 公共接口

#### 1. 单例获取接口
```javascript
/**
 * 获取LogService单例实例
 * @returns {LogService} LogService实例
 */
static getInstance(): LogService
```

#### 2. 日志记录接口
```javascript
/**
 * 记录DEBUG级别日志
 * @param {string} message - 日志消息
 * @param {...any} data - 附加数据
 */
debug(message: string, ...data: any[]): void

/**
 * 记录INFO级别日志
 * @param {string} message - 日志消息
 * @param {...any} data - 附加数据
 */
info(message: string, ...data: any[]): void

/**
 * 记录WARN级别日志
 * @param {string} message - 日志消息
 * @param {...any} data - 附加数据
 */
warn(message: string, ...data: any[]): void

/**
 * 记录ERROR级别日志
 * @param {string} message - 日志消息
 * @param {...any} data - 附加数据
 */
error(message: string, ...data: any[]): void

/**
 * 记录FATAL级别日志
 * @param {string} message - 日志消息
 * @param {...any} data - 附加数据
 */
fatal(message: string, ...data: any[]): void

/**
 * 通用日志记录
 * @param {LogLevel} level - 日志级别
 * @param {string} message - 日志消息
 * @param {...any} data - 附加数据
 */
log(level: LogLevel, message: string, ...data: any[]): void
```

#### 3. 日志查询接口
```javascript
/**
 * 查询日志
 * @param {LogFilter} filter - 查询过滤器
 * @returns {LogEntry[]} 日志条目数组
 */
query(filter: LogFilter): LogEntry[]

/**
 * 统计日志数量
 * @param {LogFilter} filter - 查询过滤器
 * @returns {number} 日志数量
 */
count(filter: LogFilter): number

/**
 * 获取最近日志
 * @param {number} limit - 限制数量
 * @param {LogLevel} [level] - 可选日志级别
 * @returns {LogEntry[]} 最近日志条目
 */
getRecent(limit: number, level?: LogLevel): LogEntry[]
```

#### 4. 日志管理接口
```javascript
/**
 * 轮转日志
 * @returns {RotationResult} 轮转结果
 */
rotate(): RotationResult

/**
 * 清理日志
 * @returns {CleanupResult} 清理结果
 */
cleanup(): CleanupResult

/**
 * 导出日志
 * @param {ExportConfig} config - 导出配置
 * @returns {ExportResult} 导出结果
 */
export(config: ExportConfig): ExportResult
```

#### 5. 分析监控接口
```javascript
/**
 * 分析日志
 * @param {AnalysisConfig} config - 分析配置
 * @returns {AnalysisResult} 分析结果
 */
analyze(config: AnalysisConfig): AnalysisResult

/**
 * 监控日志状态
 * @returns {MonitoringReport} 监控报告
 */
monitor(): MonitoringReport

/**
 * 获取日志统计
 * @returns {LogStats} 日志统计
 */
getStats(): LogStats
```

### 数据类型定义

#### LogConfig
```javascript
interface LogConfig {
  // 日志级别配置
  levels: {
    default: LogLevel;                 // 默认日志级别
    overrides: {                       // 覆盖配置
      [category: string]: LogLevel;    // 分类 -> 级别
    };
    threshold: LogLevel;               // 阈值级别（低于此级别不记录）
  };
  
  // 输出配置
  appenders: {
    [name: string]: AppenderConfig;    // 输出器配置
  };
  
  // 格式化配置
  formatting: {
    pattern: string;                   // 日志格式模式
    timestampFormat: string;           // 时间戳格式
    includeStack: boolean;             // 是否包含堆栈信息
    maxDataDepth: number;              // 最大数据深度
    truncateLength: number;            // 截断长度
  };
  
  // 存储配置
  storage: {
    enabled: boolean;                  // 是否启用存储
    maxEntries: number;                // 最大条目数
    maxSize: number;                   // 最大大小（字节）
    compression: {                     // 压缩配置
      enabled: boolean;
      algorithm: 'gzip' | 'deflate' | 'lz4';
      level: 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9;
    };
    retention: {                       // 保留策略
      [level: string]: number;         // 级别 -> 保留时间（ticks）
    };
  };
  
  // 轮转配置
  rotation: {
    enabled: boolean;                  // 是否启用轮转
    strategy: 'size' | 'time' | 'both'; // 轮转策略
    sizeThreshold: number;             // 大小阈值（字节）
    timeInterval: number;              // 时间间隔（ticks）
    maxFiles: number;                  // 最大文件数
    compression: boolean;              // 轮转时是否压缩
  };
  
  // 监控配置
  monitoring: {
    enabled: boolean;                  // 是否启用监控
    samplingInterval: number;          // 采样间隔（ticks）
    alertThresholds: {                 // 告警阈值
      errorRate: number;               // 错误率阈值（0-1）
      warningRate: number;             // 警告率阈值（0-1）
      storageUsage: number;            // 存储使用率阈值（0-1）
      growthRate: number;              // 增长率阈值
    };
    metrics: string[];                 // 监控指标
  };
  
  // 性能配置
  performance: {
    batchSize: number;                 // 批量大小
    flushInterval: number;             // 刷新间隔（ticks）
    cacheSize: number;                 // 缓存大小
    asyncWrite: boolean;               // 是否异步写入
    bufferSize: number;                // 缓冲区大小
  };
}
```

#### LogEntry
```javascript
interface LogEntry {
  // 基本信息
  id: string;                          // 日志ID
  timestamp: number;                   // 时间戳
  level: LogLevel;                     // 日志级别
  message: string;                     // 日志消息
  
  // 上下文信息
  category: string;                    // 日志分类
  module: string;                      // 模块名称
  function: string;                    // 函数名称
  line?: number;                       // 行号（如果可用）
  
  // 附加数据
  data: any;                           // 附加数据
  tags: string[];                      // 标签
  correlationId?: string;              // 关联ID
  
  // 环境信息
  tick: number;                        // 游戏tick
  room?: string;                       // 房间名称
  cpuUsed?: number;                    // CPU使用量
  memoryUsage?: number;                // 内存使用量
  
  // 错误信息（如果是错误日志）
  error?: {
    name: string;                      // 错误名称
    message: string;                   // 错误消息
    stack?: string;                    // 堆栈信息
    code?: string;                     // 错误代码
  };
  
  // 元数据
  source: string;                      // 日志来源
  host?: string;                       // 主机名
  pid?: number;                        // 进程ID
  thread?: string;                     // 线程名
}
```

#### LogFilter
```javascript
interface LogFilter {
  // 时间过滤
  startTime?: number;                  // 开始时间
  endTime?: number;                    // 结束时间
  timeRange?: {                        // 时间范围
    start: number;
    end: number;
  };
  
  // 级别过滤
  levels?: LogLevel[];                 // 包含的级别
  minLevel?: LogLevel;                 // 最小级别
  maxLevel?: LogLevel;                 // 最大级别
  
  // 内容过滤
  message?: string | RegExp;           // 消息匹配
  category?: string | string[];        // 分类匹配
  module?: string | string[];          // 模块匹配
  function?: string | string[];        // 函数匹配
  
  // 数据过滤
  tags?: string[];                     // 标签匹配
  correlationId?: string;              // 关联ID匹配
  room?: string | string[];            // 房间匹配
  
  // 分页和排序
  limit?: number;                      // 限制数量
  offset?: number;                     // 偏移量
  sortBy?: 'timestamp' | 'level' | 'category' | 'module'; // 排序字段
  sortOrder?: 'asc' | 'desc';          // 排序顺序
  
  // 高级过滤
  customFilter?: (entry: LogEntry) => boolean; // 自定义过滤器
}
```

#### RotationResult
```javascript
interface RotationResult {
  success: boolean;                    // 是否成功
  rotated: RotatedFile[];              // 轮转的文件
  currentSize: number;                 // 当前大小（字节）
  rotatedSize: number;                 // 轮转大小（字节）
  duration: number;                    // 轮转耗时（ticks）
  errors: RotationError[];             // 轮转错误
  warnings: RotationWarning[];         // 轮转警告
  
  // 统计信息
  stats: {
    totalEntries: number;              // 总条目数
    entriesRotated: number;            // 轮转条目数
    compressionRatio: number;          // 压缩比
    spaceSaved: number;                // 节省空间（字节）
    filesCreated: number;              // 创建的文件数
    filesDeleted: number;              // 删除的文件数
  };
}

interface RotatedFile {
  name: string;                        // 文件名
  size: number;                        // 文件大小（字节）
  entries: number;                     // 条目数量
  startTime: number;                   // 开始时间
  endTime: number;                     // 结束时间
  compressionRatio?: number;           // 压缩比（如果压缩）
  path?: string;                       // 文件路径
}
```

#### AnalysisResult
```javascript
interface AnalysisResult {
  success: boolean;                    // 是否成功
  analysis: AnalysisData;              // 分析数据
  insights: Insight[];                 // 洞察信息
  recommendations: Recommendation[];   // 建议信息
  duration: number;                    // 分析耗时（ticks）
  
  // 时间范围
  timeRange: {
    start: number;
    end: number;
    duration: number;
  };
  
  // 数据统计
  stats: {
    totalEntries: number;              // 总条目数
    analyzedEntries: number;           // 分析条目数
    byLevel: { [level: string]: number }; // 按级别统计
    byCategory: { [category: string]: number }; // 按分类统计
    byModule: { [module: string]: number }; // 按模块统计
    byHour: { [hour: string]: number }; // 按小时统计
  };
}

interface AnalysisData {
  // 趋势分析
  trends: {
    volume: TrendPoint[];              // 日志量趋势
    errorRate: TrendPoint[];           // 错误率趋势
    warningRate: TrendPoint[];         // 警告率趋势
    performance: TrendPoint[];         // 性能趋势
  };
  
  // 分布分析
  distributions: {
    level: Distribution;               // 级别分布
    category: Distribution;            // 分类分布
    module: Distribution;              // 模块分布
    time: Distribution;                // 时间分布
  };
  
  // 关联分析
  correlations: {
    levelCategory: Correlation;        // 级别-分类关联
    categoryModule: Correlation;       // 分类-模块关联
    timeLevel: Correlation;            // 时间-级别关联
  };
  
  // 异常检测
  anomalies: Anomaly[];                // 异常检测结果
  
  // 模式识别
  patterns: Pattern[];                 // 模式识别结果
}

interface Insight {
  type: 'trend' | 'pattern' | 'anomaly' | 'correlation'; // 洞察类型
  title: string;                       // 标题
  description: string;                 // 描述
  confidence: number;                  // 置信度（0-1）
  impact: 'low' | 'medium' | 'high' | 'critical'; // 影响程度
  evidence: Evidence[];                // 证据
  recommendations: string[];           // 建议
}
```

## 🔧 算法设计

### 1. 日志格式化算法

#### 智能格式化策略
```javascript
class LogFormatter {
  constructor(config) {
    this.config = config;
    this.patternParser = new PatternParser();
    this.dataFormatter = new DataFormatter();
  }
  
  format(entry) {
    // 1. 解析格式模式
    const pattern = this.config.formatting.pattern;
    const tokens = this.patternParser.parse(pattern);
    
    // 2. 构建格式化结果
    let result = '';
    
    tokens.forEach(token => {
      if (token.type === 'literal') {
        result += token.value;
      } else if (token.type === 'placeholder') {
        result += this.formatPlaceholder(token, entry);
      }
    });
    
    // 3. 添加附加数据
    if (entry.data !== undefined) {
      result += this.formatData(entry.data);
    }
    
    // 4. 添加堆栈信息（如果是错误）
    if (entry.error && entry.error.stack && this.config.formatting.includeStack) {
      result += '\n' + this.formatStack(entry.error.stack);
    }
    
    // 5. 应用截断
    if (this.config.formatting.truncateLength > 0) {
      result = this.truncate(result, this.config.formatting.truncateLength);
    }
    
    return result;
  }
  
  formatPlaceholder(token, entry) {
    switch (token.name) {
      case 'timestamp':
        return this.formatTimestamp(entry.timestamp, token.format);
      case 'level':
        return this.formatLevel(entry.level, token.format);
      case 'message':
        return this.format