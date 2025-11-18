"""
Helper utility functions
"""

import re
from datetime import datetime
from typing import Optional


def format_date(date_obj: Optional[datetime], format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime object to string"""
    if date_obj is None:
        return ""
    if isinstance(date_obj, str):
        return date_obj
    return date_obj.strftime(format_str)


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to maximum length"""
    if not text or len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing invalid characters"""
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    sanitized = sanitized.replace(' ', '_')
    # Limit length
    if len(sanitized) > 200:
        sanitized = sanitized[:200]
    return sanitized


def extract_author_last_name(author_string: str) -> str:
    """Extract first author's last name from author string"""
    if not author_string:
        return "Unknown"

    authors = author_string.split(',')
    if not authors:
        return "Unknown"

    first_author = authors[0].strip()
    parts = first_author.split()

    if not parts:
        return "Unknown"

    # Assume last part is the last name
    return parts[-1]


def format_number(num: float, decimals: int = 2) -> str:
    """Format number with specified decimal places"""
    return f"{num:.{decimals}f}"


def clean_abstract(abstract: str) -> str:
    """Clean abstract text by removing extra whitespace and newlines"""
    if not abstract:
        return ""

    # Replace multiple whitespaces with single space
    cleaned = re.sub(r'\s+', ' ', abstract)
    # Strip leading/trailing whitespace
    cleaned = cleaned.strip()

    return cleaned


def highlight_text(text: str, query: str) -> str:
    """Highlight search query in text (for UI)"""
    if not query:
        return text

    # Case-insensitive highlighting
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    return pattern.sub(lambda m: f"**{m.group(0)}**", text)
