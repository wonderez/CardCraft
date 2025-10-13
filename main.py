# main.py
import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from src.ui.main_window import MainWindow

def main():
    # 启用高DPI支持
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # 使用 Fusion 风格
    
    # 设置应用程序图标
    icon_path = Path(__file__).parent / "resources" / "icons" / "app.ico"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    # 设置应用程序样式
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f5f5f7;
        }
    """)
    
    window = MainWindow()
    window.setWindowIcon(app.windowIcon())  # 设置窗口图标
    window.showMaximized()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()