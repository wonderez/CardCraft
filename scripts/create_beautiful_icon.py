# ============================================
# create_beautiful_icon.py - 生成漂亮的应用图标
# ============================================
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
from pathlib import Path
import math

def create_beautiful_icon():
    """创建一个更漂亮的小红书风格应用图标"""
    
    # 创建图标目录
    icon_dir = Path("resources/icons")
    icon_dir.mkdir(parents=True, exist_ok=True)
    
    # 定义所需的图标尺寸
    sizes = [16, 32, 48, 64, 128, 256, 512]
    
    # 创建最大尺寸的图标作为基础
    base_size = 512
    img = Image.new('RGBA', (base_size, base_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制背景 - 使用小红书特色的渐变色
    # 从深粉色到浅粉色的径向渐变
    center_x, center_y = base_size // 2, base_size // 2
    radius = base_size // 2
    
    for y in range(base_size):
        for x in range(base_size):
            # 计算到中心的距离
            distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            
            # 根据距离计算颜色
            ratio = min(distance / radius, 1.0)
            
            # 小红书特色渐变：从深粉色到浅粉色
            r = int(255 - ratio * 30)
            g = int(87 - ratio * 30)
            b = int(120 - ratio * 30)
            
            # 添加一些变化使背景更有趣
            variation = int(math.sin(x / 50) * math.cos(y / 50) * 10)
            r = max(0, min(255, r + variation))
            g = max(0, min(255, g + variation))
            b = max(0, min(255, b + variation))
            
            draw.point((x, y), fill=(r, g, b, 255))
    
    # 添加圆角效果
    mask = Image.new('L', (base_size, base_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    corner_radius = base_size // 5  # 更圆的角
    mask_draw.rounded_rectangle([(0, 0), (base_size, base_size)], 
                                radius=corner_radius, fill=255)
    
    # 应用遮罩
    output = Image.new('RGBA', (base_size, base_size), (0, 0, 0, 0))
    output.paste(img, (0, 0))
    output.putalpha(mask)
    img = output
    
    # 添加光泽效果
    gloss = Image.new('RGBA', (base_size, base_size), (0, 0, 0, 0))
    gloss_draw = ImageDraw.Draw(gloss)
    
    # 绘制椭圆形高光
    gloss_width = int(base_size * 0.8)
    gloss_height = int(base_size * 0.4)
    gloss_x = (base_size - gloss_width) // 2
    gloss_y = int(base_size * 0.1)
    
    # 创建渐变高光
    for y in range(gloss_height):
        alpha = int(150 * (1 - y / gloss_height))  # 渐变透明度
        gloss_draw.ellipse(
            [gloss_x, gloss_y + y, gloss_x + gloss_width, gloss_y + y + 2],
            fill=(255, 255, 255, alpha)
        )
    
    # 应用高光
    img = Image.alpha_composite(img, gloss)
    draw = ImageDraw.Draw(img)
    
    # 绘制中心的编辑器图标 - 结合笔记本和笔的元素
    # 笔记本背景
    notebook_width = int(base_size * 0.6)
    notebook_height = int(base_size * 0.7)
    notebook_x = (base_size - notebook_width) // 2
    notebook_y = (base_size - notebook_height) // 2
    
    # 绘制白色笔记本背景
    draw.rounded_rectangle(
        [notebook_x, notebook_y, notebook_x + notebook_width, notebook_y + notebook_height],
        radius=20,
        fill=(255, 255, 255, 240),
        outline=(255, 255, 255, 255),
        width=3
    )
    
    # 绘制笔记本线条
    line_color = (220, 220, 220, 200)
    line_spacing = notebook_height // 8
    for i in range(1, 8):
        y_pos = notebook_y + i * line_spacing
        draw.line(
            [notebook_x + 20, y_pos, notebook_x + notebook_width - 20, y_pos],
            fill=line_color,
            width=2
        )
    
    # 绘制左侧的红线（小红书特色）
    red_line_x = notebook_x + 40
    draw.line(
        [red_line_x, notebook_y + 20, red_line_x, notebook_y + notebook_height - 20],
        fill=(255, 87, 120, 255),
        width=4
    )
    
    # 绘制笔图标
    pen_length = int(base_size * 0.4)
    pen_width = int(base_size * 0.05)
    pen_x = notebook_x + notebook_width - pen_width - 30
    pen_y = notebook_y + notebook_height // 2 - pen_length // 2
    
    # 笔身 - 渐变色
    for i in range(pen_length):
        ratio = i / pen_length
        r = int(50 + ratio * 50)
        g = int(50 + ratio * 50)
        b = int(50 + ratio * 50)
        draw.rectangle(
            [pen_x, pen_y + i, pen_x + pen_width, pen_y + i + 1],
            fill=(r, g, b, 255)
        )
    
    # 笔尖
    tip_height = int(base_size * 0.08)
    draw.polygon(
        [
            (pen_x, pen_y + pen_length),
            (pen_x + pen_width // 2, pen_y + pen_length + tip_height),
            (pen_x + pen_width, pen_y + pen_length)
        ],
        fill=(200, 200, 200, 255)
    )
    
    # 添加小装饰 - 小红书logo风格的小星星
    star_size = int(base_size * 0.08)
    star_x = notebook_x + notebook_width - star_size - 20
    star_y = notebook_y + 20
    
    # 绘制星星
    draw_star(draw, star_x, star_y, star_size, (255, 255, 255, 200))
    
    # 添加阴影效果
    shadow = img.filter(ImageFilter.GaussianBlur(radius=10))
    shadow = Image.new('RGBA', (base_size, base_size), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle(
        [20, 20, base_size - 20, base_size - 20],
        radius=corner_radius,
        fill=(0, 0, 0, 100)
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=15))
    
    # 合成最终图像
    final = Image.new('RGBA', (base_size, base_size), (0, 0, 0, 0))
    final.paste(shadow, (0, 0))
    final.paste(img, (0, 0), img)
    
    # 生成不同尺寸的图标
    icons = {}
    for size in sizes:
        resized = final.resize((size, size), Image.Resampling.LANCZOS)
        icon_path = icon_dir / f"icon_{size}x{size}.png"
        resized.save(icon_path, 'PNG')
        icons[size] = icon_path
        print(f"Created: {icon_path}")
    
    # 生成 ICO 文件（Windows需要）
    ico_path = icon_dir / "app.ico"
    final.save(ico_path, format='ICO', sizes=[(s, s) for s in [16, 32, 48, 64, 128, 256]])
    print(f"Created: {ico_path}")
    
    # 保存原始大图标
    original_path = icon_dir / "icon_original.png"
    final.save(original_path, 'PNG')
    print(f"Created: {original_path}")
    
    return ico_path

def draw_star(draw, x, y, size, color):
    """绘制星星"""
    # 五角星的五个顶点
    points = []
    for i in range(10):
        angle = math.pi * i / 5 - math.pi / 2
        if i % 2 == 0:
            # 外顶点
            r = size
        else:
            # 内顶点
            r = size * 0.5
        
        px = x + size + r * math.cos(angle)
        py = y + size + r * math.sin(angle)
        points.append((px, py))
    
    draw.polygon(points, fill=color)

if __name__ == "__main__":
    try:
        # 尝试使用PIL创建高质量图标
        from PIL import Image, ImageDraw, ImageFont, ImageFilter
        ico_path = create_beautiful_icon()
        print(f"\n✅ 漂亮的应用图标创建成功！")
        print(f"ICO文件位置: {ico_path}")
    except ImportError:
        print("⚠️ 需要安装 Pillow 库来生成图标")
        print("请运行: pip install Pillow")