#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
直接测试吐司提示功能
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

# 导入吐司提示组件
from src.ui.toast import show_toast

class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("吐司提示测试")
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        
        # 添加测试按钮
        success_btn = QPushButton("测试成功提示")
        success_btn.clicked.connect(self.show_success_toast)
        
        error_btn = QPushButton("测试错误提示")
        error_btn.clicked.connect(self.show_error_toast)
        
        layout.addWidget(success_btn)
        layout.addWidget(error_btn)
        self.setLayout(layout)
    
    def show_success_toast(self):
        print("显示成功提示")
        show_toast(self, "✅ 这是一个成功提示！")
    
    def show_error_toast(self):
        print("显示错误提示")
        show_toast(self, "❌ 这是一个错误提示！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())