"""
Batch Operations Tab - AI Summarization, Tagging, Duplicate Detection
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QGroupBox, QProgressBar, QTextEdit,
                               QCheckBox, QComboBox, QListWidget, QListWidgetItem,
                               QMessageBox, QFileDialog, QSpinBox)
from PySide6.QtCore import Qt, Signal, QThread, Slot
from datetime import datetime


class BatchWorker(QThread):
    """Worker thread for batch operations"""

    finished = Signal(list)
    error = Signal(str)
    progress = Signal(int, int, str)  # current, total, message

    def __init__(self, operation_type, batch_service, articles, model=None, **kwargs):
        super().__init__()
        self.operation_type = operation_type
        self.batch_service = batch_service
        self.articles = articles
        self.model = model
        self.kwargs = kwargs

    def run(self):
        """Execute batch operation"""
        try:
            if self.operation_type == 'summarize':
                results = self.batch_service.batch_summarize(
                    self.articles,
                    self.model,
                    callback=self._progress_callback
                )
            elif self.operation_type == 'tag':
                results = self.batch_service.auto_tag_articles(
                    self.articles,
                    self.model,
                    callback=self._progress_callback
                )
            elif self.operation_type == 'duplicates':
                threshold = self.kwargs.get('threshold', 0.85)
                results = self.batch_service.detect_duplicates(self.articles, threshold)
            elif self.operation_type == 'gaps':
                results = self.batch_service.identify_research_gaps(self.articles, self.model)
            else:
                results = self.articles

            self.finished.emit(results)

        except Exception as e:
            self.error.emit(str(e))

    def _progress_callback(self, current, total, message):
        """Progress callback"""
        self.progress.emit(current, total, message)


class BatchTab(QWidget):
    """Batch Operations Tab"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.batch_worker = None
        self.setup_ui()

    def setup_ui(self):
        """Setup user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel("⚡ Batch Operations")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        # Description
        desc = QLabel(
            "Perform powerful batch operations on multiple articles using AI. "
            "Summarize, auto-tag, detect duplicates, and identify research gaps."
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Model selection
        model_group = QGroupBox("AI Model Selection")
        model_layout = QHBoxLayout(model_group)

        model_layout.addWidget(QLabel("Ollama Model:"))
        self.model_combo = QComboBox()
        self.refresh_models_button = QPushButton("🔄")
        self.refresh_models_button.setMaximumWidth(40)
        self.refresh_models_button.clicked.connect(self.refresh_models)

        model_layout.addWidget(self.model_combo)
        model_layout.addWidget(self.refresh_models_button)
        model_layout.addStretch()

        layout.addWidget(model_group)

        # Operations group
        ops_group = QGroupBox("Available Operations")
        ops_layout = QVBoxLayout(ops_group)

        # Batch Summarization
        summarize_layout = QHBoxLayout()
        self.summarize_button = QPushButton("📝 Batch Summarize Selected")
        self.summarize_button.setFixedHeight(50)
        self.summarize_button.setStyleSheet("font-weight: bold; font-size: 13px;")
        self.summarize_button.clicked.connect(self.batch_summarize)
        summarize_layout.addWidget(self.summarize_button)

        summarize_info = QLabel("Generate AI summaries for all selected articles")
        summarize_info.setStyleSheet("font-style: italic; color: #666;")
        summarize_layout.addWidget(summarize_info)
        summarize_layout.addStretch()

        ops_layout.addLayout(summarize_layout)

        # Auto-Tagging
        tag_layout = QHBoxLayout()
        self.tag_button = QPushButton("🏷️ Auto-Tag Selected")
        self.tag_button.setFixedHeight(50)
        self.tag_button.setStyleSheet("font-weight: bold; font-size: 13px;")
        self.tag_button.clicked.connect(self.auto_tag)
        tag_layout.addWidget(self.tag_button)

        tag_info = QLabel("Automatically generate tags/keywords using AI")
        tag_info.setStyleSheet("font-style: italic; color: #666;")
        tag_layout.addWidget(tag_info)
        tag_layout.addStretch()

        ops_layout.addLayout(tag_layout)

        # Duplicate Detection
        dup_layout = QHBoxLayout()
        self.duplicate_button = QPushButton("🔍 Detect Duplicates")
        self.duplicate_button.setFixedHeight(50)
        self.duplicate_button.setStyleSheet("font-weight: bold; font-size: 13px;")
        self.duplicate_button.clicked.connect(self.detect_duplicates)
        dup_layout.addWidget(self.duplicate_button)

        dup_info = QLabel("Find duplicate articles based on title/DOI similarity")
        dup_info.setStyleSheet("font-style: italic; color: #666;")
        dup_layout.addWidget(dup_info)

        dup_layout.addWidget(QLabel("Threshold:"))
        self.threshold_spin = QSpinBox()
        self.threshold_spin.setMinimum(50)
        self.threshold_spin.setMaximum(100)
        self.threshold_spin.setValue(85)
        self.threshold_spin.setSuffix("%")
        dup_layout.addWidget(self.threshold_spin)
        dup_layout.addStretch()

        ops_layout.addLayout(dup_layout)

        # Research Gaps
        gaps_layout = QHBoxLayout()
        self.gaps_button = QPushButton("🎯 Identify Research Gaps")
        self.gaps_button.setFixedHeight(50)
        self.gaps_button.setStyleSheet("font-weight: bold; font-size: 13px;")
        self.gaps_button.clicked.connect(self.identify_gaps)
        gaps_layout.addWidget(self.gaps_button)

        gaps_info = QLabel("AI-powered analysis of research gaps and opportunities")
        gaps_info.setStyleSheet("font-style: italic; color: #666;")
        gaps_layout.addWidget(gaps_info)
        gaps_layout.addStretch()

        ops_layout.addLayout(gaps_layout)

        # Export Operations
        export_layout = QHBoxLayout()
        self.export_bibtex_button = QPushButton("📄 Export BibTeX")
        self.export_bibtex_button.clicked.connect(lambda: self.export_format('bibtex'))
        export_layout.addWidget(self.export_bibtex_button)

        self.export_ris_button = QPushButton("📄 Export RIS")
        self.export_ris_button.clicked.connect(lambda: self.export_format('ris'))
        export_layout.addWidget(self.export_ris_button)

        self.export_endnote_button = QPushButton("📄 Export EndNote")
        self.export_endnote_button.clicked.connect(lambda: self.export_format('endnote'))
        export_layout.addWidget(self.export_endnote_button)

        export_layout.addStretch()

        ops_layout.addLayout(export_layout)

        layout.addWidget(ops_group)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.progress_label = QLabel("")
        self.progress_label.setVisible(False)
        layout.addWidget(self.progress_label)

        # Results area
        results_label = QLabel("Results:")
        results_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(results_label)

        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setPlaceholderText(
            "Results from batch operations will appear here...\n\n"
            "Available operations:\n"
            "• Batch Summarize: Generate AI summaries for multiple articles\n"
            "• Auto-Tag: Automatically extract keywords and tags\n"
            "• Detect Duplicates: Find duplicate articles\n"
            "• Identify Research Gaps: AI analysis of research opportunities\n"
            "• Export: BibTeX, RIS, EndNote formats"
        )
        layout.addWidget(self.results_text)

        # Initialize
        self.refresh_models()

    def refresh_models(self):
        """Refresh available models"""
        self.model_combo.clear()

        if not self.main_window.ollama_service.is_available():
            self.model_combo.addItem("❌ Ollama not running")
            self.disable_ai_operations()
            return

        models = self.main_window.ollama_service.get_models()

        if not models:
            self.model_combo.addItem("No models available")
            self.disable_ai_operations()
            return

        for model in models:
            self.model_combo.addItem(model.name)

        self.enable_ai_operations()

        # Set default
        default_model = self.main_window.config.get('default_model', '')
        if default_model:
            index = self.model_combo.findText(default_model)
            if index >= 0:
                self.model_combo.setCurrentIndex(index)

    def disable_ai_operations(self):
        """Disable AI-dependent operations"""
        self.summarize_button.setEnabled(False)
        self.tag_button.setEnabled(False)
        self.gaps_button.setEnabled(False)

    def enable_ai_operations(self):
        """Enable AI-dependent operations"""
        self.summarize_button.setEnabled(True)
        self.tag_button.setEnabled(True)
        self.gaps_button.setEnabled(True)

    def batch_summarize(self):
        """Batch summarize selected articles"""
        articles = self.main_window.get_selected_articles()

        if not articles:
            QMessageBox.warning(
                self,
                "No Articles Selected",
                "Please select articles from the Literature Database tab."
            )
            return

        model = self.model_combo.currentText()
        if model.startswith("❌") or model == "No models available":
            QMessageBox.warning(self, "No Model", "Please select a valid Ollama model.")
            return

        # Import batch service
        from ..services.batch_service import BatchService
        batch_service = BatchService(self.main_window.ollama_service, self.main_window.db)

        # Confirm
        reply = QMessageBox.question(
            self,
            "Batch Summarize",
            f"Generate summaries for {len(articles)} articles?\n\nThis may take several minutes.",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        # Start operation
        self.results_text.clear()
        self.results_text.append(f"Starting batch summarization of {len(articles)} articles...\n")

        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(articles))
        self.progress_bar.setValue(0)
        self.progress_label.setVisible(True)

        self.batch_worker = BatchWorker('summarize', batch_service, articles, model)
        self.batch_worker.progress.connect(self.on_progress)
        self.batch_worker.finished.connect(self.on_summarize_finished)
        self.batch_worker.error.connect(self.on_error)
        self.batch_worker.start()

    @Slot(list)
    def on_summarize_finished(self, results):
        """Handle summarization completion"""
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)

        self.results_text.append(f"\n✅ Completed! Summarized {len(results)} articles.")

        # Reload articles
        self.main_window.load_articles_from_db()

        QMessageBox.information(
            self,
            "Batch Summarization Complete",
            f"Successfully summarized {len(results)} articles!"
        )

    def auto_tag(self):
        """Auto-tag selected articles"""
        articles = self.main_window.get_selected_articles()

        if not articles:
            QMessageBox.warning(
                self,
                "No Articles Selected",
                "Please select articles from the Literature Database tab."
            )
            return

        model = self.model_combo.currentText()
        if model.startswith("❌") or model == "No models available":
            QMessageBox.warning(self, "No Model", "Please select a valid Ollama model.")
            return

        from ..services.batch_service import BatchService
        batch_service = BatchService(self.main_window.ollama_service, self.main_window.db)

        reply = QMessageBox.question(
            self,
            "Auto-Tag",
            f"Auto-tag {len(articles)} articles using AI?\n\nThis may take several minutes.",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        self.results_text.clear()
        self.results_text.append(f"Starting auto-tagging of {len(articles)} articles...\n")

        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(articles))
        self.progress_bar.setValue(0)
        self.progress_label.setVisible(True)

        self.batch_worker = BatchWorker('tag', batch_service, articles, model)
        self.batch_worker.progress.connect(self.on_progress)
        self.batch_worker.finished.connect(self.on_tag_finished)
        self.batch_worker.error.connect(self.on_error)
        self.batch_worker.start()

    @Slot(list)
    def on_tag_finished(self, results):
        """Handle tagging completion"""
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)

        self.results_text.append(f"\n✅ Completed! Tagged {len(results)} articles.")

        self.main_window.load_articles_from_db()

        QMessageBox.information(
            self,
            "Auto-Tagging Complete",
            f"Successfully tagged {len(results)} articles!"
        )

    def detect_duplicates(self):
        """Detect duplicate articles"""
        articles = self.main_window.current_articles

        if not articles:
            QMessageBox.warning(self, "No Articles", "No articles in database.")
            return

        from ..services.batch_service import BatchService
        batch_service = BatchService(self.main_window.ollama_service, self.main_window.db)

        threshold = self.threshold_spin.value() / 100.0

        self.results_text.clear()
        self.results_text.append(f"Detecting duplicates in {len(articles)} articles...\n")
        self.results_text.append(f"Similarity threshold: {threshold:.0%}\n\n")

        self.batch_worker = BatchWorker('duplicates', batch_service, articles, threshold=threshold)
        self.batch_worker.finished.connect(self.on_duplicates_finished)
        self.batch_worker.error.connect(self.on_error)
        self.batch_worker.start()

    @Slot(list)
    def on_duplicates_finished(self, duplicate_groups):
        """Handle duplicate detection completion"""
        if not duplicate_groups:
            self.results_text.append("✅ No duplicates found!")
        else:
            self.results_text.append(f"⚠️ Found {len(duplicate_groups)} groups of duplicates:\n\n")

            for i, group in enumerate(duplicate_groups, 1):
                self.results_text.append(f"Group {i} ({len(group)} articles):")
                for article in group:
                    self.results_text.append(f"  • {article.get('title', 'Untitled')} ({article.get('year', 'N/A')})")
                self.results_text.append("")

    def identify_gaps(self):
        """Identify research gaps"""
        articles = self.main_window.current_articles

        if not articles:
            QMessageBox.warning(self, "No Articles", "No articles in database.")
            return

        model = self.model_combo.currentText()
        if model.startswith("❌") or model == "No models available":
            QMessageBox.warning(self, "No Model", "Please select a valid Ollama model.")
            return

        from ..services.batch_service import BatchService
        batch_service = BatchService(self.main_window.ollama_service, self.main_window.db)

        self.results_text.clear()
        self.results_text.append(f"Analyzing {len(articles)} articles for research gaps...\n")
        self.results_text.append("This may take a few minutes...\n\n")

        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)

        self.batch_worker = BatchWorker('gaps', batch_service, articles[:50], model)  # Limit to 50
        self.batch_worker.finished.connect(self.on_gaps_finished)
        self.batch_worker.error.connect(self.on_error)
        self.batch_worker.start()

    @Slot(list)
    def on_gaps_finished(self, analysis):
        """Handle research gaps analysis completion"""
        self.progress_bar.setVisible(False)

        if isinstance(analysis, str):
            self.results_text.append("Research Gap Analysis:\n\n")
            self.results_text.append(analysis)
        else:
            self.results_text.append("✅ Analysis complete!")

    @Slot(int, int, str)
    def on_progress(self, current, total, message):
        """Handle progress updates"""
        self.progress_bar.setValue(current)
        self.progress_label.setText(f"Processing: {message} ({current}/{total})")

    @Slot(str)
    def on_error(self, error):
        """Handle errors"""
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        self.results_text.append(f"\n❌ Error: {error}")

    def export_format(self, format_type):
        """Export to specific format"""
        articles = self.main_window.get_selected_articles()

        if not articles:
            articles = self.main_window.current_articles

        if not articles:
            QMessageBox.warning(self, "No Articles", "No articles to export.")
            return

        from ..services.advanced_export import AdvancedExportService

        extensions = {
            'bibtex': '.bib',
            'ris': '.ris',
            'endnote': '.xml'
        }

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            f"Export {format_type.upper()}",
            f"literature_{datetime.now().strftime('%Y%m%d_%H%M%S')}{extensions[format_type]}",
            f"{format_type.upper()} Files (*{extensions[format_type]})"
        )

        if file_path:
            try:
                if format_type == 'bibtex':
                    success = AdvancedExportService.export_to_bibtex(articles, file_path)
                elif format_type == 'ris':
                    success = AdvancedExportService.export_to_ris(articles, file_path)
                elif format_type == 'endnote':
                    success = AdvancedExportService.export_to_endnote(articles, file_path)

                if success:
                    QMessageBox.information(
                        self,
                        "Export Successful",
                        f"Exported {len(articles)} articles to {format_type.upper()} format."
                    )
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Error: {str(e)}")
