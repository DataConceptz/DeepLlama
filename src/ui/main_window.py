"""
Main application window
"""

from PySide6.QtWidgets import (QMainWindow, QTabWidget, QVBoxLayout, QWidget,
                               QStatusBar, QMessageBox, QMenuBar, QMenu)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction

from .themes import ThemeManager, Theme
from .search_tab import SearchTab
from .results_tab import ResultsTab
from .report_tab import ReportTab
from .chat_tab import ChatTab
from .settings_tab import SettingsTab

from ..database import DatabaseManager
from ..services import OllamaService, SearchService, ExportService, CitationService
from ..utils import Config


class MainWindow(QMainWindow):
    """Main application window"""

    # Signals
    theme_changed = Signal(Theme)
    articles_loaded = Signal(list)

    def __init__(self):
        super().__init__()

        # Initialize configuration
        self.config = Config()

        # Initialize services
        self.db = DatabaseManager()
        self.ollama_service = OllamaService(self.config.get('ollama_url'))
        self.search_service = SearchService()
        self.export_service = ExportService()
        self.citation_service = CitationService(self.config.get('citation_style'))

        # Current data
        self.current_articles = []
        self.selected_article_ids = []

        # Setup UI
        self.setup_ui()
        self.setup_menu()

        # Apply theme
        theme_name = self.config.get('theme', 'dark')
        self.apply_theme(Theme(theme_name))

        # Load existing articles from database
        self.load_articles_from_db()

    def setup_ui(self):
        """Setup main user interface"""
        self.setWindowTitle("DeepLlama - AI Literature Review Research Tool")

        # Set window size from config
        width = self.config.get('window_width', 1400)
        height = self.config.get('window_height', 900)
        self.resize(width, height)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Create tabs
        self.search_tab = SearchTab(self)
        self.results_tab = ResultsTab(self)
        self.report_tab = ReportTab(self)
        self.chat_tab = ChatTab(self)
        self.settings_tab = SettingsTab(self)

        # Add tabs
        self.tabs.addTab(self.search_tab, "🔍 Search")
        self.tabs.addTab(self.results_tab, "📊 Literature Database")
        self.tabs.addTab(self.report_tab, "📄 Report Generation")
        self.tabs.addTab(self.chat_tab, "💬 AI Chat")
        self.tabs.addTab(self.settings_tab, "⚙️ Settings")

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Connect signals
        self.search_tab.search_completed.connect(self.on_search_completed)
        self.results_tab.selection_changed.connect(self.on_article_selection_changed)
        self.settings_tab.theme_changed.connect(self.apply_theme)
        self.settings_tab.settings_changed.connect(self.on_settings_changed)

    def setup_menu(self):
        """Setup menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        import_action = QAction("&Import CSV", self)
        import_action.triggered.connect(self.results_tab.import_csv)
        file_menu.addAction(import_action)

        export_action = QAction("&Export CSV", self)
        export_action.triggered.connect(self.results_tab.export_csv)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu("&View")

        dark_theme_action = QAction("Dark Theme", self)
        dark_theme_action.triggered.connect(lambda: self.apply_theme(Theme.DARK))
        view_menu.addAction(dark_theme_action)

        light_theme_action = QAction("Light Theme", self)
        light_theme_action.triggered.connect(lambda: self.apply_theme(Theme.LIGHT))
        view_menu.addAction(light_theme_action)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def apply_theme(self, theme: Theme):
        """Apply theme to application"""
        stylesheet = ThemeManager.get_stylesheet(theme)
        self.setStyleSheet(stylesheet)
        self.config.set('theme', theme.value)
        self.theme_changed.emit(theme)

    def on_search_completed(self, articles: list):
        """Handle search completion"""
        self.current_articles = articles
        self.status_bar.showMessage(f"Found {len(articles)} articles")

        # Save articles to database
        for article in articles:
            try:
                from ..database.models import Article
                article_obj = Article(
                    title=article.get('title', ''),
                    authors=article.get('authors', ''),
                    year=article.get('year', 0),
                    journal=article.get('journal', ''),
                    doi=article.get('doi', ''),
                    keywords=article.get('keywords', ''),
                    abstract=article.get('abstract', ''),
                    summary=article.get('summary', ''),
                    source=article.get('source', ''),
                    score=article.get('score', 0.0),
                    url=article.get('url', ''),
                    full_text=article.get('full_text', '')
                )
                self.db.add_article(article_obj)
            except Exception as e:
                print(f"Error saving article: {e}")

        # Reload articles in results tab
        self.load_articles_from_db()

        # Switch to results tab
        self.tabs.setCurrentIndex(1)

    def load_articles_from_db(self):
        """Load all articles from database"""
        try:
            articles = self.db.get_all_articles()
            article_dicts = [article.to_dict() for article in articles]
            self.current_articles = article_dicts
            self.results_tab.load_articles(article_dicts)
            self.articles_loaded.emit(article_dicts)
        except Exception as e:
            print(f"Error loading articles: {e}")

    def on_article_selection_changed(self, selected_ids: list):
        """Handle article selection change"""
        self.selected_article_ids = selected_ids
        self.status_bar.showMessage(f"{len(selected_ids)} article(s) selected")

    def on_settings_changed(self):
        """Handle settings changes"""
        # Reload configuration
        self.config.load()

        # Update Ollama service URL
        ollama_url = self.config.get('ollama_url')
        self.ollama_service.base_url = ollama_url

        # Update citation style
        citation_style = self.config.get('citation_style')
        self.citation_service.style = citation_style

    def get_selected_articles(self) -> list:
        """Get currently selected articles"""
        if not self.selected_article_ids:
            return []

        return [article for article in self.current_articles
                if article.get('id') in self.selected_article_ids]

    def clear_all_data(self):
        """Clear all articles and reset application"""
        reply = QMessageBox.question(
            self,
            "Clear All Data",
            "Are you sure you want to clear all articles from the database?\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.db.clear_all_articles()
            self.current_articles = []
            self.selected_article_ids = []
            self.results_tab.clear_table()
            self.report_tab.clear_report()
            self.chat_tab.clear_chat()
            self.status_bar.showMessage("All data cleared")

    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About DeepLlama",
            "<h2>DeepLlama</h2>"
            "<p>AI Literature Review Research Tool</p>"
            "<p>Version 1.0.0</p>"
            "<p>A comprehensive desktop application for conducting deep literature reviews "
            "using local AI models.</p>"
            "<p><b>Features:</b></p>"
            "<ul>"
            "<li>Multi-source academic search</li>"
            "<li>AI-powered report generation</li>"
            "<li>Smart article management</li>"
            "<li>Export to Markdown/DOCX</li>"
            "<li>Context-aware AI chat</li>"
            "</ul>"
        )

    def closeEvent(self, event):
        """Handle window close event"""
        # Save window size
        self.config.set('window_width', self.width())
        self.config.set('window_height', self.height())

        # Close database connection
        self.db.close()

        event.accept()
