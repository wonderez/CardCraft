import sys
import os
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import QTimer

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ui.toast import show_toast

class ToastTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("吐司提示调试测试")
        self.setGeometry(200, 200, 400, 300)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 说明标签
        info_label = QLabel("点击下面的按钮测试吐司提示功能：")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # 成功提示按钮
        success_btn = QPushButton("显示成功提示")
        success_btn.clicked.connect(self.show_success_toast)
        layout.addWidget(success_btn)
        
        # 错误提示按钮
        error_btn = QPushButton("显示错误提示")
        error_btn.clicked.connect(self.show_error_toast)
        layout.addWidget(error_btn)
        
        # 导出成功提示按钮
        export_success_btn = QPushButton("显示导出成功提示")
        export_success_btn.clicked.connect(self.show_export_success_toast)
        layout.addWidget(export_success_btn)
        
        # 定时显示提示按钮
        auto_show_btn = QPushButton("5秒后自动显示提示")
        auto_show_btn.clicked.connect(self.schedule_toast)
        layout.addWidget(auto_show_btn)
    
    def show_success_toast(self):
        print("显示成功提示...")
        toast = show_toast("✅ 操作成功！", self)
        print(f"吐司对象创建成功: {toast}")
    
    def show_error_toast(self):
        print("显示错误提示...")
        toast = show_toast("❌ 操作失败！请重试", self)
        print(f"吐司对象创建成功: {toast}")
    
    def show_export_success_toast(self):
        print("显示导出成功提示...")
        toast = show_toast("✅ 导出成功！\n已保存到指定文件夹\nSize: medium: 1080×1440px", self)
        print(f"吐司对象创建成功: {toast}")
    
    def schedule_toast(self):
        print("设置5秒后显示提示...")
        QTimer.singleShot(5000, self.show_timed_toast)
    
    def show_timed_toast(self):
        print("显示定时提示...")
        toast = show_toast("⏰ 定时提示消息", self)
        print(f"吐司对象创建成功: {toast}")

def main():
    app = QApplication(sys.argv)
    window = ToastTestWindow()
    window.show()
    print("测试窗口已显示")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()