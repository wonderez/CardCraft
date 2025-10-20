import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from src.ui.toast import show_toast

class ToastTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("吐司提示测试")
        self.setGeometry(300, 300, 400, 200)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        self.test_btn = QPushButton("显示吐司提示")
        self.test_btn.clicked.connect(self.show_toast_message)
        layout.addWidget(self.test_btn)
    
    def show_toast_message(self):
        show_toast("这是一个测试吐司提示！", self)

def main():
    app = QApplication(sys.argv)
    window = ToastTestWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()