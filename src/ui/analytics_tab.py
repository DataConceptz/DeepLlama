"""
Analytics Dashboard Tab - Visualizations and Insights
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QGroupBox, QGridLayout, QTextEdit,
                               QScrollArea, QProgressBar, QComboBox)
from PySide6.QtCore import Qt, Signal, QThread, Slot
from PySide6.QtGui import QFont
from collections import Counter
from datetime import datetime
import json


class AnalyticsWorker(QThread):
    """Worker thread for analytics computation"""

    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, articles):
        super().__init__()
        self.articles = articles

    def run(self):
        """Compute analytics"""
        try:
            analytics = self.compute_analytics()
            self.finished.emit(analytics)
        except Exception as e:
            self.error.emit(str(e))

    def compute_analytics(self):
        """Compute comprehensive analytics"""
        if not self.articles:
            return {}

        # Basic stats
        total_articles = len(self.articles)

        # Year distribution
        years = [a.get('year', 0) for a in self.articles if a.get('year', 0) > 1900]
        year_counts = Counter(years)

        # Author analysis
        all_authors = []
        for article in self.articles:
            authors_str = article.get('authors', '')
            if authors_str:
                authors = [a.strip() for a in authors_str.split(',')]
                all_authors.extend(authors)
        author_counts = Counter(all_authors)

        # Journal analysis
        journals = [a.get('journal', 'Unknown') for a in self.articles if a.get('journal')]
        journal_counts = Counter(journals)

        # Source distribution
        sources = [a.get('source', 'Unknown') for a in self.articles]
        source_counts = Counter(sources)

        # Keywords analysis
        all_keywords = []
        for article in self.articles:
            keywords_str = article.get('keywords', '')
            if keywords_str:
                keywords = [k.strip() for k in keywords_str.split(',')]
                all_keywords.extend(keywords)
        keyword_counts = Counter(all_keywords)

        # Citations/Score analysis
        scores = [a.get('score', 0) for a in self.articles if a.get('score', 0) > 0]
        avg_score = sum(scores) / len(scores) if scores else 0

        # Research trends (recent vs older)
        current_year = datetime.now().year
        recent_articles = len([a for a in self.articles if a.get('year', 0) >= current_year - 5])
        older_articles = total_articles - recent_articles

        # Abstract length analysis
        abstract_lengths = [len(a.get('abstract', '')) for a in self.articles if a.get('abstract')]
        avg_abstract_length = sum(abstract_lengths) / len(abstract_lengths) if abstract_lengths else 0

        return {
            'total_articles': total_articles,
            'year_distribution': dict(sorted(year_counts.items(), reverse=True)[:10]),
            'top_authors': dict(author_counts.most_common(10)),
            'top_journals': dict(journal_counts.most_common(10)),
            'source_distribution': dict(source_counts.items()),
            'top_keywords': dict(keyword_counts.most_common(20)),
            'avg_score': avg_score,
            'recent_articles': recent_articles,
            'older_articles': older_articles,
            'avg_abstract_length': int(avg_abstract_length),
            'year_range': (min(years) if years else 0, max(years) if years else 0)
        }


class AnalyticsTab(QWidget):
    """Analytics Dashboard Tab"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.analytics_worker = None
        self.current_analytics = {}
        self.setup_ui()

    def setup_ui(self):
        """Setup user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel("📊 Analytics Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        # Description
        desc = QLabel(
            "Comprehensive analytics and insights about your literature collection. "
            "Visualize trends, identify top authors, journals, and research themes."
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Control buttons
        button_layout = QHBoxLayout()

        self.refresh_button = QPushButton("🔄 Refresh Analytics")
        self.refresh_button.setFixedHeight(40)
        self.refresh_button.setStyleSheet("font-weight: bold;")
        self.refresh_button.clicked.connect(self.refresh_analytics)
        button_layout.addWidget(self.refresh_button)

        self.export_button = QPushButton("📥 Export Analytics")
        self.export_button.clicked.connect(self.export_analytics)
        button_layout.addWidget(self.export_button)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Scroll area for analytics
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Analytics container
        analytics_container = QWidget()
        self.analytics_layout = QVBoxLayout(analytics_container)
        self.analytics_layout.setSpacing(15)

        # Overview section
        self.overview_group = QGroupBox("📈 Overview")
        self.overview_layout = QGridLayout(self.overview_group)
        self.analytics_layout.addWidget(self.overview_group)

        # Publication timeline
        self.timeline_group = QGroupBox("📅 Publication Timeline")
        self.timeline_layout = QVBoxLayout(self.timeline_group)
        self.analytics_layout.addWidget(self.timeline_group)

        # Top authors
        self.authors_group = QGroupBox("👥 Top Authors")
        self.authors_layout = QVBoxLayout(self.authors_group)
        self.analytics_layout.addWidget(self.authors_group)

        # Top journals
        self.journals_group = QGroupBox("📚 Top Journals")
        self.journals_layout = QVBoxLayout(self.journals_group)
        self.analytics_layout.addWidget(self.journals_group)

        # Keywords cloud
        self.keywords_group = QGroupBox("🏷️ Top Keywords")
        self.keywords_layout = QVBoxLayout(self.keywords_group)
        self.analytics_layout.addWidget(self.keywords_group)

        # Source distribution
        self.sources_group = QGroupBox("🗂️ Source Distribution")
        self.sources_layout = QVBoxLayout(self.sources_group)
        self.analytics_layout.addWidget(self.sources_group)

        scroll.setWidget(analytics_container)
        layout.addWidget(scroll)

        # Connect to article changes
        self.main_window.articles_loaded.connect(self.on_articles_loaded)

        # Initial analytics
        self.refresh_analytics()

    def on_articles_loaded(self, articles):
        """Handle new articles loaded"""
        self.refresh_analytics()

    def refresh_analytics(self):
        """Refresh analytics computation"""
        articles = self.main_window.current_articles

        if not articles:
            self.show_empty_state()
            return

        # Show progress
        self.refresh_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)

        # Start worker
        self.analytics_worker = AnalyticsWorker(articles)
        self.analytics_worker.finished.connect(self.on_analytics_finished)
        self.analytics_worker.error.connect(self.on_analytics_error)
        self.analytics_worker.start()

    @Slot(dict)
    def on_analytics_finished(self, analytics):
        """Handle analytics computation completion"""
        self.current_analytics = analytics
        self.refresh_button.setEnabled(True)
        self.progress_bar.setVisible(False)

        # Update UI
        self.update_overview(analytics)
        self.update_timeline(analytics)
        self.update_authors(analytics)
        self.update_journals(analytics)
        self.update_keywords(analytics)
        self.update_sources(analytics)

    @Slot(str)
    def on_analytics_error(self, error):
        """Handle analytics error"""
        self.refresh_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.show_error(error)

    def update_overview(self, analytics):
        """Update overview section"""
        # Clear previous
        while self.overview_layout.count():
            child = self.overview_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Add metrics
        metrics = [
            ("Total Articles", f"{analytics.get('total_articles', 0):,}"),
            ("Recent (Last 5 Years)", f"{analytics.get('recent_articles', 0):,}"),
            ("Older Articles", f"{analytics.get('older_articles', 0):,}"),
            ("Average Score", f"{analytics.get('avg_score', 0):.2f}"),
            ("Avg Abstract Length", f"{analytics.get('avg_abstract_length', 0):,} chars"),
            ("Year Range", f"{analytics.get('year_range', (0,0))[0]} - {analytics.get('year_range', (0,0))[1]}")
        ]

        for i, (label, value) in enumerate(metrics):
            row = i // 3
            col = (i % 3) * 2

            label_widget = QLabel(f"<b>{label}:</b>")
            value_widget = QLabel(value)
            value_widget.setStyleSheet("font-size: 18px; color: #0078d4; font-weight: bold;")

            self.overview_layout.addWidget(label_widget, row, col)
            self.overview_layout.addWidget(value_widget, row, col + 1)

    def update_timeline(self, analytics):
        """Update publication timeline"""
        # Clear previous
        while self.timeline_layout.count():
            child = self.timeline_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        year_dist = analytics.get('year_distribution', {})
        if not year_dist:
            self.timeline_layout.addWidget(QLabel("No publication data available"))
            return

        # Create text-based bar chart
        max_count = max(year_dist.values()) if year_dist else 1

        for year, count in sorted(year_dist.items(), reverse=True)[:15]:
            row = QHBoxLayout()

            year_label = QLabel(f"{year}:")
            year_label.setFixedWidth(60)
            row.addWidget(year_label)

            # Bar visualization
            bar_width = int((count / max_count) * 400)
            bar_label = QLabel("█" * int(bar_width / 8))
            bar_label.setStyleSheet("color: #0078d4;")
            row.addWidget(bar_label)

            count_label = QLabel(f"({count})")
            row.addWidget(count_label)

            row.addStretch()

            self.timeline_layout.addLayout(row)

    def update_authors(self, analytics):
        """Update top authors"""
        # Clear previous
        while self.authors_layout.count():
            child = self.authors_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        top_authors = analytics.get('top_authors', {})
        if not top_authors:
            self.authors_layout.addWidget(QLabel("No author data available"))
            return

        for i, (author, count) in enumerate(list(top_authors.items())[:10], 1):
            label = QLabel(f"{i}. {author} ({count} articles)")
            self.authors_layout.addWidget(label)

    def update_journals(self, analytics):
        """Update top journals"""
        # Clear previous
        while self.journals_layout.count():
            child = self.journals_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        top_journals = analytics.get('top_journals', {})
        if not top_journals:
            self.journals_layout.addWidget(QLabel("No journal data available"))
            return

        for i, (journal, count) in enumerate(list(top_journals.items())[:10], 1):
            label = QLabel(f"{i}. {journal} ({count} articles)")
            label.setWordWrap(True)
            self.journals_layout.addWidget(label)

    def update_keywords(self, analytics):
        """Update keywords"""
        # Clear previous
        while self.keywords_layout.count():
            child = self.keywords_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        top_keywords = analytics.get('top_keywords', {})
        if not top_keywords:
            self.keywords_layout.addWidget(QLabel("No keyword data available"))
            return

        # Create keyword cloud effect with different sizes
        keywords_text = ""
        for keyword, count in list(top_keywords.items())[:20]:
            size = min(20, 10 + count * 2)
            keywords_text += f'<span style="font-size: {size}px; margin: 5px; color: #0078d4;">{keyword} ({count})</span> '

        keywords_label = QLabel(keywords_text)
        keywords_label.setWordWrap(True)
        keywords_label.setTextFormat(Qt.RichText)
        self.keywords_layout.addWidget(keywords_label)

    def update_sources(self, analytics):
        """Update source distribution"""
        # Clear previous
        while self.sources_layout.count():
            child = self.sources_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        sources = analytics.get('source_distribution', {})
        if not sources:
            self.sources_layout.addWidget(QLabel("No source data available"))
            return

        total = sum(sources.values())
        for source, count in sources.items():
            percentage = (count / total * 100) if total > 0 else 0
            label = QLabel(f"{source}: {count} articles ({percentage:.1f}%)")
            self.sources_layout.addWidget(label)

    def show_empty_state(self):
        """Show empty state when no articles"""
        # Clear all sections
        for group in [self.overview_group, self.timeline_group, self.authors_group,
                     self.journals_group, self.keywords_group, self.sources_group]:
            layout = group.layout()
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            empty_label = QLabel("No articles in database. Add articles to see analytics.")
            empty_label.setStyleSheet("font-style: italic; color: #888;")
            layout.addWidget(empty_label)

    def show_error(self, error):
        """Show error message"""
        self.overview_layout.addWidget(QLabel(f"Error: {error}"))

    def export_analytics(self):
        """Export analytics to JSON"""
        if not self.current_analytics:
            return

        from PySide6.QtWidgets import QFileDialog
        from datetime import datetime

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Analytics",
            f"analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "JSON Files (*.json)"
        )

        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(self.current_analytics, f, indent=2)

                from PySide6.QtWidgets import QMessageBox
                QMessageBox.information(
                    self,
                    "Export Successful",
                    f"Analytics exported to:\n{file_path}"
                )
            except Exception as e:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.critical(
                    self,
                    "Export Error",
                    f"Error exporting analytics:\n\n{str(e)}"
                )
