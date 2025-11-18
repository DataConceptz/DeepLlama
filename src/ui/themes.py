"""
Theme management for the application
Provides dark, light, and custom themes
"""

from enum import Enum


class Theme(Enum):
    """Available themes"""
    DARK = "dark"
    LIGHT = "light"
    HIGH_CONTRAST = "high_contrast"
    ACADEMIC = "academic"


class ThemeManager:
    """Manages application themes and styling"""

    @staticmethod
    def get_stylesheet(theme: Theme) -> str:
        """Get stylesheet for specified theme"""
        if theme == Theme.DARK:
            return ThemeManager._dark_theme()
        elif theme == Theme.LIGHT:
            return ThemeManager._light_theme()
        elif theme == Theme.HIGH_CONTRAST:
            return ThemeManager._high_contrast_theme()
        elif theme == Theme.ACADEMIC:
            return ThemeManager._academic_theme()
        else:
            return ThemeManager._dark_theme()

    @staticmethod
    def _dark_theme() -> str:
        """Dark theme stylesheet"""
        return """
            /* Main Application */
            QMainWindow, QDialog {
                background-color: #1e1e1e;
                color: #e0e0e0;
            }

            /* Tab Widget */
            QTabWidget::pane {
                border: 1px solid #3a3a3a;
                background-color: #252525;
            }

            QTabBar::tab {
                background-color: #2d2d2d;
                color: #e0e0e0;
                padding: 10px 20px;
                border: 1px solid #3a3a3a;
                border-bottom: none;
                margin-right: 2px;
            }

            QTabBar::tab:selected {
                background-color: #252525;
                border-bottom: 2px solid #0078d4;
            }

            QTabBar::tab:hover {
                background-color: #3a3a3a;
            }

            /* Buttons */
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1084d8;
            }

            QPushButton:pressed {
                background-color: #006cc1;
            }

            QPushButton:disabled {
                background-color: #3a3a3a;
                color: #808080;
            }

            /* Input Fields */
            QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QComboBox {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #3a3a3a;
                border-radius: 4px;
                padding: 6px;
            }

            QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
                border: 2px solid #0078d4;
            }

            /* ComboBox */
            QComboBox {
                padding: 6px;
            }

            QComboBox::drop-down {
                border: none;
                width: 30px;
            }

            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #000000;
                margin-right: 10px;
            }

            QComboBox QAbstractItemView {
                background-color: #ffffff;
                color: #000000;
                selection-background-color: #0078d4;
                selection-color: white;
            }

            /* Table Widget */
            QTableWidget {
                background-color: #2d2d2d;
                color: #e0e0e0;
                gridline-color: #3a3a3a;
                border: 1px solid #3a3a3a;
            }

            QTableWidget::item {
                padding: 5px;
            }

            QTableWidget::item:selected {
                background-color: #0078d4;
                color: white;
            }

            QTableWidget::item:hover {
                background-color: #3a3a3a;
            }

            QHeaderView::section {
                background-color: #2d2d2d;
                color: #e0e0e0;
                padding: 8px;
                border: 1px solid #3a3a3a;
                font-weight: bold;
            }

            QHeaderView::section:hover {
                background-color: #3a3a3a;
            }

            /* Scroll Bars */
            QScrollBar:vertical {
                background-color: #2d2d2d;
                width: 14px;
                margin: 0px;
            }

            QScrollBar::handle:vertical {
                background-color: #5a5a5a;
                min-height: 30px;
                border-radius: 7px;
            }

            QScrollBar::handle:vertical:hover {
                background-color: #6a6a6a;
            }

            QScrollBar:horizontal {
                background-color: #2d2d2d;
                height: 14px;
                margin: 0px;
            }

            QScrollBar::handle:horizontal {
                background-color: #5a5a5a;
                min-width: 30px;
                border-radius: 7px;
            }

            QScrollBar::handle:horizontal:hover {
                background-color: #6a6a6a;
            }

            /* Labels */
            QLabel {
                color: #e0e0e0;
            }

            /* Group Box */
            QGroupBox {
                border: 1px solid #3a3a3a;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
                color: #e0e0e0;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }

            /* CheckBox */
            QCheckBox {
                color: #e0e0e0;
                spacing: 8px;
            }

            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #5a5a5a;
                border-radius: 3px;
                background-color: #2d2d2d;
            }

            QCheckBox::indicator:checked {
                background-color: #0078d4;
                border-color: #0078d4;
            }

            /* Progress Bar */
            QProgressBar {
                border: 1px solid #3a3a3a;
                border-radius: 4px;
                text-align: center;
                background-color: #2d2d2d;
                color: #e0e0e0;
            }

            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 3px;
            }

            /* Slider */
            QSlider::groove:horizontal {
                border: 1px solid #3a3a3a;
                height: 8px;
                background-color: #2d2d2d;
                margin: 2px 0;
                border-radius: 4px;
            }

            QSlider::handle:horizontal {
                background-color: #0078d4;
                border: 1px solid #0078d4;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }

            QSlider::handle:horizontal:hover {
                background-color: #1084d8;
            }

            /* Status Bar */
            QStatusBar {
                background-color: #2d2d2d;
                color: #e0e0e0;
            }

            /* Menu Bar */
            QMenuBar {
                background-color: #2d2d2d;
                color: #e0e0e0;
            }

            QMenuBar::item:selected {
                background-color: #3a3a3a;
            }

            QMenu {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3a3a3a;
            }

            QMenu::item:selected {
                background-color: #0078d4;
            }
        """

    @staticmethod
    def _light_theme() -> str:
        """Light theme stylesheet"""
        return """
            /* Main Application */
            QMainWindow, QDialog {
                background-color: #f5f5f5;
                color: #333333;
            }

            /* Tab Widget */
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background-color: #ffffff;
            }

            QTabBar::tab {
                background-color: #e0e0e0;
                color: #333333;
                padding: 10px 20px;
                border: 1px solid #cccccc;
                border-bottom: none;
                margin-right: 2px;
            }

            QTabBar::tab:selected {
                background-color: #ffffff;
                border-bottom: 2px solid #0078d4;
            }

            QTabBar::tab:hover {
                background-color: #d0d0d0;
            }

            /* Buttons */
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1084d8;
            }

            QPushButton:pressed {
                background-color: #006cc1;
            }

            QPushButton:disabled {
                background-color: #cccccc;
                color: #888888;
            }

            /* Input Fields */
            QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QComboBox {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 6px;
            }

            QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
                border: 2px solid #0078d4;
            }

            /* ComboBox */
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }

            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #333333;
                margin-right: 10px;
            }

            QComboBox QAbstractItemView {
                background-color: #ffffff;
                color: #333333;
                selection-background-color: #0078d4;
                selection-color: white;
            }

            /* Table Widget */
            QTableWidget {
                background-color: #ffffff;
                color: #333333;
                gridline-color: #e0e0e0;
                border: 1px solid #cccccc;
            }

            QTableWidget::item:selected {
                background-color: #0078d4;
                color: white;
            }

            QTableWidget::item:hover {
                background-color: #e8f4fd;
            }

            QHeaderView::section {
                background-color: #f0f0f0;
                color: #333333;
                padding: 8px;
                border: 1px solid #cccccc;
                font-weight: bold;
            }

            /* Labels */
            QLabel {
                color: #333333;
            }

            /* Group Box */
            QGroupBox {
                border: 1px solid #cccccc;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
                color: #333333;
            }

            /* CheckBox */
            QCheckBox {
                color: #333333;
            }

            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #999999;
                border-radius: 3px;
                background-color: #ffffff;
            }

            QCheckBox::indicator:checked {
                background-color: #0078d4;
                border-color: #0078d4;
            }

            /* Progress Bar */
            QProgressBar {
                border: 1px solid #cccccc;
                border-radius: 4px;
                text-align: center;
                background-color: #ffffff;
            }

            QProgressBar::chunk {
                background-color: #0078d4;
            }
        """

    @staticmethod
    def _high_contrast_theme() -> str:
        """High contrast theme for accessibility"""
        return """
            QMainWindow, QDialog {
                background-color: #000000;
                color: #ffffff;
            }

            QTabWidget::pane {
                border: 2px solid #ffffff;
                background-color: #000000;
            }

            QTabBar::tab {
                background-color: #000000;
                color: #ffffff;
                padding: 10px 20px;
                border: 2px solid #ffffff;
            }

            QTabBar::tab:selected {
                background-color: #ffffff;
                color: #000000;
            }

            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border: 2px solid #ffffff;
                padding: 8px 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #ffff00;
                color: #000000;
            }

            QLineEdit, QTextEdit, QPlainTextEdit, QComboBox {
                background-color: #000000;
                color: #ffffff;
                border: 2px solid #ffffff;
                padding: 6px;
            }

            QTableWidget {
                background-color: #000000;
                color: #ffffff;
                border: 2px solid #ffffff;
            }

            QTableWidget::item:selected {
                background-color: #ffffff;
                color: #000000;
            }

            QHeaderView::section {
                background-color: #000000;
                color: #ffffff;
                border: 2px solid #ffffff;
                font-weight: bold;
            }

            QLabel {
                color: #ffffff;
            }
        """

    @staticmethod
    def _academic_theme() -> str:
        """Academic/professional theme"""
        return """
            QMainWindow, QDialog {
                background-color: #fafafa;
                color: #2c3e50;
            }

            QTabWidget::pane {
                border: 1px solid #bdc3c7;
                background-color: #ffffff;
            }

            QTabBar::tab {
                background-color: #ecf0f1;
                color: #2c3e50;
                padding: 10px 20px;
                border: 1px solid #bdc3c7;
                border-bottom: none;
            }

            QTabBar::tab:selected {
                background-color: #ffffff;
                border-bottom: 3px solid #2980b9;
            }

            QPushButton {
                background-color: #2980b9;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 3px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #3498db;
            }

            QLineEdit, QTextEdit, QPlainTextEdit, QComboBox {
                background-color: #ffffff;
                color: #2c3e50;
                border: 1px solid #bdc3c7;
                padding: 6px;
                border-radius: 3px;
            }

            QTableWidget {
                background-color: #ffffff;
                color: #2c3e50;
                gridline-color: #ecf0f1;
                border: 1px solid #bdc3c7;
            }

            QTableWidget::item:selected {
                background-color: #2980b9;
                color: white;
            }

            QHeaderView::section {
                background-color: #34495e;
                color: #ffffff;
                padding: 8px;
                border: none;
                font-weight: bold;
            }

            QLabel {
                color: #2c3e50;
            }
        """
