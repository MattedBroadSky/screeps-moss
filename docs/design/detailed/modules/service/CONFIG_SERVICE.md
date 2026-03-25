# ConfigService 详细设计文档

## 📋 文档信息
- **模块名称**: ConfigService（配置服务）
- **所属层级**: 服务层
- **文档版本**: v1.0.0
- **创建日期**: 2026-03-25
- **最后更新**: 2026-03-25
- **负责人**: Moss (OpenClaw AI)
- **状态**: [草案]
- **优先级**: P0 (v1.0核心模块)
- **关联文档**: 
  - 所有业务模块设计文档

## 🎯 设计目标

### 核心职责
1. **配置管理** - 统一管理所有模块配置
2. **配置验证** - 验证配置的完整性和有效性
3. **配置持久化** - 保存和加载配置到内存
4. **配置版本控制** - 管理配置版本和迁移
5. **配置热更新** - 支持运行时配置更新
6. **默认配置提供** - 提供合理的默认配置

### 质量目标
- **性能**: 配置访问延迟 < 1 tick
- **可靠性**: 配置一致性 100%
- **可用性**: 服务可用性 99.99%
- **安全性**: 配置验证覆盖率 100%

## 🏗️ 类图设计

### 类结构
```
┌─────────────────────────────────────┐
│          ConfigService              │
├─────────────────────────────────────┤
│ - configs: Map<string, ModuleConfig>│
│ - defaults: Map<string, DefaultConfig>
│ - validators: Map<string, Validator>│
│ - cache: ConfigCache                │
│ - version: string                   │
│ - stats: ConfigStats                │
├─────────────────────────────────────┤
│ + getInstance(): ConfigService      │
│ + getConfig(module: string): ModuleConfig
│ + setConfig(module, config): boolean│
│ + validateConfig(config): ValidationResult
│ + getDefaultConfig(module): DefaultConfig
│ + saveConfigs(): boolean            │
│ + loadConfigs(): boolean            │
│ + migrateConfigs(): MigrationResult │
│ + watchConfig(module, callback): void
│ + unwatchConfig(module, callback): void
│ - loadDefaults(): void              │
│ - initializeValidators(): void      │
│ - updateCache(): void               │
│ - notifyWatchers(): void            │
│ - backupConfigs(): void             │
└─────────────────────────────────────┘
```

### 核心组件
```
ConfigService
    ├── ConfigManager      - 配置存储和管理
    ├── ValidatorManager   - 配置验证器管理
    ├── CacheManager       - 配置缓存管理
    ├── VersionManager     - 版本和迁移管理
    ├── WatcherManager     - 配置变更监听
    └── BackupManager      - 配置备份和恢复
```

## 📝 接口定义

### 公共接口

#### 1. 单例获取接口
```javascript
/**
 * 获取ConfigService单例实例
 * @returns {ConfigService} ConfigService实例
 */
static getInstance(): ConfigService
```

#### 2. 配置获取接口
```javascript
/**
 * 获取模块配置
 * @param {string} module - 模块名称
 * @param {boolean} [useCache=true] - 是否使用缓存
 * @returns {ModuleConfig} 模块配置
 */
getConfig(module: string, useCache?: boolean): ModuleConfig

/**
 * 获取默认配置
 * @param {string} module - 模块名称
 * @returns {DefaultConfig} 默认配置
 */
getDefaultConfig(module: string): DefaultConfig
```

#### 3. 配置设置接口
```javascript
/**
 * 设置模块配置
 * @param {string} module - 模块名称
 * @param {ModuleConfig} config - 新配置
 * @param {boolean} [validate=true] - 是否验证配置
 * @returns {boolean} 设置是否成功
 */
setConfig(module: string, config: ModuleConfig, validate?: boolean): boolean
```

#### 4. 配置验证接口
```javascript
/**
 * 验证配置
 * @param {ModuleConfig} config - 要验证的配置
 * @returns {ValidationResult} 验证结果
 */
validateConfig(config: ModuleConfig): ValidationResult
```

#### 5. 持久化接口
```javascript
/**
 * 保存所有配置到内存
 * @returns {boolean} 保存是否成功
 */
saveConfigs(): boolean

/**
 * 从内存加载所有配置
 * @returns {boolean} 加载是否成功
 */
loadConfigs(): boolean
```

#### 6. 版本管理接口
```javascript
/**
 * 迁移配置到新版本
 * @param {string} fromVersion - 源版本
 * @param {string} toVersion - 目标版本
 * @returns {MigrationResult} 迁移结果
 */
migrateConfigs(fromVersion: string, toVersion: string): MigrationResult
```

#### 7. 监听接口
```javascript
/**
 * 监听配置变更
 * @param {string} module - 模块名称
 * @param {ConfigChangeCallback} callback - 变更回调
 */
watchConfig(module: string, callback: ConfigChangeCallback): void

/**
 * 取消监听配置变更
 * @param {string} module - 模块名称
 * @param {ConfigChangeCallback} callback - 变更回调
 */
unwatchConfig(module: string, callback: ConfigChangeCallback): void
```

### 数据类型定义

#### ModuleConfig
```javascript
interface ModuleConfig {
  // 元数据
  metadata: {
    module: string;                    // 模块名称
    version: string;                   // 配置版本
    createdAt: number;                 // 创建时间
    updatedAt: number;                 // 更新时间
    createdBy: string;                 // 创建者
    updatedBy: string;                 // 更新者
    description?: string;              // 配置描述
  };
  
  // 配置数据
  data: any;                          // 模块特定配置数据
  
  // 验证信息
  validation?: {
    isValid: boolean;                  // 是否有效
    lastValidated: number;             // 最后验证时间
    errors?: ValidationError[];        // 验证错误
    warnings?: ValidationWarning[];    // 验证警告
  };
  
  // 访问控制
  access?: {
    read: string[];                    // 可读角色/用户
    write: string[];                   // 可写角色/用户
    admin: string[];                   // 管理员角色/用户
  };
}
```

#### ValidationResult
```javascript
interface ValidationResult {
  isValid: boolean;                    // 是否有效
  errors: ValidationError[];           // 错误列表
  warnings: ValidationWarning[];       // 警告列表
  suggestions: ValidationSuggestion[]; // 建议列表
  timestamp: number;                   // 验证时间
}

interface ValidationError {
  code: string;                        // 错误代码
  message: string;                     // 错误消息
  path: string;                        // 配置路径
  severity: 'error' | 'critical';      // 严重程度
  fix?: string;                        // 修复建议
}

interface ValidationWarning {
  code: string;                        // 警告代码
  message: string;                     // 警告消息
  path: string;                        // 配置路径
  severity: 'warning' | 'info';        // 严重程度
  suggestion?: string;                 // 改进建议
}
```

#### MigrationResult
```javascript
interface MigrationResult {
  success: boolean;                    // 是否成功
  migrated: number;                    // 迁移的配置数量
  failed: number;                      // 失败的配置数量
  errors: MigrationError[];            // 迁移错误
  warnings: MigrationWarning[];        // 迁移警告
  details: MigrationDetail[];          // 迁移详情
}

interface MigrationDetail {
  module: string;                      // 模块名称
  fromVersion: string;                 // 源版本
  toVersion: string;                   // 目标版本
  success: boolean;                    // 是否成功
  changes: ConfigChange[];             // 配置变更
  duration: number;                    // 迁移耗时
}
```

#### ConfigChangeCallback
```javascript
type ConfigChangeCallback = (change: ConfigChange) => void;

interface ConfigChange {
  module: string;                      // 模块名称
  type: 'create' | 'update' | 'delete' | 'validate'; // 变更类型
  oldConfig?: ModuleConfig;            // 旧配置（更新/删除时）
  newConfig?: ModuleConfig;            // 新配置（创建/更新时）
  timestamp: number;                   // 变更时间
  source: string;                      // 变更来源
}
```

## 🔧 算法设计

### 1. 配置验证算法

#### 分层验证策略
```javascript
class ConfigValidator {
  constructor() {
    this.validators = new Map();
    this.initializeValidators();
  }
  
  validate(config) {
    const results = {
      isValid: true,
      errors: [],
      warnings: [],
      suggestions: []
    };
    
    // 1. 结构验证（JSON Schema）
    const structureResult = this.validateStructure(config);
    if (!structureResult.isValid) {
      results.isValid = false;
      results.errors.push(...structureResult.errors);
      return results; // 结构错误，停止进一步验证
    }
    
    // 2. 类型验证
    const typeResult = this.validateTypes(config);
    if (!typeResult.isValid) {
      results.isValid = false;
      results.errors.push(...typeResult.errors);
    }
    results.warnings.push(...typeResult.warnings);
    
    // 3. 值范围验证
    const rangeResult = this.validateRanges(config);
    if (!rangeResult.isValid) {
      results.isValid = false;
      results.errors.push(...rangeResult.errors);
    }
    results.warnings.push(...rangeResult.warnings);
    
    // 4. 依赖关系验证
    const dependencyResult = this.validateDependencies(config);
    if (!dependencyResult.isValid) {
      results.isValid = false;
      results.errors.push(...dependencyResult.errors);
    }
    results.warnings.push(...dependencyResult.warnings);
    
    // 5. 业务逻辑验证
    const businessResult = this.validateBusinessLogic(config);
    if (!businessResult.isValid) {
      results.isValid = false;
      results.errors.push(...businessResult.errors);
    }
    results.warnings.push(...businessResult.warnings);
    results.suggestions.push(...businessResult.suggestions);
    
    // 6. 性能影响验证
    const performanceResult = this.validatePerformance(config);
    results.warnings.push(...performanceResult.warnings);
    results.suggestions.push(...performanceResult.suggestions);
    
    return results;
  }
  
  validateStructure(config) {
    // 使用JSON Schema验证配置结构
    const schema = this.getSchemaForModule(config.metadata.module);
    if (!schema) {
      return { isValid: true, errors: [], warnings: [] };
    }
    
    const result = this.jsonSchemaValidator.validate(config.data, schema);
    
    return {
      isValid: result.valid,
      errors: result.errors.map(error => ({
        code: 'STRUCTURE_ERROR',
        message: `结构错误: ${error.message}`,
        path: error.path,
        severity: 'error'
      })),
      warnings: []
    };
  }
  
  validateTypes(config) {
    const errors = [];
    const warnings = [];
    
    // 遍历配置数据，验证类型
    this.traverseConfig(config.data, (value, path) => {
      const expectedType = this.getExpectedType(config.metadata.module, path);
      if (expectedType) {
        const actualType = typeof value;
        
        if (actualType !== expectedType) {
          // 尝试类型转换
          const converted = this.tryConvertType(value, expectedType);
          if (converted.success) {
            warnings.push({
              code: 'TYPE_CONVERSION',
              message: `类型自动转换: ${path} (${actualType} -> ${expectedType})`,
              path,
              severity: 'warning',
              suggestion: `考虑显式设置正确的类型`
            });
          } else {
            errors.push({
              code: 'TYPE_MISMATCH',
              message: `类型不匹配: ${path} 期望 ${expectedType}, 实际 ${actualType}`,
              path,
              severity: 'error',
              fix: `将值设置为 ${expectedType} 类型`
            });
          }
        }
      }
    });
    
    return {
      isValid: errors.length === 0,
      errors,
      warnings
    };
  }
  
  validateRanges(config) {
    const errors = [];
    const warnings = [];
    
    this.traverseConfig(config.data, (value, path) => {
      const range = this.getValueRange(config.metadata.module, path);
      if (range) {
        if (typeof value === 'number') {
          if (value < range.min) {
            errors.push({
              code: 'VALUE_TOO_LOW',
              message: `值过低: ${path} = ${value}, 最小值为 ${range.min}`,
              path,
              severity: 'error',
              fix: `将值设置为至少 ${range.min}`
            });
          } else if (value > range.max) {
            errors.push({
              code: 'VALUE_TOO_HIGH',
              message: `值过高: ${path} = ${value}, 最大值为 ${range.max}`,
              path,
              severity: 'error',
              fix: `将值设置为最多 ${range.max}`
            });
          }
          
          // 检查是否在推荐范围内
          if (range.recommended && (value < range.recommended.min || value > range.recommended.max)) {
            warnings.push({
              code: 'OUTSIDE_RECOMMENDED_RANGE',
              message: `值在推荐范围外: ${path} = ${value}, 推荐范围 [${range.recommended.min}, ${range.recommended.max}]`,
              path,
              severity: 'warning',
              suggestion: `考虑将值调整到推荐范围内`
            });
          }
        }
      }
    });
    
    return {
      isValid: errors.length === 0,
      errors,
      warnings
    };
  }
}
```

### 2. 配置缓存算法

#### 智能缓存管理
```javascript
class ConfigCache {
  constructor() {
    this.cache = new Map();
    this.accessStats = new Map();
    this.invalidationQueue = [];
    this.maxSize = 100;
    this.ttl = 1000; // 缓存有效期（ticks）
  }
  
  get(module, useCache = true) {
    if (!useCache) {
      return null;
    }
    
    const cacheKey = this.getCacheKey(module);
    const entry = this.cache.get(cacheKey);
    
    if (entry) {
      // 检查缓存是否过期
      if (Game.time - entry.timestamp < this.ttl) {
        // 更新访问统计
        this.recordAccess(module);
        
        // 更新LRU位置
        this.updateLRU(cacheKey);
        
        return entry.config;
      } else {
        // 缓存过期，移除
        this.cache.delete(cacheKey);
        this.accessStats.delete(cacheKey);
      }
    }
    
    return null;
  }
  
  set(module, config) {
    const cacheKey = this.getCacheKey(module);
    
    // 如果缓存已满，移除最不常用的项
    if (this.cache.size >= this.maxSize) {
      this.evictLeastUsed();
    }
    
    const entry = {
      config,
      timestamp: Game.time,
      size: JSON.stringify(config).length
    };
    
    this.cache.set(cacheKey, entry);
    this.recordAccess(module);
    
    // 添加到LRU队列开头
    this.invalidationQueue.unshift(cacheKey);
    
    // 限制队列大小
    if (this.invalidationQueue.length > this.maxSize * 2) {
      this.invalidationQueue = this.invalidationQueue.slice(0, this.maxSize);
    }
    
    return true;
  }
  
  invalidate(module) {
    const cacheKey = this.getCacheKey(module);
    
    // 从缓存移除
    this.cache.delete(cacheKey);
    this.accessStats.delete(cacheKey);
    
    // 从LRU队列移除
    const index = this.invalidationQueue.indexOf(cacheKey);
    if (index !== -1) {
      this.invalidationQueue.splice(index, 1);
    }
    
    return true;
  }
  
  invalidateAll() {
    this.cache.clear();
    this.accessStats.clear();
    this.invalidationQueue = [];
    return true;
  }
  
  evictLeastUsed() {
    if (this.invalidationQueue.length === 0) return;
    
    // 从LRU队列末尾移除（最久未使用）
    const cacheKey = this.invalidationQueue.pop();
    if (cacheKey) {
      this.cache.delete(cacheKey);
      this.accessStats.delete(cacheKey);
    }
  }
  
  recordAccess(module) {
    const cacheKey = this.getCacheKey(module);
    const stats = this.accessStats.get(cacheKey) || {
      accessCount: 0,
      lastAccess: 0,
      averageInterval: 0
    };
    
    const now = Game.time;
    const interval = now - stats.lastAccess;
    
    // 更新统计
    stats.accessCount++;
    stats.lastAccess = now;
    
    // 更新平均访问间隔
    if (stats.accessCount > 1) {
      stats.averageInterval = 
        (stats.averageInterval * (stats.accessCount - 1) + interval) / stats.accessCount;
    }
    
    this.accessStats.set(cacheKey, stats);
  }
  
  updateLRU(cacheKey) {
    // 将访问的项移到队列开头
    const index = this.invalidationQueue.indexOf(cacheKey);
    if (index !== -1) {
      this.invalidationQueue.splice(index, 1);
    }
    this.invalidationQueue.unshift(cacheKey);
  }
  
  getCacheKey(module) {
    return `config:${module}`