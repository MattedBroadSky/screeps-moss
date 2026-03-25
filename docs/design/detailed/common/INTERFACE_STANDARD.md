# 接口设计规范

## 📋 文档信息
- **文档名称**: 接口设计规范
- **文档版本**: v1.0.0
- **创建日期**: 2026-03-25
- **最后更新**: 2026-03-25
- **负责人**: Moss (OpenClaw AI)
- **状态**: [草案]
- **适用范围**: 所有模块接口设计

## 🎯 设计目标

### 核心原则
1. **一致性** - 所有模块接口风格一致
2. **清晰性** - 接口意图明确，易于理解
3. **简洁性** - 接口设计简洁，避免过度复杂
4. **稳定性** - 接口稳定，避免频繁变更
5. **可扩展性** - 接口设计考虑未来扩展

### 质量目标
- **可读性**: 接口名称和参数清晰易懂
- **可维护性**: 接口变更影响最小化
- **可测试性**: 接口易于测试和验证
- **兼容性**: 向后兼容性保证

## 📝 接口命名规范

### 1. 方法命名规范

#### 动词前缀约定
```javascript
// 获取数据类方法
getXxx()      // 获取单个数据
getAllXxx()   // 获取所有数据
findXxx()     // 查找数据
queryXxx()    // 查询数据

// 设置数据类方法
setXxx()      // 设置数据
updateXxx()   // 更新数据
createXxx()   // 创建数据
deleteXxx()   // 删除数据
removeXxx()   // 移除数据

// 操作类方法
doXxx()       // 执行操作
performXxx()  // 执行操作
executeXxx()  // 执行操作
runXxx()      // 运行操作

// 检查类方法
isXxx()       // 返回布尔值
hasXxx()      // 检查是否存在
canXxx()      // 检查是否可以
shouldXxx()   // 检查是否应该

// 转换类方法
toXxx()       // 转换为
fromXxx()     // 从...转换
parseXxx()    // 解析为
```

#### 命名示例
```javascript
// 正确示例
getConfig(module: string): ModuleConfig
setConfig(module: string, config: ModuleConfig): boolean
hasConfig(module: string): boolean
updateConfig(module: string, updates: Partial<ModuleConfig>): boolean
deleteConfig(module: string): boolean

// 错误示例
config(module)          // 不明确是获取还是设置
set(module, config)     // 缺少具体名称
checkConfig(module)     // 应该用hasConfig
removeConfig(module)    // 应该用deleteConfig
```

### 2. 参数命名规范

#### 参数类型约定
```javascript
// 标识符参数
id: string              // 唯一标识符
name: string            // 名称
key: string             // 键
path: string            // 路径

// 配置参数
config: ConfigType      // 配置对象
options: OptionsType    // 选项对象
settings: SettingsType  // 设置对象

// 数据参数
data: DataType          // 数据对象
value: ValueType        // 值
item: ItemType          // 项目

// 回调参数
callback: Function      // 回调函数
handler: Function       // 处理函数
listener: Function      // 监听函数

// 标志参数
enabled: boolean        // 是否启用
force: boolean          // 是否强制
async: boolean          // 是否异步
```

#### 参数顺序约定
```javascript
// 标准参数顺序
1. 必需参数（标识符、关键数据）
2. 可选参数（配置、选项）
3. 回调参数（回调函数）
4. 标志参数（布尔标志）

// 示例
getData(id: string, options?: GetOptions, callback?: DataCallback): DataType
setData(id: string, data: DataType, force?: boolean): boolean
```

### 3. 返回值规范

#### 返回值类型约定
```javascript
// 成功/失败操作
interface OperationResult {
  success: boolean;      // 是否成功
  message?: string;      // 消息（可选）
  error?: string;        // 错误信息（失败时）
}

// 数据获取操作
interface DataResult<T> {
  success: boolean;      // 是否成功
  data?: T;              // 数据（成功时）
  error?: string;        // 错误信息（失败时）
}

// 批量操作
interface BatchResult {
  success: boolean;      // 是否成功
  processed: number;     // 处理数量
  succeeded: number;     // 成功数量
  failed: number;        // 失败数量
  errors?: string[];     // 错误列表
}

// 异步操作
interface AsyncResult<T> {
  promise: Promise<T>;   // Promise对象
  cancel: () => void;    // 取消函数
}
```

#### 返回值示例
```javascript
// 简单操作
function enableFeature(id: string): OperationResult {
  // 实现...
  return {
    success: true,
    message: '功能已启用'
  };
}

// 数据操作
function getUserData(userId: string): DataResult<UserData> {
  try {
    const data = fetchUserData(userId);
    return {
      success: true,
      data: data
    };
  } catch (error) {
    return {
      success: false,
      error: error.message
    };
  }
}

// 批量操作
function processItems(items: Item[]): BatchResult {
  const result = {
    success: true,
    processed: items.length,
    succeeded: 0,
    failed: 0,
    errors: []
  };
  
  items.forEach(item => {
    try {
      processItem(item);
      result.succeeded++;
    } catch (error) {
      result.failed++;
      result.errors.push(error.message);
      result.success = false;
    }
  });
  
  return result;
}
```

## 🏗️ 接口设计模式

### 1. 单例模式接口

#### 设计模板
```javascript
class SingletonService {
  private static instance: SingletonService;
  private constructor() {}
  
  /**
   * 获取单例实例
   */
  static getInstance(): SingletonService {
    if (!SingletonService.instance) {
      SingletonService.instance = new SingletonService();
    }
    return SingletonService.instance;
  }
  
  /**
   * 初始化服务
   */
  init(config: ServiceConfig): OperationResult {
    // 实现...
  }
  
  /**
   * 获取服务状态
   */
  getStatus(): ServiceStatus {
    // 实现...
  }
}
```

### 2. 工厂模式接口

#### 设计模板
```javascript
interface Factory<T> {
  /**
   * 创建实例
   */
  create(config: CreationConfig): T;
  
  /**
   * 销毁实例
   */
  destroy(instance: T): OperationResult;
  
  /**
   * 获取所有实例
   */
  getAll(): T[];
}

class ObjectFactory implements Factory<GameObject> {
  private instances: Map<string, GameObject> = new Map();
  
  create(config: ObjectConfig): GameObject {
    const instance = this.createInstance(config);
    this.instances.set(instance.id, instance);
    return instance;
  }
  
  destroy(instance: GameObject): OperationResult {
    if (this.instances.has(instance.id)) {
      this.instances.delete(instance.id);
      return { success: true };
    }
    return { success: false, error: '实例不存在' };
  }
  
  getAll(): GameObject[] {
    return Array.from(this.instances.values());
  }
}
```

### 3. 观察者模式接口

#### 设计模板
```javascript
interface Observable<T> {
  /**
   * 添加观察者
   */
  subscribe(observer: Observer<T>): Subscription;
  
  /**
   * 移除观察者
   */
  unsubscribe(subscription: Subscription): void;
  
  /**
   * 通知所有观察者
   */
  notify(data: T): void;
}

interface Observer<T> {
  /**
   * 接收通知
   */
  update(data: T): void;
}

interface Subscription {
  id: string;
  unsubscribe: () => void;
}
```

### 4. 策略模式接口

#### 设计模板
```javascript
interface Strategy {
  /**
   * 执行策略
   */
  execute(context: StrategyContext): StrategyResult;
  
  /**
   * 获取策略名称
   */
  getName(): string;
  
  /**
   * 检查是否适用
   */
  isApplicable(context: StrategyContext): boolean;
}

class StrategyManager {
  private strategies: Map<string, Strategy> = new Map();
  
  /**
   * 注册策略
   */
  registerStrategy(strategy: Strategy): void {
    this.strategies.set(strategy.getName(), strategy);
  }
  
  /**
   * 选择并执行策略
   */
  executeBestStrategy(context: StrategyContext): StrategyResult {
    const applicable = this.getApplicableStrategies(context);
    if (applicable.length === 0) {
      return { success: false, error: '没有适用的策略' };
    }
    
    // 选择最佳策略（例如基于优先级或评分）
    const bestStrategy = this.selectBestStrategy(applicable, context);
    return bestStrategy.execute(context);
  }
}
```

## 📊 接口文档规范

### 1. JSDoc注释规范

#### 基本注释模板
```javascript
/**
 * 功能描述
 * 
 * @param {参数类型} 参数名 - 参数描述
 * @param {参数类型} [可选参数名] - 可选参数描述
 * @returns {返回值类型} 返回值描述
 * @throws {错误类型} 错误情况描述
 * @example
 * // 使用示例
 * const result = functionName(param1, param2);
 */
function functionName(param1: Type1, param2?: Type2): ReturnType {
  // 实现...
}
```

#### 完整注释示例
```javascript
/**
 * 获取指定模块的配置
 * 
 * 从配置服务中获取指定模块的配置数据。如果模块不存在，
 * 则返回默认配置或抛出错误。
 * 
 * @param {string} module - 模块名称（例如："room-manager"）
 * @param {boolean} [useCache=true] - 是否使用缓存（默认true）
 * @returns {ModuleConfig} 模块配置对象
 * @throws {ConfigError} 当模块不存在且没有默认配置时
 * @example
 * // 获取RoomManager配置
 * const config = getConfig("room-manager");
 * console.log(config.version);
 * 
 * @example
 * // 不使用缓存获取配置
 * const config = getConfig("energy-manager", false);
 */
function getConfig(module: string, useCache: boolean = true): ModuleConfig {
  // 实现...
}
```

### 2. 接口定义文件规范

#### TypeScript接口定义
```typescript
// 接口定义
interface ServiceInterface {
  // 初始化方法
  init(config: ServiceConfig): OperationResult;
  
  // 状态方法
  getStatus(): ServiceStatus;
  isReady(): boolean;
  
  // 数据方法
  getData(id: string): DataResult<DataType>;
  setData(id: string, data: DataType): OperationResult;
  deleteData(id: string): OperationResult;
  
  // 批量操作
  batchProcess(items: Item[]): BatchResult;
  
  // 事件方法
  on(event: string, handler: EventHandler): Subscription;
  off(subscription: Subscription): void;
  
  // 清理方法
  cleanup(): CleanupResult;
  reset(): OperationResult;
}

// 配置类型定义
interface ServiceConfig {
  // 基本配置
  name: string;
  version: string;
  enabled: boolean;
  
  // 性能配置
  maxConcurrent: number;
  timeout: number;
  retryCount: number;
  
  // 监控配置
  monitoring: {
    enabled: boolean;
    samplingInterval: number;
    alertThresholds: AlertThresholds;
  };
}

// 返回值类型定义
interface OperationResult {
  success: boolean;
  message?: string;
  error?: string;
  timestamp: number;
}

interface DataResult<T> {
  success: boolean;
  data?: T;
  error?: string;
  cached?: boolean;
  timestamp: number;
}
```

## 🔧 错误处理规范

### 1. 错误类型定义

#### 标准错误类型
```typescript
// 基础错误接口
interface BaseError {
  code: string;          // 错误代码
  message: string;       // 错误消息
  timestamp: number;     // 错误时间
  stack?: string;        // 堆栈信息
}

// 具体错误类型
interface ValidationError extends BaseError {
  type: 'validation';
  field: string;         // 验证字段
  value: any;            // 字段值
  constraint: string;    // 约束条件
}

interface ResourceError extends BaseError {
  type: 'resource';
  resource: string;      // 资源名称
  operation: string;     // 操作类型
  reason: string;        // 失败原因
}

interface PermissionError extends BaseError {
  type: 'permission';
  action: string;        // 操作
  resource: string;      // 资源
  user?: string;         // 用户
  required: string[];    // 所需权限
}

interface SystemError extends BaseError {
  type: 'system';
  component: string;     // 组件
  severity: 'low' | 'medium' | 'high' | 'critical';
  recoverable: boolean;  // 是否可恢复
}
```

### 2. 错误处理模式

#### Try-Catch模式
```javascript
function safeOperation() {
  try {
    // 可能失败的操作
    const result = riskyOperation();
    return { success: true, data: result };
  } catch (error) {
    // 错误处理
    const formattedError = formatError(error);
    logError(formattedError);
    
    // 返回错误结果
    return {
      success: false,
      error: formattedError.message,
      code: formattedError.code
    };
  }
}
```

#### 错误传播模式
```javascript
function processWithErrorPropagation() {
  const errors = [];
  
  // 步骤1
  const step1Result = step1();
  if (!step1Result.success) {
    errors.push(step1Result.error);
    // 决定是否继续
    if (step1Result.fatal) {
      return { success: false, errors };
    }
  }
  
  // 步骤2
  const step2Result = step2();
  if (!step2Result.success) {
    errors.push(step2Result.error);
  }
  
  // 返回最终结果
  return {
    success: errors.length === 0,
    errors: errors.length > 0 ? errors : undefined
  };
}
```

## 🧪 接口测试规范

### 1. 测试用例模板

#### 单元测试模板
```javascript
describe('ServiceInterface', () => {
  let service: ServiceInterface;
  
  beforeEach(() => {
    service = new ServiceImplementation();
  });
  
  afterEach(() => {
    service.cleanup();
  });
  
  describe('init()', () => {
    it('应该使用有效配置成功初始化', () => {
      const config = createValidConfig();
      const result = service.init(config);
      
      expect(result.success).toBe(true);
      expect(service.isReady()).toBe(true);
    });
    
    it('应该拒绝无效配置', () => {
      const config = createInvalidConfig();
      const result = service.init(config);
      
      expect(result.success).toBe(false);
      expect(result.error).toBeDefined();
    });
  });
  
  describe('getData()', () => {
    it('应该返回存在的数据', () => {
      const testData = { id: 'test', value: 'data' };
      service.setData('test', testData);
      
      const result = service.getData('test');
      
      expect(result.success).toBe(true);
      expect(result.data).toEqual(testData);
    });
    
    it('应该处理不存在的数据', () => {
      const result = service.getData('nonexistent');
      
      expect(result.success).toBe(false);
      expect(result.error).toContain('不存在');
    });
  });
});
```

### 2. 接口兼容性测试

#### 向后兼容性测试
```javascript
describe('向后兼容性', () => {
  it('应该保持旧接口的兼容性', () => {
    // 测试旧版本接口
    const oldResult = oldInterface.doSomething('param');
    
    // 测试新版本接口
    const newResult = newInterface.doSomething('param');
    
    // 验证结果兼容性
    expect(newResult).toHaveProperty('success');
    expect(newResult).toHaveProperty('data');
    
    // 如果可能，验证数据等价性
    if (oldResult.data && newResult.data) {
      expect(convertToNewFormat(oldResult.data)).toEqual(newResult.data);
    }
  });
  
  it('应该正确处理新增参数', () => {
    // 不带新参数调用
    const result1 = newInterface.doSomething('param');
    expect(result1.success).toBe(true);
    
    // 带新参数调用
    const result2 = newInterface.doSomething('param', { newOption: true });
    expect(result2.success).toBe(true);
  });
});
```

## 📈 接口版本管理

### 1. 版本策略

#### 语义化版本控制
```javascript
// 版本格式：主版本.次版本.修订版本
const API_VERSION = '1.0.0';

// 版本变更规则：
// 主版本：不兼容的API变更
// 次版本：向后兼容的功能性新增
// 修订版本：向后兼容的问题修正
```

### 2. 版本迁移策略

#### 渐进式迁移
```javascript
class VersionedService {
  private currentVersion = '1.0.0';
  private