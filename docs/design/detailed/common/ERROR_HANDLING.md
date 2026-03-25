# 错误处理规范

## 📋 文档信息
- **文档名称**: 错误处理规范
- **文档版本**: v1.0.0
- **创建日期**: 2026-03-25
- **最后更新**: 2026-03-25
- **负责人**: Moss (OpenClaw AI)
- **状态**: [草案]
- **适用范围**: 所有模块错误处理设计

## 🎯 设计目标

### 核心原则
1. **可靠性** - 系统在错误发生时仍能继续运行
2. **可恢复性** - 错误发生后系统能自动或手动恢复
3. **可诊断性** - 错误信息足够详细以便诊断问题
4. **用户体验** - 错误处理对用户透明或提供友好提示
5. **安全性** - 错误处理不会引入安全漏洞

### 质量目标
- **错误检测率**: > 95%的错误能被检测到
- **错误恢复率**: > 90%的错误能自动恢复
- **错误诊断时间**: < 5分钟定位问题原因
- **系统可用性**: > 99.9%的正常运行时间

## 🏗️ 错误分类体系

### 1. 错误严重程度分类

#### 严重程度级别
```javascript
const ERROR_SEVERITY = {
  DEBUG: {
    level: 0,
    description: '调试信息，不影响系统运行',
    action: '记录日志，无需处理',
    color: 'gray'
  },
  
  INFO: {
    level: 1,
    description: '普通信息，系统正常运行',
    action: '记录日志，监控趋势',
    color: 'blue'
  },
  
  WARNING: {
    level: 2,
    description: '警告信息，需要注意但系统可继续运行',
    action: '记录日志，监控并分析原因',
    color: 'yellow'
  },
  
  ERROR: {
    level: 3,
    description: '错误信息，功能受影响但系统可继续运行',
    action: '记录错误，尝试自动恢复，需要人工关注',
    color: 'orange'
  },
  
  CRITICAL: {
    level: 4,
    description: '严重错误，关键功能不可用',
    action: '立即告警，尝试紧急恢复，需要人工干预',
    color: 'red'
  },
  
  FATAL: {
    level: 5,
    description: '致命错误，系统无法继续运行',
    action: '立即告警，停止受影响功能，需要紧急人工干预',
    color: 'purple'
  }
};
```

### 2. 错误类型分类

#### 功能错误类型
```javascript
const ERROR_TYPES = {
  // 验证错误
  VALIDATION_ERROR: {
    code: 'VALIDATION_001',
    description: '输入数据验证失败',
    commonCauses: ['数据格式错误', '数据范围越界', '必填字段缺失'],
    recovery: '提示用户修正输入，使用默认值或拒绝操作'
  },
  
  // 资源错误
  RESOURCE_ERROR: {
    code: 'RESOURCE_001',
    description: '资源操作失败',
    commonCauses: ['资源不存在', '资源被锁定', '权限不足'],
    recovery: '重试操作，使用备用资源，或报告错误'
  },
  
  // 网络错误
  NETWORK_ERROR: {
    code: 'NETWORK_001',
    description: '网络通信失败',
    commonCauses: ['连接超时', '服务器无响应', '网络中断'],
    recovery: '自动重试，使用缓存数据，或降级服务'
  },
  
  // 配置错误
  CONFIGURATION_ERROR: {
    code: 'CONFIG_001',
    description: '配置错误',
    commonCauses: ['配置缺失', '配置格式错误', '配置冲突'],
    recovery: '使用默认配置，从备份恢复，或提示用户修正'
  },
  
  // 逻辑错误
  LOGIC_ERROR: {
    code: 'LOGIC_001',
    description: '业务逻辑错误',
    commonCauses: ['算法错误', '状态不一致', '竞态条件'],
    recovery: '重置状态，重新计算，或使用安全模式'
  },
  
  // 系统错误
  SYSTEM_ERROR: {
    code: 'SYSTEM_001',
    description: '系统内部错误',
    commonCauses: ['内存不足', 'CPU超限', '内部异常'],
    recovery: '重启服务，清理资源，或进入维护模式'
  },
  
  // 外部服务错误
  EXTERNAL_SERVICE_ERROR: {
    code: 'EXTERNAL_001',
    description: '外部服务错误',
    commonCauses: ['API调用失败', '服务不可用', '数据格式不匹配'],
    recovery: '使用缓存数据，调用备用服务，或降级功能'
  }
};
```

## 📝 错误处理模式

### 1. 防御性编程模式

#### 输入验证模式
```javascript
/**
 * 防御性输入验证
 */
function processInput(input) {
  // === 1. 空值检查 ===
  if (input == null) {
    throw new ValidationError('输入不能为空', {
      code: 'VALIDATION_001',
      field: 'input',
      expected: '非空值'
    });
  }
  
  // === 2. 类型检查 ===
  if (typeof input !== 'object') {
    throw new ValidationError('输入必须是对象', {
      code: 'VALIDATION_002',
      field: 'input',
      expected: 'object',
      actual: typeof input
    });
  }
  
  // === 3. 必需字段检查 ===
  const requiredFields = ['id', 'name', 'type'];
  for (const field of requiredFields) {
    if (!(field in input)) {
      throw new ValidationError(`缺少必需字段: ${field}`, {
        code: 'VALIDATION_003',
        field,
        expected: '存在'
      });
    }
  }
  
  // === 4. 字段类型检查 ===
  const fieldTypes = {
    id: 'string',
    name: 'string',
    type: 'string',
    priority: 'number',
    enabled: 'boolean'
  };
  
  for (const [field, expectedType] of Object.entries(fieldTypes)) {
    if (field in input && typeof input[field] !== expectedType) {
      throw new ValidationError(`字段类型错误: ${field}`, {
        code: 'VALIDATION_004',
        field,
        expected: expectedType,
        actual: typeof input[field]
      });
    }
  }
  
  // === 5. 字段值范围检查 ===
  if (input.priority !== undefined) {
    if (input.priority < 1 || input.priority > 10) {
      throw new ValidationError('优先级必须在1-10之间', {
        code: 'VALIDATION_005',
        field: 'priority',
        expected: '1-10',
        actual: input.priority
      });
    }
  }
  
  // === 6. 业务规则检查 ===
  if (!isValidType(input.type)) {
    throw new ValidationError(`无效的类型: ${input.type}`, {
      code: 'VALIDATION_006',
      field: 'type',
      expected: '有效类型',
      actual: input.type,
      validTypes: getAllValidTypes()
    });
  }
  
  return input;
}
```

#### 资源安全访问模式
```javascript
/**
 * 资源安全访问模式
 */
class ResourceManager {
  constructor() {
    this.resources = new Map();
    this.locks = new Map();
    this.timeout = 100; // 锁定超时时间（ticks）
  }
  
  /**
   * 安全获取资源
   */
  safeGet(resourceId) {
    // 检查资源是否存在
    if (!this.resources.has(resourceId)) {
      throw new ResourceError(`资源不存在: ${resourceId}`, {
        code: 'RESOURCE_001',
        resourceId,
        action: 'get'
      });
    }
    
    // 检查资源是否被锁定
    const lock = this.locks.get(resourceId);
    if (lock && lock.expires > Game.time) {
      throw new ResourceError(`资源被锁定: ${resourceId}`, {
        code: 'RESOURCE_002',
        resourceId,
        lockedBy: lock.owner,
        expires: lock.expires,
        action: 'get'
      });
    }
    
    return this.resources.get(resourceId);
  }
  
  /**
   * 安全更新资源
   */
  safeUpdate(resourceId, updates, owner) {
    // 获取资源（会检查存在性和锁定）
    const resource = this.safeGet(resourceId);
    
    try {
      // 锁定资源
      this.lockResource(resourceId, owner);
      
      // 应用更新
      const updated = { ...resource, ...updates };
      
      // 验证更新后的资源
      this.validateResource(updated);
      
      // 保存更新
      this.resources.set(resourceId, updated);
      
      return {
        success: true,
        resource: updated,
        previous: resource
      };
      
    } catch (error) {
      // 回滚：恢复原始资源
      this.resources.set(resourceId, resource);
      
      return {
        success: false,
        error: error.message,
        errorCode: error.code,
        resource: resource // 返回原始资源
      };
      
    } finally {
      // 释放锁
      this.unlockResource(resourceId);
    }
  }
  
  lockResource(resourceId, owner) {
    this.locks.set(resourceId, {
      owner,
      expires: Game.time + this.timeout,
      lockedAt: Game.time
    });
  }
  
  unlockResource(resourceId) {
    this.locks.delete(resourceId);
  }
  
  validateResource(resource) {
    // 资源验证逻辑
    if (!resource.id) {
      throw new ValidationError('资源必须包含ID', {
        code: 'RESOURCE_VALIDATION_001',
        resource
      });
    }
    // 更多验证...
  }
}
```

### 2. 错误恢复模式

#### 重试模式
```javascript
/**
 * 智能重试模式
 */
class RetryManager {
  constructor(config = {}) {
    this.config = {
      maxRetries: 3,
      initialDelay: 1,
      maxDelay: 10,
      backoffFactor: 2,
      timeout: 50,
      ...config
    };
    
    this.retryCounts = new Map();
  }
  
  /**
   * 执行带重试的操作
   */
  async executeWithRetry(operation, context) {
    const operationId = context.id || generateId();
    let lastError = null;
    
    for (let attempt = 0; attempt <= this.config.maxRetries; attempt++) {
      try {
        // 设置超时
        const timeoutPromise = new Promise((_, reject) => {
          setTimeout(() => reject(new TimeoutError('操作超时')), this.config.timeout);
        });
        
        // 执行操作
        const result = await Promise.race([
          operation(context),
          timeoutPromise
        ]);
        
        // 成功：清除重试计数并返回结果
        this.retryCounts.delete(operationId);
        return {
          success: true,
          data: result,
          attempts: attempt + 1,
          retried: attempt > 0
        };
        
      } catch (error) {
        lastError = error;
        
        // 检查是否应该重试
        if (!this.shouldRetry(error, attempt, context)) {
          break;
        }
        
        // 计算延迟
        const delay = this.calculateDelay(attempt);
        
        // 记录重试
        this.recordRetry(operationId, attempt, error, delay);
        
        // 等待延迟
        if (delay > 0) {
          await this.sleep(delay);
        }
      }
    }
    
    // 所有重试都失败
    return {
      success: false,
      error: lastError.message,
      errorCode: lastError.code,
      attempts: this.config.maxRetries + 1,
      lastError: lastError
    };
  }
  
  shouldRetry(error, attempt, context) {
    // 检查重试次数
    if (attempt >= this.config.maxRetries) {
      return false;
    }
    
    // 检查错误类型：某些错误不应该重试
    const nonRetryableErrors = [
      'VALIDATION_ERROR',
      'PERMISSION_ERROR',
      'NOT_FOUND_ERROR'
    ];
    
    if (nonRetryableErrors.includes(error.code)) {
      return false;
    }
    
    // 检查上下文：某些操作不应该重试
    if (context.noRetry) {
      return false;
    }
    
    // 默认可以重试
    return true;
  }
  
  calculateDelay(attempt) {
    const delay = this.config.initialDelay * Math.pow(this.config.backoffFactor, attempt);
    return Math.min(delay, this.config.maxDelay);
  }
  
  recordRetry(operationId, attempt, error, delay) {
    const count = (this.retryCounts.get(operationId) || 0) + 1;
    this.retryCounts.set(operationId, count);
    
    logWarning(`操作重试: ${operationId}`, {
      attempt: attempt + 1,
      maxRetries: this.config.maxRetries,
      error: error.message,
      delay,
      totalRetries: count
    });
  }
  
  sleep(ticks) {
    return new Promise(resolve => {
      setTimeout(resolve, ticks);
    });
  }
}
```

#### 降级模式
```javascript
/**
 * 服务降级模式
 */
class DegradationManager {
  constructor() {
    this.services = new Map();
    this.degradationLevels = new Map();
    this.fallbackStrategies = new Map();
  }
  
  /**
   * 注册服务
   */
  registerService(serviceId, service, fallback) {
    this.services.set(serviceId, {
      primary: service,
      fallback: fallback,
      status: 'HEALTHY',
      lastCheck: Game.time,
      errorCount: 0
    });
    
    this.degradationLevels.set(serviceId, 'NORMAL');
  }
  
  /**
   * 执行服务调用（带自动降级）
   */
  async callService(serviceId, params) {
    const serviceInfo = this.services.get(serviceId);
    if (!serviceInfo) {
      throw new ServiceError(`服务未注册: ${serviceId}`);
    }
    
    const degradationLevel = this.degradationLevels.get(serviceId);
    
    try {
      // 根据降级级别选择执行策略
      let result;
      switch (degradationLevel) {
        case 'NORMAL':
          // 正常模式：使用主服务
          result = await this.callPrimaryService(serviceId, params, serviceInfo);
          break;
          
        case 'DEGRADED':
          // 降级模式：主服务失败时使用备用
          result = await this.callWithFallback(serviceId, params, serviceInfo);
          break;
          
        case 'FAILOVER':
          // 故障转移模式：直接使用备用
          result = await this.callFallbackService(serviceId, params, serviceInfo);
          break;
          
        case 'DISABLED':
          // 禁用模式：服务不可用
          throw new ServiceError(`服务已禁用: ${serviceId}`);
          
        default:
          throw new ServiceError(`未知的降级级别: ${degradationLevel}`);
      }
      
      // 成功：更新服务状态
      this.updateServiceHealth(serviceId, true);
      
      return {
        success: true,
        data: result,
        serviceLevel: degradationLevel,
        usedFallback: degradationLevel !== 'NORMAL'
      };
      
    } catch (error) {
      // 失败：更新服务状态并可能降级
      this.updateServiceHealth(serviceId, false);
      
      // 检查是否需要降级
      this.checkDegradation(serviceId, serviceInfo);
      
      return {
        success: false,
        error: error.message,
        errorCode: error.code,
        serviceLevel: degradationLevel,
        suggestion: this.getRecoverySuggestion(serviceId)
      };
    }
  }
  
  async callPrimaryService(serviceId, params, serviceInfo) {
    try {
      return await serviceInfo.primary(params);
    } catch (error) {
      // 记录错误
      serviceInfo.errorCount++;
      serviceInfo.lastError = error;
      serviceInfo.lastFailure = Game.time;
      
      throw error;
    }
  }
  
  async callWithFallback(serviceId, params, serviceInfo) {
    try {
      return await serviceInfo.primary(params);
    } catch (primaryError) {
      // 主服务失败，尝试备用
      logWarning(`主服务失败，使用备用: ${serviceId}`, {
        error: primaryError.message,
        attempt: 'fallback'
      });
      
      try {
        return await serviceInfo.fallback(params);
      } catch (fallbackError) {
        // 备用也失败
        throw new ServiceError(`主服务和备用都失败: ${serviceId}`, {
          primaryError: primaryError.message,
          fallbackError: fallbackError.message
        });
      }
    }
  }
  
  async callFallbackService(serviceId, params, serviceInfo) {
    return await serviceInfo.fallback(params);
  }
  
  updateServiceHealth(serviceId, success) {
    const serviceInfo = this.services.get(serviceId);
    if (!serviceInfo) return;
    
    if (success) {
      // 成功：减少错误计数，更新状态
      serviceInfo.errorCount = Math.max(0, serviceInfo.errorCount - 1);
      serviceInfo.lastSuccess = Game.time;
      serviceInfo.status = 'HEALTHY';
    } else {
      // 失败：增加错误计数
      serviceInfo.errorCount++;
      serviceInfo.status = 'UNHEALTHY';
    }
    
    serviceInfo.lastCheck = Game.time;
  }
  
  checkDegradation(serviceId, serviceInfo) {
    const errorThresholds = {
      NORMAL: 3,     // 3次错误后