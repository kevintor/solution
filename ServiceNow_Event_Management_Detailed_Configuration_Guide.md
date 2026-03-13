# ServiceNow Event Management 详细配置指南
## 从安装到生产的完整实施手册

---

## 一、Event Management 组件架构

### 1.1 核心组件

```
┌─────────────────────────────────────────────────────────────┐
│                    Event Management 架构                     │
├─────────────────────────────────────────────────────────────┤
│  事件收集层 → 事件处理层 → 告警管理层 → 响应执行层          │
├─────────────────────────────────────────────────────────────┤
│  Connectors    Event Rules   Alert Rules   Remediation      │
│  Listeners     Filters       Correlation   Notifications    │
│  APIs          Transform     Aggregation   Tickets          │
│  Webhooks      Enrichment    Prioritization Automation      │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 数据流

```
外部监控工具
     ↓
事件收集器 (Connector/Listener/API)
     ↓
事件标准化 (Event Mapping)
     ↓
事件过滤 (Filter)
     ↓
事件规则处理 (Event Rule)
     ↓
告警创建/更新 (Alert)
     ↓
告警关联分组 (Correlation)
     ↓
服务影响分析 (Impact Analysis)
     ↓
响应执行 (Remediation/Notification)
```

---

## 二、详细配置步骤

### 2.1 初始设置

#### 步骤 1：启用 Event Management
```
路径：System Definition > Plugins
搜索：Event Management
操作：Activate
等待：安装完成（约5-10分钟）
```

#### 步骤 2：运行 Guided Setup
```
路径：Event Management > Guided Setup
或：All > Guided Setup > Event Management

任务清单：
□ 安装 Event Management 应用
□ 配置角色和权限
□ 设置事件源
□ 配置事件规则
□ 设置告警管理
□ 配置服务映射
```

---

### 2.2 事件源配置

#### 2.2.1 连接器类型

| 类型 | 描述 | 适用场景 |
|------|------|----------|
| **REST API** | 通过 API 接收事件 | 自定义监控工具 |
| **SNMP Trap** | 接收 SNMP 陷阱 | 网络设备监控 |
| **Syslog** | 接收系统日志 | 服务器/应用日志 |
| **Webhook** | HTTP 回调 | 云服务集成 |
| **Native Connector** | 原生集成 | ServiceNow 认证工具 |

#### 2.2.2 配置 REST API 事件源

```
路径：Event Management > Event Sources > REST

配置项：
- Name: Custom Monitoring API
- Endpoint: /api/now/table/em_event
- Authentication: Basic OAuth
- API Key: [生成]

示例请求：
POST https://instance.service-now.com/api/now/table/em_event
Headers:
  Authorization: Bearer [token]
  Content-Type: application/json

Body:
{
  "source": "datadog",
  "node": "web-server-01",
  "metric_name": "cpu_usage",
  "value": 95,
  "severity": "critical",
  "description": "CPU usage exceeded threshold",
  "additional_info": "{\"datacenter\": \"us-east-1\"}"
}
```

#### 2.2.3 配置 SNMP Trap 监听器

```
路径：Event Management > Event Sources > SNMP

配置项：
- Name: Network Device Traps
- Port: 162
- Community String: [配置]
- MIB Mapping: 导入 MIB 文件
- OID to Event Mapping:
  1.3.6.1.4.1.9.9.43.2.0.1 → Interface Down
  1.3.6.1.4.1.9.9.43.2.0.2 → Interface Up
```

---

### 2.3 事件规则配置

#### 2.3.1 事件规则类型

| 规则类型 | 功能 | 示例 |
|----------|------|------|
| **Transform** | 转换事件字段 | 修改 severity 值 |
| **Filter** | 过滤事件 | 丢弃测试环境事件 |
| **Enrich** | 丰富事件信息 | 添加 CMDB 属性 |
| **Correlate** | 关联事件 | 合并重复事件 |
| **Alert** | 创建/更新告警 | 生成 Incident |

#### 2.3.2 创建事件规则

```
路径：Event Management > Event Rules

规则配置示例：

名称：Critical CPU Alert
顺序：100
过滤条件：
  metric_name = cpu_usage
  AND severity = critical
  AND value > 90

操作：
  1. Transform:
     - description = "High CPU on ${node}: ${value}%"
  
  2. Enrich:
     - 从 CMDB 查询 node 的 owner
     - 添加 owner 到 event
  
  3. Create Alert:
     - severity: 1-Critical
     - category: Hardware
     - assignment_group: [动态查询]
```

#### 2.3.3 事件过滤最佳实践

```javascript
// 过滤条件示例

// 1. 丢弃维护窗口内的事件
source != 'maintenance_tool'
AND (maintenance_window IS EMPTY OR maintenance_window.active = false)

// 2. 过滤低优先级测试事件
severity IN (critical, high, medium)
AND environment != 'test'

// 3. 去重条件
source = previous.source
AND node = previous.node
AND metric_name = previous.metric_name
AND ABS(time - previous.time) < 300 seconds
```

---

### 2.4 告警管理配置

#### 2.4.1 告警生命周期

```
New → Acknowledged → In Progress → Resolved → Closed
  ↓         ↓              ↓            ↓         ↓
通知    停止升级      更新状态    记录方案   归档
```

#### 2.4.2 告警规则配置

```
路径：Event Management > Alert Rules

规则1：自动确认已知问题
条件：
  description CONTAINS "scheduled maintenance"
动作：
  - Acknowledge alert
  - Set state: Acknowledged
  - Add note: "Known maintenance window"

规则2：自动创建 Incident
条件：
  severity = 1-Critical
  AND service IN [production_services]
动作：
  - Create Incident
  - Priority: 1-Critical
  - Assignment Group: [from service]
  - Short Description: ${alert.description}

规则3：升级策略
条件：
  age > 30 minutes
  AND acknowledged = false
动作：
  - Escalate to manager
  - Send SMS notification
  - Update priority to Critical
```

#### 2.4.3 告警关联配置

```
路径：Event Management > Alert Correlation

关联规则1：时间窗口关联
时间窗口：5分钟
条件：
  same node
  AND similar description (80% match)
动作：
  - Create alert group
  - Set primary alert

关联规则2：拓扑关联
条件：
  affected CI in same service
  OR CI has dependency relationship
动作：
  - Group by service
  - Identify root cause CI

关联规则3：ML智能关联 (Yokohama+)
启用：Machine Learning Correlation
训练数据：90天历史告警
最小置信度：0.75
```

---

### 2.5 服务映射配置

#### 2.5.1 服务定义

```
路径：Service Mapping > Services

服务定义示例：

名称：Online Banking System
关键性：Critical
SLA：99.9% uptime

包含CI：
- Web Servers (3 nodes)
- Application Servers (2 nodes)
- Database Primary
- Database Replica
- Load Balancer
- CDN
```

#### 2.5.2 影响规则

```
路径：Event Management > Impact Rules

规则：数据库故障影响
条件：
  CI type = Database
  AND alert severity = Critical
影响：
  - Service health: Degraded (if replica available)
  - Service health: Down (if primary only)
  - Business impact: High
  - Notify: Service Owner, VP Engineering
```

---

## 三、高级配置

### 3.1 机器学习配置 (Yokohama+)

#### 3.1.1 启用 ML 告警关联

```
路径：Event Management > Machine Learning > Settings

配置：
- Enable ML Correlation: true
- Training Schedule: Weekly
- Minimum Training Data: 1000 alerts
- Confidence Threshold: 0.75
- Auto-apply Suggestions: false (manual review)
```

#### 3.1.2 模型训练

```
路径：Event Management > Machine Learning > Model Training

步骤：
1. 选择训练数据范围 (建议90天)
2. 选择要训练的CI类别
3. 启动训练任务
4. 等待训练完成 (2-4小时)
5. 查看模型性能指标
6. 发布模型到生产
```

#### 3.1.3 ML 结果审查

```
路径：Event Management > Machine Learning > Suggestions

审查项目：
□ 建议的告警分组是否合理
□ 置信度评分是否准确
□ 误报率是否在可接受范围
□ 新出现的关联模式

操作：
- Accept: 应用到生产规则
- Reject: 不采用
- Modify: 调整后应用
```

---

### 3.2 自动化修复配置

#### 3.2.1 修复动作类型

| 类型 | 描述 | 示例 |
|------|------|------|
| **Workflow** | 执行工作流 | 自动重启服务 |
| **Script** | 运行脚本 | 清理日志文件 |
| **API Call** | 调用外部API | 扩容云资源 |
| **Notification** | 发送通知 | 短信/邮件 |

#### 3.2.2 创建修复规则

```
路径：Event Management > Remediation Rules

规则：自动重启服务
条件：
  metric_name = service_status
  AND value = stopped
  AND service IN [auto_restart_services]
  AND previous_remediation_failed = false

动作：
  1. 执行 Workflow: "Restart Service"
     - Input: ${node}, ${service_name}
  
  2. 等待 2 分钟
  
  3. 验证服务状态
     - 如果成功: Resolve alert
     - 如果失败: Escalate to L2

安全控制：
- 最大执行次数: 3
- 执行时间窗口: 8:00-22:00
- 需要批准: false (低风险操作)
```

---

### 3.3 仪表盘配置

#### 3.3.1 关键指标仪表盘

```
路径：Event Management > Overview

组件：
1. 实时告警计数器
   - Critical: [红色大数字]
   - High: [橙色数字]
   - Medium: [黄色数字]

2. 服务健康度
   - 绿色: 正常
   - 黄色: 降级
   - 红色: 中断

3. 告警趋势图
   - 时间范围: 24小时
   - 按严重性分组

4. Top 10 告警来源
   - 按数量排序
   - 可钻取详情

5. 团队工作负载
   - 待处理告警/人
   - 平均解决时间
```

#### 3.3.2 自定义仪表盘

```
路径：System UI > Dashboards

创建步骤：
1. 新建 Dashboard: "Event Management Operations"
2. 添加 Widget:
   - Alert List (filtered by assignment_group)
   - Service Health Map
   - Event Volume Chart
   - MTTR Trend
3. 设置刷新频率: 30 seconds
4. 分享给运维团队
```

---

## 四、API 参考

### 4.1 发送事件 API

```bash
# 创建事件
POST /api/now/table/em_event

Request:
{
  "source": "monitoring_tool",
  "node": "server01",
  "type": "cpu_high",
  "resource": "CPU",
  "metric_name": "cpu_usage",
  "value": 95,
  "severity": "critical",
  "description": "CPU usage is 95%",
  "additional_info": "{\"datacenter\": \"dc1\"}"
}

Response:
{
  "result": {
    "sys_id": "[event_id]",
    "number": "EVT0010001",
    "state": "processed"
  }
}
```

### 4.2 查询告警 API

```bash
# 获取活跃告警
GET /api/now/table/em_alert?sysparm_query=state!=Resolved^ORDERBYDESCseverity

# 获取特定服务告警
GET /api/now/table/em_alert?sysparm_query=service.name=Online Banking^state!=Resolved
```

### 4.3 更新告警 API

```bash
# 确认告警
PATCH /api/now/table/em_alert/{sys_id}
{
  "state": "Acknowledged",
  "acknowledged_by": "[user_id]",
  "work_notes": "Investigating"
}

# 解决告警
PATCH /api/now/table/em_alert/{sys_id}
{
  "state": "Resolved",
  "resolution_code": "Fixed",
  "resolution_notes": "Restarted service"
}
```

---

## 五、故障排除

### 5.1 事件未处理

**排查步骤：**
1. 检查 Event Source 状态
2. 查看 Event Log: Event Management > Logs
3. 验证 Event Rule 顺序和条件
4. 检查 Transform/Filter 脚本错误

### 5.2 告警未创建

**排查步骤：**
1. 确认 Event Rule 中设置了 Create Alert 动作
2. 检查 Alert Rule 的过滤条件
3. 查看 Alert Creation Log
4. 验证权限设置

### 5.3 关联不准确

**优化建议：**
1. 增加训练数据量
2. 调整关联规则权重
3. 手动标记正确/错误的关联
4. 重新训练 ML 模型

---

## 六、性能优化

### 6.1 事件处理优化

| 优化项 | 建议 |
|--------|------|
| 事件过滤 | 尽早过滤，减少后续处理 |
| 规则顺序 | 高频规则放前面 |
| 批处理 | 启用事件批处理模式 |
| 索引优化 | 确保关键字段有索引 |

### 6.2 存储优化

```
数据保留策略：
- 原始事件: 30天
- 告警记录: 90天
- 关联历史: 180天
- ML训练数据: 365天

自动清理：
路径：Event Management > Data Retention
```

---

## 七、参考链接

1. **Event Management Documentation**
   - https://www.servicenow.com/docs/r/yokohama/it-operations-management/event-management/c_EM.html

2. **Event Rules Guide**
   - https://www.servicenow.com/docs/r/it-operations-management/event-management/c_EMConfiguration.html

3. **Connectors and Listeners**
   - https://www.servicenow.com/docs/r/it-operations-management/event-management/connectors-and-listeners.html

4. **Best Practices**
   - https://www.servicenow.com/docs/r/it-operations-management/event-management/r_EMBestPractice.html

5. **Implementation Guide**
   - https://mynow.servicenow.com/now/best-practices/assets/event-management-implementation-guide

---

*文档版本: 2026.03*  
*适用版本: ServiceNow Yokohama+*  
*作者: Kimi Claw*
