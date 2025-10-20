# ============================================
# src/core/html_generator.py
# ============================================
from pathlib import Path
from typing import Optional
from src.utils.style_manager import StyleManager

class HTMLGenerator:
    def __init__(self, font_size: int = 18, page_size: str = "medium", theme: str = "xiaohongshu"):
        self.resource_path = Path(__file__).parent.parent.parent / "resources"  # 调整为正确路径
        self.templates_path = self.resource_path / "templates"
        self.base_font_size = font_size
        self.font_size = font_size
        
        self.page_sizes = {
            "small": {"width": 720, "height": 960},
            "medium": {"width": 1080, "height": 1440},
            "large": {"width": 1440, "height": 1920}
        }
        self.current_size = page_size
        self.page_width = self.page_sizes[page_size]["width"]
        self.page_height = self.page_sizes[page_size]["height"]
        
        self.style_manager = StyleManager(theme)
        self.current_theme = theme
        
    def set_page_size(self, size: str):
        """设置页面尺寸"""
        if size in self.page_sizes:
            self.current_size = size
            self.page_width = self.page_sizes[size]["width"]
            self.page_height = self.page_sizes[size]["height"]
    
    def set_theme(self, theme: str):
        """设置主题"""
        self.current_theme = theme
        self.style_manager.set_theme(theme)
    
    def set_font_size(self, size: int):
        """设置基础字体大小"""
        self.base_font_size = size
        self.font_size = size  # 同时更新font_size属性
        
    def set_font_family(self, font_family: str):
        """设置字体"""
        self.font_family = font_family
        
    def generate(self, content: str, page_num: int = 0, total_pages: int = 0) -> str:
        """
        生成完整的 HTML 页面
        
        Args:
            content: HTML内容
            page_num: 当前页码（0表示不显示）
            total_pages: 总页数
        """
        theme = self.style_manager.get_theme()
        is_dark = self.current_theme in ["dark_mode", "midnight", "douyin"]
        
        # 生成主题CSS
        theme_css = self.style_manager.generate_css(self.current_theme, self.base_font_size, getattr(self, 'font_family', None))
        
        # 加载并处理页面CSS
        page_css = self._load_template('page.css')
        page_css = self._render_css_template(page_css, is_dark, theme)
        
        # 加载JS
        js = self._load_template('scripts.js')
        
        # 生成页码信息
        page_info = ""
        if page_num > 0 and total_pages > 1:
            page_info = f"""
            <div class="page-info">
                <span class="page-number">{page_num}</span>
                <span class="page-separator">/</span>
                <span class="page-total">{total_pages}</span>
            </div>
            """
        
        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>小红书卡片 - {self.style_manager.get_theme().name}</title>
    <style>
        {theme_css}
        {page_css}
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="content" id="content">
                {content}
            </div>
            {page_info}
        </div>
    </div>
    <script>{js}</script>
</body>
</html>
"""
        return html
    
    def _load_template(self, filename: str) -> str:
        """加载模板文件"""
        path = self.templates_path / filename
        if not path.exists():
            raise FileNotFoundError(f"Template file not found: {path}")
        return path.read_text(encoding='utf-8')
    
    def _render_css_template(self, css: str, is_dark: bool, theme) -> str:
        """渲染CSS模板，替换占位符"""
        replacements = {
            '{{page_width}}': str(self.page_width),
            '{{page_height}}': str(self.page_height),
            '{{card_background}}': 'rgba(255, 255, 255, 0.98)' if not is_dark else 'rgba(20, 20, 35, 0.98)',
            '{{shadow_color1}}': self.style_manager.add_alpha(theme.primary_color, 0.15),
            '{{shadow_color2}}': self.style_manager.add_alpha('#000000', 0.1),
            '{{page_info_bg}}': self.style_manager.add_alpha(theme.primary_color, 0.1),
            '{{page_info_border}}': self.style_manager.add_alpha(theme.primary_color, 0.2),
            '{{separator_color}}': self.style_manager.add_alpha(theme.text_color, 0.4),
            '{{total_color}}': self.style_manager.add_alpha(theme.text_color, 0.6),
            '{{deco_color1}}': self.style_manager.add_alpha(theme.primary_color, 0.1),
            '{{deco_color2}}': self.style_manager.add_alpha(theme.secondary_color, 0.1),
            '{{img_shadow}}': self.style_manager.add_alpha('#000000', 0.1)
        }
        for key, value in replacements.items():
            css = css.replace(key, value)
        return css
    
    def get_page_css(self) -> str:
        """已弃用：现在使用外部模板"""
        raise DeprecationWarning("Use generate() with external templates instead")
    
    def get_js(self) -> str:
        """已弃用：现在使用外部模板"""
        raise DeprecationWarning("Use generate() with external templates instead")