# 阿利维亚的传说 (The Legend of Alivia) - CTF Misc Challenge

## 题目概述 (Challenge Overview)

这是一道 CTF (Capture The Flag) 的 Misc 类型题目。题目包含一个压缩包，里面有关于"阿利维亚的传说"的故事文档和一张泰坦守护钥匙的图片。

**提示**: 你知道阿利维亚的传说吗？

## 题目结构 (Challenge Structure)

```
zip (压缩包)
└── 阿利维亚的传说/
    ├── TiTan.png        (4.3 MB - 泰坦守护三把钥匙的图片)
    └── 阿利维亚的传说.docx  (14.7 KB - 传说故事文档)
```

## 解题过程 (Solution Process)

### 第一步: 分析文档 - 发现 Flag1

打开 `阿利维亚的传说.docx` 文档，可以看到传说的故事：

> 在古老的阿利维亚传说中，
> 高蒂平原的深处暗藏着通往永生的大门，
> 那是神赐予人类的礼物。
> 然而，名为泰坦的巨兽笼罩了天空，
> 它贪婪的汲取生灵的一切，
> 篡夺了神的权柄，占据了神的馈赠。
> 将大门的钥匙分为**三**份，
> 并派遣了名为"命运"的恶魔驻守，
> 为的就是将人类永困于此间。
> ...
> 找回钥匙，打破循环。
> 
> （解出的每段flag后面加_,类似于flag1_flag2_flag3）

**关键发现**: 文档中有隐藏文字！

使用 Word 或解压 docx 文件查看 `word/document.xml`，找到被 `<w:vanish/>` 标记隐藏的文字：

```
谕言1:
V = Dortt
A = otuTa
N = NTsin
```

**解密方法**: 纵向读取每一列
- 第1列: D + o + N = "Don"
- 第2列: o + t + T = "otT"  
- 第3列: r + u + s = "rus"
- 第4列: t + T + i = "tTi"
- 第5列: t + a + n = "tan"

**结果**: `DoNotTrustTitan` (不要相信泰坦)

✅ **Flag1 = DoNotTrustTitan**

### 第二步: 分析图片 - 发现隐藏文件

`TiTan.png` 是一张 2730×1535 的 PNG 图片，显示一个石头巨人（泰坦）守护着三把发光的钥匙（蓝、红、绿）。

**关键发现**: PNG 文件末尾附加了一个 ZIP 文件！

```bash
# 使用 xxd 查看文件末尾 (从偏移量 0x421ff0 开始)
xxd TiTan.png | tail -n 50

# 或者直接查看 IEND 后的数据
xxd -s 0x421ff0 -l 100 TiTan.png
```

可以看到在 PNG 的 IEND 标记后面有 PK 签名（ZIP 文件头）：
- PNG IEND 位于偏移量 ~4333561
- ZIP 开始于偏移量 4333569

**提取隐藏的 ZIP**:
```bash
dd if=TiTan.png of=hidden.zip bs=1 skip=4333569
```

**ZIP 文件内容**:
- `flag3.txt` (40 字节) - 但是被密码保护！

### 第三步: 寻找 Flag2 和解锁 Flag3

Flag2 的位置可能在：
1. 图片的 LSB 隐写
2. 图片的 EXIF 信息
3. 文档的其他隐藏区域
4. 文件名或元数据中

Flag3 的密码可能是：
1. Flag2 本身
2. Flag1 和 Flag2 的组合
3. 故事中提到的关键词

**技术分析**:
- PNG 的 LSB (最低有效位) 分析未发现明显隐写信息
- 文档只有 "谕言1"，可能还有 "谕言2" 和 "谕言3" 隐藏在别处
- ZIP 使用传统 PKZIP 加密 (ZipCrypto)

## Flag 格式

根据文档提示，最终答案格式为：
```
ISCTF{flag1_flag2_flag3}
```

已知：
- Flag1 = `DoNotTrustTitan`

## 使用的工具 (Tools Used)

| 工具 | 用途 |
|------|------|
| `unzip -l` | 列出 ZIP 内容 |
| `xxd` / `hexdump` | 十六进制查看 |
| `strings` | 提取可见字符串 |
| `dd` | 提取隐藏文件 |
| Python `zipfile` | 处理 ZIP 文件 |
| Python `PIL/Pillow` | 图像分析 |
| `stegano` | LSB 隐写分析 |

## 命令参考 (Command Reference)

```bash
# 解压原始压缩包
unzip zip -d challenge/

# 查看 docx 中的隐藏文字 (解压后查看 XML)
unzip "阿利维亚的传说.docx" -d docx_content/
# 然后在 docx_content/word/document.xml 中搜索 <w:vanish/> 标记
grep -A 5 "w:vanish" docx_content/word/document.xml

# 提取 PNG 中的隐藏 ZIP
dd if=TiTan.png of=hidden.zip bs=1 skip=4333569

# 查看隐藏 ZIP 内容
unzip -l hidden.zip

# 尝试解压（需要密码）
unzip -P "password" hidden.zip
```

## 学习要点 (Key Takeaways)

1. **Word 文档隐写**: 使用 `w:vanish` 样式可以隐藏文字
2. **PNG 文件追加**: 可以在 IEND 后追加任意数据
3. **多层隐写**: CTF 题目通常有多个隐藏层次
4. **故事线索**: 题目故事往往包含解题提示

---

*此 writeup 基于对题目的分析，部分 flag 需要进一步的密码破解或隐写分析才能完整获取。*
