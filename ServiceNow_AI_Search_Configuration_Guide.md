# ServiceNow AI Search 配置指南
## 手把手操作手册 (2026版)

---

## 前置条件

### 系统要求
- ServiceNow 版本：Xanadu 或更高
- 插件：`AI Search` 已启用
- 权限：admin 或 ai_search_admin 角色

### 检查清单
- [ ] 确认平台版本支持
- [ ] 拥有管理员权限
- [ ] 知识库已有内容
- [ ] 测试环境准备就绪

---

## 第一阶段：启用 AI Search

### 步骤 1：激活插件

**操作路径：**
```
All > System Definition > Plugins
```

**操作步骤：**
1. 搜索 "AI Search"
2. 找到插件 `com.snc.ai_search`
3. 点击 **Activate**
4. 等待激活完成（约5-10分钟）

**验证激活：**
```
All > AI Search
```
确认左侧导航出现 AI Search 菜单

---

### 步骤 2：运行 Guided Setup

**操作路径：**
```
All > AI Search > Guided Setup
```

**配置流程：**

#### 2.1 欢迎页面
- 点击 **Get Started**
- 阅读功能介绍
- 点击 **Next**

#### 2.2 配置 Indexed Sources
**什么是 Indexed Sources？**
告诉 AI Search 去哪里搜索数据（哪些表、哪些字段）

**默认配置：**
| 数据源 | 表名 | 说明 |
|--------|------|------|
| Knowledge Base | `kb_knowledge` | 知识库文章 |
| Catalog Items | `sc_cat_item` | 服务目录项 |
| Incidents | `incident` | 事件记录 |

**添加自定义数据源：**

1. 点击 **New** 创建新数据源
2. 填写表单：
   ```
   Name: 自定义知识库
   Table: u_custom_kb
   Active: true
   ```
3. 配置字段映射：
   ```
   Title Field: short_description
   Content Field: text
   Number Field: number
   ```
4. 设置过滤器（可选）：
   ```
   Condition: active=true^workflow_state=published
   ```
5. 点击 **Submit**

**配置子表：**
- 展开 **Child Tables**
- 添加需要包含的子表
- 例如：`kb_knowledge_base` 包含多个知识库

---

### 步骤 3：配置 Search Profiles

**操作路径：**
```
All > AI Search > Search Profiles
```

**什么是 Search Profiles？**
定义搜索行为的配置集合，决定 AI 如何理解和响应查询。

**创建 Search Profile：**

1. 点击 **New**
2. 填写基本信息：
   ```
   Name: IT Support Search
   Description: IT服务台AI搜索配置
   Active: true
   ```

3. 配置搜索范围：
   ```
   Indexed Sources: 
   - kb_knowledge (IT知识库)
   - incident (历史事件)
   - sc_cat_item (IT服务目录)
   ```

4. 设置 AI 行为：
   ```
   Enable Genius Results: true
   Enable Auto-complete: true
   Enable Spell Check: true
   Max Results: 10
   ```

5. 配置个性化：
   ```
   User Context Fields:
   - department
   - location
   - title
   ```

6. 点击 **Submit**

---

### 步骤 4：配置 Search Application

**操作路径：**
```
All > AI Search > Search Applications
```

**创建 Search Application：**

1. 点击 **New**
2. 填写配置：
   ```
   Name: IT Portal Search
   Search Profile: IT Support Search
   Active: true
   ```

3. 配置界面选项：
   ```
   Show Filters: true
   Show Sort Options: true
   Results Per Page: 10
   Enable Voice Search: false
   ```

4. 设置结果展示：
   ```
   Card View: true
   Show Thumbnails: false
   Show Metadata: true
   Show Last Updated: true
   ```

5. 点击 **Submit**

---

## 第二阶段：知识库优化

### 步骤 5：内容质量检查

**操作路径：**
```
All > Knowledge > Administration > Knowledge Bases
```

**质量检查清单：**

#### 5.1 元数据完整性
检查每篇文章是否包含：
- [ ] Short description（简洁标题）
- [ ] Description（详细内容）
- [ ] Category（分类）
- [ ] Knowledge Base（所属知识库）
- [ ] Valid to（有效期）
- [ ] Workflow state（已发布）

#### 5.2 批量修复脚本
```javascript
// 修复缺失元数据的文章
var gr = new GlideRecord('kb_knowledge');
gr.addQuery('short_description', '');
gr.query();
while (gr.next()) {
    gr.short_description = gr.description.substring(0, 100);
    gr.update();
}
```

---

### 步骤 6：配置同义词

**操作路径：**
```
All > AI Search > Synonyms
```

**添加同义词组：**

1. 点击 **New**
2. 配置同义词：
   ```
   Name: VPN相关
   Type: Synonym Group
   Terms:
   - VPN
   - 虚拟专用网络
   - 远程访问
   - 公司网络
   - 拨号
   ```
3. 点击 **Submit**

**推荐同义词组：**
| 组名 | 同义词 |
|------|--------|
| 密码 | 密码, password, 口令, 登录凭证 |
| 邮箱 | 邮箱, email, 邮件, Outlook |
| 打印机 | 打印机, printer, 打印, 无法打印 |
| 网络 | 网络, network, 上网, 断网, 连接 |

---

### 步骤 7：设置结果提升规则

**操作路径：**
```
All > AI Search > Result Improvement Rules
```

**创建提升规则：**

**规则1：优先显示最新内容**
```
Name: 优先最新文章
Condition: 所有查询
Action: Boost
Boost Value: +10%
Criteria: sys_updated_on (最近30天)
```

**规则2：根据用户部门提升**
```
Name: 部门相关内容优先
Condition: user.department = IT
Action: Boost
Boost Value: +20%
Criteria: kb_category = IT Support
```

**规则3：置顶关键文章**
```
Name: 置顶密码重置指南
Condition: query contains "密码" OR "password"
Action: Pin to Top
Article: KB0010001 - 如何重置密码
```

---

## 第三阶段：界面集成

### 步骤 8：Service Portal 集成

**操作路径：**
```
Service Portal > Portals
```

**配置步骤：**

1. 选择要配置的 Portal（如：id=it）
2. 进入 **Pages**
3. 找到首页（index）
4. 添加 Widget：
   ```
   Widget: AI Search
   Search Application: IT Portal Search
   ```

5. 配置 Widget 属性：
   ```
   Placeholder: 搜索知识库、服务、历史工单...
   Show Filters: true
   Auto-focus: true
   ```

6. 保存并发布

---

### 步骤 9：Now Assist 集成

**操作路径：**
```
All > Now Assist > Administration
```

**启用 AI 对话：**

1. 进入 **Now Assist Configuration**
2. 启用 **AI Search Integration**
3. 配置对话流程：
   ```
   Welcome Message: 您好！我是AI助手，请问有什么可以帮您？
   Fallback Message: 抱歉，我没找到相关信息。请尝试用其他关键词搜索。
   ```

4. 设置操作权限：
   ```
   Allow Create Incident: true
   Allow Search Knowledge: true
   Allow View Catalog: true
   ```

5. 配置升级规则：
   ```
   Confidence Threshold: 0.7
   Low Confidence Action: 转人工
   ```

---

## 第四阶段：测试验证

### 步骤 10：功能测试

**测试用例清单：**

| 测试项 | 操作 | 预期结果 |
|--------|------|----------|
| 基础搜索 | 输入 "VPN" | 显示VPN相关文章 |
| 自然语言 | 输入 "怎么连公司网络" | 理解意图，返回VPN指南 |
| 同义词 | 输入 "虚拟专用网络" | 返回VPN相关结果 |
| 无结果 | 输入 "xyz123" | 显示无结果提示 |
| 个性化 | IT部门用户搜索 | 优先IT相关内容 |
| 多语言 | 输入 "password reset" | 返回密码重置指南 |

**测试脚本：**
```python
# 自动化测试示例
queries = [
    "VPN",
    "怎么连公司网络", 
    "密码重置",
    "打印机坏了",
    "无法登录邮箱"
]

for query in queries:
    result = ai_search(query)
    assert len(result) > 0, f"查询 '{query}' 无结果"
    print(f"✓ {query}: 找到 {len(result)} 条结果")
```

---

### 步骤 11：性能调优

**监控指标：**
```
All > AI Search > Analytics
```

**关键指标：**
| 指标 | 健康值 | 调优建议 |
|------|--------|----------|
| 平均响应时间 | < 500ms | 增加索引频率 |
| 搜索成功率 | > 90% | 优化同义词 |
| 点击率 | > 40% | 调整结果排序 |
| 零结果率 | < 10% | 补充知识内容 |

**索引优化：**
```
All > AI Search > AI Search Index > Index Schedules
```
- 设置增量索引：每15分钟
- 设置全量索引：每天凌晨2点

---

## 第五阶段：上线推广

### 步骤 12：用户培训

**培训材料准备：**
- [ ] 快速入门指南（1页）
- [ ] 搜索技巧视频（3分钟）
- [ ] FAQ文档
- [ ] 反馈渠道说明

**培训内容：**
1. AI Search 能做什么
2. 如何提问更有效
3. 反馈机制使用
4. 常见问题和解决

---

### 步骤 13：反馈收集

**配置反馈表单：**
```
All > AI Search > Feedback Configuration
```

**启用反馈：**
- 显示 thumbs up/down 按钮
- 允许文字反馈
- 匿名收集选项

**定期审查：**
- 每周审查反馈数据
- 识别改进机会
- 更新知识内容

---

## 故障排除

### 常见问题

**问题1：搜索结果为空**
- 检查 Indexed Sources 是否配置正确
- 确认表中有数据
- 验证过滤器条件

**问题2：搜索结果不准确**
- 添加同义词
- 调整 Result Improvement Rules
- 优化知识库内容

**问题3：响应慢**
- 检查索引状态
- 增加索引频率
- 优化查询条件

**问题4：权限错误**
- 检查用户角色
- 验证 ACL 配置
- 确认知识库访问权限

---

## 附录：快速参考

### 关键配置项速查

| 配置项 | 路径 | 说明 |
|--------|------|------|
| 启用AI Search | Plugins | 激活插件 |
| 数据源 | AI Search > Indexed Sources | 配置搜索范围 |
| 搜索配置 | AI Search > Search Profiles | 定义搜索行为 |
| 同义词 | AI Search > Synonyms | 扩展搜索词汇 |
| 结果排序 | AI Search > Result Improvement Rules | 调整结果权重 |
| 界面配置 | Service Portal | 前端展示 |
| 分析报表 | AI Search > Analytics | 监控效果 |

### 推荐配置值

```yaml
# Search Profile 推荐配置
Max Results: 10
Enable Genius Results: true
Enable Auto-complete: true
Enable Spell Check: true
Confidence Threshold: 0.7

# Indexed Source 推荐配置
Index Frequency: 15 minutes (incremental)
Full Reindex: Daily at 2:00 AM
Include Attachments: false (性能考虑)

# Result Improvement 推荐规则
- 最新内容提升: +10%
- 用户部门匹配: +20%
- 高评分文章: +15%
```

---

*配置指南版本: 2026.03*  
*适用平台: ServiceNow Xanadu+*  
*作者: Kimi Claw*
