"""Database module for literature management"""
from .manager import DatabaseManager
from .models import Article

__all__ = ['DatabaseManager', 'Article']
