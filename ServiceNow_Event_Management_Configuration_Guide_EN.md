# ServiceNow Event Management Detailed Configuration Guide
## Complete Implementation Handbook from Installation to Production

---

## 1. Event Management Component Architecture

### 1.1 Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Event Management Architecture             │
├─────────────────────────────────────────────────────────────┤
│  Event Collection → Event Processing → Alert Management → Response Execution │
├─────────────────────────────────────────────────────────────┤
│  Connectors       Event Rules        Alert Rules        Remediation      │
│  Listeners        Filters            Correlation        Notifications    │
│  APIs             Transform          Aggregation        Tickets          │
│  Webhooks         Enrichment         Prioritization     Automation       │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Data Flow

```
External Monitoring Tools
     ↓
Event Collectors (Connector/Listener/API)
     ↓
Event Standardization (Event Mapping)
     ↓
Event Filtering (Filter)
     ↓
Event Rule Processing (Event Rule)
     ↓
Alert Creation/Update (Alert)
     ↓
Alert Correlation & Grouping (Correlation)
     ↓
Service Impact Analysis (Impact Analysis)
     ↓
Response Execution (Remediation/Notification)
```

---

## 2. Detailed Configuration Steps

### 2.1 Initial Setup

#### Step 1: Enable Event Management
```
Path: System Definition > Plugins
Search: Event Management
Action: Activate
Wait: Installation complete (5-10 minutes)
```

#### Step 2: Run Guided Setup
```
Path: Event Management > Guided Setup
Or: All > Guided Setup > Event Management

Task Checklist:
□ Install Event Management application
□ Configure roles and permissions
□ Set up event sources
□ Configure event rules
□ Set up alert management
□ Configure service mapping
```

---

### 2.2 Event Source Configuration

#### 2.2.1 Connector Types

| Type | Description | Use Case |
|------|-------------|----------|
| **REST API** | Receive events via API | Custom monitoring tools |
| **SNMP Trap** | Receive SNMP traps | Network device monitoring |
| **Syslog** | Receive system logs | Server/Application logs |
| **Webhook** | HTTP callbacks | Cloud service integration |
| **Native Connector** | Native integration | ServiceNow certified tools |

#### 2.2.2 Configure REST API Event Source

```
Path: Event Management > Event Sources > REST

Configuration:
- Name: Custom Monitoring API
- Endpoint: /api/now/table/em_event
- Authentication: Basic OAuth
- API Key: [Generate]

Sample Request:
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

#### 2.2.3 Configure SNMP Trap Listener

```
Path: Event Management > Event Sources > SNMP

Configuration:
- Name: Network Device Traps
- Port: 162
- Community String: [Configure]
- MIB Mapping: Import MIB files
- OID to Event Mapping:
  1.3.6.1.4.1.9.9.43.2.0.1 → Interface Down
  1.3.6.1.4.1.9.9.43.2.0.2 → Interface Up
```

---

### 2.3 Event Rule Configuration

#### 2.3.1 Event Rule Types

| Rule Type | Function | Example |
|-----------|----------|---------|
| **Transform** | Transform event fields | Modify severity value |
| **Filter** | Filter events | Drop test environment events |
| **Enrich** | Enrich event information | Add CMDB attributes |
| **Correlate** | Correlate events | Merge duplicate events |
| **Alert** | Create/Update alerts | Generate Incident |

#### 2.3.2 Create Event Rule

```
Path: Event Management > Event Rules

Rule Configuration Example:

Name: Critical CPU Alert
Order: 100
Filter Conditions:
  metric_name = cpu_usage
  AND severity = critical
  AND value > 90

Actions:
  1. Transform:
     - description = "High CPU on ${node}: ${value}%"
  
  2. Enrich:
     - Query node owner from CMDB
     - Add owner to event
  
  3. Create Alert:
     - severity: 1-Critical
     - category: Hardware
     - assignment_group: [Dynamic lookup]
```

#### 2.3.3 Event Filtering Best Practices

```javascript
// Filter condition examples

// 1. Drop events during maintenance windows
source != 'maintenance_tool'
AND (maintenance_window IS EMPTY OR maintenance_window.active = false)

// 2. Filter low priority test events
severity IN (critical, high, medium)
AND environment != 'test'

// 3. Deduplication conditions
source = previous.source
AND node = previous.node
AND metric_name = previous.metric_name
AND ABS(time - previous.time) < 300 seconds
```

---

### 2.4 Alert Management Configuration

#### 2.4.1 Alert Lifecycle

```
New → Acknowledged → In Progress → Resolved → Closed
  ↓         ↓              ↓            ↓         ↓
Notify    Stop escalation Update status Record solution Archive
```

#### 2.4.2 Alert Rule Configuration

```
Path: Event Management > Alert Rules

Rule 1: Auto-acknowledge known issues
Condition:
  description CONTAINS "scheduled maintenance"
Action:
  - Acknowledge alert
  - Set state: Acknowledged
  - Add note: "Known maintenance window"

Rule 2: Auto-create Incident
Condition:
  severity = 1-Critical
  AND service IN [production_services]
Action:
  - Create Incident
  - Priority: 1-Critical
  - Assignment Group: [from service]
  - Short Description: ${alert.description}

Rule 3: Escalation policy
Condition:
  age > 30 minutes
  AND acknowledged = false
Action:
  - Escalate to manager
  - Send SMS notification
  - Update priority to Critical
```

#### 2.4.3 Alert Correlation Configuration

```
Path: Event Management > Alert Correlation

Correlation Rule 1: Time window correlation
Time window: 5 minutes
Condition:
  same node
  AND similar description (80% match)
Action:
  - Create alert group
  - Set primary alert

Correlation Rule 2: Topology correlation
Condition:
  affected CI in same service
  OR CI has dependency relationship
Action:
  - Group by service
  - Identify root cause CI

Correlation Rule 3: ML intelligent correlation (Yokohama+)
Enable: Machine Learning Correlation
Training data: 90 days historical alerts
Minimum confidence: 0.75
```

---

### 2.5 Service Mapping Configuration

#### 2.5.1 Service Definition

```
Path: Service Mapping > Services

Service Definition Example:

Name: Online Banking System
Criticality: Critical
SLA: 99.9% uptime

Included CIs:
- Web Servers (3 nodes)
- Application Servers (2 nodes)
- Database Primary
- Database Replica
- Load Balancer
- CDN
```

#### 2.5.2 Impact Rules

```
Path: Event Management > Impact Rules

Rule: Database failure impact
Condition:
  CI type = Database
  AND alert severity = Critical
Impact:
  - Service health: Degraded (if replica available)
  - Service health: Down (if primary only)
  - Business impact: High
  - Notify: Service Owner, VP Engineering
```

---

## 3. Advanced Configuration

### 3.1 Machine Learning Configuration (Yokohama+)

#### 3.1.1 Enable ML Alert Correlation

```
Path: Event Management > Machine Learning > Settings

Configuration:
- Enable ML Correlation: true
- Training Schedule: Weekly
- Minimum Training Data: 1000 alerts
- Confidence Threshold: 0.75
- Auto-apply Suggestions: false (manual review)
```

#### 3.1.2 Model Training

```
Path: Event Management > Machine Learning > Model Training

Steps:
1. Select training data range (recommend 90 days)
2. Select CI categories to train
3. Start training job
4. Wait for training complete (2-4 hours)
5. Review model performance metrics
6. Deploy model to production
```

#### 3.1.3 ML Results Review

```
Path: Event Management > Machine Learning > Suggestions

Review Items:
□ Are suggested alert groupings reasonable?
□ Are confidence scores accurate?
□ Is false positive rate acceptable?
□ Any new correlation patterns emerging?

Actions:
- Accept: Apply to production rules
- Reject: Do not adopt
- Modify: Adjust and apply
```

---

### 3.2 Automated Remediation Configuration

#### 3.2.1 Remediation Action Types

| Type | Description | Example |
|------|-------------|---------|
| **Workflow** | Execute workflow | Auto-restart service |
| **Script** | Run script | Clean log files |
| **API Call** | Call external API | Scale cloud resources |
| **Notification** | Send notification | SMS/Email |

#### 3.2.2 Create Remediation Rule

```
Path: Event Management > Remediation Rules

Rule: Auto-restart service
Condition:
  metric_name = service_status
  AND value = stopped
  AND service IN [auto_restart_services]
  AND previous_remediation_failed = false

Action:
  1. Execute Workflow: "Restart Service"
     - Input: ${node}, ${service_name}
  
  2. Wait 2 minutes
  
  3. Verify service status
     - If success: Resolve alert
     - If failure: Escalate to L2

Safety Controls:
- Maximum execution count: 3
- Execution time window: 8:00-22:00
- Requires approval: false (low risk operation)
```

---

### 3.3 Dashboard Configuration

#### 3.3.1 Key Metrics Dashboard

```
Path: Event Management > Overview

Components:
1. Real-time Alert Counter
   - Critical: [Red large number]
   - High: [Orange number]
   - Medium: [Yellow number]

2. Service Health
   - Green: Normal
   - Yellow: Degraded
   - Red: Outage

3. Alert Trend Chart
   - Time range: 24 hours
   - Grouped by severity

4. Top 10 Alert Sources
   - Sorted by count
   - Drill-down available

5. Team Workload
   - Pending alerts/person
   - Average resolution time
```

#### 3.3.2 Custom Dashboard

```
Path: System UI > Dashboards

Creation Steps:
1. Create New Dashboard: "Event Management Operations"
2. Add Widgets:
   - Alert List (filtered by assignment_group)
   - Service Health Map
   - Event Volume Chart
   - MTTR Trend
3. Set refresh frequency: 30 seconds
4. Share with operations team
```

---

## 4. API Reference

### 4.1 Send Event API

```bash
# Create Event
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

### 4.2 Query Alerts API

```bash
# Get active alerts
GET /api/now/table/em_alert?sysparm_query=state!=Resolved^ORDERBYDESCseverity

# Get specific service alerts
GET /api/now/table/em_alert?sysparm_query=service.name=Online Banking^state!=Resolved
```

### 4.3 Update Alert API

```bash
# Acknowledge alert
PATCH /api/now/table/em_alert/{sys_id}
{
  "state": "Acknowledged",
  "acknowledged_by": "[user_id]",
  "work_notes": "Investigating"
}

# Resolve alert
PATCH /api/now/table/em_alert/{sys_id}
{
  "state": "Resolved",
  "resolution_code": "Fixed",
  "resolution_notes": "Restarted service"
}
```

---

## 5. Troubleshooting

### 5.1 Events Not Processing

**Troubleshooting Steps:**
1. Check Event Source status
2. View Event Log: Event Management > Logs
3. Verify Event Rule order and conditions
4. Check Transform/Filter script errors

### 5.2 Alerts Not Created

**Troubleshooting Steps:**
1. Confirm Event Rule has Create Alert action
2. Check Alert Rule filter conditions
3. View Alert Creation Log
4. Verify permission settings

### 5.3 Correlation Inaccurate

**Optimization Suggestions:**
1. Increase training data volume
2. Adjust correlation rule weights
3. Manually mark correct/incorrect correlations
4. Retrain ML model

---

## 6. Performance Optimization

### 6.1 Event Processing Optimization

| Optimization | Recommendation |
|--------------|----------------|
| Event Filtering | Filter early to reduce downstream processing |
| Rule Order | Place high-frequency rules first |
| Batch Processing | Enable event batch processing mode |
| Index Optimization | Ensure key fields are indexed |

### 6.2 Storage Optimization

```
Data Retention Policy:
- Raw Events: 30 days
- Alert Records: 90 days
- Correlation History: 180 days
- ML Training Data: 365 days

Auto-cleanup:
Path: Event Management > Data Retention
```

---

## 7. Reference Links

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

*Document Version: 2026.03*  
*Applicable Version: ServiceNow Yokohama+*  
*Author: Kimi Claw*
