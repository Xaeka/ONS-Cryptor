# ==============================================
# ONS_Cryptor v1.0.0 GUI可视化版
# 支持：nscript.dat / nscr_sec.dat / onscript.nt2 / onscript.nt3 / nscript.___
# 全窗口自动居中 | 菜单栏快捷打开目录 | 解密弹窗增加跳转文件夹
# 基于kalawore/ons_decryptor全算法 | GB2312固定编码
# 作者：XAEKA
# ==============================================

import os
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, Menu

# ========== 全局通用：弹窗居中函数（所有子窗口统一调用） ==========
def center_window(win:tk.Toplevel, width:int, height:int):
    scr_w = win.winfo_screenwidth()
    scr_h = win.winfo_screenheight()
    x = int((scr_w - width)/2)
    y = int((scr_h - height)/2)
    win.geometry(f"{width}x{height}+{x}+{y}")

# ========== 原作者全套解密算法 START ==========
def crypt_xor_1(data: bytes):
    key = 0x84
    return bytearray(b ^ key for b in data)

def crypt_xor_2(data: bytes):
    mk = [0x79,0x57,0x0d,0x80,0x04]
    return bytearray(b ^ mk[i%5] for i,b in enumerate(data))

def crypt_nt2(data: bytes):
    k = 0x81
    return bytearray(((b+1)&0xFF)^k for b in data)

def crypt_nt3_file(inpath:str, outpath:str):
    HEADER = 0x920
    KEYOFF = 0x91C
    MAGIC = 0x5D588B65
    with open(inpath,"rb") as f:
        f.seek(KEYOFF)
        nt3_key = int.from_bytes(f.read(4),"little",signed=True)
        f.seek(HEADER)
        raw = f.read()
    out = bytearray()
    datasize = len(raw)
    for idx,b in enumerate(raw):
        pos = idx+1
        tmpk = nt3_key ^ b
        cnt = (datasize+1)-pos
        term = b*cnt + MAGIC
        tmpk += term
        nt3_key = tmpk & 0xFFFFFFFF
        if nt3_key>0x7FFFFFFF:
            nt3_key -= 0x100000000
        out.append(b ^ (nt3_key & 0xFF))
    with open(outpath,"wb") as f:
        f.write(out)

def crypt_key3(data:bytes, keytable:bytes):
    invtab = [0]*256
    for idx,val in enumerate(keytable):
        invtab[val]=idx
    k=0x84
    return bytearray(invtab[b^k] for b in data)
# ========== 原作者全套解密算法 END ==========

def mkdir_safe(path):
    if not os.path.exists(path):
        os.makedirs(path)

# 同名旧文件自动备份：旧文件更名 原名_年月日时分+3位序号.后缀
def backup_old_file(file_path: str):
    if not os.path.exists(file_path):
        return
    file_dir = os.path.dirname(file_path)
    full_name = os.path.basename(file_path)
    name, ext = os.path.splitext(full_name)
    # 生成格式 YYYYMMDDHHMM
    time_str = datetime.datetime.now().strftime("%Y%m%d%H%M")
    seq = 1
    # 循环自增序号，避免备份文件重名
    while True:
        new_back_name = f"{name}_{time_str}{seq:03d}{ext}"
        new_back_full = os.path.join(file_dir, new_back_name)
        if not os.path.exists(new_back_full):
            os.rename(file_path, new_back_full)
            break
        seq += 1


# 菜单栏：快捷打开目录
def open_dec_dir():
    mkdir_safe("decrypted")
    os.startfile("decrypted")
def open_enc_dir():
    mkdir_safe("encrypted")
    os.startfile("encrypted")

# 统一成功弹窗：解密/加密共用，原生默认按钮样式，无复古配色
def show_success_dialog(save_path, win_title="解密成功"):
    dlg = tk.Toplevel()
    center_window(dlg,420,180)
    dlg.title(win_title)
    tk.Label(dlg,text=f"输出路径：{save_path}",font=("微软雅黑",11),pady=25).pack()
    frm = tk.Frame(dlg)
    frm.pack()
    def open_folder():
        dlg.destroy()
        os.startfile(os.path.dirname(save_path))
    # 移除bg/fg颜色，使用系统原生按钮
    tk.Button(frm,text="前往文件所在路径",width=14,command=open_folder).grid(row=0,column=0,padx=12)
    tk.Button(frm,text="确定",width=10,command=dlg.destroy).grid(row=0,column=1,padx=12)
    
# 解密入口
def decrypt_work():
    infile = filedialog.askopenfilename(
        title="选择待解密ONS脚本",
        filetypes=[("ONS脚本", "*.dat;*.nt2;*.nt3;*.___"),("全部文件","*.*")]
    )
    if not infile:
        return
    basename = os.path.basename(infile).lower()
    outdir = "decrypted"
    mkdir_safe(outdir)
    outname = os.path.splitext(basename)[0]+"_dec.txt"
    outpath = os.path.join(outdir,outname)

    try:
        if basename == "nscript.dat":
            raw = open(infile,"rb").read()
            res = crypt_xor_1(raw)
        elif basename == "nscr_sec.dat":
            raw = open(infile,"rb").read()
            res = crypt_xor_2(raw)
        elif basename == "onscript.nt2":
            raw = open(infile,"rb").read()
            res = crypt_nt2(raw)
        elif basename == "onscript.nt3":
            crypt_nt3_file(infile, outpath)
            show_success_dialog(outpath)
            return
        elif basename == "nscript.___":
            keybin = filedialog.askopenfilename(title="选择256字节密钥表key.bin",filetypes=[("密钥文件","*.bin")])
            if not keybin:
                messagebox.showwarning("取消","未选择密钥文件，终止解密")
                return
            keydata = open(keybin,"rb").read()
            if len(keydata)!=256:
                messagebox.showerror("错误","密钥必须严格256字节！")
                return
            raw = open(infile,"rb").read()
            res = crypt_key3(raw,keydata)
        else:
            messagebox.showerror("不支持","当前后缀不在支持列表内")
            return
        backup_old_file(outpath)
        with open(outpath,"wb") as f:
            f.write(res)
        show_success_dialog(outpath, "解密成功")
    except Exception as e:
        messagebox.showerror("异常",str(e))

# 加密入口（格式选择弹窗自动居中）
def encrypt_work():
    infile = filedialog.askopenfilename(title="选择明文TXT(GB2312)",filetypes=[("文本","*.txt"),("全部","*.*")])
    if not infile:
        return
    outdir = "encrypted"
    mkdir_safe(outdir)
    sel = tk.Toplevel()
    sel.title("选择目标加密格式")
    center_window(sel,360,180) #加密选择框居中
    opt = tk.StringVar(value="nscript.dat")
    tk.Radiobutton(sel,text="nscript.dat(模式1)",variable=opt,value="nscript.dat").pack(anchor="w",padx=30,pady=6)
    tk.Radiobutton(sel,text="nscr_sec.dat(模式2)",variable=opt,value="nscr_sec.dat").pack(anchor="w",padx=30,pady=6)
    tk.Radiobutton(sel,text="onscript.nt2(模式4)",variable=opt,value="onscript.nt2").pack(anchor="w",padx=30,pady=6)
    def confirm():
        sel.destroy()
        outname = opt.get()
        outpath = os.path.join(outdir,outname)
        raw = open(infile,"rb").read()
        if outname=="nscript.dat":
            res = crypt_xor_1(raw)
        elif outname=="nscr_sec.dat":
            res = crypt_xor_2(raw)
        elif outname=="onscript.nt2":
            k=0x81
            res = bytearray( (b^k -1)&0xFF for b in raw )
        else:
            return
        backup_old_file(outpath)
        open(outpath,"wb").write(res)
        show_success_dialog(outpath, "加密成功")
    tk.Button(sel,text="确定",command=confirm).pack(pady=15)
    sel.mainloop()

# ====== 关于弹窗函数 ======
def show_help():
    help_text = """【ONS Cryptor 使用说明】
1.解密：点击【🔓解密文件】，选中dat/nt2/nt3/___脚本
  ·解密文件自动保存在软件同目录decrypted文件夹，输出GB231编码TXT
2.加密：点击【🔒加密文件】，选中修改完毕的GB2312编码TXT，按需选择加密格式
  ·加密文件自动保存在encrypted文件夹
【重要注意事项】
①修改文本仅可修改双引号内中文对话，禁止改动代码、符号、\换行、br标签
②明文文件必须保存为GB2312编码，否则加密后游戏乱码方框
③nt3格式仅支持解密，暂无加密功能"""
    messagebox.showinfo("使用说明", help_text)
def show_about():
    about_text = """ONS Cryptor v1.0.0
基于kalawore/ons_decryptor开源算法二次开发
GitHub项目地址：https://github.com/Xaeka/ONS-Cryptor"""
    messagebox.showinfo("关于软件", about_text)

# 主窗口
def main_gui():
    root = tk.Tk()
    root.title("ONS_Cryptor v1.0.0 | 全格式ONS脚本加解密")
    win_w = 520
    win_h = 300
    scr_w = root.winfo_screenwidth()
    scr_h = root.winfo_screenheight()
    x = int((scr_w - win_w)/2)
    y = int((scr_h - win_h)/2)
    root.geometry(f"{win_w}x{win_h}+{x}+{y}")
    root.resizable(False,False)

    # 顶部菜单栏：解密目录｜加密目录｜关于
    menubar = Menu(root)
    # 快捷打开文件夹菜单
    menubar.add_cascade(label="解密目录",command=open_dec_dir)
    menubar.add_cascade(label="加密目录",command=open_enc_dir)
    # 原关于下拉菜单
    menu_about = Menu(menubar, tearoff=0)
    menu_about.add_command(label="使用说明", command=show_help)
    menu_about.add_command(label="关于", command=show_about)
    menubar.add_cascade(label="关于", menu=menu_about)
    root.config(menu=menubar)

    # 页面控件
    tk.Label(root,text="ONS_Cryptor 全格式加解密工具",font=("微软雅黑",17,"bold"),fg="#223355").pack(pady=22)
    tk.Label(root,text="支持: dat/nt2/nt3/nscr_sec.dat/nscript.___ | 文本编码固定GB2312",font=("微软雅黑",9)).pack()
    frm = tk.Frame(root)
    frm.pack(pady=35)
    tk.Button(frm,text="🔓 解密文件",width=13,bg="#28a745",fg="white",font=("微软雅黑",12),command=decrypt_work).grid(row=0,column=0,padx=22)
    tk.Button(frm,text="🔒 加密文件",width=13,bg="#2980d0",fg="white",font=("微软雅黑",12),command=encrypt_work).grid(row=0,column=1,padx=22)
    tk.Label(root,text="基于kalawore/ons_decryptor全算法开源优化",font=("微软雅黑",8),fg="#777777").pack(side="bottom",pady=12)
    root.mainloop()

if __name__=="__main__":
    main_gui()