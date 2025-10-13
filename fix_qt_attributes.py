import os
import re

def fix_qt_widget_attributes(directory):
    """修复Qt.WidgetAttribute相关的API差异"""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 修复Qt.WidgetAttribute
                    new_content = re.sub(r'Qt\.WA_TransparentForMouseEvents', 'Qt.WidgetAttribute.WA_TransparentForMouseEvents', content)
                    
                    # 修复Qt.AlignmentFlag
                    new_content = re.sub(r'Qt\.AlignCenter', 'Qt.AlignmentFlag.AlignCenter', new_content)
                    new_content = re.sub(r'Qt\.AlignLeft', 'Qt.AlignmentFlag.AlignLeft', new_content)
                    new_content = re.sub(r'Qt\.AlignRight', 'Qt.AlignmentFlag.AlignRight', new_content)
                    
                    # 修复Qt.FocusPolicy
                    new_content = re.sub(r'Qt\.StrongFocus', 'Qt.FocusPolicy.StrongFocus', new_content)
                    new_content = re.sub(r'Qt\.NoFocus', 'Qt.FocusPolicy.NoFocus', new_content)
                    
                    # 修复Qt.ScrollBarPolicy
                    new_content = re.sub(r'Qt\.ScrollBarAlwaysOff', 'Qt.ScrollBarPolicy.ScrollBarAlwaysOff', new_content)
                    new_content = re.sub(r'Qt\.ScrollBarAlwaysOn', 'Qt.ScrollBarPolicy.ScrollBarAlwaysOn', new_content)
                    new_content = re.sub(r'Qt\.ScrollBarAsNeeded', 'Qt.ScrollBarPolicy.ScrollBarAsNeeded', new_content)
                    
                    # 修复Qt.Key
                    new_content = re.sub(r'Qt\.Key_', 'Qt.Key.', new_content)
                    
                    # 修复Qt.CursorShape
                    new_content = re.sub(r'Qt\.PointingHandCursor', 'Qt.CursorShape.PointingHandCursor', new_content)
                    new_content = re.sub(r'Qt\.ArrowCursor', 'Qt.CursorShape.ArrowCursor', new_content)
                    
                    # 如果内容有变化，写回文件
                    if content != new_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"已修复Qt属性API: {file_path}")
                except Exception as e:
                    print(f"处理文件 {file_path} 时出错: {e}")

if __name__ == "__main__":
    src_dir = os.path.join(os.path.dirname(__file__), 'src')
    fix_qt_widget_attributes(src_dir)
    print("Qt属性API修复完成!")