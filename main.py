#!/usr/bin/env python3
"""
DeepLlama - AI Literature Review Research Tool
Main entry point
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from src.ui import MainWindow


def main():
    """Main application entry point"""

    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    # Create application
    app = QApplication(sys.argv)

    # Set application metadata
    app.setApplicationName("DeepLlama")
    app.setApplicationDisplayName("DeepLlama - AI Literature Review Tool")
    app.setOrganizationName("DeepLlama")
    app.setOrganizationDomain("deepllama.app")

    # Create and show main window
    window = MainWindow()
    window.show()

    # Run event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
