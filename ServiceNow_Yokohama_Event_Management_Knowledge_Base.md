# ServiceNow Yokohama Event Management 知识库
## 完整功能文档与实施指南

---

## 一、产品概述

### 1.1 什么是 Event Management
ServiceNow Event Management 是 IT 运营管理(ITOM)的核心组件，用于：
- **事件收集**：从各种监控工具收集事件
- **智能关联**：使用机器学习自动关联相关告警
- **降噪处理**：过滤冗余事件，减少告警疲劳
- **服务影响分析**：评估事件对业务服务的影响

### 1.2 Yokohama 版本核心增强
Yokohama 版本在 Event Management 方面引入了重大改进，特别是基于机器学习的告警关联功能。

---

## 二、Yokohama 版本新特性

### 2.1 网络流量告警关联 (Network Traffic-Based Alert Grouping)
**文档链接**：`https://www.servicenow.com/docs/r/yokohama/release-notes/event-management-rn.html`

**核心功能**：
- 使用发现的 TCP 连接进行告警分组
- 结合机器学习算法识别相关告警
- 自动识别基础设施依赖关系

**价值**：
- 减少 60-80% 的冗余告警
- 更快定位根本原因
- 提高运维团队效率

### 2.2 自动化告警分组 (Automated Alert Grouping)
**文档链接**：`https://www.servicenow.com/docs/r/yokohama/it-operations-management/event-management/c_SACorrelatedAlertGroups.html`

**技术实现**：
```
机器学习算法分析：
- 历史告警数据模式
- 时间相关性
- 拓扑依赖关系
- 事件属性相似性
```

**分组类型**：
| 分组类型 | 描述 | 适用场景 |
|---------|------|----------|
| 智能关联 | 基于 ML 的自动分组 | 复杂环境下的告警关联 |
| 拓扑关联 | 基于 CMDB 关系 | 已知依赖关系的组件 |
| 时间关联 | 时间窗口内的事件 | 批量故障场景 |

### 2.3 增强的告警管理规则
**新功能**：
- 更灵活的告警处理规则
- 基于机器学习的阈值建议
- 自动化的告警升级策略

---

## 三、核心功能详解

### 3.1 事件处理流程

```
事件收集 → 标准化 → 过滤 → 关联 → 分级 → 响应
    ↓         ↓        ↓       ↓       ↓       ↓
  各类监控   统一格式   去噪   ML分组   优先级  自动化
  工具集成           降噪处理        评估    处理
```

### 3.2 告警分组算法

#### 3.2.1 机器学习关联 (Intelligent Correlation)
**算法类型**：
- 聚类算法（K-means, DBSCAN）
- 时间序列分析
- 图神经网络（分析拓扑关系）

**输入数据**：
- 告警属性（源、类型、严重程度）
- 时间戳
- 受影响配置项(CI)
- 历史处理记录

**输出结果**：
- 告警分组建议
- 置信度评分
- 推荐的根本原因

#### 3.2.2 拓扑关联
基于 CMDB 中的配置项关系：
- 主机-虚拟机关系
- 应用-数据库依赖
- 网络设备连接

### 3.3 服务影响分析

**功能**：
- 自动映射事件到业务服务
- 计算服务健康度
- 生成影响报告

**仪表盘**：
```
导航路径：Event Management > Overview
功能：
- 全局事件视图
- 服务健康度仪表板
- 告警趋势分析
- 团队工作负载
```

---

## 四、实施指南

### 4.1 前置条件

**技术要求**：
- [ ] ServiceNow Yokohama 版本
- [ ] ITOM 许可
- [ ] 机器学习插件启用
- [ ] 充足的训练数据（至少3个月历史告警）

**组织要求**：
- [ ] 明确的告警处理流程
- [ ] 定义好的服务目录
- [ ] 完整的 CMDB 数据

### 4.2 配置步骤

#### 步骤 1：启用 Event Management
```
导航：System Definition > Plugins
搜索：Event Management
操作：Activate
```

#### 步骤 2：配置事件源
**支持的数据源**：
| 类型 | 示例工具 | 集成方式 |
|------|----------|----------|
| 监控工具 | SolarWinds, Nagios, Zabbix | 连接器/REST API |
| 云平台 | AWS CloudWatch, Azure Monitor | 原生集成 |
| APM | Dynatrace, AppDynamics | 插件 |
| 日志 | Splunk, ELK | 日志分析 |

**配置路径**：
```
Event Management > Event Sources
```

#### 步骤 3：配置告警分组规则
```
导航：Event Management > Alert Grouping
```

**推荐配置**：
```yaml
自动分组:
  启用: true
  算法: 机器学习
  训练周期: 30天
  最小置信度: 0.75
  
拓扑分组:
  启用: true
  最大深度: 3层
  关系类型: [依赖, 包含, 连接]
  
时间分组:
  启用: true
  时间窗口: 5分钟
  相似度阈值: 0.8
```

#### 步骤 4：训练机器学习模型
**注意事项**：
- 需要至少 1000 条历史告警记录
- 训练时间：2-4 小时
- 建议每月重新训练

**操作路径**：
```
Event Management > Machine Learning > Model Training
```

### 4.3 最佳实践

#### 4.3.1 告警降噪策略
**分层过滤**：
1. **事件过滤**：丢弃无关事件
2. **重复抑制**：相同事件去重
3. **维护窗口**：计划内变更抑制告警
4. **ML分组**：智能关联减少告警量

#### 4.3.2 告警分级建议
| 级别 | 响应时间 | 升级策略 | 示例 |
|------|----------|----------|------|
| P1-紧急 | 15分钟 | 立即通知管理层 | 核心系统宕机 |
| P2-高 | 1小时 | 30分钟升级 | 重要服务降级 |
| P3-中 | 4小时 | 2小时升级 | 非关键告警 |
| P4-低 | 24小时 | 不升级 | 信息性事件 |

#### 4.3.3 持续优化
**每周审查**：
- 分析未分组告警
- 调整分组规则
- 优化过滤条件

**每月审查**：
- 重新训练ML模型
- 评估告警准确性
- 更新服务映射

---

## 五、集成方案

### 5.1 与 ITSM 集成
**功能**：
- 自动创建 Incident
- 关联 Problem 记录
- 变更请求联动

**配置**：
```
Event Management > Settings > Incident Creation Rules
```

### 5.2 与 AIOps 集成
**增强功能**：
- 异常检测
- 容量预测
- 智能告警压缩

### 5.3 API 接口
**主要 API**：
```javascript
// 发送事件
POST /api/now/table/em_event
{
  "source": "monitoring_tool",
  "node": "server01",
  "metric_name": "cpu_usage",
  "value": 95,
  "severity": "critical"
}

// 查询告警
GET /api/now/table/em_alert
```

---

## 六、故障排除

### 6.1 常见问题

**问题1：ML分组不准确**
- 原因：训练数据不足
- 解决：收集更多历史数据，重新训练

**问题2：告警风暴**
- 原因：缺乏有效的过滤规则
- 解决：配置维护窗口，启用抑制规则

**问题3：服务映射错误**
- 原因：CMDB数据不完整
- 解决：完善配置项关系

### 6.2 性能优化
**建议**：
- 定期清理历史事件（保留90天）
- 优化数据库索引
- 使用流式处理高并发事件

---

## 七、参考资源

### 7.1 官方文档
1. **Event Management Release Notes (Yokohama)**
   - URL: `https://www.servicenow.com/docs/r/yokohama/release-notes/event-management-rn.html`

2. **Configuring Event Management**
   - URL: `https://www.servicenow.com/docs/r/yokohama/it-operations-management/event-management/using-event-management.html`

3. **Alert Grouping Documentation**
   - URL: `https://www.servicenow.com/docs/r/yokohama/it-operations-management/event-management/c_SACorrelatedAlertGroups.html`

4. **Yokohama New Features**
   - URL: `https://www.servicenow.com/docs/r/yokohama/release-notes/new-features-changes.html`

### 7.2 社区资源
- ServiceNow Community: ITOM Forum
- Medium: Event Management 最佳实践

---

## 八、实施检查清单

### 8.1 部署前
- [ ] 确认平台版本为 Yokohama
- [ ] 完成 ITOM 许可配置
- [ ] 准备历史告警数据
- [ ] 定义服务目录
- [ ] 培训运维团队

### 8.2 部署中
- [ ] 配置事件源
- [ ] 设置告警规则
- [ ] 训练ML模型
- [ ] 配置服务映射
- [ ] 测试集成流程

### 8.3 部署后
- [ ] 监控告警准确性
- [ ] 收集用户反馈
- [ ] 优化分组规则
- [ ] 定期模型重训练
- [ ] 文档更新

---

*知识库版本: 2026.03*  
*适用版本: ServiceNow Yokohama*  
*数据来源: ServiceNow 官方文档、Tavily Search*  
*作者: Kimi Claw*
