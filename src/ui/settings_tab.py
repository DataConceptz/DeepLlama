"""
Settings tab
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QLineEdit, QComboBox, QGroupBox,
                               QDoubleSpinBox, QSpinBox, QCheckBox, QMessageBox,
                               QGridLayout, QFontComboBox)
from PySide6.QtCore import Signal

from ..ui.themes import Theme


class SettingsTab(QWidget):
    """Settings tab widget"""

    theme_changed = Signal(Theme)
    settings_changed = Signal()

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        """Setup user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel("⚙️ Settings")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        # Ollama Settings
        ollama_group = QGroupBox("Ollama Configuration")
        ollama_layout = QGridLayout(ollama_group)

        ollama_layout.addWidget(QLabel("Ollama URL:"), 0, 0)
        self.ollama_url_input = QLineEdit()
        self.ollama_url_input.setPlaceholderText("http://localhost:11434")
        ollama_layout.addWidget(self.ollama_url_input, 0, 1)

        ollama_layout.addWidget(QLabel("Default Model:"), 1, 0)
        self.default_model_combo = QComboBox()
        self.refresh_models_button = QPushButton("🔄 Refresh")
        self.refresh_models_button.clicked.connect(self.refresh_models)

        model_layout = QHBoxLayout()
        model_layout.addWidget(self.default_model_combo)
        model_layout.addWidget(self.refresh_models_button)
        ollama_layout.addLayout(model_layout, 1, 1)

        ollama_layout.addWidget(QLabel("Temperature:"), 2, 0)
        self.temperature_spin = QDoubleSpinBox()
        self.temperature_spin.setMinimum(0.0)
        self.temperature_spin.setMaximum(2.0)
        self.temperature_spin.setSingleStep(0.1)
        self.temperature_spin.setValue(0.7)
        ollama_layout.addWidget(self.temperature_spin, 2, 1)

        ollama_layout.addWidget(QLabel("Max Tokens:"), 3, 0)
        self.max_tokens_spin = QSpinBox()
        self.max_tokens_spin.setMinimum(100)
        self.max_tokens_spin.setMaximum(10000)
        self.max_tokens_spin.setValue(2000)
        ollama_layout.addWidget(self.max_tokens_spin, 3, 1)

        layout.addWidget(ollama_group)

        # Search Settings
        search_group = QGroupBox("Search Configuration")
        search_layout = QGridLayout(search_group)

        search_layout.addWidget(QLabel("Default # of Results:"), 0, 0)
        self.default_results_spin = QSpinBox()
        self.default_results_spin.setMinimum(1)
        self.default_results_spin.setMaximum(1000)
        self.default_results_spin.setValue(50)
        search_layout.addWidget(self.default_results_spin, 0, 1)

        search_layout.addWidget(QLabel("Citation Style:"), 1, 0)
        self.citation_style_combo = QComboBox()
        self.citation_style_combo.addItems(["APA", "MLA", "Chicago", "IEEE"])
        search_layout.addWidget(self.citation_style_combo, 1, 1)

        layout.addWidget(search_group)

        # UI Settings
        ui_group = QGroupBox("User Interface")
        ui_layout = QGridLayout(ui_group)

        ui_layout.addWidget(QLabel("Theme:"), 0, 0)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light", "High Contrast", "Academic"])
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        ui_layout.addWidget(self.theme_combo, 0, 1)

        ui_layout.addWidget(QLabel("Font Family:"), 1, 0)
        self.font_family_combo = QFontComboBox()
        ui_layout.addWidget(self.font_family_combo, 1, 1)

        ui_layout.addWidget(QLabel("Font Size:"), 2, 0)
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setMinimum(8)
        self.font_size_spin.setMaximum(20)
        self.font_size_spin.setValue(10)
        ui_layout.addWidget(self.font_size_spin, 2, 1)

        layout.addWidget(ui_group)

        # Database Settings
        db_group = QGroupBox("Database")
        db_layout = QGridLayout(db_group)

        self.auto_save_checkbox = QCheckBox("Auto-save articles")
        self.auto_save_checkbox.setChecked(True)
        db_layout.addWidget(self.auto_save_checkbox, 0, 0, 1, 2)

        layout.addWidget(db_group)

        layout.addStretch()

        # Action buttons
        button_layout = QHBoxLayout()

        self.save_button = QPushButton("💾 Save Settings")
        self.save_button.setFixedHeight(40)
        self.save_button.setStyleSheet("font-weight: bold;")
        self.save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(self.save_button)

        self.reset_button = QPushButton("🔄 Reset to Defaults")
        self.reset_button.clicked.connect(self.reset_settings)
        button_layout.addWidget(self.reset_button)

        button_layout.addStretch()

        layout.addLayout(button_layout)

    def load_settings(self):
        """Load settings from config"""
        config = self.main_window.config

        # Ollama settings
        self.ollama_url_input.setText(config.get('ollama_url', 'http://localhost:11434'))
        self.temperature_spin.setValue(config.get('temperature', 0.7))
        self.max_tokens_spin.setValue(config.get('max_tokens', 2000))

        # Search settings
        self.default_results_spin.setValue(config.get('default_num_results', 50))
        self.citation_style_combo.setCurrentText(config.get('citation_style', 'APA'))

        # UI settings
        theme = config.get('theme', 'dark')
        theme_map = {'dark': 'Dark', 'light': 'Light', 'high_contrast': 'High Contrast', 'academic': 'Academic'}
        self.theme_combo.setCurrentText(theme_map.get(theme, 'Dark'))

        self.font_family_combo.setCurrentFont(config.get('font_family', 'Segoe UI'))
        self.font_size_spin.setValue(config.get('font_size', 10))

        # Database settings
        self.auto_save_checkbox.setChecked(config.get('auto_save', True))

        # Refresh models
        self.refresh_models()

    def refresh_models(self):
        """Refresh available models"""
        self.default_model_combo.clear()

        if not self.main_window.ollama_service.is_available():
            self.default_model_combo.addItem("❌ Ollama not running")
            return

        models = self.main_window.ollama_service.get_models()

        if not models:
            self.default_model_combo.addItem("No models available")
            return

        self.default_model_combo.addItem("(None)")

        for model in models:
            self.default_model_combo.addItem(model.name)

        # Set current default
        default_model = self.main_window.config.get('default_model', '')
        if default_model:
            index = self.default_model_combo.findText(default_model)
            if index >= 0:
                self.default_model_combo.setCurrentIndex(index)

    def save_settings(self):
        """Save settings to config"""
        config = self.main_window.config

        # Ollama settings
        config.set('ollama_url', self.ollama_url_input.text())

        default_model = self.default_model_combo.currentText()
        if default_model and not default_model.startswith("❌") and default_model != "(None)":
            config.set('default_model', default_model)
        else:
            config.set('default_model', '')

        config.set('temperature', self.temperature_spin.value())
        config.set('max_tokens', self.max_tokens_spin.value())

        # Search settings
        config.set('default_num_results', self.default_results_spin.value())
        config.set('citation_style', self.citation_style_combo.currentText())

        # UI settings
        theme_map = {'Dark': 'dark', 'Light': 'light', 'High Contrast': 'high_contrast', 'Academic': 'academic'}
        theme = theme_map.get(self.theme_combo.currentText(), 'dark')
        config.set('theme', theme)

        config.set('font_family', self.font_family_combo.currentFont().family())
        config.set('font_size', self.font_size_spin.value())

        # Database settings
        config.set('auto_save', self.auto_save_checkbox.isChecked())

        # Emit settings changed signal
        self.settings_changed.emit()

        QMessageBox.information(
            self,
            "Settings Saved",
            "Settings have been saved successfully."
        )

    def reset_settings(self):
        """Reset settings to defaults"""
        reply = QMessageBox.question(
            self,
            "Reset Settings",
            "Are you sure you want to reset all settings to defaults?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.main_window.config.reset_to_defaults()
            self.load_settings()

            QMessageBox.information(
                self,
                "Settings Reset",
                "Settings have been reset to defaults."
            )

    def on_theme_changed(self, theme_name: str):
        """Handle theme change"""
        theme_map = {
            'Dark': Theme.DARK,
            'Light': Theme.LIGHT,
            'High Contrast': Theme.HIGH_CONTRAST,
            'Academic': Theme.ACADEMIC
        }

        theme = theme_map.get(theme_name, Theme.DARK)
        self.theme_changed.emit(theme)
