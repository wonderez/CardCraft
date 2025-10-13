import os
import re

def fix_qt_orientation(directory):
    """修复Qt.Orientation相关的API差异"""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 修复Qt.Orientation
                    new_content = re.sub(r'Qt\.Horizontal', 'Qt.Orientation.Horizontal', content)
                    new_content = re.sub(r'Qt\.Vertical', 'Qt.Orientation.Vertical', content)
                    
                    # 修复Qt.WindowType
                    new_content = re.sub(r'Qt\.Window', 'Qt.WindowType.Window', new_content)
                    new_content = re.sub(r'Qt\.Dialog', 'Qt.WindowType.Dialog', new_content)
                    new_content = re.sub(r'Qt\.Tool', 'Qt.WindowType.Tool', new_content)
                    
                    # 修复Qt.WindowFlags
                    new_content = re.sub(r'Qt\.CustomizeWindowHint', 'Qt.WindowType.CustomizeWindowHint', new_content)
                    new_content = re.sub(r'Qt\.WindowCloseButtonHint', 'Qt.WindowType.WindowCloseButtonHint', new_content)
                    new_content = re.sub(r'Qt\.WindowMinimizeButtonHint', 'Qt.WindowType.WindowMinimizeButtonHint', new_content)
                    new_content = re.sub(r'Qt\.WindowMaximizeButtonHint', 'Qt.WindowType.WindowMaximizeButtonHint', new_content)
                    new_content = re.sub(r'Qt\.WindowStaysOnTopHint', 'Qt.WindowType.WindowStaysOnTopHint', new_content)
                    
                    # 如果内容有变化，写回文件
                    if content != new_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"已修复Qt方向API: {file_path}")
                except Exception as e:
                    print(f"处理文件 {file_path} 时出错: {e}")

if __name__ == "__main__":
    src_dir = os.path.join(os.path.dirname(__file__), 'src')
    fix_qt_orientation(src_dir)
    print("Qt方向API修复完成!")