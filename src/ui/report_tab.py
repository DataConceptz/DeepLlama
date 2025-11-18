"""
Report generation tab
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QComboBox, QTextEdit, QGroupBox,
                               QProgressBar, QFileDialog, QMessageBox, QSlider,
                               QDoubleSpinBox, QGridLayout)
from PySide6.QtCore import Qt, Signal, QThread, Slot
from datetime import datetime


class ReportWorker(QThread):
    """Worker thread for report generation"""

    finished = Signal(str)
    error = Signal(str)
    progress = Signal(str)

    def __init__(self, ollama_service, model, articles, query, temperature):
        super().__init__()
        self.ollama_service = ollama_service
        self.model = model
        self.articles = articles
        self.query = query
        self.temperature = temperature
        self.current_text = ""

    def run(self):
        """Generate report"""
        try:
            def callback(chunk):
                self.current_text += chunk
                self.progress.emit(chunk)

            # Generate report
            report = self.ollama_service.generate_report(
                model=self.model,
                articles=self.articles,
                query=self.query,
                temperature=self.temperature,
                callback=callback
            )

            self.finished.emit(report)

        except Exception as e:
            self.error.emit(str(e))


class ReportTab(QWidget):
    """Report generation tab widget"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.report_worker = None
        self.current_report = ""
        self.setup_ui()

    def setup_ui(self):
        """Setup user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel("📄 AI Report Generation")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        # Description
        desc = QLabel(
            "Generate comprehensive, fully-cited literature review reports using local Ollama models. "
            "Select articles from the Literature Database tab and choose a model to generate your report."
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Settings group
        settings_group = QGroupBox("Report Settings")
        settings_layout = QGridLayout(settings_group)

        # Model selection
        settings_layout.addWidget(QLabel("Model:"), 0, 0)
        self.model_combo = QComboBox()
        self.refresh_models_button = QPushButton("🔄")
        self.refresh_models_button.setMaximumWidth(40)
        self.refresh_models_button.setToolTip("Refresh model list")
        self.refresh_models_button.clicked.connect(self.refresh_models)

        model_layout = QHBoxLayout()
        model_layout.addWidget(self.model_combo)
        model_layout.addWidget(self.refresh_models_button)
        settings_layout.addLayout(model_layout, 0, 1)

        # Temperature
        settings_layout.addWidget(QLabel("Temperature:"), 1, 0)
        self.temperature_spin = QDoubleSpinBox()
        self.temperature_spin.setMinimum(0.0)
        self.temperature_spin.setMaximum(2.0)
        self.temperature_spin.setSingleStep(0.1)
        self.temperature_spin.setValue(self.main_window.config.get('temperature', 0.7))
        self.temperature_spin.setToolTip("Controls creativity (0.0 = focused, 2.0 = creative)")
        settings_layout.addWidget(self.temperature_spin, 1, 1)

        # Citation style
        settings_layout.addWidget(QLabel("Citation Style:"), 2, 0)
        self.citation_combo = QComboBox()
        self.citation_combo.addItems(["APA", "MLA", "Chicago", "IEEE"])
        current_style = self.main_window.config.get('citation_style', 'APA')
        self.citation_combo.setCurrentText(current_style)
        settings_layout.addWidget(self.citation_combo, 2, 1)

        layout.addWidget(settings_group)

        # Selected articles info
        self.selection_label = QLabel("0 articles selected for report")
        self.selection_label.setStyleSheet("font-weight: bold; color: #0078d4;")
        layout.addWidget(self.selection_label)

        # Action buttons
        button_layout = QHBoxLayout()

        self.generate_button = QPushButton("✨ Generate Report")
        self.generate_button.setFixedHeight(40)
        self.generate_button.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.generate_button.clicked.connect(self.generate_report)
        button_layout.addWidget(self.generate_button)

        self.stop_button = QPushButton("⏹️ Stop")
        self.stop_button.setFixedHeight(40)
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_generation)
        button_layout.addWidget(self.stop_button)

        button_layout.addStretch()

        self.clear_button = QPushButton("🗑️ Clear")
        self.clear_button.clicked.connect(self.clear_report)
        button_layout.addWidget(self.clear_button)

        self.export_md_button = QPushButton("📥 Export Markdown")
        self.export_md_button.clicked.connect(self.export_markdown)
        button_layout.addWidget(self.export_md_button)

        self.export_docx_button = QPushButton("📥 Export DOCX")
        self.export_docx_button.clicked.connect(self.export_docx)
        button_layout.addWidget(self.export_docx_button)

        layout.addLayout(button_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Report output
        output_label = QLabel("Generated Report:")
        output_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(output_label)

        self.report_text = QTextEdit()
        self.report_text.setPlaceholderText(
            "Your generated report will appear here...\n\n"
            "Tips:\n"
            "1. Select articles from the Literature Database tab\n"
            "2. Choose an Ollama model\n"
            "3. Adjust temperature for creativity\n"
            "4. Click 'Generate Report'\n\n"
            "The report will include proper citations, executive summary, "
            "methodology, findings, and references."
        )
        layout.addWidget(self.report_text)

        # Initial model refresh
        self.refresh_models()

        # Connect to selection changes
        self.main_window.results_tab.selection_changed.connect(self.on_selection_changed)

    def refresh_models(self):
        """Refresh available Ollama models"""
        self.model_combo.clear()

        if not self.main_window.ollama_service.is_available():
            self.model_combo.addItem("❌ Ollama not running")
            self.generate_button.setEnabled(False)
            QMessageBox.warning(
                self,
                "Ollama Not Available",
                "Ollama is not running. Please start Ollama and try again.\n\n"
                "Visit https://ollama.ai for installation instructions."
            )
            return

        models = self.main_window.ollama_service.get_models()

        if not models:
            self.model_combo.addItem("No models available")
            self.generate_button.setEnabled(False)
            return

        for model in models:
            self.model_combo.addItem(model.name)

        self.generate_button.setEnabled(True)

        # Set default model if configured
        default_model = self.main_window.config.get('default_model', '')
        if default_model:
            index = self.model_combo.findText(default_model)
            if index >= 0:
                self.model_combo.setCurrentIndex(index)

    def on_selection_changed(self, selected_ids: list):
        """Handle article selection change"""
        count = len(selected_ids)
        self.selection_label.setText(f"{count} article(s) selected for report")

    def generate_report(self):
        """Generate literature review report"""
        # Get selected articles
        selected_articles = self.main_window.get_selected_articles()

        if not selected_articles:
            QMessageBox.warning(
                self,
                "No Articles Selected",
                "Please select at least one article from the Literature Database tab."
            )
            return

        # Get model
        model = self.model_combo.currentText()
        if model.startswith("❌") or model == "No models available":
            QMessageBox.warning(
                self,
                "No Model Selected",
                "Please select a valid Ollama model."
            )
            return

        # Get temperature
        temperature = self.temperature_spin.value()

        # Get query (use first article title as basis)
        query = selected_articles[0].get('title', 'Literature Review')

        # Clear previous report
        self.report_text.clear()
        self.current_report = ""

        # Disable buttons
        self.generate_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)

        # Create and start worker
        self.report_worker = ReportWorker(
            self.main_window.ollama_service,
            model,
            selected_articles,
            query,
            temperature
        )
        self.report_worker.finished.connect(self.on_generation_finished)
        self.report_worker.error.connect(self.on_generation_error)
        self.report_worker.progress.connect(self.on_generation_progress)
        self.report_worker.start()

    @Slot(str)
    def on_generation_progress(self, chunk: str):
        """Handle generation progress"""
        # Append chunk to report
        self.report_text.insertPlainText(chunk)

        # Scroll to bottom
        scrollbar = self.report_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    @Slot(str)
    def on_generation_finished(self, report: str):
        """Handle generation completion"""
        self.current_report = report
        self.generate_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)

        # Clean up worker
        if self.report_worker:
            self.report_worker = None

        QMessageBox.information(
            self,
            "Report Generated",
            "Report generation completed successfully!"
        )

    @Slot(str)
    def on_generation_error(self, error: str):
        """Handle generation error"""
        self.generate_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)

        QMessageBox.critical(
            self,
            "Generation Error",
            f"Error generating report:\n\n{error}"
        )

        # Clean up worker
        if self.report_worker:
            self.report_worker = None

    def stop_generation(self):
        """Stop report generation"""
        if self.report_worker and self.report_worker.isRunning():
            self.report_worker.terminate()
            self.report_worker.wait()
            self.report_worker = None

        self.generate_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)

    def clear_report(self):
        """Clear the generated report"""
        self.report_text.clear()
        self.current_report = ""

    def export_markdown(self):
        """Export report to Markdown"""
        if not self.current_report and not self.report_text.toPlainText():
            QMessageBox.warning(
                self,
                "No Report",
                "No report to export. Please generate a report first."
            )
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Markdown",
            f"literature_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            "Markdown Files (*.md)"
        )

        if file_path:
            try:
                content = self.report_text.toPlainText()

                metadata = {
                    'title': 'Literature Review Report',
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'generated_by': 'DeepLlama',
                    'model': self.model_combo.currentText()
                }

                success = self.main_window.export_service.export_to_markdown(
                    content,
                    file_path,
                    metadata
                )

                if success:
                    QMessageBox.information(
                        self,
                        "Export Successful",
                        f"Report exported to:\n{file_path}"
                    )
                else:
                    QMessageBox.warning(
                        self,
                        "Export Failed",
                        "Failed to export report."
                    )

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Export Error",
                    f"Error exporting report:\n\n{str(e)}"
                )

    def export_docx(self):
        """Export report to DOCX"""
        if not self.current_report and not self.report_text.toPlainText():
            QMessageBox.warning(
                self,
                "No Report",
                "No report to export. Please generate a report first."
            )
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export DOCX",
            f"literature_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
            "Word Documents (*.docx)"
        )

        if file_path:
            try:
                content = self.report_text.toPlainText()

                metadata = {
                    'title': 'Literature Review Report',
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'author': 'DeepLlama'
                }

                success = self.main_window.export_service.export_to_docx(
                    content,
                    file_path,
                    metadata
                )

                if success:
                    QMessageBox.information(
                        self,
                        "Export Successful",
                        f"Report exported to:\n{file_path}"
                    )
                else:
                    QMessageBox.warning(
                        self,
                        "Export Failed",
                        "Failed to export report. Make sure python-docx is installed."
                    )

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Export Error",
                    f"Error exporting report:\n\n{str(e)}"
                )
