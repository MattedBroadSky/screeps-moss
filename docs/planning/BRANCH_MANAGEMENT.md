# 分支管理策略

## 1. 分支结构

### 1.1 主要分支
- **main**: 主分支，包含稳定的、可部署的代码
- **develop**: 开发分支，集成所有功能开发

### 1.2 支持分支
- **feature/***: 功能开发分支
- **bugfix/***: 错误修复分支
- **hotfix/***: 紧急修复分支
- **release/***: 发布准备分支
- **docs/***: 文档更新分支

## 2. 分支命名规范

### 2.1 功能分支
```
feature/<功能名称>-<JIRA编号>
示例: feature/energy-management-SCR-001
```

### 2.2 修复分支
```
bugfix/<问题描述>-<JIRA编号>
示例: bugfix/creep-spawn-fix-SCR-002
```

### 2.3 紧急修复分支
```
hotfix/<版本号>-<问题描述>
示例: hotfix/v1.0.1-memory-leak
```

### 2.4 发布分支
```
release/<版本号>
示例: release/v1.0.0
```

### 2.5 文档分支
```
docs/<文档类型>
示例: docs/architecture-design
```

## 3. 分支生命周期

### 3.1 创建分支
```bash
# 从 develop 分支创建功能分支
git checkout develop
git pull origin develop
git checkout -b feature/energy-management-SCR-001
```

### 3.2 开发流程
1. 在功能分支上进行开发
2. 定期从 develop 分支合并更新
3. 提交清晰的提交信息

### 3.3 合并流程
1. 完成开发后，创建 Pull Request
2. 代码审查通过后，合并到 develop 分支
3. 删除已合并的功能分支

### 3.4 发布流程
1. 从 develop 分支创建 release 分支
2. 在 release 分支上进行最终测试和修复
3. 合并到 main 分支并打标签
4. 将 release 分支合并回 develop 分支

## 4. 提交规范

### 4.1 提交信息格式
```
<类型>: <描述>

[可选正文]
[可选脚注]
```

### 4.2 提交类型
- **feat**: 新功能
- **fix**: 错误修复
- **docs**: 文档更新
- **style**: 代码格式调整
- **refactor**: 代码重构
- **test**: 测试相关
- **chore**: 构建过程或辅助工具变动

### 4.3 示例
```
feat: 添加能量管理系统

- 实现能量采集模块
- 添加能量分配算法
- 完成单元测试

关联任务: SCR-001
```

## 5. 分支保护规则

### 5.1 main 分支保护
- ✅ 要求 Pull Request 审查
- ✅ 要求状态检查通过
- ✅ 禁止强制推送
- ✅ 要求线性提交历史

### 5.2 develop 分支保护
- ✅ 要求 Pull Request 审查
- ✅ 要求状态检查通过
- ✅ 禁止强制推送

## 6. 代码审查流程

### 6.1 审查要求
- 至少需要 1 名审查者批准
- 所有 CI 检查必须通过
- 代码符合编码规范

### 6.2 审查重点
- 功能完整性
- 代码质量
- 测试覆盖率
- 文档更新

## 7. 紧急情况处理

### 7.1 紧急修复流程
1. 从 main 分支创建 hotfix 分支
2. 在 hotfix 分支上修复问题
3. 创建 Pull Request 到 main 分支
4. 合并后同步到 develop 分支

### 7.2 回滚流程
1. 确定需要回滚的提交
2. 创建 revert 提交
3. 按照正常流程合并

## 8. 工具支持

### 8.1 Git Hooks
- 预提交检查
- 提交信息格式验证
- 代码质量检查

### 8.2 CI/CD 集成
- 自动化测试
- 代码质量分析
- 自动化部署

## 9. 最佳实践

### 9.1 分支管理
- 保持分支短小精悍
- 及时删除已合并的分支
- 定期同步上游分支

### 9.2 提交管理
- 小步提交，频繁提交
- 提交信息清晰明确
- 一个提交一个功能

### 9.3 合并策略
- 使用 rebase 保持提交历史整洁
- 解决冲突时保持代码质量
- 确保测试覆盖

## 10. 附录

### 10.1 常用命令
```bash
# 查看分支
git branch -a

# 创建并切换分支
git checkout -b feature/new-feature

# 推送分支
git push origin feature/new-feature

# 删除本地分支
git branch -d feature/old-feature

# 删除远程分支
git push origin --delete feature/old-feature

# 同步上游分支
git fetch --all
git rebase origin/develop
```

### 10.2 参考资源
- [Git Flow 工作流](https://nvie.com/posts/a-successful-git-branching-model/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

---

**文档版本**: v1.0  
**最后更新**: 2026-03-23  
**维护者**: Moss (OpenClaw AI)