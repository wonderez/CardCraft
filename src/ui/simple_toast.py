#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简化的吐司提示实现
"""

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPalette, QColor


class SimpleToast(QWidget):
    """简化的吐司提示实现"""
    
    def __init__(self, message: str, parent=None):
        super().__init__(parent)
        
        # 设置窗口标志
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        
        # 创建UI
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        
        self.label = QLabel(message)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                background-color: rgba(40, 40, 40, 200);
                border-radius: 10px;
                padding: 10px 20px;
                border: 2px solid rgba(255, 255, 255, 50);
            }
        """)
        
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        # 设置透明度动画
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.0)
        self.setGraphicsEffect(self.opacity_effect)
        
        # 创建动画
        self.fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in.setDuration(300)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self.fade_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out.setDuration(500)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.setEasingCurve(QEasingCurve.Type.InCubic)
        
        # 连接动画完成信号
        self.fade_out.finished.connect(self.close)
        
        # 设置定时器
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.start_fade_out)
    
    def show_toast(self, parent=None, dialog_pos=None):
        """显示吐司提示"""
        # 调整大小
        self.adjustSize()
        
        # 设置位置
        if dialog_pos:
            # 使用进度对话框的位置
            x = dialog_pos.x() + (dialog_pos.width() - self.width()) // 2
            y = dialog_pos.y() + (dialog_pos.height() - self.height()) // 2
        elif parent:
            parent_rect = parent.geometry()
            x = parent_rect.x() + (parent_rect.width() - self.width()) // 2
            y = parent_rect.y() + parent_rect.height() - 150  # 距离底部150像素
        else:
            screen = QApplication.primaryScreen().geometry()
            x = (screen.width() - self.width()) // 2
            y = screen.height() - 150
        
        self.move(x, y)
        
        # 显示并开始淡入动画
        self.show()
        self.raise_()
        self.fade_in.start()
        
        # 启动定时器
        self.timer.start(3000)  # 3秒后开始淡出
    
    def start_fade_out(self):
        """开始淡出动画"""
        self.fade_out.start()


def show_simple_toast(parent=None, message: str = "", dialog_pos=None):
    """显示简化吐司提示的便捷函数"""
    toast = SimpleToast(message, parent)
    toast.show_toast(parent, dialog_pos)
    return toast