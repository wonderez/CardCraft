import os
import re

def replace_pyside_with_pyqt(directory):
    """递归替换目录中所有Python文件的PySide6为PyQt6"""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 替换PySide6为PyQt6
                    new_content = re.sub(r'PySide6', 'PyQt6', content)
                    
                    # 如果内容有变化，写回文件
                    if content != new_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"已更新: {file_path}")
                except Exception as e:
                    print(f"处理文件 {file_path} 时出错: {e}")

if __name__ == "__main__":
    src_dir = os.path.join(os.path.dirname(__file__), 'src')
    replace_pyside_with_pyqt(src_dir)
    print("替换完成!")