# ISCTF 2025 APT分析题目答案

## 分析报告

本题模拟了一个高级持续性威胁(APT)组织的攻击手法，通过分析附件中的恶意样本，回答以下问题:

---

### 问题1: 题目模仿的APT组织中文代号为
**答案: 银狐**

分析: 该攻击使用LNK诱饵文件作为入口、MSI安装包配合Transform修改进行载荷投递、利用Zoom软件进行DLL侧加载(白加黑)、使用SharePoint作为C2通信渠道。这些是"银狐"APT组织的典型攻击特征。

---

### 问题2: 第一阶段载荷中的入口文件全名为
**答案: ISCTF基础规则说明文档.pdf.lnk**

分析: 攻击入口是一个伪装成PDF文档的Windows快捷方式(.lnk)文件，诱导用户点击执行。LNK文件执行命令:
```
msiexec.exe /i TJe1w TRANSFORMS=fR6Wl /qn
```

---

### 问题3: 第一阶段中使用了一个带有数字签名的文件（非系统文件），其中签名者名称为
**答案: Zoom Video Communications, Inc.**

分析: TJe1w文件是一个合法的Zoom Remote Control MSI安装包，包含Zoom公司的数字签名。从MSI的DigitalSignature流中提取证书可以看到签名者信息。

---

### 问题4: 第一阶段中恶意载荷释放的文件名分别为
**答案1: zRC.dll**
**答案2: zRC.dat** 
**答案3: ISCTF2025.pdf** (PDF诱饵文件，从资源中提取并释放)

分析: Transform文件(fR6Wl)修改MSI安装包:
- 安装恶意DLL (zRC.dll) 替代合法Zoom DLL
- 释放数据文件 (zRC.dat) 用于Stage 3
- 释放PDF诱饵文件并用ShellExecute打开

---

### 问题5: 第二阶段使用了一种常见的白加黑技巧，其中黑文件名为
**答案: zRC.dll**

分析: 白加黑(DLL Side-Loading)技巧:
- 白文件: Zoom合法程序(ZoomRemoteControl.exe等)
- 黑文件: zRC.dll (恶意DLL，导出GetZoomRCAppCore函数伪装成zRCAppCore.dll)

---

### 问题6: 第二阶段对下一阶段载荷进行了简单的保护，保护使用的算法为
**答案: XOR**

分析: zRC.dll中嵌入的SC资源(Stage 3 shellcode)使用XOR加密保护。

---

### 问题7: 第二阶段对下一阶段载荷进行了简单的保护，保护使用的密码为
**答案: tf7*TV&8u**

分析: XOR密钥为9字节循环密钥: `tf7*TV&8u`
验证: 使用此密钥解密SC资源后得到有效的MZ/PE文件头。

---

### 问题8: 第三阶段载荷使用了一种开源的保护工具，工具英文缩写为
**答案: UPX**

分析: 使用XOR密钥解密后的Stage 3是一个UPX压缩的PE可执行文件。使用`upx -d`可以成功解压。

---

### 问题9: 第三阶段载荷首次回连域名为
**答案: colonised-my.sharepoint.com**

分析: 从解压后的Stage 3二进制中提取的宽字符串显示首次回连使用SharePoint站点。
完整URL: `https://colonised-my.sharepoint.com/personal/f00001111_colonised_onmicrosoft_com/_layouts/52/download.aspx?share=EQsrTSD_4ehGvYTXbmU5zR0B0lk4L-x0r8yGztFlye2j9Q`

---

### 问题10: 第三阶段载荷获取命令的回连地址为（格式：IP:端口）
**答案: (需要从SharePoint下载的配置中获取)**

分析: 恶意程序首先从SharePoint下载配置文件，实际的命令控制服务器IP:端口可能在配置文件中动态获取。在静态分析的二进制中未找到硬编码的IP:端口。

---

### 问题11: 第三阶段载荷获取命令时发送的内容为
**答案: get_cmd**

分析: 在Stage 3二进制的.rdata段中发现字符串"get_cmd"，这是恶意程序向C2服务器请求命令时发送的内容。

---

### 问题12: 访问最终回连地址得到flag
**答案: (需要访问实际C2服务器获取)**

---

## 技术细节

### 攻击链概览
```
入口点 → Stage 1 → Stage 2 → Stage 3
   │         │          │          │
   │         │          │          └─ UPX压缩的RAT,使用SharePoint C2
   │         │          └─ DLL侧加载 + 进程注入(dllhost.exe)
   │         └─ MSI + Transform安装恶意DLL
   └─ LNK快捷方式诱饵
```

### 关键IOC
| 指标类型 | 值 |
|---------|-----|
| 入口文件 | ISCTF基础规则说明文档.pdf.lnk |
| 恶意DLL | zRC.dll |
| C2域名 | colonised-my.sharepoint.com |
| User-Agent | Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0 |
| 持久化 | 计划任务 ZoomUpdater (每小时执行) |
| XOR密钥 | tf7*TV&8u |
| 保护工具 | UPX |

### 文件哈希
(待补充)
