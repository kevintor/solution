# ServiceNow MID Server SNMP Trap 接收配置指南

## 目录

1. [架构概览](#架构概览)
2. [MID Server 层配置](#mid-server-层配置)
3. [ServiceNow 平台层配置](#servicenow-平台层配置)
4. [高级配置](#高级配置)
5. [验证与故障排查](#验证与故障排查)

---

## 架构概览

```
┌─────────────────┐      UDP 162       ┌──────────────────┐      HTTPS      ┌──────────────┐
│  Network Device │ ─────────────────▶ │  MID Server      │ ──────────────▶ │ ServiceNow   │
│  (Switch/Router)│    SNMP v1/v2c/v3  │  SNMP Trapd      │   REST API      │ Event Mgmt   │
│                 │    or v3           │  + Transformer   │   (ECC Queue)   │              │
└─────────────────┘                    └──────────────────┘                 └──────────────┘
```

---

## MID Server 层配置

### 1. 安装 SNMP 组件

MID Server 本身没有内置 SNMP trap 接收器，需要额外配置。

#### Linux (RHEL/CentOS/Ubuntu)

```bash
# RHEL/CentOS
sudo yum install net-snmp net-snmp-utils

# Ubuntu/Debian
sudo apt-get install snmpd snmp
```

#### 配置 snmptrapd 接收器

编辑 `/etc/snmp/snmptrapd.conf`：

```conf
# 启用所有日志
disableAuthorization yes

# 接收所有 community
authCommunity log,execute,net public

# 定义 trap 处理脚本
traphandle default /opt/snow/snmp/trap_handler.sh

# 或发送到特定 OID 处理器
traphandle .1.3.6.1.4.1.9.0.1 /opt/snow/snmp/cisco_handler.sh
```

启动服务：

```bash
sudo systemctl enable snmptrapd
sudo systemctl start snmptrapd
sudo netstat -tulnp | grep 162
```

#### Windows

```powershell
# 通过 Server Manager 安装 SNMP Service
# 或使用 PowerShell
Add-WindowsFeature SNMP-Service
```

---

### 2. 自定义 Trap Handler 脚本

创建 `/opt/snow/snmp/trap_handler.sh`：

```bash
#!/bin/bash
# SNMP Trap 处理器 - 转发到 ServiceNow MID Server

# 读取 trap 数据
read HOSTNAME
read IP
read VARBINDS

# 提取关键字段
TRAP_OID=$(echo "$VARBINDS" | grep -oP 'OID: \K\S+')
SEVERITY=$(echo "$VARBINDS" | grep -oP 'severity=\K\S+' || echo "3")
MESSAGE=$(echo "$VARBINDS" | grep -oP 'message=\K.*' || echo "Unknown event")

# 生成 JSON payload
JSON=$(cat <<EOF
{
  "source": "SNMP Trap",
  "node": "$HOSTNAME",
  "resource": "$IP",
  "type": "$TRAP_OID",
  "severity": $SEVERITY,
  "description": "$MESSAGE",
  "additional_info": "$VARBINDS",
  "time_of_event": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
)

# 发送到 MID Server 本地 API
curl -X POST \
  -H "Content-Type: application/json" \
  -d "$JSON" \
  http://localhost:8080/api/mid/snmpevent \
  2>/dev/null

# 同时写入本地日志
echo "$(date): $JSON" >> /var/log/snow/snmp_traps.log
```

设置权限：

```bash
sudo chmod +x /opt/snow/snmp/trap_handler.sh
sudo mkdir -p /var/log/snow
```

---

## ServiceNow 平台层配置

### 1. 创建 Event Source

**路径：** Event Management → Event Sources → New

| 字段 | 值 |
|------|-----|
| **Name** | SNMP Trap Source |
| **Type** | SNMP Trap |
| **MID Server** | 选择你的 MID Server |
| **Collection method** | Listener (UDP 162) |
| **Community String** | public (或自定义) |
| **SNMP Version** | v2c 或 v3 |

### 2. OID 到 Event 字段映射

**路径：** Event Management → SNMP → OID Mapping

#### 示例 OID 映射表

| OID | Field Name | Target Event Field | Transform |
|-----|-----------|-------------------|-----------|
| 1.3.6.1.4.1.1234.1.1 | eventType | type | - |
| 1.3.6.1.4.1.1234.1.2 | severity | severity | map(1=Critical,2=Major,3=Minor,4=Warning,5=Clear) |
| 1.3.6.1.4.1.1234.1.3 | message | description | - |
| 1.3.6.1.4.1.1234.1.4 | host | node | - |

#### 标准 Trap OID

| Trap | OID | Description |
|------|-----|-------------|
| coldStart | 1.3.6.1.6.3.1.1.5.1 | 设备冷启动 |
| warmStart | 1.3.6.1.6.3.1.1.5.2 | 设备热启动 |
| linkDown | 1.3.6.1.6.3.1.1.5.3 | 链路断开 |
| linkUp | 1.3.6.1.6.3.1.1.5.4 | 链路恢复 |
| authenticationFailure | 1.3.6.1.6.3.1.1.5.5 | 认证失败 |

---

## 高级配置

### SNMP v3 安全配置

编辑 `snmptrapd.conf`：

```conf
# 创建 v3 用户
createUser snmpv3user SHA "authpass" AES "privpass"

# 允许该用户接收 trap
authUser log snmpv3user
```

**ServiceNow 端配置：**
- Security Level: AuthPriv
- Username: snmpv3user
- Authentication Protocol: SHA
- Privacy Protocol: AES

### Python 中间件（高性能处理）

创建 `/opt/snow/snmp/trap_processor.py`：

```python
#!/usr/bin/env python3
import socket
import json
import requests
from concurrent.futures import ThreadPoolExecutor

MID_SERVER_API = "http://localhost:8080/api/mid/snmpevent"
WORKER_THREADS = 10

def process_trap(trap_data):
    try:
        event = {
            "source": "SNMP",
            "type": extract_oid(trap_data),
            "severity": extract_severity(trap_data),
            "node": extract_source_ip(trap_data),
            "description": extract_message(trap_data),
            "time_of_event": datetime.utcnow().isoformat()
        }
        
        resp = requests.post(MID_SERVER_API, json=event, timeout=5)
        return resp.status_code == 200
        
    except Exception as e:
        logger.error(f"Failed: {e}")
        return False

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 162))
    
    with ThreadPoolExecutor(max_workers=WORKER_THREADS) as executor:
        while True:
            data, addr = sock.recvfrom(65535)
            executor.submit(process_trap, data)

if __name__ == "__main__":
    main()
```

---

## 验证与故障排查

### 测试发送 Trap

```bash
snmptrap -v 2c -c public <mid-server-ip>:162 \
  "" 1.3.6.1.4.1.1234.0.1 \
  1.3.6.1.4.1.1234.1.1 s "Test Event" \
  1.3.6.1.4.1.1234.1.2 i 3 \
  1.3.6.1.4.1.1234.1.3 s "Test SNMP trap"
```

### 检查日志

```bash
# MID Server 日志
tail -f /var/log/snow/mid_server.log

# SNMP 接收日志
tail -f /var/log/snow/snmp_traps.log

# 系统日志
tail -f /var/log/messages | grep snmptrapd
```

### 常用排查命令

```bash
# 检查端口监听
sudo netstat -tulnp | grep :162
sudo ss -tulnp | grep :162

# 检查防火墙
sudo iptables -L -n | grep 162

# 抓包验证
sudo tcpdump -i any port 162 -n

# 检查 MID Server 状态
curl http://localhost:8080/api/mid/health
```

---

## 完整数据流

```
1. Network Device 发送 SNMP Trap ──UDP 162──▶
2. MID Server snmptrapd 接收 ──▶
3. traphandler.sh 处理 ──▶
4. 转换为 JSON ──HTTP──▶
5. MID Server ECC Queue ──HTTPS──▶
6. ServiceNow Event Management
7. Event Rules 处理 ──▶
8. Alert/Incident/Remediation
```

---

## 关键要点总结

1. **MID Server 不原生支持 SNMP**，需要额外配置 snmptrapd
2. **需要自定义脚本**将 SNMP 转换为 ServiceNow 可识别的 JSON 格式
3. **OID 映射**需要在 ServiceNow 平台手动配置
4. **生产环境**建议使用 SNMP v3 认证 + 加密
5. **高并发场景**建议使用 Python 中间件替代 shell 脚本

---

*文档生成时间：2026-03-14*
