#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from ui.toast import show_toast

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("吐司提示测试")
        self.setGeometry(100, 100, 300, 200)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        test_btn = QPushButton("测试吐司提示")
        test_btn.clicked.connect(self.show_toast)
        layout.addWidget(test_btn)
    
    def show_toast(self):
        show_toast(self, "这是一个测试吐司提示！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())