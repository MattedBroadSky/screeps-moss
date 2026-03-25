# 算法设计指南

## 📋 文档信息
- **文档名称**: 算法设计指南
- **文档版本**: v1.0.0
- **创建日期**: 2026-03-25
- **最后更新**: 2026-03-25
- **负责人**: Moss (OpenClaw AI)
- **状态**: [草案]
- **适用范围**: 所有模块算法设计

## 🎯 设计目标

### 核心原则
1. **高效性** - 算法执行效率高，CPU使用合理
2. **可读性** - 算法逻辑清晰，易于理解和维护
3. **可靠性** - 算法稳定可靠，正确处理边界情况
4. **可测试性** - 算法易于测试和验证
5. **可扩展性** - 算法设计考虑未来扩展

### 质量目标
- **性能**: 算法复杂度在Screeps CPU限制内
- **正确性**: 算法结果准确无误
- **健壮性**: 算法能处理各种异常情况
- **维护性**: 算法代码易于理解和修改

## 📊 算法复杂度要求

### 1. CPU预算分配

#### 总体CPU限制
```javascript
// Screeps游戏每tick CPU限制
const TOTAL_CPU_LIMIT = 500; // 实际值根据游戏阶段变化

// 模块CPU预算分配
const MODULE_CPU_BUDGETS = {
  roomManager: 5,      // RoomManager最大CPU
  energyManager: 3,    // EnergyManager最大CPU
  creepManager: 3,     // CreepManager最大CPU
  roleManager: 4,      // RoleManager最大CPU
  configService: 1,    // ConfigService最大CPU
  memoryService: 2,    // MemoryService最大CPU
  logService: 1,       // LogService最大CPU
};
```

#### 算法复杂度指导
```javascript
// 可接受的算法复杂度（大O表示法）
const ACCEPTABLE_COMPLEXITY = {
  // 常数时间 - 优先使用
  O(1): '优秀，优先使用',
  
  // 对数时间 - 良好
  O(log n): '良好，适用于大数据集',
  
  // 线性时间 - 可接受
  O(n): '可接受，注意数据规模',
  
  // 线性对数时间 - 谨慎使用
  O(n log n): '谨慎使用，需要优化',
  
  // 平方时间 - 避免使用
  O(n²): '避免使用，需要重构',
  
  // 指数时间 - 禁止使用
  O(2^n): '禁止使用'
};
```

### 2. 内存使用限制

#### 内存预算
```javascript
// Screeps游戏内存限制
const TOTAL_MEMORY_LIMIT = 2097152; // 2MB

// 模块内存预算
const MODULE_MEMORY_BUDGETS = {
  roomManager: 102400,     // 100KB
  energyManager: 51200,    // 50KB
  creepManager: 102400,    // 100KB
  roleManager: 102400,     // 100KB
  configService: 51200,    // 50KB
  memoryService: 204800,   // 200KB（包含数据存储）
  logService: 102400,      // 100KB
};
```

## 🏗️ 算法设计模式

### 1. 分治算法模式

#### 设计模板
```javascript
/**
 * 分治算法模板
 */
function divideAndConquer(problem, params) {
  // 1. 基本情况：问题足够小，直接解决
  if (isBaseCase(problem)) {
    return solveDirectly(problem);
  }
  
  // 2. 分解：将问题分解为子问题
  const subproblems = divideProblem(problem);
  
  // 3. 解决：递归解决子问题
  const subresults = [];
  for (const subproblem of subproblems) {
    // 注意：限制递归深度，避免栈溢出
    if (getRecursionDepth() < MAX_RECURSION_DEPTH) {
      subresults.push(divideAndConquer(subproblem, params));
    } else {
      // 达到最大深度，使用替代方法
      subresults.push(solveWithAlternative(subproblem));
    }
  }
  
  // 4. 合并：合并子问题的解
  return combineResults(subresults);
}

// 示例：快速排序
function quickSort(arr, left = 0, right = arr.length - 1) {
  if (left >= right) return arr; // 基本情况
  
  // 分解：选择基准并分区
  const pivotIndex = partition(arr, left, right);
  
  // 解决：递归排序左右部分
  quickSort(arr, left, pivotIndex - 1);
  quickSort(arr, pivotIndex + 1, right);
  
  return arr;
}
```

### 2. 动态规划模式

#### 设计模板
```javascript
/**
 * 动态规划算法模板
 */
function dynamicProgramming(problem) {
  // 1. 定义状态
  const n = problem.size;
  const dp = new Array(n + 1);
  
  // 2. 初始化基础情况
  dp[0] = baseCaseValue;
  
  // 3. 状态转移
  for (let i = 1; i <= n; i++) {
    // 计算当前状态
    dp[i] = calculateState(dp, i, problem);
    
    // 内存优化：如果只需要前几个状态
    if (i > OPTIMIZATION_WINDOW) {
      dp[i - OPTIMIZATION_WINDOW] = undefined; // 释放内存
    }
  }
  
  // 4. 返回结果
  return dp[n];
}

// 示例：斐波那契数列（带记忆化）
function fibonacci(n, memo = {}) {
  // 基本情况
  if (n <= 1) return n;
  
  // 检查是否已计算
  if (memo[n] !== undefined) {
    return memo[n];
  }
  
  // 计算并存储结果
  memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo);
  
  // 内存优化：限制记忆化大小
  if (Object.keys(memo).length > MAX_MEMO_SIZE) {
    // 移除最旧的结果
    const oldestKey = Object.keys(memo)[0];
    delete memo[oldestKey];
  }
  
  return memo[n];
}
```

### 3. 贪心算法模式

#### 设计模板
```javascript
/**
 * 贪心算法模板
 */
function greedyAlgorithm(problem) {
  // 1. 预处理：排序或准备数据
  const items = prepareItems(problem);
  
  // 2. 初始化结果
  const result = [];
  let remaining = problem.capacity;
  
  // 3. 贪心选择
  for (const item of items) {
    // 检查是否可以加入
    if (canAddItem(item, remaining)) {
      result.push(item);
      remaining -= item.cost;
      
      // 提前终止：如果已经满足条件
      if (isSolutionComplete(result, problem)) {
        break;
      }
    }
  }
  
  // 4. 验证和优化
  if (isValidSolution(result, problem)) {
    return optimizeSolution(result, problem);
  } else {
    // 贪心失败，使用备用算法
    return fallbackAlgorithm(problem);
  }
}

// 示例：任务调度
function scheduleTasks(tasks, timeLimit) {
  // 按优先级排序（贪心选择标准）
  tasks.sort((a, b) => b.priority - a.priority);
  
  const schedule = [];
  let remainingTime = timeLimit;
  let totalValue = 0;
  
  for (const task of tasks) {
    if (task.duration <= remainingTime) {
      schedule.push(task);
      remainingTime -= task.duration;
      totalValue += task.value;
      
      // 提前终止：如果时间用完
      if (remainingTime <= 0) break;
    }
  }
  
  return { schedule, totalValue, remainingTime };
}
```

### 4. 回溯算法模式

#### 设计模板
```javascript
/**
 * 回溯算法模板
 */
function backtracking(problem) {
  const solutions = [];
  
  /**
   * 回溯函数
   */
  function backtrack(current, remaining) {
    // 终止条件：找到解
    if (isSolution(current, problem)) {
      solutions.push([...current]); // 复制当前解
      return;
    }
    
    // 终止条件：无法继续
    if (!canContinue(current, remaining, problem)) {
      return;
    }
    
    // 生成候选
    const candidates = generateCandidates(current, remaining, problem);
    
    // 尝试每个候选
    for (const candidate of candidates) {
      // 做出选择
      current.push(candidate);
      const newRemaining = updateRemaining(remaining, candidate);
      
      // 递归探索
      backtrack(current, newRemaining);
      
      // 撤销选择
      current.pop();
    }
  }
  
  // 开始回溯
  backtrack([], problem.initial);
  
  // 返回最佳解
  return findBestSolution(solutions, problem);
}

// 示例：路径查找
function findPaths(graph, start, end, maxDepth = 10) {
  const paths = [];
  const visited = new Set();
  
  function dfs(current, path, depth) {
    // 终止条件：达到目标
    if (current === end) {
      paths.push([...path]);
      return;
    }
    
    // 终止条件：达到最大深度
    if (depth >= maxDepth) {
      return;
    }
    
    // 终止条件：已访问
    if (visited.has(current)) {
      return;
    }
    
    // 标记访问
    visited.add(current);
    path.push(current);
    
    // 探索邻居
    const neighbors = graph.getNeighbors(current);
    for (const neighbor of neighbors) {
      dfs(neighbor, path, depth + 1);
    }
    
    // 回溯
    path.pop();
    visited.delete(current);
  }
  
  dfs(start, [], 0);
  return paths;
}
```

## 📝 算法实现规范

### 1. 代码结构规范

#### 标准算法函数结构
```javascript
/**
 * 算法函数标准结构
 */
function standardAlgorithm(input, options = {}) {
  // === 1. 参数验证和预处理 ===
  if (!isValidInput(input)) {
    throw new ValidationError('无效输入');
  }
  
  const config = {
    ...DEFAULT_CONFIG,
    ...options
  };
  
  // === 2. 初始化 ===
  const startTime = Game.cpu.getUsed();
  const state = initializeState(input, config);
  
  // === 3. 主算法逻辑 ===
  try {
    const result = executeAlgorithm(state, config);
    
    // === 4. 结果验证 ===
    if (!isValidResult(result, input)) {
      throw new AlgorithmError('算法结果无效');
    }
    
    // === 5. 性能监控 ===
    const cpuUsed = Game.cpu.getUsed() - startTime;
    if (cpuUsed > config.maxCpu) {
      logWarning(`算法CPU使用过高: ${cpuUsed}`);
    }
    
    // === 6. 返回结果 ===
    return {
      success: true,
      data: result,
      metrics: {
        cpuUsed,
        memoryUsed: getMemoryUsage(),
        iterations: state.iterations
      }
    };
    
  } catch (error) {
    // === 7. 错误处理 ===
    return {
      success: false,
      error: error.message,
      errorCode: error.code,
      fallbackResult: getFallbackResult(input)
    };
  }
}
```

### 2. 性能优化技巧

#### 缓存优化
```javascript
/**
 * 带缓存的算法
 */
class CachedAlgorithm {
  constructor() {
    this.cache = new Map();
    this.accessCount = new Map();
    this.maxCacheSize = 100;
  }
  
  compute(key, computeFunction) {
    // 检查缓存
    if (this.cache.has(key)) {
      this.accessCount.set(key, (this.accessCount.get(key) || 0) + 1);
      return this.cache.get(key);
    }
    
    // 计算新值
    const startTime = Game.cpu.getUsed();
    const result = computeFunction();
    const cpuUsed = Game.cpu.getUsed() - startTime;
    
    // 缓存结果（如果值得缓存）
    if (this.shouldCache(result, cpuUsed)) {
      this.cacheResult(key, result);
    }
    
    return result;
  }
  
  cacheResult(key, value) {
    // 如果缓存已满，移除最不常用的
    if (this.cache.size >= this.maxCacheSize) {
      this.evictLeastUsed();
    }
    
    this.cache.set(key, value);
    this.accessCount.set(key, 0);
  }
  
  evictLeastUsed() {
    let minKey = null;
    let minAccess = Infinity;
    
    for (const [key, access] of this.accessCount) {
      if (access < minAccess) {
        minAccess = access;
        minKey = key;
      }
    }
    
    if (minKey) {
      this.cache.delete(minKey);
      this.accessCount.delete(minKey);
    }
  }
  
  shouldCache(result, cpuUsed) {
    // 缓存策略：
    // 1. 计算成本高的结果
    // 2. 频繁使用的结果
    // 3. 大小适中的结果
    const resultSize = JSON.stringify(result).length;
    return cpuUsed > 0.5 && resultSize < 1000;
  }
}
```

#### 延迟计算
```javascript
/**
 * 延迟计算模式
 */
class LazyComputation {
  constructor(computeFunction) {
    this.computeFunction = computeFunction;
    this.cachedResult = null;
    this.isComputed = false;
  }
  
  get value() {
    if (!this.isComputed) {
      this.cachedResult = this.computeFunction();
      this.isComputed = true;
    }
    return this.cachedResult;
  }
  
  invalidate() {
    this.isComputed = false;
    this.cachedResult = null;
  }
}

// 使用示例
const expensiveCalculation = new LazyComputation(() => {
  console.log('执行昂贵计算...');
  return computeExpensiveValue();
});

// 第一次访问触发计算
console.log(expensiveCalculation.value); // 输出：执行昂贵计算... 然后结果

// 后续访问使用缓存
console.log(expensiveCalculation.value); // 直接输出结果，不执行计算
```

### 3. 内存优化技巧

#### 对象池模式
```javascript
/**
 * 对象池实现
 */
class ObjectPool {
  constructor(createFunction, resetFunction, initialSize = 10) {
    this.createFunction = createFunction;
    this.resetFunction = resetFunction;
    this.pool = [];
    this.activeCount = 0;
    
    // 预创建对象
    for (let i = 0; i < initialSize; i++) {
      this.pool.push(this.createFunction());
    }
  }
  
  acquire() {
    if (this.pool.length > 0) {
      this.activeCount++;
      return this.pool.pop();
    } else {
      // 池为空，创建新对象
      this.activeCount++;
      return this.createFunction();
    }
  }
  
  release(obj) {
    // 重置对象状态
    this.resetFunction(obj);
    
    // 放回池中（限制池大小）
    if (this.pool.length < this.maxPoolSize) {
      this.pool.push(obj);
    }
    this.activeCount--;
  }
  
  get stats() {
    return {
      poolSize: this.pool.length,
      activeCount: this.activeCount,
      totalCreated: this.pool.length + this.activeCount
    };
  }
}

// 使用示例：Creep任务对象池
const taskPool = new ObjectPool(
  () => ({ type: '', target: null, priority: 0, data: {} }),
  (task) => {
    task.type = '';
    task.target = null;
    task.priority = 0;
    task.data = {};
  },
  20 // 初始大小
);

// 获取任务对象
const task = taskPool.acquire();
task.type = 'harvest';
task.target = source.id;
task.priority = 10;

// 使用后释放
taskPool.release(task);
```

## 🧪 算法测试规范

### 1. 测试用例设计

#### 边界条件测试
```javascript
describe('算法边界条件测试', () => {
  it('应该处理空输入', () => {
    const result = algorithm([]);
    expect(result.success).toBe(true);
    expect(result.data).toEqual([]);
  });
  
  it('应该处理单个元素', () => {
    const result = algorithm([42]);
    expect(result.success).toBe(true);
    expect(result.data).toEqual([42]);
  });
  
  it('应该处理最大规模输入', () => {
    const maxInput = generateMaxSizeInput();
    const result = algorithm(maxInput);
    
    expect(result.success).toBe(true);
    expect(result.metrics.cpuUsed).toBeLessThan(CPU_LIMIT);
    expect(result.metrics.memoryUsed).toBeLessThan(MEMORY_LIMIT);
  });
  
  it('应该处理无效输入', () => {
    expect(() => algorithm(null)).toThrow(ValidationError);
    expect(() => algorithm(undefined)).toThrow(ValidationError);
    expect(() => algorithm('invalid')).toThrow(ValidationError);
  });
});
```

### 2. 性能测试

#### 性能基准测试
```javascript
describe('算法性能测试', () => {
  const testSizes = [10, 100, 1000, 10000];
  
  testSizes.forEach(size => {
    it(`应该高效处理 ${size} 个元素`, () => {
      const input = generateTestData(size);
      const startCpu = Game.cpu.getUsed();
      
