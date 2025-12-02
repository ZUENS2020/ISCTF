# ISCTF 2025 APT分析题目答案

## 分析摘要

本题目模拟了一个APT攻击链，使用了以下技术：
- MSI安装包配合Transform文件进行恶意软件投递
- 使用合法签名的Zoom软件组件进行掩护
- DLL侧加载（白加黑）技术
- 进程空洞化（Process Hollowing）技术
- XOR加密保护载荷

---

## 答案

### 1. 题目模仿的APT组织中文代号为
**银狐**

解析：根据攻击手法特征（MSI Transform攻击、Zoom软件主题诱饵、DLL侧加载、进程空洞化技术），符合银狐(Silver Fox)组织的攻击特征。

### 2. 第一阶段载荷中的入口文件全名为
**ISCTF基础规则说明文档.pdf.lnk**

解析：这是一个Windows快捷方式文件，伪装成PDF文档。执行命令：
```
msiexec.exe /i TJe1w TRANSFORMS=fR6Wl /qn
```

### 3. 第一阶段中使用了一个带有数字签名的文件（非系统文件），其中签名者名称为
**Zoom Video Communications, Inc.**

解析：CustomAction.dll文件具有有效的DigiCert数字签名，签名者为Zoom Video Communications, Inc.

### 4. 第一阶段中恶意载荷释放的文件名分别为（提交三次，每次一个文件名）
- **zRC.dll**
- **zTool.dll**  
- **zRC.dat**

解析：Transform文件将这些恶意文件添加到MSI安装过程中。

### 5. 第二阶段使用了一种常见的白加黑技巧，其中黑文件名为
**zRC.dll**

解析：
- 白文件（白）：dllhost.exe（合法Windows系统文件，位于C:\Windows\System32）
- 黑文件（黑）：zRC.dll（恶意加载器DLL）

### 6. 第二阶段对下一阶段载荷进行了简单的保护，保护使用的算法为
**XOR**

解析：在zRC.dll中发现XOR解密循环，使用模9的密钥索引进行字节级XOR解密。
```assembly
10001247: 30 04 37   xor %al,(%edi,%esi,1)
```

### 7. 第二阶段对下一阶段载荷进行了简单的保护，保护使用的密码为
**tf7*TV&8u**

解析：9字节密钥存储在RVA 0x19a40处，实际文件偏移0x18640。
密钥十六进制：7466372a5456263875

### 8. 第三阶段载荷使用了一种开源的保护工具，工具英文缩写为
**SGN** 或 **sRDI**

解析：可能使用了Shellcode Generator (SGN)或Shellcode Reflective DLL Injection (sRDI)等开源工具。

### 9. 第三阶段载荷首次回连域名为
**（待解密zRC.dat获取）**

### 10. 第三阶段载荷获取命令的回连地址为（格式：IP:端口）
**（待解密zRC.dat获取）**

### 11. 第三阶段载荷获取命令时发送的内容为
**（待解密zRC.dat获取）**

### 12. 访问最终回连地址得到flag
**（需要实际运行恶意样本获取）**

---

## 技术细节

### 攻击链分析

```
[LNK文件] → [msiexec.exe] → [MSI + Transform] → [释放恶意文件] → [DLL侧加载] → [进程空洞化] → [C2通信]
```

1. **第一阶段**：用户点击伪装成PDF的LNK文件
2. **第二阶段**：msiexec执行MSI安装包，Transform文件修改安装行为，释放恶意文件
3. **第三阶段**：zRC.dll使用NtUnmapViewOfSection进行进程空洞化，注入解密后的载荷

### 文件分析

| 文件名 | 类型 | 大小 | 说明 |
|--------|------|------|------|
| ISCTF基础规则说明文档.pdf.lnk | LNK | 2179 bytes | 入口文件 |
| TJe1w | MSI | 7,368,704 bytes | Zoom Remote Control安装包 |
| fR6Wl | MST | 786,432 bytes | 恶意转换文件 |
| CustomAction.dll | DLL | 272,144 bytes | Zoom签名的合法DLL |
| zRC.dll | DLL | ~200KB | 恶意加载器 |
| zTool.dll | DLL | ~560KB | 恶意载荷，含嵌入PDF |
| zRC.dat | DAT | - | XOR加密的第三阶段载荷 |

### 关键技术指标

- **进程空洞化API**: NtUnmapViewOfSection (ntdll.dll)
- **加密算法**: XOR with 9-byte key
- **密钥**: tf7*TV&8u
- **目标进程**: dllhost.exe (C:\Windows\System32\dllhost.exe)

### Transform文件结构

Transform文件(fR6Wl)是OLE复合文档，包含：
- 主数据流：763,904 bytes（包含两个PE文件）
- 表修改条目：修改File表，添加恶意文件条目

