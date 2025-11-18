"""
AI Chat tab for interacting with articles
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QTextEdit, QLineEdit, QComboBox,
                               QCheckBox, QGroupBox, QScrollArea)
from PySide6.QtCore import Qt, Signal, QThread, Slot
from datetime import datetime


class ChatWorker(QThread):
    """Worker thread for chat"""

    finished = Signal(str)
    error = Signal(str)
    progress = Signal(str)

    def __init__(self, ollama_service, model, messages, temperature):
        super().__init__()
        self.ollama_service = ollama_service
        self.model = model
        self.messages = messages
        self.temperature = temperature

    def run(self):
        """Execute chat"""
        try:
            def callback(chunk):
                self.progress.emit(chunk)

            response = self.ollama_service.chat(
                model=self.model,
                messages=self.messages,
                temperature=self.temperature,
                stream=True,
                callback=callback
            )

            self.finished.emit(response)

        except Exception as e:
            self.error.emit(str(e))


class ChatTab(QWidget):
    """Chat tab widget"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.chat_worker = None
        self.chat_history = []
        self.setup_ui()

    def setup_ui(self):
        """Setup user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel("💬 AI Chat Assistant")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        # Description
        desc = QLabel(
            "Chat with AI about your selected articles. Ask questions, compare methodologies, "
            "or get insights about the research."
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Settings
        settings_layout = QHBoxLayout()

        settings_layout.addWidget(QLabel("Model:"))
        self.model_combo = QComboBox()
        settings_layout.addWidget(self.model_combo)

        self.refresh_button = QPushButton("🔄")
        self.refresh_button.setMaximumWidth(40)
        self.refresh_button.clicked.connect(self.refresh_models)
        settings_layout.addWidget(self.refresh_button)

        self.use_articles_checkbox = QCheckBox("Use selected articles as context")
        self.use_articles_checkbox.setChecked(True)
        settings_layout.addWidget(self.use_articles_checkbox)

        settings_layout.addStretch()

        self.clear_history_button = QPushButton("🗑️ Clear History")
        self.clear_history_button.clicked.connect(self.clear_chat)
        settings_layout.addWidget(self.clear_history_button)

        layout.addLayout(settings_layout)

        # Selected articles info
        self.selection_label = QLabel("0 articles in context")
        self.selection_label.setStyleSheet("font-style: italic;")
        layout.addWidget(self.selection_label)

        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setPlaceholderText(
            "Chat conversation will appear here...\n\n"
            "Ask questions like:\n"
            "• What are the main findings across these articles?\n"
            "• Compare the methodologies used\n"
            "• What are the research gaps?\n"
            "• Summarize the key contributions"
        )
        layout.addWidget(self.chat_display)

        # Input area
        input_layout = QHBoxLayout()

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message here...")
        self.message_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.message_input)

        self.send_button = QPushButton("📤 Send")
        self.send_button.setFixedWidth(100)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        layout.addLayout(input_layout)

        # Initial setup
        self.refresh_models()

        # Connect to selection changes
        self.main_window.results_tab.selection_changed.connect(self.on_selection_changed)

    def refresh_models(self):
        """Refresh available models"""
        self.model_combo.clear()

        if not self.main_window.ollama_service.is_available():
            self.model_combo.addItem("❌ Ollama not running")
            self.send_button.setEnabled(False)
            return

        models = self.main_window.ollama_service.get_models()

        if not models:
            self.model_combo.addItem("No models available")
            self.send_button.setEnabled(False)
            return

        for model in models:
            self.model_combo.addItem(model.name)

        self.send_button.setEnabled(True)

        # Set default model
        default_model = self.main_window.config.get('default_model', '')
        if default_model:
            index = self.model_combo.findText(default_model)
            if index >= 0:
                self.model_combo.setCurrentIndex(index)

    def on_selection_changed(self, selected_ids: list):
        """Handle article selection change"""
        count = len(selected_ids)
        self.selection_label.setText(f"{count} article(s) in context")

    def send_message(self):
        """Send chat message"""
        message = self.message_input.text().strip()

        if not message:
            return

        # Get model
        model = self.model_combo.currentText()
        if model.startswith("❌") or model == "No models available":
            self.append_system_message("⚠️ Please select a valid model")
            return

        # Add user message to display
        self.append_user_message(message)

        # Clear input
        self.message_input.clear()

        # Disable send button
        self.send_button.setEnabled(False)

        # Build context from articles if enabled
        context = ""
        if self.use_articles_checkbox.isChecked():
            selected_articles = self.main_window.get_selected_articles()

            if selected_articles:
                context = "Here are the research articles for context:\n\n"
                for i, article in enumerate(selected_articles, 1):
                    context += f"[Article {i}]\n"
                    context += f"Title: {article.get('title', 'Untitled')}\n"
                    context += f"Authors: {article.get('authors', 'Unknown')}\n"
                    context += f"Year: {article.get('year', 'N/A')}\n"
                    context += f"Abstract: {article.get('abstract', 'No abstract')}\n\n"

        # Build messages for chat
        messages = []

        # Add system message with context
        if context:
            messages.append({
                "role": "system",
                "content": "You are a helpful research assistant. Use the provided articles to answer questions accurately. Cite articles when making claims."
            })
            messages.append({
                "role": "user",
                "content": context
            })

        # Add chat history
        for msg in self.chat_history[-10:]:  # Last 10 messages
            messages.append(msg)

        # Add current message
        current_message = {"role": "user", "content": message}
        messages.append(current_message)
        self.chat_history.append(current_message)

        # Start chat worker
        temperature = self.main_window.config.get('temperature', 0.7)

        self.chat_worker = ChatWorker(
            self.main_window.ollama_service,
            model,
            messages,
            temperature
        )
        self.chat_worker.finished.connect(self.on_chat_finished)
        self.chat_worker.error.connect(self.on_chat_error)
        self.chat_worker.progress.connect(self.on_chat_progress)

        # Add assistant message placeholder
        self.append_assistant_message("", in_progress=True)

        self.chat_worker.start()

    @Slot(str)
    def on_chat_progress(self, chunk: str):
        """Handle chat progress"""
        # Update the last message
        cursor = self.chat_display.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(chunk)
        self.chat_display.setTextCursor(cursor)

        # Scroll to bottom
        scrollbar = self.chat_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    @Slot(str)
    def on_chat_finished(self, response: str):
        """Handle chat completion"""
        # Add to history
        self.chat_history.append({
            "role": "assistant",
            "content": response
        })

        # Re-enable send button
        self.send_button.setEnabled(True)

        # Clean up worker
        if self.chat_worker:
            self.chat_worker = None

    @Slot(str)
    def on_chat_error(self, error: str):
        """Handle chat error"""
        self.append_system_message(f"❌ Error: {error}")
        self.send_button.setEnabled(True)

        if self.chat_worker:
            self.chat_worker = None

    def append_user_message(self, message: str):
        """Append user message to chat"""
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_display.append(
            f"<div style='margin: 10px 0;'>"
            f"<b style='color: #0078d4;'>You</b> "
            f"<span style='color: #888; font-size: 10px;'>{timestamp}</span><br>"
            f"{message}"
            f"</div>"
        )

    def append_assistant_message(self, message: str, in_progress: bool = False):
        """Append assistant message to chat"""
        timestamp = datetime.now().strftime("%H:%M")
        prefix = "🤖 " if in_progress else ""

        self.chat_display.append(
            f"<div style='margin: 10px 0;'>"
            f"<b style='color: #28a745;'>{prefix}Assistant</b> "
            f"<span style='color: #888; font-size: 10px;'>{timestamp}</span><br>"
        )

        if message:
            self.chat_display.insertPlainText(message)

    def append_system_message(self, message: str):
        """Append system message to chat"""
        self.chat_display.append(
            f"<div style='margin: 10px 0; color: #888; font-style: italic;'>"
            f"{message}"
            f"</div>"
        )

    def clear_chat(self):
        """Clear chat history"""
        self.chat_display.clear()
        self.chat_history = []
        self.append_system_message("Chat history cleared")
