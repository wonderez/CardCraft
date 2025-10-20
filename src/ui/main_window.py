# ============================================
# src/ui/main_window.py - 增强版工具栏
# ============================================
from PyQt6.QtWidgets import (QMainWindow, QHBoxLayout, QVBoxLayout, 
                               QWidget, QToolBar, QSplitter, QPushButton,
                               QFileDialog, QMessageBox, QStatusBar, QLabel,
                               QGraphicsDropShadowEffect, QComboBox, QFrame,
                               QToolButton, QMenu, QDialog, QTextEdit,
                               QDialogButtonBox, QSpinBox, QGridLayout, QLineEdit)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, QRectF, QSize, QPoint, QPointF
from PyQt6.QtGui import QAction, QIcon, QColor, QLinearGradient, QRadialGradient, QPainter, QBrush, QKeySequence, QTextCursor, QFontDatabase, QPainterPath
from src.ui.editor_widget import EditorWidget
from src.ui.preview_widget import PreviewWidget
from src.utils.style_manager import StyleManager
import re

class ModernGradientBackground(QWidget):
    """现代化渐变背景组件 - 包含粒子系统和多层次渐变"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ModernGradientBackground")
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setMouseTracking(False)
        
        # 确保背景填充整个父窗口
        if parent:
            self.setGeometry(0, 0, parent.width(), parent.height())
        
        # 动画计时器
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update)
        self.animation_timer.start(16)  # 约60fps，更快更流畅
        
        # 背景参数
        self.gradient_offset = 0
        
        # 粒子系统
        self.particles = []
        self.init_particles(50)  # 初始化50个粒子
    
    def init_particles(self, count):
        """初始化粒子系统"""
        import random
        for _ in range(count):
            particle = {
                'x': 0,
                'y': 0,
                'size': 1,
                'speed': 0.5,
                'angle': 0,
                'color': QColor(255, 255, 255, 100),
                'lifetime': 100
            }
            self.particles.append(particle)
    
    def reset_particle(self, particle, width, height):
        """重置粒子状态"""
        import random
        import math
        # 随机位置，但更倾向于边缘
        edge = random.randint(0, 3)  # 0:上, 1:右, 2:下, 3:左
        if edge == 0:
            particle['x'] = random.randint(0, width)
            particle['y'] = 0
        elif edge == 1:
            particle['x'] = width
            particle['y'] = random.randint(0, height)
        elif edge == 2:
            particle['x'] = random.randint(0, width)
            particle['y'] = height
        else:
            particle['x'] = 0
            particle['y'] = random.randint(0, height)
        
        # 随机大小（1-4像素）
        particle['size'] = random.uniform(1, 4)
        
        # 随机速度（0.2-1.5像素/帧）
        particle['speed'] = random.uniform(0.5, 2.5)
        
        # 随机方向（指向窗口内部）
        center_x, center_y = width / 2, height / 2
        dx, dy = center_x - particle['x'], center_y - particle['y']
        dist = (dx**2 + dy**2)**0.5 if dx != 0 or dy != 0 else 1
        particle['angle'] = math.atan2(dy, dx)
        
        # 随机透明度（30-100）
        opacity = random.randint(30, 100)
        
        # 基于角度选择颜色
        hue = ((self.gradient_offset / 360) + random.uniform(0, 0.3)) % 1
        particle['color'] = QColor.fromHsvF(hue, random.uniform(0.6, 0.9), random.uniform(0.7, 1.0), opacity/255)
        
        # 随机生命周期（100-300帧）
        particle['lifetime'] = random.randint(50, 200)
    
    def update_particles(self, width, height):
        """更新粒子位置和状态"""
        import math
        for particle in self.particles:
            # 更新位置
            particle['x'] += math.cos(particle['angle']) * particle['speed']
            particle['y'] += math.sin(particle['angle']) * particle['speed']
            
            # 减少生命周期
            particle['lifetime'] -= 1
            
            # 如果粒子离开窗口或生命周期结束，重置
            if (particle['x'] < -50 or particle['x'] > width + 50 or
                particle['y'] < -50 or particle['y'] > height + 50 or
                particle['lifetime'] <= 0):
                self.reset_particle(particle, width, height)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        # 获取窗口大小
        width = self.width()
        height = self.height()
        
        # 确保粒子系统有足够的粒子
        import random
        if len(self.particles) < 50:
            self.init_particles(50 - len(self.particles))
        
        # 更新粒子
        self.update_particles(width, height)
        
        # 创建多层次渐变背景
        # 1. 基础层 - 深色调底色
        base_gradient = QLinearGradient(0, 0, width, height)
        base_gradient.setColorAt(0, QColor(10, 10, 25, 255))
        base_gradient.setColorAt(1, QColor(20, 15, 40, 255))
        painter.fillRect(self.rect(), base_gradient)
        
        # 2. 动态渐变层 - 柔和的彩色光带
        # 计算HSV颜色变化
        hue1 = (180 + self.gradient_offset) % 360 / 360
        hue2 = (280 + self.gradient_offset) % 360 / 360
        hue3 = (320 + self.gradient_offset) % 360 / 360
        
        # 主光带 - 从左上角到右下角
        main_glow = QLinearGradient(0, 0, width, height)
        main_glow.setColorAt(0, QColor.fromHsvF(hue1, 0.4, 0.2, 0.8))
        main_glow.setColorAt(0.5, QColor.fromHsvF(hue2, 0.4, 0.3, 0.8))
        main_glow.setColorAt(1, QColor.fromHsvF(hue3, 0.4, 0.2, 0.8))
        
        # 次光带 - 从右上角到左下角
        secondary_glow = QLinearGradient(width, 0, 0, height)
        secondary_glow.setColorAt(0, QColor.fromHsvF((hue1 + 180) % 1, 0.4, 0.2, 0.5))
        secondary_glow.setColorAt(0.5, QColor.fromHsvF((hue2 + 180) % 1, 0.4, 0.3, 0.5))
        secondary_glow.setColorAt(1, QColor.fromHsvF((hue3 + 180) % 1, 0.4, 0.2, 0.5))
        
        # 创建发光层
        glow_layer = QPainterPath()
        glow_layer.addRect(QRectF(self.rect()))
        
        # 绘制主光带（70%透明度）
        painter.setOpacity(0.7)
        painter.fillPath(glow_layer, main_glow)
        
        # 绘制次光带（40%透明度）
        painter.setOpacity(0.4)
        painter.fillPath(glow_layer, secondary_glow)
        
        # 3. 光晕层 - 柔和的光斑效果
        painter.setOpacity(0.4)
        for i in range(8):  # 8个大光斑
            # 计算光晕位置（缓慢移动）
            x = int(width * (0.1 + 0.8 * ((i * 7 + self.gradient_offset * 0.04) % 1)))
            y = int(height * (0.1 + 0.8 * ((i * 11 + self.gradient_offset * 0.06) % 1)))
            size = 150 + 200 * ((i * 13 + self.gradient_offset * 0.02) % 1)
            
            # 创建径向渐变光晕
            halo_gradient = QRadialGradient(x, y, size, x, y)
            halo_hue = (hue1 + i * 0.12) % 1
            halo_gradient.setColorAt(0, QColor.fromHsvF(halo_hue, 0.6, 0.8, 0.7))
            halo_gradient.setColorAt(0.3, QColor.fromHsvF(halo_hue, 0.6, 0.6, 0.4))
            halo_gradient.setColorAt(1, QColor(0, 0, 0, 0))
            
            painter.setBrush(halo_gradient)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPoint(x, y), int(size), int(size))
        
        # 4. 粒子层
        painter.setOpacity(1.0)
        for particle in self.particles:
            # 根据生命周期计算透明度衰减
            alpha = particle['color'].alpha() * (particle['lifetime'] / 200)
            draw_color = QColor(particle['color'])
            draw_color.setAlpha(int(alpha))
            
            # 绘制粒子
            painter.setBrush(draw_color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(
                QPointF(particle['x'], particle['y']), 
                particle['size'], 
                particle['size']
            )
        
        # 更新偏移（更缓慢，更自然）
        self.gradient_offset = (self.gradient_offset + 1.0) % 360

class TableDialog(QDialog):
    """插入表格对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📊 插入表格")
        self.setFixedSize(300, 150)
        self.init_ui()
        
    def init_ui(self):
        layout = QGridLayout(self)
        
        # 行数
        layout.addWidget(QLabel("行数:"), 0, 0)
        self.rows_spin = QSpinBox()
        self.rows_spin.setRange(2, 20)
        self.rows_spin.setValue(3)
        layout.addWidget(self.rows_spin, 0, 1)
        
        # 列数
        layout.addWidget(QLabel("列数:"), 1, 0)
        self.cols_spin = QSpinBox()
        self.cols_spin.setRange(2, 10)
        self.cols_spin.setValue(3)
        layout.addWidget(self.cols_spin, 1, 1)
        
        # 按钮
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons, 2, 0, 1, 2)
        
        self.setStyleSheet("""
            QDialog {
                background: rgba(30, 30, 50, 0.95);
            }
            QLabel {
                color: white;
                font-size: 13px;
            }
            QSpinBox {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
                padding: 5px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.15);
            }
        """)

class LinkDialog(QDialog):
    """插入链接对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔗 插入链接")
        self.setFixedSize(400, 180)
        self.init_ui()
        
    def init_ui(self):
        layout = QGridLayout(self)
        
        # 链接文字
        layout.addWidget(QLabel("链接文字:"), 0, 0)
        self.text_edit = QLineEdit()
        self.text_edit.setPlaceholderText("输入显示的文字")
        layout.addWidget(self.text_edit, 0, 1)
        
        # 链接地址
        layout.addWidget(QLabel("链接地址:"), 1, 0)
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("https://example.com")
        layout.addWidget(self.url_edit, 1, 1)
        
        # 按钮
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons, 2, 0, 1, 2)
        
        self.setStyleSheet("""
            QDialog {
                background: rgba(30, 30, 50, 0.95);
            }
            QLabel {
                color: white;
                font-size: 13px;
            }
            QLineEdit {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
                padding: 5px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.15);
            }
        """)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 先创建自动更新计时器
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_preview)
        self.update_timer.setInterval(300)  # 300ms延迟
        
        # 初始化样式管理器
        self.style_manager = StyleManager()
        
        # 然后初始化UI
        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("✨ CardCraft - Markdown转精美卡片编辑器")
        self.setGeometry(100, 100, 1700, 950)
        self.setMinimumSize(1200, 700)
        
        # 创建菜单栏
        # self.create_menu_bar()  # 隐藏菜单栏，按用户要求
        
        # 创建主容器
        main_container = QWidget()
        self.setCentralWidget(main_container)
        
        # 创建极光背景
        self.modern_bg = ModernGradientBackground(main_container)
        # 确保背景填充整个窗口
        self.modern_bg.setGeometry(0, 0, main_container.width(), main_container.height())
        self.modern_bg.lower()
        
        # 主布局
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 应用全局样式
        self.setStyleSheet(self.get_global_styles_qt_compatible())
        
        # 创建编辑器和预览组件
        self.editor = EditorWidget()
        self.preview = PreviewWidget()
        
        # 创建左侧工具栏和右侧工具栏
        self.toolbar_container, self.right_toolbar = self.create_enhanced_toolbar()
        
        # 创建内容区域
        content_area = QWidget()
        content_area.setObjectName("contentArea")
        content_layout = QHBoxLayout(content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setObjectName("mainSplitter")
        
        # 为组件添加玻璃容器，将工具栏传递给相应容器
        editor_container = self.create_glass_container(self.editor, "📝 Markdown 编辑器")  # 不传递工具栏，隐藏左侧工具栏
        preview_container = self.create_glass_container(self.preview, "👀 实时预览", self.right_toolbar)
        
        # 将容器添加到分割器中
        splitter.addWidget(editor_container)
        splitter.addWidget(preview_container)
        
        # 设置分割器初始比例
        splitter.setSizes([850, 850])
        
        content_layout.addWidget(splitter)
        main_layout.addWidget(content_area, 1)
        
        # 创建底部状态栏
        self.create_status_bar()
        
        # 初始更新
        self.update_preview()
        self.update_char_count()
        
        # 确保背景在最底层
        self.modern_bg.lower()
        
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件')
        
        # 打开文件动作
        open_action = QAction('打开', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        # 添加分隔线
        file_menu.addSeparator()
        
        # 退出动作
        exit_action = QAction('退出', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
    def create_enhanced_toolbar(self):
        """创建增强版工具栏，返回左侧工具栏和右侧工具栏"""
        # 创建左侧工具栏（编辑器使用）
        left_toolbar = QFrame()
        left_toolbar.setObjectName("toolbarContainer")
        left_toolbar.setFixedHeight(40)  # 从55减小到40
        
        left_layout = QHBoxLayout(left_toolbar)
        left_layout.setContentsMargins(10, 5, 10, 5)  # 减小边距
        left_layout.setSpacing(8)  # 减小间距
        
        # 左侧：基础格式化按钮组
        format_group = QFrame()
        format_group.setObjectName("buttonGroup")
        format_layout = QHBoxLayout(format_group)
        format_layout.setContentsMargins(8, 3, 8, 3)
        format_layout.setSpacing(5)
        
        # 基础格式化按钮 - 使用简洁符号
        basic_buttons = [
            ("B", "加粗 (Ctrl+B)", self.insert_bold, True, False),
            ("I", "斜体 (Ctrl+I)", self.insert_italic, False, True),
            ("S", "删除线", self.insert_strikethrough, False, False),
            ("</>", "代码", self.insert_inline_code, False, False),
            ("{}", "代码块", self.insert_code_block, False, False),
        ]
        
        for text, tooltip, callback, is_bold, is_italic in basic_buttons:
            btn = QToolButton()
            btn.setText(text)
            btn.setToolTip(tooltip)
            btn.clicked.connect(callback)
            btn.setFixedSize(28, 28)  # 从35x35减小到28x28
            
            # 设置字体样式
            font = btn.font()
            font.setFamily("Consolas, monospace")  # 使用等宽字体
            font.setPointSize(9)  # 减小字体大小
            if is_bold:
                font.setBold(True)
            if is_italic:
                font.setItalic(True)
            btn.setFont(font)
            
            btn.setStyleSheet(self.get_tool_button_style())
            format_layout.addWidget(btn)
        
        left_layout.addWidget(format_group)
        
        # 添加分隔线
        separator1 = self.create_separator()
        left_layout.addWidget(separator1)
        
        # 中间左：标题选择器
        heading_group = QFrame()
        heading_layout = QHBoxLayout(heading_group)
        heading_layout.setContentsMargins(0, 0, 0, 0)
        heading_layout.setSpacing(8)
        
        heading_label = QLabel("标题:")
        heading_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        heading_layout.addWidget(heading_label)
        
        self.heading_selector = QComboBox()
        self.heading_selector.setFixedWidth(100)
        self.heading_selector.addItems([
            "正文",
            "H1 一级标题",
            "H2 二级标题", 
            "H3 三级标题",
            "H4 四级标题",
            "H5 五级标题",
            "H6 六级标题"
        ])
        self.heading_selector.setCurrentIndex(0)
        self.heading_selector.setStyleSheet(self.get_mini_combobox_style())
        heading_layout.addWidget(self.heading_selector)
        
        left_layout.addWidget(heading_group)
        
        # 中间右：列表和链接按钮组
        list_group = QFrame()
        list_group.setObjectName("buttonGroup")
        list_layout = QHBoxLayout(list_group)
        list_layout.setContentsMargins(8, 3, 8, 3)
        list_layout.setSpacing(5)
        
        # 列表和链接按钮 - 使用简洁符号
        list_buttons = [
            ("•", "无序列表", self.insert_unordered_list),
            ("1.", "有序列表", self.insert_ordered_list),
            ("🔗", "链接", self.insert_link),
            ("📷", "图片", self.insert_image),
            ("⊞", "表格", self.insert_table),
            (">", "引用", self.insert_quote),
            ("—", "分隔线", self.insert_divider),
        ]
        
        for text, tooltip, callback in list_buttons:
            btn = QToolButton()
            btn.setText(text)
            btn.setToolTip(tooltip)
            btn.clicked.connect(callback)
            btn.setFixedSize(28, 28)  # 从35x35减小到28x28
            
            # 设置字体样式
            font = btn.font()
            font.setFamily("Consolas, monospace")  # 使用等宽字体
            font.setPointSize(9)  # 减小字体大小
            btn.setFont(font)
            
            btn.setStyleSheet(self.get_tool_button_style())
            list_layout.addWidget(btn)
        
        left_layout.addWidget(list_group)
        
        # 添加分隔线
        separator2 = self.create_separator()
        left_layout.addWidget(separator2)
        
        # 操作按钮组
        action_group = QFrame()
        action_group.setObjectName("buttonGroup")
        action_layout = QHBoxLayout(action_group)
        action_layout.setContentsMargins(5, 2, 5, 2)  # 减小边距
        action_layout.setSpacing(5)  # 减小间距
        
        # 撤销/重做
        undo_btn = QPushButton("↶")
        undo_btn.setToolTip("撤销 (Ctrl+Z)")
        undo_btn.clicked.connect(self.editor.undo)
        undo_btn.setFixedSize(28, 28)  # 从35x35减小到28x28
        
        # 设置字体样式
        font = undo_btn.font()
        font.setFamily("Consolas, monospace")  # 使用等宽字体
        font.setPointSize(9)  # 减小字体大小
        undo_btn.setFont(font)
        
        undo_btn.setStyleSheet(self.get_action_button_style())
        action_layout.addWidget(undo_btn)

        redo_btn = QPushButton("↷")
        redo_btn.setToolTip("重做 (Ctrl+Y)")
        redo_btn.clicked.connect(self.editor.redo)
        redo_btn.setFixedSize(28, 28)  # 从35x35减小到28x28
        
        # 设置字体样式
        font = redo_btn.font()
        font.setFamily("Consolas, monospace")  # 使用等宽字体
        font.setPointSize(9)  # 减小字体大小
        redo_btn.setFont(font)
        
        redo_btn.setStyleSheet(self.get_action_button_style())
        action_layout.addWidget(redo_btn)

        # 清空
        clear_btn = QPushButton("×")  # 使用更简洁的符号
        clear_btn.setToolTip("清空所有内容")
        clear_btn.clicked.connect(self.clear_content)
        clear_btn.setFixedSize(28, 28)  # 从35x35减小到28x28
        
        # 设置字体样式
        font = clear_btn.font()
        font.setFamily("Consolas, monospace")  # 使用等宽字体
        font.setPointSize(9)  # 减小字体大小
        clear_btn.setFont(font)
        
        clear_btn.setStyleSheet(self.get_action_button_style())
        action_layout.addWidget(clear_btn)
        
        left_layout.addWidget(action_group)
        
        # 添加弹性空间
        left_layout.addStretch()
        
        # 左侧工具栏不需要主题选择器，它将移到右侧
        
        # 创建右侧工具栏（预览使用）
        right_toolbar = QFrame()
        right_toolbar.setObjectName("embeddedToolbarContainer")
        right_toolbar.setFixedHeight(45)
        
        right_layout = QHBoxLayout(right_toolbar)
        right_layout.setContentsMargins(15, 5, 15, 5)
        right_layout.setSpacing(10)
        
        # 主题选择器（不显示标签）
        self.theme_selector = QComboBox()
        self.theme_selector.setToolTip("主题选择")
        self.theme_selector.setFixedWidth(120)
        themes = self.style_manager.get_theme_display_names()
        for key, name in themes.items():
            self.theme_selector.addItem(name, key)
        self.theme_selector.setCurrentText("CardCraft Classic")
        self.theme_selector.setStyleSheet(self.get_combobox_style())
        right_layout.addWidget(self.theme_selector)
        
        # 尺寸选择器（不显示标签）
        self.size_selector = QComboBox()
        self.size_selector.setToolTip("尺寸选择")
        self.size_selector.setFixedWidth(80)
        self.size_selector.addItems(["720p", "1080p", "1440p"])
        self.size_selector.setCurrentIndex(1)  # 默认选择"1080p"
        self.size_selector.setStyleSheet(self.get_combobox_style())
        right_layout.addWidget(self.size_selector)
        
        # 添加分隔线
        right_separator1 = self.create_separator()
        right_layout.addWidget(right_separator1)
        
        # 字体选择器（不显示标签）
        self.font_selector = QComboBox()
        self.font_selector.setToolTip("字体选择")
        self.font_selector.setFixedWidth(100)
        self.font_selector.setStyleSheet(self.get_combobox_style())
        
        # 获取系统字体
        from PyQt6.QtGui import QFontInfo
        font_families = QFontDatabase.families()
        
        # 获取最近使用的字体列表
        recent_fonts = self.style_manager.get_setting("recent_fonts", [])
        
        # 常用字体列表
        common_fonts = ["微软雅黑", "Arial", "Times New Roman", "宋体", "黑体", "SimSun", "SimHei"]
        added_fonts = set()
        
        # 1. 添加最近使用的字体（最多5个）
        if recent_fonts:
            for font in recent_fonts[:5]:  # 只取前5个
                if font in font_families and font not in added_fonts:
                    self.font_selector.addItem(font)
                    added_fonts.add(font)
            
            # 如果有最近使用的字体，添加分隔符
            if added_fonts:
                self.font_selector.insertSeparator(self.font_selector.count())
        
        # 2. 添加常用字体（如果还没添加）
        for font in common_fonts:
            if font in font_families and font not in added_fonts:
                self.font_selector.addItem(font)
                added_fonts.add(font)
        
        # 添加分隔符
        self.font_selector.insertSeparator(self.font_selector.count())
        
        # 3. 添加所有其他字体（中文字体优先）
        # 分离中文字体和其他字体
        chinese_fonts = []
        other_fonts = []
        
        for font in font_families:
            if font not in added_fonts:
                # 判断是否为中文字体（包含中文字符或常见中文字体名称）
                if any(char in font for char in "微软雅黑宋体黑体楷体仿宋体思源方正汉仪文泉驿等线圆体") or \
                   any(keyword in font for keyword in ["SimSun", "SimHei", "KaiTi", "FangSong", "Microsoft YaHei", "PingFang", "Hiragino", "Noto Sans CJK", "Source Han Sans", "WenQuanYi"]):
                    chinese_fonts.append(font)
                else:
                    other_fonts.append(font)
        
        # 先添加中文字体（按字母顺序排序）
        for font in sorted(chinese_fonts):
            self.font_selector.addItem(font)
        
        # 再添加其他字体（按字母顺序排序）
        for font in sorted(other_fonts):
            self.font_selector.addItem(font)
        
        # 从设置中加载上次选择的字体
        saved_font = self.style_manager.get_setting("font_family", "微软雅黑")
        font_index = self.font_selector.findText(saved_font)
        if font_index >= 0:
            self.font_selector.setCurrentIndex(font_index)
        
        right_layout.addWidget(self.font_selector)
        
        # 字体大小选择器（不显示标签）
        self.font_size_selector = QComboBox()
        self.font_size_selector.setToolTip("字体大小选择")
        self.font_size_selector.setFixedWidth(80)
        self.font_size_selector.addItems(["小", "标准", "大", "超大", "最大"])
        self.font_size_selector.setCurrentIndex(1)  # 默认选择"标准"
        self.font_size_selector.setStyleSheet(self.get_combobox_style())
        
        # 从设置中加载上次选择的字体大小
        saved_font_size = self.style_manager.get_setting("font_size", "标准")
        font_size_index = self.font_size_selector.findText(saved_font_size)
        if font_size_index >= 0:
            self.font_size_selector.setCurrentIndex(font_size_index)
        
        right_layout.addWidget(self.font_size_selector)
        
        # 图片优化选择器（不显示标签）
        self.image_quality_selector = QComboBox()
        self.image_quality_selector.setToolTip("图片优化选择")
        self.image_quality_selector.setFixedWidth(80)
        self.image_quality_selector.addItems(["不优化", "优化", "超级优化"])
        self.image_quality_selector.setCurrentIndex(1)  # 默认选择"优化"
        self.image_quality_selector.setStyleSheet(self.get_combobox_style())
        right_layout.addWidget(self.image_quality_selector)
        
        # 添加分隔线
        right_separator = self.create_separator()
        right_layout.addWidget(right_separator)
        
        # 导出按钮（简化文本）
        self.export_btn = QPushButton("导出")
        self.export_btn.setToolTip("导出图片")
        self.export_btn.clicked.connect(self.export_images)
        self.export_btn.setStyleSheet(self.get_export_button_style())
        right_layout.addWidget(self.export_btn)
        
        # 连接标题选择器信号
        self.heading_selector.currentIndexChanged.connect(self.on_heading_changed)
        
        return left_toolbar, right_toolbar
    
    def create_separator(self):
        """创建分隔线"""
        separator = QFrame()
        separator.setFrameStyle(QFrame.Shape.VLine | QFrame.Shadow.Sunken)
        separator.setStyleSheet("background: rgba(255, 255, 255, 0.1);")
        separator.setFixedWidth(1)
        return separator
    
    def get_tool_button_style(self):
        """工具按钮样式 - 简洁无装饰，图标居中"""
        return """
            QToolButton {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                color: white;
                border-radius: 4px;
                font-size: 11px;
                font-weight: normal;
                padding: 2px;
                text-align: center;
            }
            QToolButton:hover {
                background: rgba(0, 255, 136, 0.1);
                border-color: rgba(0, 255, 136, 0.3);
                color: #00ff88;
            }
            QToolButton:pressed {
                background: rgba(0, 255, 136, 0.2);
            }
        """
    
    def get_action_button_style(self):
        """操作按钮样式 - 简洁无装饰，图标居中"""
        return """
            QPushButton {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                color: white;
                border-radius: 4px;
                font-size: 11px;
                font-weight: normal;
                text-align: center;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.08);
                border-color: rgba(255, 255, 255, 0.2);
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.12);
            }
        """
    
    def get_mini_combobox_style(self):
        """迷你下拉框样式"""
        return """
            QComboBox {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
                padding: 5px 8px;
                border-radius: 6px;
                font-size: 12px;
            }
            QComboBox:hover {
                background: rgba(255, 255, 255, 0.12);
            }
            QComboBox::drop-down {
                border: none;
                width: 16px;
            }
            QComboBox::down-arrow {
                image: none;
                border-style: solid;
                border-width: 3px 3px 0 3px;
                border-color: white transparent transparent transparent;
            }
            QComboBox QAbstractItemView {
                background: rgba(30, 30, 50, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
                selection-background-color: rgba(0, 255, 136, 0.3);
                padding: 5px;
            }
        """
    
    def get_export_button_style(self):
        """导出按钮样式"""
        return """
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 rgba(0, 255, 136, 0.3),
                    stop: 1 rgba(0, 255, 200, 0.3));
                border: 2px solid #00ff88;
                color: #00ff88;
                padding: 8px 20px;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 rgba(0, 255, 136, 0.4),
                    stop: 1 rgba(0, 255, 200, 0.4));
            }
            QPushButton:pressed {
                background: rgba(0, 255, 136, 0.5);
            }
        """
    
    def get_combobox_style(self):
        """下拉框样式"""
        return """
            QComboBox {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
                padding: 5px 10px;
                border-radius: 8px;
                font-size: 13px;
            }
            QComboBox:hover {
                background: rgba(255, 255, 255, 0.12);
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-style: solid;
                border-width: 4px 4px 0 4px;
                border-color: white transparent transparent transparent;
            }
            QComboBox QAbstractItemView {
                background: rgba(30, 30, 50, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
                selection-background-color: rgba(0, 255, 136, 0.3);
                padding: 5px;
            }
        """
    
    # ===== 编辑器操作方法 =====
    
    def on_heading_changed(self, index):
        """处理标题选择改变"""
        cursor = self.editor.editor.textCursor()
        cursor.movePosition(QTextCursor.StartOfLine)
        
        # 获取当前行文本
        cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
        line_text = cursor.selectedText()
        
        # 移除已有的标题标记
        cleaned_text = line_text.lstrip('#').lstrip()
        
        # 根据选择添加新的标题标记
        if index == 0:  # 正文
            cursor.insertText(cleaned_text)
        else:  # H1-H6
            heading_level = '#' * index
            cursor.insertText(f"{heading_level} {cleaned_text}")
    
    def insert_bold(self):
        """插入粗体标记"""
        cursor = self.editor.editor.textCursor()
        if cursor.hasSelection():
            text = cursor.selectedText()
            cursor.insertText(f"**{text}**")
        else:
            cursor.insertText("****")
            cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, 2)
            self.editor.editor.setTextCursor(cursor)
    
    def insert_italic(self):
        """插入斜体标记"""
        cursor = self.editor.editor.textCursor()
        if cursor.hasSelection():
            text = cursor.selectedText()
            cursor.insertText(f"*{text}*")
        else:
            cursor.insertText("**")
            cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, 1)
            self.editor.editor.setTextCursor(cursor)
    
    def insert_strikethrough(self):
        """插入删除线标记"""
        cursor = self.editor.editor.textCursor()
        if cursor.hasSelection():
            text = cursor.selectedText()
            cursor.insertText(f"~~{text}~~")
        else:
            cursor.insertText("~~~~")
            cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, 2)
            self.editor.editor.setTextCursor(cursor)
    
    def insert_inline_code(self):
        """插入行内代码标记"""
        cursor = self.editor.editor.textCursor()
        if cursor.hasSelection():
            text = cursor.selectedText()
            cursor.insertText(f"`{text}`")
        else:
            cursor.insertText("``")
            cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, 1)
            self.editor.editor.setTextCursor(cursor)
    
    def insert_code_block(self):
        """插入代码块"""
        cursor = self.editor.editor.textCursor()
        if cursor.hasSelection():
            text = cursor.selectedText()
            cursor.insertText(f"```\n{text}\n```")
        else:
            cursor.insertText("```python\n\n```")
            cursor.movePosition(QTextCursor.Up, QTextCursor.MoveAnchor, 1)
            self.editor.editor.setTextCursor(cursor)
    
    def insert_unordered_list(self):
        """插入无序列表 - 支持多行转换"""
        cursor = self.editor.editor.textCursor()
        
        # 检查是否有选中文本
        if cursor.hasSelection():
            # 获取选中的文本
            selected_text = cursor.selectedText()
            
            # 将段落分隔符转换为换行符（Qt使用特殊字符表示段落）
            lines = selected_text.replace('\u2029', '\n').split('\n')
            
            # 转换每一行为列表项
            list_lines = []
            for line in lines:
                line = line.strip()
                if line:  # 忽略空行
                    # 检查是否已经是列表项
                    if line.startswith('- '):
                        list_lines.append(line)  # 已经是无序列表
                    elif line.startswith('* ') or line.startswith('+ '):
                        # 其他无序列表标记，统一为 -
                        list_lines.append('- ' + line[2:])
                    elif re.match(r'^\d+\.\s', line):
                        # 有序列表，转换为无序
                        list_lines.append('- ' + re.sub(r'^\d+\.\s+', '', line))
                    elif line.startswith('- [ ] ') or line.startswith('- [x] '):
                        # 任务列表，保留内容但改为普通无序列表
                        content = line[6:] if line.startswith('- [ ] ') else line[6:]
                        list_lines.append('- ' + content)
                    else:
                        # 普通文本，添加列表标记
                        list_lines.append('- ' + line)
            
            # 替换选中的文本
            if list_lines:
                cursor.insertText('\n'.join(list_lines))
        else:
            # 没有选中文本，只在当前行添加列表标记
            cursor.movePosition(QTextCursor.StartOfLine)
            
            # 获取当前行文本
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            line_text = cursor.selectedText().strip()
            
            # 检查并转换当前行
            if line_text:
                if not line_text.startswith('- '):
                    # 移除其他列表标记
                    if line_text.startswith('* ') or line_text.startswith('+ '):
                        cursor.insertText('- ' + line_text[2:])
                    elif re.match(r'^\d+\.\s', line_text):
                        cursor.insertText('- ' + re.sub(r'^\d+\.\s+', '', line_text))
                    elif line_text.startswith('- [ ] ') or line_text.startswith('- [x] '):
                        content = line_text[6:]
                        cursor.insertText('- ' + content)
                    else:
                        cursor.insertText('- ' + line_text)
                else:
                    # 已经是无序列表，保持不变
                    cursor.insertText(line_text)
            else:
                # 空行，直接添加列表标记
                cursor.insertText('- ')
    
    def insert_ordered_list(self):
        """插入有序列表 - 支持多行转换"""
        cursor = self.editor.editor.textCursor()
        
        # 检查是否有选中文本
        if cursor.hasSelection():
            # 获取选中的文本
            selected_text = cursor.selectedText()
            
            # 将段落分隔符转换为换行符
            lines = selected_text.replace('\u2029', '\n').split('\n')
            
            # 转换每一行为列表项
            list_lines = []
            list_number = 1
            for line in lines:
                line = line.strip()
                if line:  # 忽略空行
                    # 检查是否已经是列表项
                    if re.match(r'^\d+\.\s', line):
                        # 已经是有序列表，重新编号
                        content = re.sub(r'^\d+\.\s+', '', line)
                        list_lines.append(f"{list_number}. {content}")
                        list_number += 1
                    elif line.startswith('- ') or line.startswith('* ') or line.startswith('+ '):
                        # 无序列表，转换为有序
                        list_lines.append(f"{list_number}. {line[2:]}")
                        list_number += 1
                    elif line.startswith('- [ ] ') or line.startswith('- [x] '):
                        # 任务列表，转换为有序列表
                        content = line[6:]
                        list_lines.append(f"{list_number}. {content}")
                        list_number += 1
                    else:
                        # 普通文本，添加列表编号
                        list_lines.append(f"{list_number}. {line}")
                        list_number += 1
            
            # 替换选中的文本
            if list_lines:
                cursor.insertText('\n'.join(list_lines))
        else:
            # 没有选中文本，只在当前行添加列表标记
            cursor.movePosition(QTextCursor.StartOfLine)
            
            # 获取当前行文本
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            line_text = cursor.selectedText().strip()
            
            # 检查并转换当前行
            if line_text:
                if not re.match(r'^\d+\.\s', line_text):
                    # 移除其他列表标记
                    if line_text.startswith('- ') or line_text.startswith('* ') or line_text.startswith('+ '):
                        cursor.insertText('1. ' + line_text[2:])
                    elif line_text.startswith('- [ ] ') or line_text.startswith('- [x] '):
                        content = line_text[6:]
                        cursor.insertText('1. ' + content)
                    else:
                        cursor.insertText('1. ' + line_text)
                else:
                    # 已经是有序列表，保持不变
                    cursor.insertText(line_text)
            else:
                # 空行，直接添加列表标记
                cursor.insertText('1. ')
    
    def insert_task_list(self):
        """插入任务列表 - 支持多行转换"""
        cursor = self.editor.editor.textCursor()
        
        # 检查是否有选中文本
        if cursor.hasSelection():
            # 获取选中的文本
            selected_text = cursor.selectedText()
            
            # 将段落分隔符转换为换行符
            lines = selected_text.replace('\u2029', '\n').split('\n')
            
            # 转换每一行为任务列表项
            list_lines = []
            for line in lines:
                line = line.strip()
                if line:  # 忽略空行
                    # 检查是否已经是任务列表
                    if line.startswith('- [ ] ') or line.startswith('- [x] ') or line.startswith('- [X] '):
                        list_lines.append(line)  # 已经是任务列表，保持不变
                    elif line.startswith('- ') or line.startswith('* ') or line.startswith('+ '):
                        # 普通无序列表，转换为任务列表
                        list_lines.append('- [ ] ' + line[2:])
                    elif re.match(r'^\d+\.\s', line):
                        # 有序列表，转换为任务列表
                        content = re.sub(r'^\d+\.\s+', '', line)
                        list_lines.append('- [ ] ' + content)
                    else:
                        # 普通文本，添加任务列表标记
                        list_lines.append('- [ ] ' + line)
            
            # 替换选中的文本
            if list_lines:
                cursor.insertText('\n'.join(list_lines))
        else:
            # 没有选中文本，只在当前行添加任务列表标记
            cursor.movePosition(QTextCursor.StartOfLine)
            
            # 获取当前行文本
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            line_text = cursor.selectedText().strip()
            
            # 检查并转换当前行
            if line_text:
                if not (line_text.startswith('- [ ] ') or line_text.startswith('- [x] ')):
                    # 移除其他列表标记
                    if line_text.startswith('- ') or line_text.startswith('* ') or line_text.startswith('+ '):
                        cursor.insertText('- [ ] ' + line_text[2:])
                    elif re.match(r'^\d+\.\s', line_text):
                        content = re.sub(r'^\d+\.\s+', '', line_text)
                        cursor.insertText('- [ ] ' + content)
                    else:
                        cursor.insertText('- [ ] ' + line_text)
                else:
                    # 已经是任务列表，切换选中状态
                    if line_text.startswith('- [ ] '):
                        cursor.insertText('- [x] ' + line_text[6:])
                    else:
                        cursor.insertText('- [ ] ' + line_text[6:])
            else:
                # 空行，直接添加任务列表标记
                cursor.insertText('- [ ] ')
    
    def insert_quote(self):
        """插入引用"""
        cursor = self.editor.editor.textCursor()
        cursor.movePosition(QTextCursor.StartOfLine)
        cursor.insertText("> ")
    
    def insert_divider(self):
        """插入分隔线"""
        self.editor.insertPlainText("\n---\n")
    
    def insert_link(self):
        """插入链接（带对话框）"""
        dialog = LinkDialog(self)
        if dialog.exec():
            text = dialog.text_edit.text() or "链接文字"
            url = dialog.url_edit.text() or "https://example.com"
            self.editor.insertPlainText(f"[{text}]({url})")
    
    def insert_image(self):
        """插入图片"""
        # 弹出文件选择对话框
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片",
            "",
            "Images (*.png *.jpg *.jpeg *.gif *.bmp *.svg);;All Files (*)"
        )
        
        if file_path:
            # 获取文件名作为替代文本
            import os
            file_name = os.path.basename(file_path)
            
            # 插入图片语法
            cursor = self.editor.editor.textCursor()
            cursor.insertText(f"![{file_name}]({file_path})")
            
            # 提示用户
            self.status_bar.showMessage(f"已插入图片: {file_name}", 3000)
    
    def insert_table(self):
        """插入表格"""
        dialog = TableDialog(self)
        if dialog.exec():
            rows = dialog.rows_spin.value()
            cols = dialog.cols_spin.value()
            
            # 生成表格
            table = []
            
            # 表头
            header = "|"
            for i in range(cols):
                header += f" 列{i+1} |"
            table.append(header)
            
            # 分隔线
            separator = "|"
            for _ in range(cols):
                separator += " --- |"
            table.append(separator)
            
            # 数据行
            for r in range(rows - 1):
                row = "|"
                for c in range(cols):
                    row += f" 数据 |"
                table.append(row)
            
            # 插入表格
            self.editor.insertPlainText("\n" + "\n".join(table) + "\n")
    
    # ===== 其他方法保持不变 =====
    
    def create_glass_container(self, widget, title, toolbar=None):
        """创建增强版毛玻璃容器，可选包含工具栏"""
        container = QFrame()
        container.setObjectName("glassContainer")
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 标题栏 - 改进设计
        title_bar = QFrame()
        title_bar.setObjectName("glassTitleBar")
        title_bar.setFixedHeight(50)
        
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(20, 0, 20, 0)
        title_layout.setSpacing(15)
        
        # 添加微妙的图标占位符（可替换为实际图标）
        icon_placeholder = QFrame()
        icon_placeholder.setObjectName("titleIconPlaceholder")
        icon_placeholder.setFixedSize(18, 18)
        title_layout.addWidget(icon_placeholder)
        
        title_label = QLabel(title)
        title_label.setObjectName("glassTitle")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        # 添加装饰性分隔线
        separator = QFrame()
        separator.setObjectName("titleSeparator")
        separator.setFixedHeight(20)
        separator.setFixedWidth(1)
        title_layout.addWidget(separator)
        
        # 添加额外信息标签（例如状态或提示）
        info_label = QLabel()
        info_label.setObjectName("titleInfoLabel")
        info_label.setText("准备就绪")
        title_layout.addWidget(info_label)
        
        layout.addWidget(title_bar)
        
        # 如果提供了工具栏，添加在标题栏下方
        if toolbar:
            toolbar_container = QFrame()
            toolbar_container.setObjectName("embeddedToolbarContainer")
            toolbar_layout = QVBoxLayout(toolbar_container)
            toolbar_layout.setContentsMargins(15, 0, 15, 0)
            toolbar_layout.setSpacing(0)
            toolbar_layout.addWidget(toolbar)
            layout.addWidget(toolbar_container)
        
        # 添加组件 - 增加内边距和层次结构
        content_container = QFrame()
        content_container.setObjectName("glassContentContainer")
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.addWidget(widget, 1)
        
        # 添加发光效果 - 容器和内容区分发光
        container_glow = QGraphicsDropShadowEffect()
        container_glow.setBlurRadius(35)
        container_glow.setOffset(0, 5)
        container_glow.setColor(QColor(100, 100, 200, 100))
        container.setGraphicsEffect(container_glow)
        
        # 内容组件的发光效果
        widget_glow = QGraphicsDropShadowEffect()
        widget_glow.setBlurRadius(25)
        widget_glow.setOffset(0, 0)
        widget_glow.setColor(QColor(0, 224, 255, 60))
        widget.setGraphicsEffect(widget_glow)
        
        layout.addWidget(content_container, 1)
        
        return container
    
    def create_status_bar(self):
        """创建毛玻璃状态栏"""
        self.status_bar = QStatusBar()
        self.status_bar.setObjectName("glassStatusBar")
        self.status_bar.setFixedHeight(40)
        self.setStatusBar(self.status_bar)
        
        # 字数统计
        self.char_count_label = QLabel("Words: 0")
        self.char_count_label.setObjectName("statusLabel")
        
        # 主题信息
        self.theme_info_label = QLabel("主题: CardCraft Classic")
        self.theme_info_label.setObjectName("statusLabel")
        
        self.status_bar.addPermanentWidget(self.theme_info_label)
        self.status_bar.addPermanentWidget(self.char_count_label)
    
    def get_global_styles_qt_compatible(self):
        """获取Qt兼容的全局样式表 - 现代化版本"""
        return """
        /* 全局字体和重置 */
        * {
            font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
        }
        
        /* 主窗口 */
        QMainWindow {
            background: transparent;
        }
        
        /* 内容区域 */
        #contentArea {
            background: transparent;
            border: none;
        }
        
        /* 现代化毛玻璃容器 */
        #glassContainer {
            background: rgba(30, 30, 55, 0.75);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 22px;
        }
        
        #glassTitleBar {
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 rgba(255, 255, 255, 0.12),
                stop: 1 rgba(255, 255, 255, 0.07));
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            border-top-left-radius: 22px;
            border-top-right-radius: 22px;
        }
        
        #glassTitle {
            color: rgba(255, 255, 255, 0.95);
            font-size: 17px;
            font-weight: 600;
            letter-spacing: 1.2px;
        }
        
        #titleIconPlaceholder {
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                stop: 0 rgba(0, 255, 255, 0.8),
                stop: 1 rgba(255, 0, 255, 0.8));
            border-radius: 4px;
        }
        
        #titleSeparator {
            background: rgba(255, 255, 255, 0.1);
        }
        
        #titleInfoLabel {
            color: rgba(0, 255, 255, 0.7);
            font-size: 13px;
            font-weight: 500;
        }
        
        #glassContentContainer {
            background: rgba(255, 255, 255, 0.03);
            border-bottom-left-radius: 22px;
            border-bottom-right-radius: 22px;
        }
        
        /* 嵌入式工具栏容器 - 编辑器内部使用 */
        #embeddedToolbarContainer {
            background: rgba(255, 255, 255, 0.02);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }
        
        /* 工具栏容器 - 增强设计 */
        #toolbarContainer {
            background: rgba(20, 20, 45, 0.98);
            border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        }
        
        #buttonGroup {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 15px;
            padding: 5px;
        }
        
        /* 按钮美化 */
        QPushButton {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            color: rgba(255, 255, 255, 0.85);
            padding: 6px 12px;
            font-size: 13px;
            font-weight: 500;
        }
        
        QPushButton:hover {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: rgba(255, 255, 255, 0.95);
        }
        
        QPushButton:pressed {
            background: rgba(255, 255, 255, 0.15);
        }
        
        QPushButton:checked {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 rgba(0, 200, 255, 0.3),
                stop: 1 rgba(0, 150, 255, 0.3));
            border: 1px solid rgba(0, 200, 255, 0.4);
            color: rgba(255, 255, 255, 1);
        }
        
        /* 分割器 - 增强设计 */
        #mainSplitter::handle {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 rgba(255, 255, 255, 0),
                stop: 0.5 rgba(255, 255, 255, 0.2),
                stop: 1 rgba(255, 255, 255, 0));
            width: 4px;
            margin: 20px 0;
        }
        
        #mainSplitter::handle:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 rgba(0, 255, 255, 0),
                stop: 0.5 rgba(0, 255, 255, 0.6),
                stop: 1 rgba(0, 255, 255, 0));
            width: 4px;
        }
        
        /* 状态栏 - 现代化设计 */
        #glassStatusBar {
            background: rgba(20, 20, 45, 0.95);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.8);
        }
        
        #statusLabel {
            color: rgba(255, 255, 255, 0.85);
            font-size: 12px;
            font-weight: 500;
            padding: 5px 15px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            margin: 0 8px;
        }
        
        /* 滚动条美化 - 现代化设计 */
        QScrollBar:vertical {
            background: rgba(255, 255, 255, 0.03);
            width: 10px;
            border-radius: 5px;
            margin: 5px 2px;
        }
        
        QScrollBar::handle:vertical {
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 rgba(0, 200, 255, 0.4),
                stop: 1 rgba(150, 0, 255, 0.4));
            border-radius: 5px;
            min-height: 40px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        QScrollBar::handle:vertical:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 rgba(0, 200, 255, 0.6),
                stop: 1 rgba(150, 0, 255, 0.6));
        }
        
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {
            background: transparent;
        }
        
        /* 工具提示 - 增强设计 */
        QToolTip {
            background: rgba(30, 30, 55, 0.98);
            border: 1px solid rgba(0, 200, 255, 0.4);
            color: rgba(255, 255, 255, 0.95);
            padding: 7px 12px;
            border-radius: 8px;
            font-size: 13px;
        }
        
        /* 下拉框美化 */
        QComboBox {
            background: rgba(30, 30, 55, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 10px;
            color: rgba(255, 255, 255, 0.85);
            padding: 6px 12px;
            font-size: 13px;
        }
        
        QComboBox:hover {
            border: 1px solid rgba(255, 255, 255, 0.25);
        }
        
        /* 文本编辑区美化 */
        QTextEdit, QLineEdit {
            background: rgba(25, 25, 45, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            color: rgba(255, 255, 255, 0.9);
            padding: 12px;
            font-size: 14px;
            selection-background-color: rgba(0, 200, 255, 0.4);
            selection-color: white;
        }
        
        QTextEdit:focus, QLineEdit:focus {
            border: 1px solid rgba(0, 200, 255, 0.4);
            background: rgba(30, 30, 50, 0.75);
        }
        """
    
    def resizeEvent(self, event):
        """窗口大小改变时调整背景"""
        super().resizeEvent(event)
        if hasattr(self, 'modern_bg'):
            self.modern_bg.resize(self.size())
    
    def setup_connections(self):
        """设置信号连接"""
        self.editor.textChanged.connect(self.on_text_changed)
        self.editor.scrollChanged.connect(self.preview.handle_scroll)
        self.preview.pageChanged.connect(self.on_page_changed)
        self.theme_selector.currentIndexChanged.connect(self.on_theme_changed)
        self.font_selector.currentIndexChanged.connect(self.on_font_changed)
        self.font_size_selector.currentIndexChanged.connect(self.on_font_size_changed)
        self.size_selector.currentIndexChanged.connect(self.on_size_selector_changed)
        
        if hasattr(self.preview, 'sizeChanged'):
            self.preview.sizeChanged.connect(self.on_size_changed)
    
    def on_text_changed(self):
        """文本改变时启动计时器"""
        # 添加更新锁，防止并发
        if hasattr(self, '_updating') and self._updating:
            return
        
        self.update_timer.stop()
        self.update_timer.start()
        self.update_char_count()
    
    def update_preview(self):
        """更新预览"""
        self._updating = True  # 加锁
        try:
            self.update_timer.stop()
            markdown_text = self.editor.get_text()
            
            # 添加图片检测日志
            img_count = markdown_text.count('![')
            print(f"检测到 {img_count} 个图片标记")
            
            self.preview.update_content(markdown_text)
        finally:
            self._updating = False  # 解锁
    
    def update_char_count(self):
        """更新字数统计"""
        text = self.editor.get_text()
        char_count = len(text.replace(" ", "").replace("\n", ""))
        word_count = len(text.split())
        self.char_count_label.setText(f"字符: {char_count} | 单词: {word_count}")
    
    def on_page_changed(self, current, total):
        """页码改变时更新状态栏"""
        if total > 1:
            self.status_bar.showMessage(f"第 {current}/{total} 页", 2000)
    
    def on_theme_changed(self, index):
        """处理主题改变"""
        theme_key = self.theme_selector.currentData()
        if theme_key:
            self.preview.change_theme(theme_key)
            theme_name = self.theme_selector.currentText()
            # 主题名称已更新为"CardCraft Classic"，直接使用
            display_name = theme_name
            self.theme_info_label.setText(f"主题: {display_name}")
            self.status_bar.showMessage(f"已切换到: {display_name}", 3000)
    
    def on_font_changed(self, index):
        """处理字体改变"""
        font_family = self.font_selector.currentText()
        
        # 更新预览组件的字体
        self.preview.change_font_family(font_family)
        
        # 保存字体设置
        self.style_manager.save_setting("font_family", font_family)
        
        # 更新最近使用的字体列表
        recent_fonts = self.style_manager.get_setting("recent_fonts", [])
        
        # 如果字体已在列表中，先移除
        if font_family in recent_fonts:
            recent_fonts.remove(font_family)
        
        # 将字体添加到列表开头
        recent_fonts.insert(0, font_family)
        
        # 限制列表长度为最多5个
        recent_fonts = recent_fonts[:5]
        
        # 保存更新后的列表
        self.style_manager.save_setting("recent_fonts", recent_fonts)
        
        # 更新状态栏
        self.status_bar.showMessage(f"字体: {font_family}", 3000)
    
    def on_font_size_changed(self, index):
        """处理字体大小改变"""
        font_sizes = {
            0: 14,  # 小
            1: 18,  # 标准
            2: 22,  # 大
            3: 26,  # 超大
            4: 30   # 最大
        }
        
        font_size = font_sizes.get(index, 18)
        font_size_name = self.font_size_selector.currentText()
        
        # 更新预览组件的字体大小
        self.preview.change_font_size(font_size)
        
        # 保存字体大小设置
        self.style_manager.save_setting("font_size", font_size_name)
        
        # 更新状态栏
        self.status_bar.showMessage(f"字体大小: {font_size_name}", 3000)
    
    def on_size_selector_changed(self, index):
        """处理尺寸选择器变化"""
        # 直接调用preview组件的on_size_changed方法，传入索引
        if hasattr(self.preview, 'on_size_changed'):
            self.preview.on_size_changed(index)
        
        # 尺寸映射用于状态显示
        size_map = {
            0: "small",  # 720p
            1: "medium",  # 1080p
            2: "large"  # 1440p
        }
        size = size_map.get(index, "medium")
        
        # 更新状态栏显示
        self.on_size_changed(size)
    
    def on_size_changed(self, size):
        """处理尺寸改变"""
        size_display = {
            "small": "720p (720×960)",
            "medium": "1080p (1080×1440)",
            "large": "1440p (1440×1920)"
        }
        display_name = size_display.get(size, size)
        self.status_bar.showMessage(f"尺寸: {display_name}", 3000)
    
    def clear_content(self):
        """清空内容"""
        reply = QMessageBox.question(
            self, "清空内容",
            "确定要清空所有内容吗？\n此操作无法撤销。",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.editor.editor.clear()
            self.status_bar.showMessage("✅ 内容已清空", 2000)
    
    def open_file(self):
        """打开文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "打开Markdown文件",
            "",
            "Markdown文件 (*.md *.markdown);;所有文件 (*.*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.editor.set_text(content)
                    self.status_bar.showMessage(f"已打开文件: {file_path}", 3000)
            except Exception as e:
                QMessageBox.critical(
                    self, "打开文件失败",
                    f"无法打开文件:\n{str(e)}",
                    QMessageBox.StandardButton.Ok
                )
                self.status_bar.showMessage("❌ 打开文件失败", 3000)

    def export_images(self):
        """导出图片"""
        if not self.editor.get_text().strip():
            QMessageBox.warning(
                self, "提示",
                "没有内容可导出。请先输入一些文本。",
                QMessageBox.StandardButton.Ok
            )
            return
        
        folder = QFileDialog.getExistingDirectory(
            self, 
            "选择导出文件夹",
            "",
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks
        )
        
        if folder:
            try:
                theme_name = self.theme_selector.currentText()
                image_quality = self.image_quality_selector.currentIndex()
                quality_names = ["不优化", "优化", "超级优化"]
                quality_name = quality_names[image_quality]
                
                self.status_bar.showMessage(f"正在导出图片 (主题: {theme_name}, 优化: {quality_name})...", 0)
                self.preview.export_pages(folder, image_quality)
                
            except Exception as e:
                QMessageBox.critical(
                    self, "导出失败",
                    f"导出过程中出错:\n{str(e)}",
                    QMessageBox.StandardButton.Ok
                )
                self.status_bar.showMessage("❌ 导出失败", 3000)