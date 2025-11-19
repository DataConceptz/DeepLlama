"""
Enhanced report generation tab with writing styles, humanization, and performance optimizations
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QComboBox, QTextEdit, QGroupBox,
                               QProgressBar, QFileDialog, QMessageBox,
                               QDoubleSpinBox, QGridLayout, QCheckBox, QSpinBox)
from PySide6.QtCore import Qt, Signal, QThread, Slot, QTimer
from datetime import datetime
import time


class ReportWorker(QThread):
    """Worker thread for report generation with enhanced features"""

    finished = Signal(str)
    error = Signal(str)
    progress = Signal(str)
    time_update = Signal(float)

    def __init__(self, ollama_service, model, articles, query, temperature,
                 writing_style, humanize, report_type, fast_mode, timeout):
        super().__init__()
        self.ollama_service = ollama_service
        self.model = model
        self.articles = articles
        self.query = query
        self.temperature = temperature
        self.writing_style = writing_style
        self.humanize = humanize
        self.report_type = report_type
        self.fast_mode = fast_mode
        self.timeout = timeout
        self.current_text = ""
        self.start_time = None
        self._is_cancelled = False

    def run(self):
        """Generate report with enhanced features"""
        try:
            self.start_time = time.time()

            def callback(chunk):
                if self._is_cancelled:
                    return
                self.current_text += chunk
                self.progress.emit(chunk)
                elapsed = time.time() - self.start_time
                self.time_update.emit(elapsed)

            # Generate report with enhanced parameters
            report = self.ollama_service.generate_enhanced_report(
                model=self.model,
                articles=self.articles,
                query=self.query,
                temperature=self.temperature,
                writing_style=self.writing_style,
                humanize=self.humanize,
                report_type=self.report_type,
                fast_mode=self.fast_mode,
                timeout=self.timeout,
                callback=callback
            )

            if not self._is_cancelled:
                self.finished.emit(report)

        except TimeoutError:
            self.error.emit("Report generation timed out. Try using Fast Mode or a smaller model.")
        except Exception as e:
            self.error.emit(str(e))

    def cancel(self):
        """Cancel the generation"""
        self._is_cancelled = True


class ReportTab(QWidget):
    """Enhanced report generation tab widget"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.report_worker = None
        self.current_report = ""
        self.generation_start_time = None
        self.setup_ui()

    def setup_ui(self):
        """Setup enhanced user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel("📄 AI Report Generation")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        # Description
        desc = QLabel(
            "Generate comprehensive, fully-cited literature review reports with customizable writing styles, "
            "tone humanization, and performance optimization using local Ollama models."
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Settings group
        settings_group = QGroupBox("Report Configuration")
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

        # Report Type
        settings_layout.addWidget(QLabel("Report Type:"), 1, 0)
        self.report_type_combo = QComboBox()
        self.report_type_combo.addItems([
            "Comprehensive Literature Review",
            "Executive Summary",
            "Detailed Analysis",
            "Synthesis Report",
            "Comparative Study"
        ])
        self.report_type_combo.setToolTip("Select the type of report to generate")
        settings_layout.addWidget(self.report_type_combo, 1, 1)

        # Writing Style
        settings_layout.addWidget(QLabel("Writing Style:"), 2, 0)
        self.writing_style_combo = QComboBox()
        self.writing_style_combo.addItems([
            "Academic",
            "Professional",
            "Technical",
            "Executive Summary",
            "Journalistic"
        ])
        self.writing_style_combo.setCurrentText("Academic")
        self.writing_style_combo.setToolTip(
            "Academic: Formal, scholarly tone with technical terminology\n"
            "Professional: Business-appropriate, clear and concise\n"
            "Technical: Detailed, methodology-focused\n"
            "Executive Summary: High-level, decision-maker focused\n"
            "Journalistic: Accessible, narrative-driven"
        )
        settings_layout.addWidget(self.writing_style_combo, 2, 1)

        # Temperature
        settings_layout.addWidget(QLabel("Temperature:"), 3, 0)
        self.temperature_spin = QDoubleSpinBox()
        self.temperature_spin.setMinimum(0.0)
        self.temperature_spin.setMaximum(2.0)
        self.temperature_spin.setSingleStep(0.1)
        self.temperature_spin.setValue(self.main_window.config.get('temperature', 0.7))
        self.temperature_spin.setToolTip("Controls creativity (0.0 = focused, 2.0 = creative)")
        settings_layout.addWidget(self.temperature_spin, 3, 1)

        # Citation style
        settings_layout.addWidget(QLabel("Citation Style:"), 4, 0)
        self.citation_combo = QComboBox()
        self.citation_combo.addItems(["APA", "MLA", "Chicago", "IEEE"])
        current_style = self.main_window.config.get('citation_style', 'APA')
        self.citation_combo.setCurrentText(current_style)
        settings_layout.addWidget(self.citation_combo, 4, 1)

        # Humanize Writing Toggle
        settings_layout.addWidget(QLabel("Humanize Writing:"), 5, 0)
        self.humanize_checkbox = QCheckBox("Enable natural, conversational tone")
        self.humanize_checkbox.setChecked(True)
        self.humanize_checkbox.setToolTip(
            "When enabled:\n"
            "• Uses more natural, conversational language\n"
            "• Varies sentence structure and length\n"
            "• Incorporates transitional phrases\n"
            "• Reduces repetitive and mechanical phrasing\n"
            "• Maintains professionalism while improving flow"
        )
        settings_layout.addWidget(self.humanize_checkbox, 5, 1)

        # Fast Mode Toggle
        settings_layout.addWidget(QLabel("Performance:"), 6, 0)
        fast_mode_layout = QHBoxLayout()
        self.fast_mode_checkbox = QCheckBox("Fast Mode")
        self.fast_mode_checkbox.setChecked(False)
        self.fast_mode_checkbox.setToolTip("Optimize for speed with shorter, more concise reports")
        fast_mode_layout.addWidget(self.fast_mode_checkbox)

        # Timeout setting
        fast_mode_layout.addWidget(QLabel("Timeout:"))
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setMinimum(30)
        self.timeout_spin.setMaximum(600)
        self.timeout_spin.setValue(180)
        self.timeout_spin.setSuffix(" sec")
        self.timeout_spin.setToolTip("Maximum time to wait for report generation")
        fast_mode_layout.addWidget(self.timeout_spin)
        fast_mode_layout.addStretch()

        settings_layout.addLayout(fast_mode_layout, 6, 1)

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

        self.clear_button = QPushButton("🗑️ Clear Report")
        self.clear_button.setToolTip("Clear the generated report and reset")
        self.clear_button.clicked.connect(self.clear_report)
        button_layout.addWidget(self.clear_button)

        self.reset_button = QPushButton("🔄 Reset All")
        self.reset_button.setToolTip("Reset all settings to defaults")
        self.reset_button.clicked.connect(self.reset_all)
        button_layout.addWidget(self.reset_button)

        self.export_md_button = QPushButton("📥 Export MD")
        self.export_md_button.clicked.connect(self.export_markdown)
        button_layout.addWidget(self.export_md_button)

        self.export_docx_button = QPushButton("📥 Export DOCX")
        self.export_docx_button.clicked.connect(self.export_docx)
        button_layout.addWidget(self.export_docx_button)

        layout.addLayout(button_layout)

        # Progress bar with time estimate
        progress_layout = QVBoxLayout()

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)

        self.time_label = QLabel("")
        self.time_label.setStyleSheet("font-style: italic; color: #666;")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setVisible(False)
        progress_layout.addWidget(self.time_label)

        layout.addLayout(progress_layout)

        # Report output
        output_header = QHBoxLayout()
        output_label = QLabel("Generated Report:")
        output_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        output_header.addWidget(output_label)

        self.word_count_label = QLabel("")
        self.word_count_label.setStyleSheet("font-style: italic; color: #666;")
        output_header.addStretch()
        output_header.addWidget(self.word_count_label)

        layout.addLayout(output_header)

        self.report_text = QTextEdit()
        self.report_text.setPlaceholderText(
            "Your generated report will appear here...\n\n"
            "✨ New Features:\n"
            "• Choose from 5 writing styles (Academic, Professional, Technical, etc.)\n"
            "• Enable humanized writing for natural, flowing text\n"
            "• Fast Mode for quick report generation\n"
            "• Multiple report types (Comprehensive, Summary, Analysis, etc.)\n"
            "• Real-time progress with time estimates\n\n"
            "📝 Quick Start:\n"
            "1. Select articles from the Literature Database tab\n"
            "2. Choose your preferred writing style\n"
            "3. Enable 'Humanize Writing' for natural tone\n"
            "4. Select report type and click 'Generate Report'\n\n"
            "The report will include proper citations, executive summary, "
            "methodology, findings, and references in your chosen style."
        )
        self.report_text.textChanged.connect(self.update_word_count)
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
        """Generate enhanced literature review report"""
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

        # Get all parameters
        temperature = self.temperature_spin.value()
        writing_style = self.writing_style_combo.currentText()
        humanize = self.humanize_checkbox.isChecked()
        report_type = self.report_type_combo.currentText()
        fast_mode = self.fast_mode_checkbox.isChecked()
        timeout = self.timeout_spin.value()

        # Get query (use article topics)
        query = selected_articles[0].get('title', 'Literature Review')

        # Clear previous report
        self.report_text.clear()
        self.current_report = ""
        self.generation_start_time = time.time()

        # Update UI
        self.generate_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.time_label.setVisible(True)
        self.time_label.setText("Generating report...")

        # Create and start worker with enhanced parameters
        self.report_worker = ReportWorker(
            self.main_window.ollama_service,
            model,
            selected_articles,
            query,
            temperature,
            writing_style,
            humanize,
            report_type,
            fast_mode,
            timeout
        )
        self.report_worker.finished.connect(self.on_generation_finished)
        self.report_worker.error.connect(self.on_generation_error)
        self.report_worker.progress.connect(self.on_generation_progress)
        self.report_worker.time_update.connect(self.on_time_update)
        self.report_worker.start()

    @Slot(str)
    def on_generation_progress(self, chunk: str):
        """Handle generation progress"""
        # Append chunk to report
        self.report_text.insertPlainText(chunk)

        # Scroll to bottom
        scrollbar = self.report_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    @Slot(float)
    def on_time_update(self, elapsed: float):
        """Update time label"""
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        self.time_label.setText(f"⏱️ Time elapsed: {minutes}m {seconds}s")

    @Slot(str)
    def on_generation_finished(self, report: str):
        """Handle generation completion"""
        self.current_report = report
        self.generate_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)

        # Show completion time
        if self.generation_start_time:
            elapsed = time.time() - self.generation_start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            self.time_label.setText(f"✅ Generated in {minutes}m {seconds}s")

            # Hide after 5 seconds
            QTimer.singleShot(5000, lambda: self.time_label.setVisible(False))

        # Clean up worker
        if self.report_worker:
            self.report_worker = None

        # Update word count
        self.update_word_count()

        # Show completion message
        QMessageBox.information(
            self,
            "Report Generated",
            f"Report generation completed successfully!\n\n"
            f"Writing Style: {self.writing_style_combo.currentText()}\n"
            f"Report Type: {self.report_type_combo.currentText()}\n"
            f"Word Count: {len(report.split())}"
        )

    @Slot(str)
    def on_generation_error(self, error: str):
        """Handle generation error"""
        self.generate_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.time_label.setVisible(False)

        QMessageBox.critical(
            self,
            "Generation Error",
            f"Error generating report:\n\n{error}\n\n"
            f"Try:\n"
            f"• Using Fast Mode for quicker generation\n"
            f"• Selecting a smaller model\n"
            f"• Increasing the timeout setting\n"
            f"• Reducing the number of selected articles"
        )

        # Clean up worker
        if self.report_worker:
            self.report_worker = None

    def stop_generation(self):
        """Stop report generation"""
        if self.report_worker and self.report_worker.isRunning():
            self.report_worker.cancel()
            self.report_worker.terminate()
            self.report_worker.wait()
            self.report_worker = None

        self.generate_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.time_label.setVisible(False)

        QMessageBox.information(
            self,
            "Generation Stopped",
            "Report generation has been cancelled."
        )

    def clear_report(self):
        """Clear the generated report"""
        if self.current_report or self.report_text.toPlainText():
            reply = QMessageBox.question(
                self,
                "Clear Report",
                "Are you sure you want to clear the current report?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.report_text.clear()
                self.current_report = ""
                self.word_count_label.setText("")
                self.time_label.setVisible(False)

    def reset_all(self):
        """Reset all settings to defaults"""
        reply = QMessageBox.question(
            self,
            "Reset Settings",
            "Reset all report settings to defaults?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.writing_style_combo.setCurrentText("Academic")
            self.report_type_combo.setCurrentIndex(0)
            self.humanize_checkbox.setChecked(True)
            self.fast_mode_checkbox.setChecked(False)
            self.temperature_spin.setValue(0.7)
            self.timeout_spin.setValue(180)
            self.citation_combo.setCurrentText("APA")

    def update_word_count(self):
        """Update word count label"""
        text = self.report_text.toPlainText()
        if text:
            word_count = len(text.split())
            char_count = len(text)
            self.word_count_label.setText(
                f"📊 {word_count:,} words | {char_count:,} characters"
            )
        else:
            self.word_count_label.setText("")

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
                    'model': self.model_combo.currentText(),
                    'writing_style': self.writing_style_combo.currentText(),
                    'report_type': self.report_type_combo.currentText(),
                    'humanized': 'Yes' if self.humanize_checkbox.isChecked() else 'No'
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
                    'author': 'DeepLlama',
                    'writing_style': self.writing_style_combo.currentText(),
                    'report_type': self.report_type_combo.currentText()
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
