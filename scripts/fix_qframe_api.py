import os
import re

def fix_qframe_style(directory):
    """修复QFrame相关的API差异"""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 修复QFrame.Shape
                    new_content = re.sub(r'QFrame\.VLine', 'QFrame.Shape.VLine', content)
                    new_content = re.sub(r'QFrame\.HLine', 'QFrame.Shape.HLine', content)
                    new_content = re.sub(r'QFrame\.Box', 'QFrame.Shape.Box', content)
                    new_content = re.sub(r'QFrame\.Panel', 'QFrame.Shape.Panel', content)
                    new_content = re.sub(r'QFrame\.StyledPanel', 'QFrame.Shape.StyledPanel', content)
                    
                    # 修复QFrame.Shadow
                    new_content = re.sub(r'QFrame\.Sunken', 'QFrame.Shadow.Sunken', new_content)
                    new_content = re.sub(r'QFrame\.Raised', 'QFrame.Shadow.Raised', new_content)
                    new_content = re.sub(r'QFrame\.Plain', 'QFrame.Shadow.Plain', new_content)
                    
                    # 如果内容有变化，写回文件
                    if content != new_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"已修复QFrame API: {file_path}")
                except Exception as e:
                    print(f"处理文件 {file_path} 时出错: {e}")

if __name__ == "__main__":
    src_dir = os.path.join(os.path.dirname(__file__), 'src')
    fix_qframe_style(src_dir)
    print("QFrame API修复完成!")