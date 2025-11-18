"""
Results tab for displaying and managing articles
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView,
                               QCheckBox, QLabel, QFileDialog, QMessageBox,
                               QTextEdit, QDialog, QDialogButtonBox, QAbstractItemView)
from PySide6.QtCore import Qt, Signal
from datetime import datetime


class ArticleDetailDialog(QDialog):
    """Dialog for viewing full article details"""

    def __init__(self, article: dict, parent=None):
        super().__init__(parent)
        self.article = article
        self.setup_ui()

    def setup_ui(self):
        """Setup dialog UI"""
        self.setWindowTitle("Article Details")
        self.resize(800, 600)

        layout = QVBoxLayout(self)

        # Article details
        details_text = QTextEdit()
        details_text.setReadOnly(True)

        content = f"""<h2>{self.article.get('title', 'Untitled')}</h2>

<p><b>Authors:</b> {self.article.get('authors', 'Unknown')}</p>
<p><b>Year:</b> {self.article.get('year', 'N/A')}</p>
<p><b>Journal:</b> {self.article.get('journal', 'Unknown')}</p>
<p><b>DOI:</b> {self.article.get('doi', 'N/A')}</p>
<p><b>Source:</b> {self.article.get('source', 'Unknown')}</p>
<p><b>Keywords:</b> {self.article.get('keywords', 'N/A')}</p>
<p><b>URL:</b> <a href="{self.article.get('url', '')}">{self.article.get('url', 'N/A')}</a></p>

<h3>Abstract</h3>
<p>{self.article.get('abstract', 'No abstract available')}</p>

<h3>Summary</h3>
<p>{self.article.get('summary', 'No summary generated yet')}</p>

<h3>Notes</h3>
<p>{self.article.get('notes', 'No notes')}</p>
"""

        details_text.setHtml(content)
        layout.addWidget(details_text)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)


class ResultsTab(QWidget):
    """Results tab widget"""

    selection_changed = Signal(list)

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.articles = []
        self.setup_ui()

    def setup_ui(self):
        """Setup user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title and controls
        header_layout = QHBoxLayout()

        title = QLabel("📊 Literature Database")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Article count
        self.count_label = QLabel("0 articles")
        self.count_label.setStyleSheet("font-size: 14px;")
        header_layout.addWidget(self.count_label)

        layout.addLayout(header_layout)

        # Action buttons
        button_layout = QHBoxLayout()

        self.clear_button = QPushButton("🗑️ Clear All")
        self.clear_button.clicked.connect(self.confirm_clear_all)
        button_layout.addWidget(self.clear_button)

        self.import_button = QPushButton("📥 Import CSV")
        self.import_button.clicked.connect(self.import_csv)
        button_layout.addWidget(self.import_button)

        self.export_button = QPushButton("📤 Export CSV")
        self.export_button.clicked.connect(self.export_csv)
        button_layout.addWidget(self.export_button)

        button_layout.addStretch()

        self.select_all_button = QPushButton("☑️ Select All")
        self.select_all_button.clicked.connect(self.select_all)
        button_layout.addWidget(self.select_all_button)

        self.deselect_all_button = QPushButton("☐ Deselect All")
        self.deselect_all_button.clicked.connect(self.deselect_all)
        button_layout.addWidget(self.deselect_all_button)

        layout.addLayout(button_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels([
            "✓", "Title", "Authors", "Year", "Journal", "DOI",
            "Keywords", "Abstract", "Source", "Score", "Date Added"
        ])

        # Table settings
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.MultiSelection)
        self.table.setSortingEnabled(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)

        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)  # Checkbox
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Title
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Authors
        header.setSectionResizeMode(7, QHeaderView.Stretch)  # Abstract

        self.table.setColumnWidth(0, 40)

        # Double-click to view details
        self.table.cellDoubleClicked.connect(self.show_article_details)

        layout.addWidget(self.table)

        # Selection info
        self.selection_label = QLabel("0 articles selected")
        layout.addWidget(self.selection_label)

    def load_articles(self, articles: list):
        """Load articles into table"""
        self.articles = articles
        self.table.setRowCount(0)
        self.table.setSortingEnabled(False)

        for article in articles:
            self.add_article_row(article)

        self.table.setSortingEnabled(True)
        self.update_counts()

    def add_article_row(self, article: dict):
        """Add a single article row to table"""
        row = self.table.rowCount()
        self.table.insertRow(row)

        # Checkbox
        checkbox = QCheckBox()
        checkbox.setStyleSheet("margin-left: 10px;")
        checkbox.stateChanged.connect(self.on_selection_changed)
        self.table.setCellWidget(row, 0, checkbox)

        # Store article ID in checkbox
        checkbox.setProperty("article_id", article.get('id'))

        # Title
        title_item = QTableWidgetItem(article.get('title', 'Untitled'))
        title_item.setData(Qt.UserRole, article)  # Store full article data
        self.table.setItem(row, 1, title_item)

        # Authors
        authors = article.get('authors', 'Unknown')
        # Truncate if too long
        if len(authors) > 50:
            authors = authors[:47] + "..."
        self.table.setItem(row, 2, QTableWidgetItem(authors))

        # Year
        year_item = QTableWidgetItem(str(article.get('year', '')))
        year_item.setData(Qt.UserRole, article.get('year', 0))
        self.table.setItem(row, 3, year_item)

        # Journal
        self.table.setItem(row, 4, QTableWidgetItem(article.get('journal', '')))

        # DOI
        self.table.setItem(row, 5, QTableWidgetItem(article.get('doi', '')))

        # Keywords
        keywords = article.get('keywords', '')
        if len(keywords) > 50:
            keywords = keywords[:47] + "..."
        self.table.setItem(row, 6, QTableWidgetItem(keywords))

        # Abstract - FULL TEXT, NO TRUNCATION
        abstract = article.get('abstract', 'No abstract')
        abstract_item = QTableWidgetItem(abstract)
        abstract_item.setToolTip(abstract)  # Show full text on hover
        self.table.setItem(row, 7, abstract_item)

        # Source
        self.table.setItem(row, 8, QTableWidgetItem(article.get('source', '')))

        # Score
        score = article.get('score', 0.0)
        score_item = QTableWidgetItem(f"{score:.2f}")
        score_item.setData(Qt.UserRole, score)
        self.table.setItem(row, 9, score_item)

        # Date Added
        date_added = article.get('date_added', '')
        if isinstance(date_added, datetime):
            date_added = date_added.strftime("%Y-%m-%d %H:%M")
        elif isinstance(date_added, str) and date_added:
            try:
                dt = datetime.fromisoformat(date_added)
                date_added = dt.strftime("%Y-%m-%d %H:%M")
            except:
                pass
        self.table.setItem(row, 10, QTableWidgetItem(str(date_added)))

    def on_selection_changed(self):
        """Handle selection change"""
        selected_ids = []

        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                article_id = checkbox.property("article_id")
                if article_id:
                    selected_ids.append(article_id)

        self.selection_label.setText(f"{len(selected_ids)} article(s) selected")
        self.selection_changed.emit(selected_ids)

    def select_all(self):
        """Select all articles"""
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0)
            if checkbox:
                checkbox.setChecked(True)

    def deselect_all(self):
        """Deselect all articles"""
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0)
            if checkbox:
                checkbox.setChecked(False)

    def show_article_details(self, row: int, column: int):
        """Show full article details in dialog"""
        title_item = self.table.item(row, 1)
        if title_item:
            article = title_item.data(Qt.UserRole)
            if article:
                dialog = ArticleDetailDialog(article, self)
                dialog.exec()

    def confirm_clear_all(self):
        """Confirm and clear all articles"""
        self.main_window.clear_all_data()

    def clear_table(self):
        """Clear the table"""
        self.table.setRowCount(0)
        self.articles = []
        self.update_counts()

    def import_csv(self):
        """Import articles from CSV"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import CSV File",
            "",
            "CSV Files (*.csv)"
        )

        if file_path:
            try:
                articles = self.main_window.export_service.load_articles_csv(file_path)

                if articles:
                    # Save to database
                    from ..database.models import Article
                    for article_dict in articles:
                        article = Article(
                            title=article_dict.get('title', ''),
                            authors=article_dict.get('authors', ''),
                            year=article_dict.get('year', 0),
                            journal=article_dict.get('journal', ''),
                            doi=article_dict.get('doi', ''),
                            keywords=article_dict.get('keywords', ''),
                            abstract=article_dict.get('abstract', ''),
                            source=article_dict.get('source', 'CSV Import'),
                            score=article_dict.get('score', 0.0),
                            url=article_dict.get('url', ''),
                            notes=article_dict.get('notes', '')
                        )
                        self.main_window.db.add_article(article)

                    # Reload table
                    self.main_window.load_articles_from_db()

                    QMessageBox.information(
                        self,
                        "Import Successful",
                        f"Successfully imported {len(articles)} articles."
                    )
                else:
                    QMessageBox.warning(
                        self,
                        "Import Failed",
                        "No articles found in the CSV file."
                    )

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Import Error",
                    f"Error importing CSV: {str(e)}"
                )

    def export_csv(self):
        """Export articles to CSV"""
        if not self.articles:
            QMessageBox.warning(
                self,
                "No Data",
                "No articles to export."
            )
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export CSV File",
            "literature_export.csv",
            "CSV Files (*.csv)"
        )

        if file_path:
            try:
                success = self.main_window.export_service.save_articles_csv(
                    self.articles,
                    file_path
                )

                if success:
                    QMessageBox.information(
                        self,
                        "Export Successful",
                        f"Successfully exported {len(self.articles)} articles to {file_path}"
                    )
                else:
                    QMessageBox.warning(
                        self,
                        "Export Failed",
                        "Failed to export articles."
                    )

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Export Error",
                    f"Error exporting CSV: {str(e)}"
                )

    def update_counts(self):
        """Update article count labels"""
        count = len(self.articles)
        self.count_label.setText(f"{count} article(s)")
