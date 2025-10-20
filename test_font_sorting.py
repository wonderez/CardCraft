#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试字体排序功能
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication, QComboBox, QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QFontDatabase
from src.utils.style_manager import StyleManager

class FontTestApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("字体排序功能测试")
        self.setGeometry(100, 100, 400, 300)
        
        self.style_manager = StyleManager()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # 说明标签
        info_label = QLabel("字体排序测试：\n1. 最近使用的5个字体排在最上面\n2. 中文字体排序靠前")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # 字体选择器
        self.font_selector = QComboBox()
        self.font_selector.setToolTip("字体选择")
        self.font_selector.setFixedWidth(350)
        
        # 获取系统字体
        font_families = QFontDatabase.families()
        
        # 获取最近使用的字体列表
        recent_fonts = self.style_manager.get_setting("recent_fonts", [])
        
        # 常用字体列表
        common_fonts = ["微软雅黑", "Arial", "Times New Roman", "宋体", "黑体", "SimSun", "SimHei"]
        added_fonts = set()
        
        # 1. 添加最近使用的字体（最多5个）
        if recent_fonts:
            for font in recent_fonts[:5]:  # 只取前5个
                if font in font_families and font not in added_fonts:
                    self.font_selector.addItem(font)
                    added_fonts.add(font)
            
            # 如果有最近使用的字体，添加分隔符
            if added_fonts:
                self.font_selector.insertSeparator(self.font_selector.count())
        
        # 2. 添加常用字体（如果还没添加）
        for font in common_fonts:
            if font in font_families and font not in added_fonts:
                self.font_selector.addItem(font)
                added_fonts.add(font)
        
        # 添加分隔符
        self.font_selector.insertSeparator(self.font_selector.count())
        
        # 3. 添加所有其他字体（中文字体优先）
        # 分离中文字体和其他字体
        chinese_fonts = []
        other_fonts = []
        
        for font in font_families:
            if font not in added_fonts:
                # 判断是否为中文字体（包含中文字符或常见中文字体名称）
                if any(char in font for char in "微软雅黑宋体黑体楷体仿宋体思源方正汉仪文泉驿等线圆体") or \
                   any(keyword in font for keyword in ["SimSun", "SimHei", "KaiTi", "FangSong", "Microsoft YaHei", "PingFang", "Hiragino", "Noto Sans CJK", "Source Han Sans", "WenQuanYi"]):
                    chinese_fonts.append(font)
                else:
                    other_fonts.append(font)
        
        # 先添加中文字体（按字母顺序排序）
        for font in sorted(chinese_fonts):
            self.font_selector.addItem(font)
        
        # 再添加其他字体（按字母顺序排序）
        for font in sorted(other_fonts):
            self.font_selector.addItem(font)
        
        # 连接信号
        self.font_selector.currentIndexChanged.connect(self.on_font_changed)
        
        layout.addWidget(self.font_selector)
        
        # 当前选择标签
        self.current_label = QLabel("当前选择: 无")
        layout.addWidget(self.current_label)
        
        # 最近使用的字体标签
        self.recent_label = QLabel("最近使用的字体: 无")
        layout.addWidget(self.recent_label)
        
        self.setLayout(layout)
    
    def on_font_changed(self, index):
        """处理字体改变"""
        font_family = self.font_selector.currentText()
        
        # 更新当前选择标签
        self.current_label.setText(f"当前选择: {font_family}")
        
        # 更新最近使用的字体列表
        recent_fonts = self.style_manager.get_setting("recent_fonts", [])
        
        # 如果字体已在列表中，先移除
        if font_family in recent_fonts:
            recent_fonts.remove(font_family)
        
        # 将字体添加到列表开头
        recent_fonts.insert(0, font_family)
        
        # 限制列表长度为最多5个
        recent_fonts = recent_fonts[:5]
        
        # 保存更新后的列表
        self.style_manager.save_setting("recent_fonts", recent_fonts)
        
        # 更新最近使用的字体标签
        self.recent_label.setText(f"最近使用的字体: {', '.join(recent_fonts)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FontTestApp()
    window.show()
    sys.exit(app.exec())