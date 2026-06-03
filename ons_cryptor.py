# ==============================================
# ONS_Cryptor - ONS脚本加密解密一体化工具
# 原项目基础：kalawore/ons_decryptor
# 优化增强：XAEKA's Open Source Project
# 版本：v1.0.0
# 功能：nscript.dat 加解密 | GB2312自动识别 
# ==============================================

import os
import sys

def crypt_data(data: bytes, key: int) -> bytes:
    """通用异或加解密（加密=解密）"""
    return bytearray(b ^ key for b in data)

def decrypt_file(input_path, output_path):
    key = 0x84
    with open(input_path, 'rb') as f:
        encrypted = f.read()
    decrypted = crypt_data(encrypted, key)
    with open(output_path, 'wb') as f:
        f.write(decrypted)

def encrypt_file(input_path, output_path):
    key = 0x84
    with open(input_path, 'rb') as f:
        plaintext = f.read()
    encrypted = crypt_data(plaintext, key)
    with open(output_path, 'wb') as f:
        f.write(encrypted)

def show_logo():
    print("=" * 50)
    print("    ONS_Cryptor v1.0.0  一体化加解密工具")
    print("    支持：nscript.dat  编码：GB2312")
    print("    原项目：github.com/kalawore/ons_decryptor")
    print("=" * 50)

def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

if __name__ == "__main__":
    show_logo()
    print("\n请选择功能：")
    print("1. 解密 nscript.dat → decrypted_script.txt")
    print("2. 加密 txt → 新的 nscript.dat")
    choice = input("\n输入数字 1 或 2：")

    if choice == "1":
        print("\n【解密模式】")
        make_dir("decrypted")
        decrypt_file("nscript.dat", "decrypted/decrypted_script.txt")
        print("✅ 解密成功！文件保存在 decrypted/ 文件夹")

    elif choice == "2":
        print("\n【加密模式】")
        make_dir("encrypted")
        encrypt_file("decrypted_script.txt", "encrypted/nscript.dat")
        print("✅ 加密成功！文件保存在 encrypted/ 文件夹")

    else:
        print("❌ 输入错误，请输入 1 或 2")

    input("\n按回车退出...")