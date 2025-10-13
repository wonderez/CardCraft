import os
import re

def fix_pyqt6_api(directory):
    """修复PyQt6与PySide6的API差异"""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 修复Signal导入
                    new_content = re.sub(r'from PyQt6\.QtCore import.*Signal', 'from PyQt6.QtCore import pyqtSignal', content)
                    new_content = re.sub(r'Signal\(\)', 'pyqtSignal()', new_content)
                    new_content = re.sub(r' = Signal\(', ' = pyqtSignal(', new_content)
                    
                    # 如果内容有变化，写回文件
                    if content != new_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"已修复API: {file_path}")
                except Exception as e:
                    print(f"处理文件 {file_path} 时出错: {e}")

if __name__ == "__main__":
    src_dir = os.path.join(os.path.dirname(__file__), 'src')
    fix_pyqt6_api(src_dir)
    print("API修复完成!")