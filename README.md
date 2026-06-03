<div align="center">
<!-- 项目图标，默认调用仓库内app.ico，后续可替换GUI截图png -->
<img src="https://raw.githubusercontent.com/Xaeka/ONS-Cryptor/main/app.ico" width="128"/>
</div>

# ONS_Cryptor v1.0.0
✨ 可视化ONScripter全格式脚本加解密工具 ✨

## 🌟 项目介绍
基于开源项目 [kalawore/ons_decryptor](https://github.com/kalawore/ons_decryptor) 全套原生加密算法二次重构、GUI可视化开发；
专门用于**全系列ONS安卓移植游戏**脚本纠错修改，一键解密→修正错别字语病→重新加密生成游戏可正常读取的脚本文件。
明文统一固定 **GB2312编码**，适配国内汉化ONS，杜绝修改后乱码、方框文字。

### 📋 全支持加密格式对照表
| 文件名 | 加密模式 | 加解密支持 | 备注说明 |
|--------|----------|------------|------|
| nscript.dat | 模式1（0x84单字节异或） | ✅ 解密+加密 | 较为常用 |
| nscr_sec.dat | 模式2（5字节循环密钥异或） | ✅ 解密+加密 | 早期小众版本ONS脚本 |
| onscript.nt2 | 模式4（字节公式变换加密） | ✅ 解密+加密 | 部分日区专属移植脚本 |
| onscript.nt3 | 模式5（头部流式动态密钥） | ✅仅解密 | 原项目无逆向加密算法，无法重新打包 |
| nscript.___ | 模式3（256字节密钥查表） | ✅解密(需key.bin密钥) | 解密必须附带256字节key.bin密钥文件 |

## 🛠 软件核心功能清单
### 1. 顶部可视化菜单栏
菜单栏三栏：`解密目录`｜`加密目录`｜`关于`
- 解密目录：一键自动打开`decrypted`文件夹，目录不存在自动创建
- 加密目录：一键自动打开`encrypted`文件夹，目录不存在自动创建
- 关于下拉菜单：【使用说明】【关于】两个弹窗

### 2. 安全防覆盖备份机制（重点优化）
> 解密/加密输出时，若输出路径已存在同名旧文件：
> 原文件自动备份重命名：`原文件名_YYYYMMDDHHMM+3位序号.后缀`
> 示例：`nscript.dat` → `nscript_202606032015001.dat`，从根源避免误覆盖丢失原版脚本

### 3. 弹窗人性化优化
1. 解密成功弹窗：【确定】+【前往文件所在路径】双按钮，一键跳转系统资源管理器定位文件
2. 加密成功弹窗：与解密弹窗样式统一，同样支持一键跳转输出目录
3. 全程序所有弹窗（格式选择弹窗/提示弹窗）默认屏幕居中，不会随机漂移到屏幕边角

## 🚀 使用教程
### 方式①：直接使用成品EXE（推荐一般用户）
1. 在项目Release发布页下载 `ONS Cryptor.exe`
2. 双击直接启动可视化GUI窗口，无需Python运行环境
3. 🔓解密：点击【🔓解密文件】→选中目标`.dat/.nt2/.nt3/.___`脚本 → 解密TXT自动存入`decrypted`
4. 🔒加密：点击【🔒加密文件】→选中修改完毕的**GB2312编码TXT** → 弹窗选择对应加密格式 → 加密成品存入`encrypted`
> 快捷技巧：顶部菜单栏随时一键打开解密/加密文件夹，省去手动查找目录

### 界面简单预览

<div align="center">
<img src="https://i.postimg.cc/15yQ0Jky/ONS-Cryptor-Index-Page.png" width="520"/>
</div>

### 方式②：本地源码直接运行
```bash
# 前置：本地安装Python3.x环境
python ons_cryptor_gui.py
```
### 方式③：自行编译打包生成 EXE
```bash
# 1. 安装打包依赖
pip install pyinstaller
# 2. 带图标打包，成品名称：ONS Cryptor.exe
pyinstaller -F -w -n "ONS Cryptor" -i app.ico ons_cryptor_gui.py
# 打包完成后，EXE文件输出在dist/文件夹内
```
## ⚠️ 关键使用注意事项
1. 文本修改规范：仅修改双引号""内部对话汉字，禁止改动引号、br、换行符、脚本控制代码，随意修改会导致游戏运行闪退  
2. 编码硬性要求：修改后的 TXT 文档必须保存为 GB2312 编码，UTF-8 格式加密后进游戏会出现全方框乱码  
3. nt3 格式限制：onscript.nt3仅支持解密，无加密实现，不能二次打包回游戏  

## 🙏 开源致谢
本项目加解密内核算法 100% 基于开源作者 kalawore 的 ons_decryptor 项目  
原开源仓库：https://github.com/kalawore/ons_decryptor

## 🧑‍💻 项目作者
XAEKA | 项目主页：https://github.com/Xaeka/ONS-Cryptor

## 📦 版本标识
当前正式发行版：v1.0.0

## 🔔 免责声明

* 本工具仅供学习、研究和个人数据备份使用。
* 请在符合当地法律法规的前提下使用本工具。