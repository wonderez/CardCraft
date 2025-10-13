from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPalette, QColor


class ToastWidget(QWidget):
    """简化版自定义吐司提示组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        
        # 设置基本属性
        self.display_duration = 2000  # 显示时间2秒
        
        # 创建UI
        self.setup_ui()
        
        # 创建定时器
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide)
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(0)
        
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
            color: white;
            font-size: 14px;
            font-weight: 500;
        """)
        
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        # 设置默认样式
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 180);
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 30);
            }
        """)
    
    def show_message(self, message: str, parent=None):
        """显示消息"""
        print(f"Toast: 显示消息 - {message}")
        self.label.setText(message)
        
        # 调整大小
        self.adjustSize()
        print(f"Toast: 调整大小后 - 宽度: {self.width()}, 高度: {self.height()}")
        
        # 设置位置（如果提供了父窗口，则相对于父窗口居中）
        if parent:
            # 获取父窗口的全局位置
            if hasattr(parent, 'window'):
                parent_window = parent.window()
            else:
                parent_window = parent
                
            parent_rect = parent_window.geometry()
            x = parent_rect.x() + (parent_rect.width() - self.width()) // 2
            y = parent_rect.y() + parent_rect.height() - 100  # 距离底部100像素
            print(f"Toast: 父窗口位置 - x: {parent_rect.x()}, y: {parent_rect.y()}, 宽度: {parent_rect.width()}, 高度: {parent_rect.height()}")
            print(f"Toast: 计算后的吐司位置 - x: {x}, y: {y}")
        else:
            # 如果没有父窗口，则在屏幕底部居中
            screen = QApplication.primaryScreen().geometry()
            x = (screen.width() - self.width()) // 2
            y = screen.height() - 100
            print(f"Toast: 屏幕位置 - 宽度: {screen.width()}, 高度: {screen.height()}")
            print(f"Toast: 计算后的吐司位置 - x: {x}, y: {y}")
        
        self.move(x, y)
        
        # 显示
        self.show()
        self.raise_()
        print(f"Toast: 已调用show()和raise_()")
        
        # 启动显示计时器
        self.timer.start(self.display_duration)
        print(f"Toast: 已启动计时器，持续时间: {self.display_duration}ms")


def show_toast(parent=None, message: str = ""):
    """显示吐司提示的便捷函数"""
    toast = ToastWidget()
    toast.show_message(message, parent)
    return toast