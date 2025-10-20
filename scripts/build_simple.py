#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================
# build_simple.py - 简化的打包脚本
# ============================================

import os
import sys
import shutil
import subprocess
from pathlib import Path

def main():
    """主函数"""
    print("""
╔══════════════════════════════════════════╗
║     CardCraft - Markdown转精美卡片编辑器 - 打包工具      ║
║            Version 1.0.0              ║
╚══════════════════════════════════════════╝
    """)
    
    # 清理旧的构建文件
    print("🧹 清理旧的构建文件...")
    build_dir = Path.cwd() / "build"
    dist_dir = Path.cwd() / "dist"
    
    if build_dir.exists():
        shutil.rmtree(build_dir)
        print(f"  ✓ 删除 {build_dir}")
        
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
        print(f"  ✓ 删除 {dist_dir}")
    
    # 检查主脚本
    main_script = Path.cwd() / "main.py"
    if not main_script.exists():
        print(f"  ✗ 找不到 main.py")
        return False
    
    # 构建命令
    print("\n🔨 开始构建...")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", "CardCraft",
    ]
    
    # 添加资源文件
    resources_dir = Path.cwd() / "resources"
    if resources_dir.exists():
        cmd.extend(["--add-data", f"{resources_dir};resources"])
    
    # 添加src目录
    src_dir = Path.cwd() / "src"
    if src_dir.exists():
        cmd.extend(["--add-data", f"{src_dir};src"])
    
    # 添加图标
    ico_file = resources_dir / "icons" / "app.ico"
    if ico_file.exists():
        cmd.extend(["--icon", str(ico_file)])
    
    # 添加隐藏导入
    hidden_imports = [
        "PySide6.QtCore",
        "PySide6.QtGui",
        "PySide6.QtWidgets",
        "PySide6.QtWebEngineCore",
        "PySide6.QtWebEngineWidgets",
        "markdown",
        "bs4",
    ]
    
    for imp in hidden_imports:
        cmd.extend(["--hidden-import", imp])
    
    # 排除不需要的模块
    excludes = ["tkinter", "matplotlib", "numpy", "pandas", "scipy", "test", "tests"]
    for exc in excludes:
        cmd.extend(["--exclude-module", exc])
    
    # 添加主脚本
    cmd.append("main.py")
    
    print(f"  执行命令: {' '.join(cmd[:5])}...")
    
    try:
        # 执行打包
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        if result.returncode == 0:
            print("  ✓ 构建成功！")
            
            # 检查输出文件
            exe_path = dist_dir / "CardCraft.exe"
            
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / 1024 / 1024
                print(f"  ✓ 生成文件: {exe_path}")
                print(f"  ✓ 文件大小: {size_mb:.2f} MB")
                
                print(f"""
╔══════════════════════════════════════════╗
║              ✅ 打包完成！                ║
╚══════════════════════════════════════════╝

📁 输出目录: {dist_dir}
📄 可执行文件: CardCraft.exe

运行方式:
  1. 直接双击 CardCraft.exe
  2. 或从命令行运行: .\\dist\\CardCraft.exe

提示:
  - 首次运行可能需要几秒钟加载
  - 确保系统已安装 Microsoft Visual C++ Redistributable
  - 如遇到问题，请查看构建日志
                """)
                
                return True
            else:
                print("  ✗ 找不到生成的可执行文件")
                return False
        else:
            print("  ✗ 构建失败")
            print(f"\n错误输出:\n{result.stderr}")
            return False
            
    except Exception as e:
        print(f"  ✗ 构建出错: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)