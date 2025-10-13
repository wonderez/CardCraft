# ============================================
# src/utils/exporter.py
# ============================================
from PyQt6.QtCore import pyqtSignal, QTimer, QEventLoop, QSize, Qt, QPoint, QRect, QObject
from PyQt6.QtGui import QImage, QPainter, QFont, QColor, QPageSize, QRegion
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtWidgets import QWidget
from pathlib import Path
from typing import List, Optional
import json
import time

class ImageExporter(QObject):
    """图片导出器"""
    
    # 信号
    progress = pyqtSignal(int, int)  # 当前进度，总数
    finished = pyqtSignal(bool, str)  # 是否成功，消息
    page_exported = pyqtSignal(int, str)  # 页码，文件路径
    
    def __init__(self, web_view: QWebEngineView):
        super().__init__()
        self.web_view = web_view
        self.pages_to_export = []
        self.current_export_index = 0
        self.output_folder = ""
        self.html_generator = None
        self.export_format = "PNG"
        self.quality = 100
        self._is_exporting = False
        
    def export_pages(self, pages: List[str], output_folder: str, html_generator, 
                     format: str = "PNG", quality: int = 100) -> None:
        """
        导出多个页面为图片
        
        Args:
            pages: HTML页面内容列表
            output_folder: 输出文件夹路径
            html_generator: HTML生成器实例
            format: 图片格式 (PNG/JPEG)
            quality: 图片质量 (1-100)
        """
        try:
            self.pages_to_export = pages
            self.output_folder = Path(output_folder)
            self.current_export_index = 0
            self.html_generator = html_generator
            self.export_format = format
            self.quality = quality
            self._is_exporting = True
            
            # 确保输出文件夹存在
            self.output_folder.mkdir(parents=True, exist_ok=True)
            
            # 确保WebView是固定尺寸
            try:
                # 获取页面尺寸，添加安全检查
                if hasattr(html_generator, 'page_width') and hasattr(html_generator, 'page_height'):
                    width = html_generator.page_width
                    height = html_generator.page_height
                else:
                    # 使用默认尺寸
                    width = 1080
                    height = 1440
                    
                self.web_view.setFixedSize(width, height)
                self.web_view.setZoomFactor(1.0)  # 重置缩放
            except Exception as e:
                print(f"设置WebView尺寸错误: {str(e)}")
                # 尝试使用默认尺寸
                self.web_view.setFixedSize(1080, 1440)
                self.web_view.setZoomFactor(1.0)
            
            # 开始导出第一页
            self._export_next_page()
            
        except Exception as e:
            # 打印详细错误信息用于调试
            import traceback
            error_details = traceback.format_exc()
            print(f"导出初始化错误详情: {error_details}")
            
            self._is_exporting = False
            self.finished.emit(False, f"导出初始化失败: {str(e)}")
    
    def _export_next_page(self):
        """导出下一页"""
        if not self._is_exporting:
            return
            
        if self.current_export_index >= len(self.pages_to_export):
            # 导出完成
            self._is_exporting = False
            self.finished.emit(True, f"成功导出 {len(self.pages_to_export)} 张图片")
            return
        
        # 发送进度信号
        self.progress.emit(self.current_export_index + 1, len(self.pages_to_export))
        
        # 获取当前页内容
        page_content = self.pages_to_export[self.current_export_index]
        page_num = self.current_export_index + 1
        
        # 生成完整HTML（包含页码信息）
        try:
            full_html = self.html_generator.generate(
                page_content, 
                page_num=page_num, 
                total_pages=len(self.pages_to_export)
            )
        except Exception as e:
            print(f"生成HTML错误: {str(e)}")
            self._is_exporting = False
            self.finished.emit(False, f"生成HTML失败: {str(e)}")
            return
        
        # 加载HTML到WebView
        try:
            from PyQt6.QtCore import QUrl
            self.web_view.setHtml(full_html, QUrl("file:///"))
        except Exception as e:
            print(f"加载HTML错误: {str(e)}")
            self._is_exporting = False
            self.finished.emit(False, f"加载HTML失败: {str(e)}")
            return
        
        # 等待页面加载完成后导出
        QTimer.singleShot(1500, lambda: self._capture_page(page_num))
    
    def _capture_page(self, page_num: int):
        """捕获当前页面为图片"""
        if not self._is_exporting:
            return
            
        # 构建输出文件名
        extension = self.export_format.lower()
        filename = f"card_{page_num:02d}.{extension}"
        output_path = self.output_folder / filename
        
        # 使用精确的捕获方法
        self._capture_fixed_size(output_path, page_num)
    
    def _capture_fixed_size(self, output_path: Path, page_num: int):
        """捕获固定尺寸的页面"""
        try:
            # 从html_generator获取当前尺寸，添加安全检查
            if hasattr(self.html_generator, 'page_width') and hasattr(self.html_generator, 'page_height'):
                target_width = self.html_generator.page_width
                target_height = self.html_generator.page_height
            else:
                # 使用默认尺寸
                target_width = 1080
                target_height = 1440
            
            # 创建目标图片
            image = QImage(target_width, target_height, QImage.Format.Format_ARGB32)
            image.fill(Qt.GlobalColor.white)  # 使用GlobalColor避免Qt版本兼容性问题
            
            # 创建painter
            painter = QPainter(image)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
            
            # 确保WebView是正确的尺寸
            self.web_view.resize(target_width, target_height)
            
            # 渲染WebView到图片
            # 使用固定的源矩形来确保只捕获卡片区域
            source_rect = QRect(0, 0, target_width, target_height)
            target_rect = QRect(0, 0, target_width, target_height)
            
            # 渲染WebView
            if isinstance(self.web_view, QWidget):
                self.web_view.render(
                    painter,
                    QPoint(0, 0),
                    QRegion(source_rect),
                    QWidget.RenderFlag.DrawWindowBackground | QWidget.RenderFlag.DrawChildren
                )
            
            # 可选：添加导出时间水印
            self._add_export_watermark(painter, page_num)
            
            # 结束painter
            painter.end()
            
            # 保存图片
            success = image.save(str(output_path), self.export_format, self.quality)
            
            if success:
                self.page_exported.emit(page_num, str(output_path))
                # 继续导出下一页
                self.current_export_index += 1
                QTimer.singleShot(100, self._export_next_page)
            else:
                self._is_exporting = False
                self.finished.emit(False, f"保存图片失败: {output_path}")
                
        except Exception as e:
            # 打印详细错误信息用于调试
            import traceback
            error_details = traceback.format_exc()
            print(f"导出错误详情: {error_details}")
            
            self._is_exporting = False
            self.finished.emit(False, f"导出页面 {page_num} 时出错: {str(e)}")
    
    def _add_export_watermark(self, painter: QPainter, page_num: int):
        """添加导出水印（可选）"""
        try:
            # 设置水印字体和颜色
            font = QFont("Arial", 9)
            painter.setFont(font)
            painter.setPen(QColor(200, 200, 200, 80))
            
            # 在右下角添加生成时间（非常淡的水印）
            timestamp = time.strftime("%Y%m%d")
            painter.drawText(
                1000, 1420,
                f"{timestamp}"
            )
        except Exception as e:
            # 水印添加失败不影响导出，只打印错误信息
            print(f"添加水印失败: {str(e)}")
    
    def export_as_pdf(self, pages: List[str], output_file: str, html_generator):
        """
        导出为PDF文件（所有页面合并为一个PDF）
        
        Args:
            pages: HTML页面内容列表
            output_file: 输出PDF文件路径
            html_generator: HTML生成器实例
        """
        try:
            # 创建PDF打印机
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(output_file)
            
            # 设置页面大小为小红书卡片比例
            # 注意：PDF使用点(point)作为单位，1点 = 1/72英寸
            # 1080px × 1440px 在 96 DPI 下约等于 810pt × 1080pt
            page_size = QPageSize(QSize(810, 1080), QPageSize.Unit.Point)
            printer.setPageSize(page_size)
            printer.setPageMargins(0, 0, 0, 0, QPrinter.Unit.Millimeter)
            
            # 合并所有页面内容
            combined_html = self._combine_pages_for_pdf(pages, html_generator)
            
            # 加载合并后的HTML
            from PyQt6.QtCore import QUrl
            self.web_view.setHtml(combined_html, QUrl("file:///"))
            
            # 等待加载完成后打印
            loop = QEventLoop()
            
            def on_load_finished():
                try:
                    self.web_view.page().print(printer, lambda success: loop.quit())
                except Exception as e:
                    print(f"PDF打印错误: {str(e)}")
                    loop.quit()
            
            QTimer.singleShot(1000, on_load_finished)
            loop.exec()
            
            self.finished.emit(True, f"PDF导出成功: {output_file}")
            
        except Exception as e:
            # 打印详细错误信息用于调试
            import traceback
            error_details = traceback.format_exc()
            print(f"PDF导出错误详情: {error_details}")
            
            self.finished.emit(False, f"PDF导出失败: {str(e)}")
    
    def _combine_pages_for_pdf(self, pages: List[str], html_generator) -> str:
        """合并多个页面为PDF格式"""
        combined_content = ""
        
        for i, page in enumerate(pages, 1):
            if i > 1:
                # 添加分页符
                combined_content += '<div style="page-break-before: always;"></div>'
            
            # 添加页面内容，包装在固定尺寸的容器中
            combined_content += f'''
            <div style="width: 1080px; height: 1440px; position: relative; overflow: hidden;">
                {page}
            </div>
            '''
        
        # 生成完整HTML
        return html_generator.generate(combined_content)
    
    def cancel_export(self):
        """取消导出"""
        self._is_exporting = False
        self.pages_to_export = []
        self.finished.emit(False, "导出已取消")