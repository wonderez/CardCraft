import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from src.ui.toast import show_toast

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Toast Test")
        self.setGeometry(100, 100, 300, 200)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 成功提示按钮
        success_btn = QPushButton("显示成功提示")
        success_btn.clicked.connect(self.show_success_toast)
        layout.addWidget(success_btn)
        
        # 错误提示按钮
        error_btn = QPushButton("显示错误提示")
        error_btn.clicked.connect(self.show_error_toast)
        layout.addWidget(error_btn)
    
    def show_success_toast(self):
        show_toast("✅ 导出成功！\n已保存到指定文件夹", self)
    
    def show_error_toast(self):
        show_toast("❌ 导出失败！\n请检查文件权限", self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())