import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QHBoxLayout
from PyQt6.QtCore import QTimer
from src.ui.toast import show_toast

class ToastTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("吐司提示显示测试")
        self.setGeometry(300, 300, 500, 300)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # 添加文本编辑器
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("输入要显示在吐司提示中的消息...")
        main_layout.addWidget(self.text_edit)
        
        # 添加按钮布局
        button_layout = QHBoxLayout()
        
        self.success_btn = QPushButton("显示成功提示")
        self.success_btn.clicked.connect(self.show_success_toast)
        button_layout.addWidget(self.success_btn)
        
        self.error_btn = QPushButton("显示错误提示")
        self.error_btn.clicked.connect(self.show_error_toast)
        button_layout.addWidget(self.error_btn)
        
        self.custom_btn = QPushButton("显示自定义提示")
        self.custom_btn.clicked.connect(self.show_custom_toast)
        button_layout.addWidget(self.custom_btn)
        
        main_layout.addLayout(button_layout)
        
        # 设置默认文本
        self.text_edit.setText("导出成功！\n文件大小: 1080×1440px")
    
    def show_success_toast(self):
        message = "✅ 导出成功！\n文件已保存到指定位置"
        show_toast(message, self)
    
    def show_error_toast(self):
        message = "❌ 导出失败！\n请检查文件路径是否正确"
        show_toast(message, self)
    
    def show_custom_toast(self):
        message = self.text_edit.toPlainText()
        if not message.strip():
            message = "这是一个自定义吐司提示"
        show_toast(message, self)

def main():
    app = QApplication(sys.argv)
    window = ToastTestWindow()
    window.show()
    
    # 延迟显示一个初始提示
    QTimer.singleShot(500, lambda: show_toast("欢迎使用吐司提示测试程序！", window))
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()