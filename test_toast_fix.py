#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import tempfile

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt6.QtCore import Qt
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from ui.toast import show_toast


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("吐司提示测试")
        self.setGeometry(100, 100, 400, 300)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 添加说明标签
        label = QLabel("点击下面的按钮测试吐司提示:")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        # 创建测试按钮
        success_btn = QPushButton("显示成功提示")
        success_btn.clicked.connect(self.show_success_toast)
        layout.addWidget(success_btn)
        
        error_btn = QPushButton("显示错误提示")
        error_btn.clicked.connect(self.show_error_toast)
        layout.addWidget(error_btn)
        
        export_success_btn = QPushButton("显示导出成功提示")
        export_success_btn.clicked.connect(self.show_export_success_toast)
        layout.addWidget(export_success_btn)
        
        # 测试定时器
        self.test_counter = 0
    
    def show_success_toast(self):
        show_toast(self, "✅ 操作成功完成!")
    
    def show_error_toast(self):
        show_toast(self, "❌ 操作失败，请重试")
    
    def show_export_success_toast(self):
        show_toast(self, "✅ 图片导出成功!\nSize: medium: 1080×1440px")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = TestWindow()
    window.show()
    
    print("测试窗口已显示")
    sys.exit(app.exec())