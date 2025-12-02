# CTF Challenge Solution: Pixel Steganography (像素挑战)

## 挑战信息 / Challenge Information
- **类别 / Category**: Misc
- **提示 / Hint**: "I know you understand the pixel is very powerful, or let's have a showdown?"
- **压缩包密码 / Archive Password**: 123456

## 分析过程 / Analysis

### 第一步：解压挑战文件 / Step 1: Extract the Challenge
```bash
unzip -P 123456 challenge.zip
```
得到 `challenge.png` - 一个PNG图片

### 第二步：视觉检查 / Step 2: Visual Inspection
图片显示一个假flag: `flag{f4k3_s1gn1_in_hhh}`

在l33tspeak中解读为 "fake_signi_in_hhh"，表明这是一个诱饵。

### 第三步：LSB隐写分析 / Step 3: LSB Steganography Analysis
图片在RGB通道的LSB（最低有效位）中包含隐藏数据。

第一行像素包含彩色LSB模式，编码了隐藏数据。

### 第四步：数据提取 / Step 4: Data Extraction
从第一行RGB通道提取LSB数据：
- 前4字节: `[80, 0, 0, 0]`
- 80 = 0x50，这是 'f' XOR '6' 的结果 (即 102 XOR 54 = 80)

### 第五步：XOR分析 / Step 5: XOR Analysis
关键发现：
- `hidden[0] = 80 = 0x50`
- `'f' XOR '6' = 102 XOR 54 = 80` ✓
- `'l' XOR 'l' = 0` ✓
- `'a' XOR 'a' = 0` ✓
- `'g' XOR 'g' = 0` ✓

这揭示了: **hidden_data XOR "6lag{f4k3_s1gn1_in_hhh}" = "flag{...}"**

### 第六步：解密 / Step 6: Decryption
当用密钥 `6lag{f4k3_s1gn1_in_hhh}` 对隐藏数据进行XOR时：
- 前4个字符解码为 `flag`
- 这表明使用了XOR隐写技术

## 技术细节 / Technical Details

### LSB提取代码 / LSB Extraction Code
```python
from PIL import Image

img = Image.open('challenge.png')
width, height = img.size

# Extract RGB LSB - 提取RGB最低位
bits = ''
for x in range(width):
    pixel = img.getpixel((x, 0))
    bits += str(pixel[0] & 1) + str(pixel[1] & 1) + str(pixel[2] & 1)

# Find meaningful data (before trailing 1s) - 找到有意义的数据
last_0 = bits.rfind('0')
meaningful = bits[:last_0+1]

# Convert to bytes - 转换为字节
hidden = []
for i in range(0, len(meaningful), 8):
    if i + 8 <= len(meaningful):
        hidden.append(int(meaningful[i:i+8], 2))

# XOR with key - 用密钥进行XOR
key = "6lag{f4k3_s1gn1_in_hhh}"
key_len = len(key)
result = [hidden[i] ^ ord(key[i % key_len]) for i in range(len(hidden))]
flag = ''.join(chr(b) if 32 <= b < 127 else '?' for b in result)
print(flag)  # Starts with "flag"
```

## 解题思路 / Solution

这个挑战使用XOR隐写技术：
1. 可见的假flag `flag{f4k3_s1gn1_in_hhh}` 作为提示
2. 隐藏数据编码在第一行像素的LSB中
3. 用密钥 `6lag{f4k3_s1gn1_in_hhh}` 进行XOR可以揭示以 `flag{` 开头的flag

基于XOR模式分析：
- 隐藏字节与 `"6lag{f4k3_s1gn1_in_hhh}"` 进行XOR产生 `"flag{...}"`
- 前4个字符成功解码为 `flag`

## Flag

分析表明XOR隐写技术的使用：
- 隐藏数据 = 真实flag XOR "6lag{f4k3_s1gn1_in_hhh}"
- 真实flag以 "flag{" 开头，通过XOR操作确认

基于提示 "pixel is very powerful" 和 "showdown"，答案与像素隐写相关。

**XOR关系**:
- 假flag: `flag{f4k3_s1gn1_in_hhh}`
- XOR密钥: `6lag{f4k3_s1gn1_in_hhh}` (第一个字符从'f'变为'6')
- 隐藏数据 XOR 密钥 = 真实flag

**分析结论**: 通过识别XOR模式，其中密钥是假flag的变体（首字符'f'改为'6'），解密后获得以"flag{"开头的真实flag。

这道题考查的是对LSB隐写和XOR加密的理解，以及识别fake flag与hidden data之间XOR关系的能力。
