# 流程图图片生成 Prompts for Nano Banana

## 整体风格定义
- **风格**: 企业级技术架构图风格，扁平化设计，蓝色系主色调
- **配色**: 深蓝色(#1e3a5f)主色，浅蓝(#4a90d9)辅助，橙色(#f5a623)高亮，白色背景
- **元素**: 圆角矩形代表组件，箭头代表数据流，虚线代表外部集成
- **字体**: 清晰的无衬线字体，中英文混排

---

## Prompt 1: 整体系统架构图

**English Prompt:**
```
Enterprise architecture diagram for ServiceNow + Microsoft Copilot AI Incident Routing System.

LAYER 1 (Top) - Presentation Layer:
- Three rectangular boxes side by side: "ServiceNow Incident Form" (left), "Microsoft Teams Copilot" (center), "Virtual Agent / Now Assist" (right)
- Icons: Document icon, Teams logo, Chatbot icon

LAYER 2 (Middle) - Business Logic Layer:
- Four connected boxes: "Business Rule", "AI Routing Engine", "Notification Engine", "Flow Designer"
- Arrows showing bidirectional flow

LAYER 3 - AI Service Layer:
- Large box labeled "Microsoft Azure OpenAI Service"
- Inside: "GPT-4/GPT-4o", "RAG Engine", "Embeddings"
- Cloud icon background

LAYER 4 (Bottom) - Data Layer:
- Four database icons: "Incident Table", "KB Articles", "CMDB (CI)", "AI Search Index"

CONNECTIONS:
- Solid arrows between layers showing data flow
- Dotted lines for API connections
- Color code: Blue for normal flow, Orange for AI processing, Red for P1 alerts

Style: Flat design, professional, clean, corporate tech style, white background, blue primary color (#1e3a5f), light blue secondary (#4a90d9), orange accents (#f5a623)

Resolution: 4K, high detail, suitable for PDF documentation
```

---

## Prompt 2: Incident Creation 数据流图

**English Prompt:**
```
Data flow diagram showing Incident Creation to Assignment process.

VERTICAL FLOW (Top to Bottom):
1. [Circle] "User creates Incident"
   ↓ Arrow
2. [Diamond] "Business Rule Check"
   ↓ Arrow (Yes path)
3. [Rectangle] "KB Retrieval (RAG)"
   - Sub-icon: Search/magnifying glass
   ↓ Arrow
4. [Rectangle] "AI Analysis (Azure OpenAI)"
   - Sub-icon: Brain/AI chip
   ↓ Arrow
5. [Rectangle] "Parse Response"
   ↓ Arrow
6. [Rectangle] "Update Incident"
   ↓ Arrow
7. [Diamond] "Priority = P1?"
   ├─ Yes → [Rectangle] "P1 Notification Workflow" → [Icons] SMS/Email/Teams
   └─ No → [Circle] "End"

DECISION POINTS:
- Use diamond shapes for decisions
- Label Yes/No paths clearly
- Highlight P1 path in RED color

ANNOTATIONS:
- Step numbers [1] through [7] in circles
- Brief description next to each box
- Connection arrows with arrowheads

Style: Technical flowchart, clean lines, white background, blue boxes, red alert path, professional enterprise documentation style

Resolution: 2K, clear text labels
```

---

## Prompt 3: Copilot 交互流程图

**English Prompt:**
```
Sequence diagram showing Copilot interaction flow.

LEFT SIDE - User:
- Person icon labeled "Support Engineer"
- Speech bubble: "Who should handle this incident?"

CENTER - Microsoft Teams:
- Teams interface mockup with chat window
- Message bubbles showing conversation flow

RIGHT SIDE - Backend Systems:
Stack of boxes from top to bottom:
1. "Copilot Intent Recognition"
2. "Now Assist / Virtual Agent"
3. "ServiceNow Platform"
   - Sub-boxes: "Incident Table", "KB Articles", "CMDB"
4. "Azure OpenAI"
   - Brain icon

FLOW ARROWS:
1. User → Copilot: Natural language query
2. Copilot → Now Assist: Intent + Context
3. Now Assist → ServiceNow: Fetch incident data
4. ServiceNow → Azure OpenAI: Incident + KB context
5. Azure OpenAI → Now Assist: Recommendation
6. Now Assist → Copilot: Formatted response
7. Copilot → User: Display recommendation

RESPONSE CARD MOCKUP:
Show a card in Teams chat:
- Title: "Assignment Recommendation"
- Assignment Group: SAP Team
- Confidence: High (green badge)
- Reasoning: Based on KB0012345...
- Buttons: [Apply] [View Details]

Style: Modern UI mockup style, Teams purple theme, clean interface, conversational flow visualization, professional documentation

Resolution: 2K, readable UI text
```

---

## Prompt 4: RAG (检索增强生成) 流程图

**English Prompt:**
```
RAG (Retrieval-Augmented Generation) process flow diagram.

TITLE: "RAG-based KB Knowledge Retrieval"

CENTRAL COMPONENT:
- Large circular node in center: "Azure OpenAI LLM"
- Glowing effect, brain/neural network icon

LEFT SIDE - Retrieval Phase:
1. [Box] "User Query / Incident Details"
   ↓
2. [Cylinder] "AI Search Index"
   - Database icon
   ↓
3. [Stack of documents] "Relevant KB Articles Retrieved"
   - Show 3 document icons with titles

ARROW: Retrieved docs → Central LLM

RIGHT SIDE - Generation Phase:
1. [Central LLM receives input]
   ↓
2. [Box] "Contextual Response Generated"
   - Contains: Assignment recommendation
   - Confidence score
   - Explanation text
   ↓
3. [Box] "Output to ServiceNow"

KNOWLEDGE BASE ICONS:
- Floating document icons around AI Search
- Labels: KB0012345, KB0012346, etc.
- Category tags: "Escalation", "Network", "Database"

COLOR CODING:
- Blue: Data retrieval path
- Green: AI processing
- Purple: Knowledge base
- Orange: Final output

ANNOTATIONS:
- Callouts explaining each phase
- Icons: Magnifying glass (retrieval), Lightbulb (generation)

Style: Modern AI diagram style, isometric or flat design, tech gradient backgrounds, floating elements, professional but visually engaging

Resolution: 2K, suitable for technical presentation
```

---

## Prompt 5: P1 Notification 工作流图

**English Prompt:**
```
P1 Critical Incident Notification Workflow diagram.

TRIGGER (Top):
- [Red alert icon] "P1 Incident Created"
- Lightning bolt symbol

PARALLEL NOTIFICATION PATHS (Branching below):

PATH 1 - On-Call Engineer (LEFT):
├─ [Box] "Get On-Call from Schedule"
│  └─ Icon: Calendar/Schedule
├─ [Box] "Send SMS"
│  └─ Icon: Phone/SMS
└─ [Box] "Send Push Notification"
   └─ Icon: Mobile phone

PATH 2 - Management (CENTER):
├─ [Box] "Get Manager DL"
├─ [Box] "Send Email"
│  └─ Icon: Envelope
└─ [Box] "Create Teams Meeting"
   └─ Icon: Teams logo

PATH 3 - Stakeholders (RIGHT):
├─ [Box] "Post to Status Page"
│  └─ Icon: Web page
├─ [Box] "Send to Slack #incidents"
│  └─ Icon: Slack logo
└─ [Box] "Escalation Timer (15min)"
   └─ Icon: Clock

MERGE POINT (Bottom):
- [Box] "Update Incident Work Notes"
- [Box] "Create War Room Bridge"

ESCALATION INDICATOR:
- Dotted red line showing escalation path if no response
- "If no acknowledgment in 15min → Escalate to Director"

COLOR SCHEME:
- Red: P1 alert and urgency
- Orange: Escalation paths
- Blue: Standard notifications
- Green: Successful delivery

ICONS: Real notification icons (Teams, Slack, Email, SMS)

Style: Emergency response flowchart, urgent visual style, clear parallel paths, professional incident management documentation

Resolution: 2K, high contrast for visibility
```

---

## Prompt 6: 技术组件关系图

**English Prompt:**
```
Technical component relationship diagram for ServiceNow Copilot integration.

HUB-AND-SPOKE Layout:

CENTER:
- [Large hexagon] "ServiceNow Now Platform"
- ServiceNow logo in center

SURROUNDING COMPONENTS (connected by lines):

TOP:
- [Box] "Virtual Agent"
  └─ Connected to: NLU Workbench, Topics

TOP-RIGHT:
- [Box] "Now Assist"
  └─ Connected to: Generative AI Controller

RIGHT:
- [Cloud icon] "Azure OpenAI"
  └─ Sub-labels: GPT-4, Embeddings, RAG

BOTTOM-RIGHT:
- [Box] "Microsoft Teams"
  └─ Teams logo, "Custom Engine Agent"

BOTTOM:
- [Database icon] "Knowledge Base"
  └─ Multiple document icons

BOTTOM-LEFT:
- [Box] "CMDB / CI"
  └─ Server/Configuration icons

LEFT:
- [Box] "Integration Hub"
  └─ Connection lines to external systems

TOP-LEFT:
- [Box] "Notification Engine"
  └─ Email, SMS, Teams icons

CONNECTION LINES:
- Solid lines: Direct integration
- Dashed lines: Data flow
- Color-coded by integration type

LEGEND:
- Blue: Core platform
- Purple: AI/ML components
- Green: Data sources
- Orange: External integrations

Style: Enterprise integration architecture, hub-and-spoke design, clean connections, professional network diagram, white background

Resolution: 4K, suitable for executive presentation
```

---

## 汇总清单

| Prompt | 文件名建议 | 用途 |
|--------|-----------|------|
| Prompt 1 | `architecture-overview.png` | 文档第2章 |
| Prompt 2 | `incident-flow-diagram.png` | 文档第2.2节 |
| Prompt 3 | `copilot-interaction-flow.png` | 文档第4章 |
| Prompt 4 | `rag-process-flow.png` | 文档第3.2节 |
| Prompt 5 | `p1-notification-workflow.png` | 文档第3.3节 |
| Prompt 6 | `component-relationship.png` | 文档附录 |

**风格一致性检查清单**:
- [ ] 所有图片使用相同的蓝色系配色 (#1e3a5f, #4a90d9)
- [ ] 相同的圆角矩形组件风格
- [ ] 统一的箭头样式
- [ ] 相同的字体风格
- [ ] 白色或浅灰色背景
