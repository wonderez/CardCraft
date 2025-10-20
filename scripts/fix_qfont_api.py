import os
import re

def fix_qfont_api(directory):
    """修复QFont相关的API差异"""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 修复QFont.Weight
                    new_content = re.sub(r'QFont\.Bold', 'QFont.Weight.Bold', content)
                    new_content = re.sub(r'QFont\.Normal', 'QFont.Weight.Normal', content)
                    
                    # 如果内容有变化，写回文件
                    if content != new_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"已修复QFont API: {file_path}")
                except Exception as e:
                    print(f"处理文件 {file_path} 时出错: {e}")

if __name__ == "__main__":
    src_dir = os.path.join(os.path.dirname(__file__), 'src')
    fix_qfont_api(src_dir)
    print("QFont API修复完成!")