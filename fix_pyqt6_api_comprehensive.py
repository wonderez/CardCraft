import os
import re

def fix_pyqt6_api_comprehensive(directory):
    """全面修复PyQt6与PySide6的API差异"""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 修复QFont.StyleHint
                    new_content = re.sub(r'QFont\.Monospace', 'QFont.StyleHint.Monospace', content)
                    
                    # 修复QTextOption
                    new_content = re.sub(r'QTextEdit\.WidgetWidth', 'QTextEdit.LineWrapMode.WidgetWidth', new_content)
                    new_content = re.sub(r'QTextOption\.WordWrap', 'QTextOption.WrapMode.WordWrap', new_content)
                    
                    # 修复QPainter.RenderHint
                    new_content = re.sub(r'QPainter\.Antialiasing', 'QPainter.RenderHint.Antialiasing', new_content)
                    new_content = re.sub(r'QPainter\.TextAntialiasing', 'QPainter.RenderHint.TextAntialiasing', new_content)
                    new_content = re.sub(r'QPainter\.SmoothPixmapTransform', 'QPainter.RenderHint.SmoothPixmapTransform', new_content)
                    
                    # 修复QWidget.RenderFlag
                    new_content = re.sub(r'QWidget\.DrawWindowBackground', 'QWidget.RenderFlag.DrawWindowBackground', new_content)
                    new_content = re.sub(r'QWidget\.DrawChildren', 'QWidget.RenderFlag.DrawChildren', new_content)
                    
                    # 如果内容有变化，写回文件
                    if content != new_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"已修复API: {file_path}")
                except Exception as e:
                    print(f"处理文件 {file_path} 时出错: {e}")

if __name__ == "__main__":
    src_dir = os.path.join(os.path.dirname(__file__), 'src')
    fix_pyqt6_api_comprehensive(src_dir)
    print("全面API修复完成!")