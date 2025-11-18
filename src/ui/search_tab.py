"""
Search tab for querying academic databases
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QSpinBox, QCheckBox,
                               QGroupBox, QProgressBar, QTextEdit, QGridLayout)
from PySide6.QtCore import Qt, Signal, QThread, Slot


class SearchWorker(QThread):
    """Worker thread for searching"""

    finished = Signal(list)
    error = Signal(str)
    progress = Signal(str)

    def __init__(self, search_service, query, max_results, sources):
        super().__init__()
        self.search_service = search_service
        self.query = query
        self.max_results = max_results
        self.sources = sources

    def run(self):
        """Execute search"""
        try:
            self.progress.emit("Searching academic databases...")
            results = self.search_service.search_all(
                self.query,
                self.max_results,
                self.sources
            )
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))


class SearchTab(QWidget):
    """Search tab widget"""

    search_completed = Signal(list)

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.search_worker = None
        self.setup_ui()

    def setup_ui(self):
        """Setup user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel("📚 Academic Literature Search")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        # Description
        desc = QLabel(
            "Search across multiple academic databases including OpenAlex, PubMed, arXiv, "
            "Semantic Scholar, and CORE. Enter keywords, phrases, or research topics to find relevant articles."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("margin-bottom: 15px;")
        layout.addWidget(desc)

        # Search input group
        search_group = QGroupBox("Search Query")
        search_layout = QVBoxLayout(search_group)

        # Query input
        query_layout = QHBoxLayout()
        query_layout.addWidget(QLabel("Query:"))
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Enter keywords, phrases, or research topic...")
        self.query_input.returnPressed.connect(self.start_search)
        query_layout.addWidget(self.query_input)
        search_layout.addLayout(query_layout)

        # Number of results
        results_layout = QHBoxLayout()
        results_layout.addWidget(QLabel("Number of articles:"))
        self.num_results_spin = QSpinBox()
        self.num_results_spin.setMinimum(1)
        self.num_results_spin.setMaximum(1000)
        self.num_results_spin.setValue(self.main_window.config.get('default_num_results', 50))
        self.num_results_spin.setFixedWidth(100)
        results_layout.addWidget(self.num_results_spin)
        results_layout.addStretch()
        search_layout.addLayout(results_layout)

        layout.addWidget(search_group)

        # Source selection group
        source_group = QGroupBox("Data Sources")
        source_layout = QGridLayout(source_group)

        self.source_checkboxes = {}
        sources = [
            ('openalex', 'OpenAlex'),
            ('pubmed', 'PubMed'),
            ('arxiv', 'arXiv'),
            ('semantic_scholar', 'Semantic Scholar'),
            ('core', 'CORE')
        ]

        default_sources = self.main_window.config.get('default_search_sources', [])

        for i, (key, label) in enumerate(sources):
            checkbox = QCheckBox(label)
            checkbox.setChecked(key in default_sources)
            self.source_checkboxes[key] = checkbox
            row = i // 3
            col = i % 3
            source_layout.addWidget(checkbox, row, col)

        # Select/Deselect all buttons
        select_buttons_layout = QHBoxLayout()
        select_all_btn = QPushButton("Select All")
        select_all_btn.clicked.connect(self.select_all_sources)
        select_all_btn.setMaximumWidth(120)
        select_buttons_layout.addWidget(select_all_btn)

        deselect_all_btn = QPushButton("Deselect All")
        deselect_all_btn.clicked.connect(self.deselect_all_sources)
        deselect_all_btn.setMaximumWidth(120)
        select_buttons_layout.addWidget(deselect_all_btn)
        select_buttons_layout.addStretch()

        source_layout.addLayout(select_buttons_layout, (len(sources) // 3) + 1, 0, 1, 3)

        layout.addWidget(source_group)

        # Search button
        button_layout = QHBoxLayout()
        self.search_button = QPushButton("🔍 Search")
        self.search_button.setFixedHeight(40)
        self.search_button.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.search_button.clicked.connect(self.start_search)
        button_layout.addStretch()
        button_layout.addWidget(self.search_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)

        # Status text
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(150)
        self.status_text.setPlaceholderText("Search status will appear here...")
        layout.addWidget(self.status_text)

        layout.addStretch()

    def select_all_sources(self):
        """Select all source checkboxes"""
        for checkbox in self.source_checkboxes.values():
            checkbox.setChecked(True)

    def deselect_all_sources(self):
        """Deselect all source checkboxes"""
        for checkbox in self.source_checkboxes.values():
            checkbox.setChecked(False)

    def get_selected_sources(self) -> list:
        """Get list of selected sources"""
        return [key for key, checkbox in self.source_checkboxes.items()
                if checkbox.isChecked()]

    def start_search(self):
        """Start the search process"""
        query = self.query_input.text().strip()

        if not query:
            self.status_text.append("<b style='color: orange;'>⚠️ Please enter a search query</b>")
            return

        sources = self.get_selected_sources()
        if not sources:
            self.status_text.append("<b style='color: orange;'>⚠️ Please select at least one data source</b>")
            return

        max_results = self.num_results_spin.value()

        # Disable search button
        self.search_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress

        # Clear status
        self.status_text.clear()
        self.status_text.append(f"<b>🔍 Searching for:</b> {query}")
        self.status_text.append(f"<b>📊 Max results:</b> {max_results}")
        self.status_text.append(f"<b>📚 Sources:</b> {', '.join(sources)}")
        self.status_text.append("")

        # Create and start worker thread
        self.search_worker = SearchWorker(
            self.main_window.search_service,
            query,
            max_results,
            sources
        )
        self.search_worker.finished.connect(self.on_search_finished)
        self.search_worker.error.connect(self.on_search_error)
        self.search_worker.progress.connect(self.on_search_progress)
        self.search_worker.start()

    @Slot(list)
    def on_search_finished(self, results: list):
        """Handle search completion"""
        self.search_button.setEnabled(True)
        self.progress_bar.setVisible(False)

        if results:
            self.status_text.append(f"<b style='color: green;'>✅ Found {len(results)} articles!</b>")

            # Show summary by source
            sources_count = {}
            for article in results:
                source = article.get('source', 'Unknown')
                sources_count[source] = sources_count.get(source, 0) + 1

            self.status_text.append("")
            self.status_text.append("<b>Results by source:</b>")
            for source, count in sources_count.items():
                self.status_text.append(f"  • {source}: {count} articles")

            # Emit signal
            self.search_completed.emit(results)
        else:
            self.status_text.append("<b style='color: orange;'>⚠️ No articles found. Try different keywords or sources.</b>")

    @Slot(str)
    def on_search_error(self, error: str):
        """Handle search error"""
        self.search_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_text.append(f"<b style='color: red;'>❌ Error: {error}</b>")

    @Slot(str)
    def on_search_progress(self, message: str):
        """Handle search progress update"""
        self.status_text.append(message)
