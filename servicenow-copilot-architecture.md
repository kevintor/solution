# ServiceNow + Microsoft Copilot AI Incident Routing 系统
## 整体架构设计方案

---

## 1. 执行摘要

### 1.1 项目背景
当前ServiceNow incident分配依赖于静态规则或人工判断，无法充分利用KB中的处理流程知识。本项目旨在构建一个AI驱动的智能路由系统，能够：
- 根据CI关联的KB自动推荐assignment group
- 通过Copilot提供自然语言交互界面
- P1 incident自动触发通知机制

### 1.2 核心目标
| 目标 | 描述 |
|------|------|
| **智能路由** | 基于KB内容自动推荐assignment group |
| **AI助手** | 通过Copilot提供交互式建议查询 |
| **快速响应** | P1 incident自动触发多渠道通知 |
| **知识整合** | RAG技术让AI学习企业KB内容 |

---

## 2. 系统架构总览

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        用户交互层 (Presentation Layer)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────────────┐ │
│  │  ServiceNow  │  │ Microsoft    │  │  Virtual Agent / Now Assist      │ │
│  │  Incident    │  │ Teams        │  │  (自然语言界面)                   │ │
│  │  Form        │  │ Copilot      │  │                                  │ │
│  └──────┬───────┘  └──────┬───────┘  └──────────────┬───────────────────┘ │
└─────────┼─────────────────┼─────────────────────────┼─────────────────────┘
          │                 │                         │
          ▼                 ▼                         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        业务逻辑层 (Business Logic Layer)                    │
│  ┌────────────────┐  ┌──────────────┐  ┌──────────────────────────────┐  │
│  │ Business Rule  │  │ AI Routing   │  │ Notification Engine          │  │
│  │ (触发逻辑)      │  │ Engine       │  │ (P1 Alert)                   │  │
│  └────────┬───────┘  └──────┬───────┘  └──────────────┬───────────────┘  │
│           │                 │                         │                  │
│  ┌────────▼───────┐  ┌──────▼───────┐  ┌──────────────▼───────────────┐  │
│  │ Flow Designer  │  │ Script       │  │ On-Call Schedule             │  │
│  │ (Workflow)     │  │ Include      │  │ Integration                  │  │
│  └────────────────┘  └──────────────┘  └──────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        AI/ML 层 (AI Service Layer)                        │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │              Microsoft Azure OpenAI Service                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐    │    │
│  │  │ GPT-4/GPT-4o │  │ RAG Engine   │  │ Embeddings           │    │    │
│  │  │ (LLM)        │  │ (KB检索)      │  │ (向量化)              │    │    │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                              ▲                                          │
│                              │                                          │
└──────────────────────────────┼──────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        数据层 (Data Layer)                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Incident     │  │ KB Articles  │  │ CMDB (CI)    │  │ AI Search    │  │
│  │ Table        │  │ (处理流程)    │  │ (support_grp)│  │ Index        │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 数据流架构

```
Incident Creation Flow:
────────────────────────────────────────────────────────────────────────────

User creates Incident
        │
        ▼
┌─────────────────┐
│ Business Rule   │───[1]───▶ Check if cmdb_ci is set
│ (After Insert)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ KB Retrieval    │───[2]───▶ Query KB articles related to CI
│ (RAG - Step 1)  │         (use AI Search or scripted query)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ AI Analysis     │───[3]───▶ Send KB content + Incident details
│ (Azure OpenAI)  │         to LLM for assignment recommendation
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Parse Response  │───[4]───▶ Extract assignment_group from AI response
│ (Script Include)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Update Incident │───[5]───▶ Set assignment_group
│ (Set Values)    │         Add work note with AI reasoning
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Priority Check  │───[6]───▶ If Priority = 1 (P1)
│ (Condition)     │         Trigger notification workflow
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
  P1=Y       P1=N
    │         │
    ▼         │
┌─────────────────┐
│ P1 Notification │───[7]───▶ Send SMS/Email/Teams notification
│ Workflow        │         to on-call engineer + manager
└─────────────────┘

Copilot Interaction Flow:
────────────────────────────────────────────────────────────────────────────

Support Engineer opens Teams Copilot
        │
        ▼
┌─────────────────┐
│ Natural Lang    │───[8]───▶ "Who should handle this incident?"
│ Query Input     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Copilot routes  │───[9]───▶ Intent recognition (Now Assist NLU)
│ to Now Assist   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Virtual Agent   │───[10]──▶ Fetch incident details
│ Topic Execution │         Query KB for similar cases
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ AI generates    │───[11]──▶ Azure OpenAI generates recommendation
│ recommendation  │         with explanation
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Display in      │───[12]──▶ Show recommendation + confidence score
│ Teams Chat      │         + option to apply assignment
└─────────────────┘
```

---

## 3. 核心组件设计

### 3.1 CI-KB关联模型

```javascript
// CI-KB关联数据结构
{
    "cmdb_ci": {
        "sys_id": "unique_ci_id",
        "name": "SAP Production Server",
        "support_group": "SAP Team (sys_id)",
        "kb_articles": [
            {
                "number": "KB0012345",
                "title": "SAP Server Incident Handling",
                "category": "escalation_procedure",
                "assignment_rules": {
                    "network_issue": "Network Team",
                    "db_issue": "DBA Team", 
                    "app_issue": "SAP Team"
                }
            }
        ]
    }
}
```

### 3.2 AI路由引擎设计

```javascript
// Script Include: AIRoutingEngine
var AIRoutingEngine = Class.create();
AIRoutingEngine.prototype = {
    initialize: function() {
        this.azureEndpoint = gs.getProperty('azure.openai.endpoint');
        this.apiKey = gs.getProperty('azure.openai.key');
        this.deploymentName = gs.getProperty('azure.openai.deployment');
    },
    
    // 主函数：获取assignment group推荐
    getAssignmentRecommendation: function(incidentId) {
        var incident = new GlideRecord('incident');
        if (!incident.get(incidentId)) return null;
        
        // 1. 收集上下文信息
        var context = this._gatherContext(incident);
        
        // 2. 检索相关KB
        var kbContent = this._retrieveKBContent(context.ciSysId);
        
        // 3. 构建prompt
        var prompt = this._buildPrompt(incident, context, kbContent);
        
        // 4. 调用Azure OpenAI
        var aiResponse = this._callAzureOpenAI(prompt);
        
        // 5. 解析响应
        return this._parseAIResponse(aiResponse);
    },
    
    // RAG: 检索增强生成
    _retrieveKBContent: function(ciSysId) {
        // 使用ServiceNow AI Search或直接查询
        var kbGR = new GlideRecord('kb_knowledge');
        kbGR.addQuery('cmdb_ci', ciSysId);
        kbGR.addActiveQuery();
        kbGR.query();
        
        var articles = [];
        while (kbGR.next()) {
            articles.push({
                number: kbGR.getValue('number'),
                title: kbGR.getValue('short_description'),
                content: kbGR.getValue('text')
            });
        }
        return articles;
    },
    
    _buildPrompt: function(incident, context, kbContent) {
        return {
            system: "You are an expert ITSM routing assistant. Based on the incident details and KB articles, recommend the best assignment group.",
            user: {
                incident: {
                    short_description: incident.short_description,
                    description: incident.description,
                    category: incident.category,
                    subcategory: incident.subcategory,
                    ci_name: context.ciName,
                    urgency: incident.urgency,
                    impact: incident.impact
                },
                kb_articles: kbContent,
                available_groups: context.availableGroups
            },
            output_format: {
                assignment_group: "recommended_group_name",
                confidence: "high/medium/low",
                reasoning: "explanation"
            }
        };
    }
};
```

### 3.3 P1通知工作流

```
P1 Notification Workflow:
┌─────────────────┐
│ Trigger:        │
│ Priority = 1    │
│ AND             │
│ State = New     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Action 1:       │
│ Get On-Call     │
│ Engineer        │
│ (from Schedule) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Action 2:       │
│ Send Email      │
│ (Manager DL)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Action 3:       │
│ Send SMS        │
│ (On-Call Phone) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Action 4:       │
│ Teams Message   │
│ (Escalation Ch) │
└─────────────────┘
```

---

## 4. Microsoft Copilot 集成方案

### 4.1 集成架构

| 组件 | 功能 | 配置要点 |
|------|------|----------|
| **Custom Engine Agent** | Copilot与ServiceNow的桥梁 | Zurich+版本内置支持 |
| **Now Assist** | ServiceNow的AI平台 | 需Now Assist许可证 |
| **Generative AI Controller** | 连接Azure OpenAI | 配置API endpoint和key |
| **Virtual Agent** | 对话界面 | Topic设计和NLU训练 |

### 4.2 Copilot交互场景

**场景1: Assignment建议查询**
```
User: "Who should handle INC0012345?"
Copilot: [识别intent] → 调用Now Assist
Now Assist: [查询incident] → 获取CI和KB信息
Now Assist: [调用Azure OpenAI] → 生成推荐
Copilot: "Based on the KB article KB0012345, this SAP server issue 
          should be assigned to the SAP Team. 
          Confidence: High
          Would you like me to update the assignment?"
```

**场景2: 历史案例查询**
```
User: "Have we seen this issue before?"
Copilot: [搜索similar incidents] → 返回历史案例
Copilot: "Found 3 similar incidents in the past 30 days. 
          Resolution: Restart SAP service."
```

---

## 5. 实施路线图

### 5.1 阶段划分

| 阶段 | 时间 | 交付物 | 负责方 |
|------|------|--------|--------|
| **Phase 1** | Week 1-2 | 基础配置：CI-KB关联、Assignment规则 | @shirmpclaw |
| **Phase 2** | Week 3-4 | Azure OpenAI集成、Script Include开发 | @shirmpclaw |
| **Phase 3** | Week 5-6 | P1通知工作流、On-call schedule集成 | @shirmpclaw |
| **Phase 4** | Week 7-8 | Copilot集成、Virtual Agent配置 | @shirmpclaw |
| **Phase 5** | Week 9-10 | 测试优化、培训、上线 | 联合 |

### 5.2 依赖关系

```
[CI数据清理] ──────┐
                  ▼
[KB标准化] ────▶ [AI Routing Engine] ────▶ [Copilot Integration]
                  ▲                          ▲
[Azure OpenAI] ──┘                          │
                                             │
[P1 Notification] ──────────────────────────┘
```

---

## 6. 风险评估与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| AI推荐不准确 | 高 | 保留人工覆盖机制，设置confidence阈值 |
| Azure OpenAI延迟 | 中 | 异步处理，设置timeout，fallback到静态规则 |
| P1通知失败 | 高 | 多渠道冗余(SMS+Email+Teams) |
| 数据隐私 | 高 | PII脱敏，限制AI访问范围 |

---

## 7. 附录

### 附录A: 需要的ServiceNow插件
- Virtual Agent
- Now Assist
- Conversational Integration with Microsoft Teams
- Integration Hub (for P1 notifications)

### 附录B: Azure资源需求
- Azure OpenAI Service (GPT-4/GPT-4o)
- Azure AI Search (for RAG indexing)
- (可选) Azure Functions (for webhook处理)

---

*文档生成时间: 2026-03-08*
*版本: v1.0*
*作者: 富贵虾 (AI Architect) + @shirmpclaw (Implementation)*
