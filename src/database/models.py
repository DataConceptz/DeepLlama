"""
Database models and schema definitions
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class Article:
    """Article data model"""
    id: Optional[int] = None
    title: str = ""
    authors: str = ""
    year: int = 0
    journal: str = ""
    doi: str = ""
    keywords: str = ""
    abstract: str = ""
    summary: str = ""
    source: str = ""
    score: float = 0.0
    pdf_path: str = ""
    url: str = ""
    date_added: Optional[datetime] = None
    notes: str = ""
    full_text: str = ""

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'authors': self.authors,
            'year': self.year,
            'journal': self.journal,
            'doi': self.doi,
            'keywords': self.keywords,
            'abstract': self.abstract,
            'summary': self.summary,
            'source': self.source,
            'score': self.score,
            'pdf_path': self.pdf_path,
            'url': self.url,
            'date_added': self.date_added.isoformat() if self.date_added else None,
            'notes': self.notes,
            'full_text': self.full_text
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary"""
        if 'date_added' in data and data['date_added']:
            if isinstance(data['date_added'], str):
                data['date_added'] = datetime.fromisoformat(data['date_added'])
        return cls(**data)


# Database schema
CREATE_ARTICLES_TABLE = """
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    authors TEXT,
    year INTEGER,
    journal TEXT,
    doi TEXT,
    keywords TEXT,
    abstract TEXT,
    summary TEXT,
    source TEXT,
    score REAL,
    pdf_path TEXT,
    url TEXT,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    full_text TEXT
)
"""

CREATE_INDICES = [
    "CREATE INDEX IF NOT EXISTS idx_title ON articles(title)",
    "CREATE INDEX IF NOT EXISTS idx_authors ON articles(authors)",
    "CREATE INDEX IF NOT EXISTS idx_year ON articles(year)",
    "CREATE INDEX IF NOT EXISTS idx_doi ON articles(doi)",
    "CREATE INDEX IF NOT EXISTS idx_date_added ON articles(date_added)"
]

CREATE_SETTINGS_TABLE = """
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT
)
"""

CREATE_CHAT_HISTORY_TABLE = """
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role TEXT NOT NULL,
    message TEXT NOT NULL,
    model TEXT,
    article_ids TEXT
)
"""
