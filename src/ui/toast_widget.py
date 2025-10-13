# ============================================
# src/ui/toast_widget.py
# ============================================
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QApplication
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, QPoint, pyqtSignal
from PyQt6.QtGui import QPalette, QColor, QPainter, QFont


class ToastWidget(QWidget):
    """自定义吐司提示组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool |
            Qt.WindowType.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
        
        # 设置默认属性
        self.duration = 3000  # 显示时间（毫秒）
        self.animation_duration = 300  # 动画时间（毫秒）
        
        # 初始化UI
        self.init_ui()
        
        # 初始化动画
        self.init_animations()
        
        # 初始化定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.hide_toast)
        
    def init_ui(self):
        """初始化UI"""
        # 主容器
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 消息容器
        self.container = QWidget()
        self.container.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 40, 220);
                border: 1px solid rgba(0, 224, 255, 0.3);
                border-radius: 8px;
                padding: 12px 20px;
            }
        """)
        
        container_layout = QHBoxLayout(self.container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        
        # 消息标签
        self.message_label = QLabel()
        self.message_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 14px;
                font-weight: 500;
            }
        """)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setWordWrap(True)
        
        container_layout.addWidget(self.message_label)
        main_layout.addWidget(self.container)
        
    def init_animations(self):
        """初始化动画"""
        # 淡入动画
        self.fade_in_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_anim.setDuration(self.animation_duration)
        self.fade_in_anim.setStartValue(0.0)
        self.fade_in_anim.setEndValue(1.0)
        self.fade_in_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # 淡出动画
        self.fade_out_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out_anim.setDuration(self.animation_duration)
        self.fade_out_anim.setStartValue(1.0)
        self.fade_out_anim.setEndValue(0.0)
        self.fade_out_anim.setEasingCurve(QEasingCurve.Type.InCubic)
        self.fade_out_anim.finished.connect(self.on_fade_out_finished)
        
    def show_toast(self, message, duration=None, parent=None):
        """显示吐司提示"""
        # 设置消息文本
        self.message_label.setText(message)
        
        # 设置显示时间
        if duration is not None:
            self.duration = duration
            
        # 调整大小
        self.adjustSize()
        
        # 设置位置
        self.position_toast(parent)
        
        # 显示并开始动画
        self.show()
        self.fade_in_anim.start()
        
        # 启动定时器
        self.timer.start(self.duration)
        
    def position_toast(self, parent=None):
        """定位吐司提示"""
        if parent:
            # 相对于父窗口居中显示
            parent_rect = parent.geometry()
            x = parent_rect.x() + (parent_rect.width() - self.width()) // 2
            y = parent_rect.y() + parent_rect.height() - self.height() - 50
            self.move(x, y)
        else:
            # 在屏幕底部居中显示
            screen = QApplication.primaryScreen().geometry()
            x = (screen.width() - self.width()) // 2
            y = screen.height() - self.height() - 50
            self.move(x, y)
            
    def hide_toast(self):
        """隐藏吐司提示"""
        self.timer.stop()
        self.fade_out_anim.start()
        
    def on_fade_out_finished(self):
        """淡出动画完成后的处理"""
        self.hide()
        
    def paintEvent(self, event):
        """绘制事件 - 添加阴影效果"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制阴影
        for i in range(10):
            alpha = 20 - i * 2
            if alpha <= 0:
                break
            color = QColor(0, 0, 0, alpha)
            painter.setPen(color)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(
                QRect(
                    5 - i // 2,
                    5 - i // 2,
                    self.width() - 10 + i,
                    self.height() - 10 + i
                ),
                8,
                8
            )