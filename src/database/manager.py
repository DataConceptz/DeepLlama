"""
Database manager for SQLite operations
"""

import sqlite3
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path
from .models import Article, CREATE_ARTICLES_TABLE, CREATE_INDICES, CREATE_SETTINGS_TABLE, CREATE_CHAT_HISTORY_TABLE


class DatabaseManager:
    """Manages all database operations"""

    def __init__(self, db_path: str = "data/literature.db"):
        """Initialize database connection"""
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Connect to database"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """Create database tables if they don't exist"""
        self.cursor.execute(CREATE_ARTICLES_TABLE)
        for index_sql in CREATE_INDICES:
            self.cursor.execute(index_sql)
        self.cursor.execute(CREATE_SETTINGS_TABLE)
        self.cursor.execute(CREATE_CHAT_HISTORY_TABLE)
        self.conn.commit()

    def add_article(self, article: Article) -> int:
        """Add a new article to the database"""
        sql = """
        INSERT INTO articles (title, authors, year, journal, doi, keywords, abstract,
                            summary, source, score, pdf_path, url, notes, full_text)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(sql, (
            article.title, article.authors, article.year, article.journal,
            article.doi, article.keywords, article.abstract, article.summary,
            article.source, article.score, article.pdf_path, article.url,
            article.notes, article.full_text
        ))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_article(self, article_id: int) -> Optional[Article]:
        """Get article by ID"""
        sql = "SELECT * FROM articles WHERE id = ?"
        self.cursor.execute(sql, (article_id,))
        row = self.cursor.fetchone()
        if row:
            return self._row_to_article(row)
        return None

    def get_all_articles(self, order_by: str = "date_added DESC") -> List[Article]:
        """Get all articles"""
        sql = f"SELECT * FROM articles ORDER BY {order_by}"
        self.cursor.execute(sql)
        return [self._row_to_article(row) for row in self.cursor.fetchall()]

    def search_articles(self, query: str, fields: List[str] = None) -> List[Article]:
        """Search articles by query"""
        if fields is None:
            fields = ["title", "authors", "abstract", "keywords"]

        conditions = " OR ".join([f"{field} LIKE ?" for field in fields])
        sql = f"SELECT * FROM articles WHERE {conditions} ORDER BY date_added DESC"
        params = [f"%{query}%" for _ in fields]

        self.cursor.execute(sql, params)
        return [self._row_to_article(row) for row in self.cursor.fetchall()]

    def update_article(self, article: Article):
        """Update an existing article"""
        sql = """
        UPDATE articles SET title=?, authors=?, year=?, journal=?, doi=?,
                          keywords=?, abstract=?, summary=?, source=?, score=?,
                          pdf_path=?, url=?, notes=?, full_text=?
        WHERE id=?
        """
        self.cursor.execute(sql, (
            article.title, article.authors, article.year, article.journal,
            article.doi, article.keywords, article.abstract, article.summary,
            article.source, article.score, article.pdf_path, article.url,
            article.notes, article.full_text, article.id
        ))
        self.conn.commit()

    def delete_article(self, article_id: int):
        """Delete an article"""
        self.cursor.execute("DELETE FROM articles WHERE id=?", (article_id,))
        self.conn.commit()

    def clear_all_articles(self):
        """Clear all articles from database"""
        self.cursor.execute("DELETE FROM articles")
        self.conn.commit()

    def get_articles_by_ids(self, article_ids: List[int]) -> List[Article]:
        """Get multiple articles by IDs"""
        if not article_ids:
            return []
        placeholders = ','.join('?' * len(article_ids))
        sql = f"SELECT * FROM articles WHERE id IN ({placeholders})"
        self.cursor.execute(sql, article_ids)
        return [self._row_to_article(row) for row in self.cursor.fetchall()]

    def _row_to_article(self, row: sqlite3.Row) -> Article:
        """Convert database row to Article object"""
        return Article(
            id=row['id'],
            title=row['title'],
            authors=row['authors'] or "",
            year=row['year'] or 0,
            journal=row['journal'] or "",
            doi=row['doi'] or "",
            keywords=row['keywords'] or "",
            abstract=row['abstract'] or "",
            summary=row['summary'] or "",
            source=row['source'] or "",
            score=row['score'] or 0.0,
            pdf_path=row['pdf_path'] or "",
            url=row['url'] or "",
            date_added=datetime.fromisoformat(row['date_added']) if row['date_added'] else None,
            notes=row['notes'] or "",
            full_text=row['full_text'] or ""
        )

    # Settings methods
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        self.cursor.execute("SELECT value FROM settings WHERE key=?", (key,))
        row = self.cursor.fetchone()
        return row['value'] if row else default

    def set_setting(self, key: str, value: Any):
        """Set a setting value"""
        self.cursor.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
            (key, str(value))
        )
        self.conn.commit()

    # Chat history methods
    def add_chat_message(self, role: str, message: str, model: str = "", article_ids: List[int] = None):
        """Add a chat message to history"""
        article_ids_str = ",".join(map(str, article_ids)) if article_ids else ""
        sql = """
        INSERT INTO chat_history (role, message, model, article_ids)
        VALUES (?, ?, ?, ?)
        """
        self.cursor.execute(sql, (role, message, model, article_ids_str))
        self.conn.commit()

    def get_chat_history(self, limit: int = 50) -> List[Dict]:
        """Get recent chat history"""
        sql = "SELECT * FROM chat_history ORDER BY timestamp DESC LIMIT ?"
        self.cursor.execute(sql, (limit,))
        rows = self.cursor.fetchall()
        return [{
            'id': row['id'],
            'timestamp': row['timestamp'],
            'role': row['role'],
            'message': row['message'],
            'model': row['model'],
            'article_ids': [int(x) for x in row['article_ids'].split(',')] if row['article_ids'] else []
        } for row in rows]

    def clear_chat_history(self):
        """Clear all chat history"""
        self.cursor.execute("DELETE FROM chat_history")
        self.conn.commit()

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
