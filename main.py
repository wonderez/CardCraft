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
    
    # 检查是否有命令行参数（文件路径）
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.exists(file_path) and os.path.isfile(file_path):
            # 延迟加载文件，确保窗口已完全初始化
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(100, lambda: load_file_to_window(window, file_path))
    
    sys.exit(app.exec())

def load_file_to_window(window, file_path):
    """将文件内容加载到窗口中"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            window.editor.set_text(content)
            window.status_bar.showMessage(f"已打开文件: {file_path}", 3000)
    except Exception as e:
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.critical(
            window, "打开文件失败",
            f"无法打开文件:\n{str(e)}",
            QMessageBox.StandardButton.Ok
        )
        window.status_bar.showMessage("❌ 打开文件失败", 3000)

if __name__ == "__main__":
    main()