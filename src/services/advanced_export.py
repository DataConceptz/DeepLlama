"""
Advanced Export Service - BibTeX, RIS, EndNote, JSON
"""

from typing import List, Dict
from datetime import datetime


class AdvancedExportService:
    """Service for exporting to various academic formats"""

    @staticmethod
    def export_to_bibtex(articles: List[Dict], filepath: str) -> bool:
        """Export articles to BibTeX format"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                for article in articles:
                    bibtex_entry = AdvancedExportService._article_to_bibtex(article)
                    f.write(bibtex_entry)
                    f.write("\n\n")
            return True
        except Exception as e:
            print(f"Error exporting to BibTeX: {e}")
            return False

    @staticmethod
    def _article_to_bibtex(article: Dict) -> str:
        """Convert article to BibTeX format"""
        # Generate citation key
        first_author = article.get('authors', 'Unknown').split(',')[0].strip().replace(' ', '')
        year = article.get('year', 'YEAR')
        title_words = article.get('title', 'Title').split()[:2]
        cite_key = f"{first_author}{year}{''.join(title_words)}"

        # Clean cite key
        cite_key = ''.join(c for c in cite_key if c.isalnum())

        # Determine entry type
        journal = article.get('journal', '')
        if 'arxiv' in journal.lower() or 'preprint' in journal.lower():
            entry_type = 'article'
        else:
            entry_type = 'article'

        # Build BibTeX entry
        bibtex = f"@{entry_type}{{{cite_key},\n"

        # Add fields
        if article.get('title'):
            bibtex += f"  title     = {{{article['title']}}},\n"

        if article.get('authors'):
            authors = article['authors'].replace(',', ' and')
            bibtex += f"  author    = {{{authors}}},\n"

        if article.get('year'):
            bibtex += f"  year      = {{{article['year']}}},\n"

        if article.get('journal'):
            bibtex += f"  journal   = {{{article['journal']}}},\n"

        if article.get('doi'):
            bibtex += f"  doi       = {{{article['doi']}}},\n"

        if article.get('url'):
            bibtex += f"  url       = {{{article['url']}}},\n"

        if article.get('abstract'):
            # Escape special characters
            abstract = article['abstract'].replace('{', '\\{').replace('}', '\\}')
            bibtex += f"  abstract  = {{{abstract}}},\n"

        if article.get('keywords'):
            bibtex += f"  keywords  = {{{article['keywords']}}},\n"

        # Remove trailing comma
        bibtex = bibtex.rstrip(',\n') + "\n"
        bibtex += "}"

        return bibtex

    @staticmethod
    def export_to_ris(articles: List[Dict], filepath: str) -> bool:
        """Export articles to RIS format (Reference Manager)"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                for article in articles:
                    ris_entry = AdvancedExportService._article_to_ris(article)
                    f.write(ris_entry)
                    f.write("\n")
            return True
        except Exception as e:
            print(f"Error exporting to RIS: {e}")
            return False

    @staticmethod
    def _article_to_ris(article: Dict) -> str:
        """Convert article to RIS format"""
        ris = "TY  - JOUR\n"  # Type: Journal Article

        # Title
        if article.get('title'):
            ris += f"TI  - {article['title']}\n"

        # Authors
        if article.get('authors'):
            authors = [a.strip() for a in article['authors'].split(',')]
            for author in authors:
                ris += f"AU  - {author}\n"

        # Year
        if article.get('year'):
            ris += f"PY  - {article['year']}\n"

        # Journal
        if article.get('journal'):
            ris += f"JO  - {article['journal']}\n"

        # DOI
        if article.get('doi'):
            ris += f"DO  - {article['doi']}\n"

        # URL
        if article.get('url'):
            ris += f"UR  - {article['url']}\n"

        # Abstract
        if article.get('abstract'):
            ris += f"AB  - {article['abstract']}\n"

        # Keywords
        if article.get('keywords'):
            keywords = [k.strip() for k in article['keywords'].split(',')]
            for keyword in keywords:
                ris += f"KW  - {keyword}\n"

        # Database
        if article.get('source'):
            ris += f"DB  - {article['source']}\n"

        # Date added
        if article.get('date_added'):
            ris += f"DA  - {article['date_added']}\n"

        ris += "ER  -\n"  # End of record

        return ris

    @staticmethod
    def export_to_endnote(articles: List[Dict], filepath: str) -> bool:
        """Export articles to EndNote XML format"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                f.write('<xml>\n')
                f.write('<records>\n')

                for article in articles:
                    endnote_entry = AdvancedExportService._article_to_endnote_xml(article)
                    f.write(endnote_entry)

                f.write('</records>\n')
                f.write('</xml>\n')
            return True
        except Exception as e:
            print(f"Error exporting to EndNote: {e}")
            return False

    @staticmethod
    def _article_to_endnote_xml(article: Dict) -> str:
        """Convert article to EndNote XML format"""
        xml = "  <record>\n"
        xml += "    <database name='DeepLlama' path='literature.db'>DeepLlama</database>\n"
        xml += "    <source-app name='DeepLlama'>DeepLlama</source-app>\n"
        xml += "    <ref-type name='Journal Article'>17</ref-type>\n"

        # Title
        if article.get('title'):
            xml += f"    <titles>\n"
            xml += f"      <title>{AdvancedExportService._escape_xml(article['title'])}</title>\n"
            xml += f"    </titles>\n"

        # Authors
        if article.get('authors'):
            xml += "    <contributors>\n"
            xml += "      <authors>\n"
            authors = [a.strip() for a in article['authors'].split(',')]
            for author in authors:
                xml += f"        <author>{AdvancedExportService._escape_xml(author)}</author>\n"
            xml += "      </authors>\n"
            xml += "    </contributors>\n"

        # Year
        if article.get('year'):
            xml += "    <dates>\n"
            xml += f"      <year>{article['year']}</year>\n"
            xml += "    </dates>\n"

        # Journal
        if article.get('journal'):
            xml += "    <periodical>\n"
            xml += f"      <full-title>{AdvancedExportService._escape_xml(article['journal'])}</full-title>\n"
            xml += "    </periodical>\n"

        # DOI
        if article.get('doi'):
            xml += f"    <electronic-resource-num>{article['doi']}</electronic-resource-num>\n"

        # URL
        if article.get('url'):
            xml += "    <urls>\n"
            xml += f"      <related-urls><url>{article['url']}</url></related-urls>\n"
            xml += "    </urls>\n"

        # Abstract
        if article.get('abstract'):
            xml += f"    <abstract>{AdvancedExportService._escape_xml(article['abstract'])}</abstract>\n"

        # Keywords
        if article.get('keywords'):
            xml += "    <keywords>\n"
            keywords = [k.strip() for k in article['keywords'].split(',')]
            for keyword in keywords:
                xml += f"      <keyword>{AdvancedExportService._escape_xml(keyword)}</keyword>\n"
            xml += "    </keywords>\n"

        xml += "  </record>\n"

        return xml

    @staticmethod
    def _escape_xml(text: str) -> str:
        """Escape XML special characters"""
        return (text.replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;')
                   .replace('"', '&quot;')
                   .replace("'", '&apos;'))

    @staticmethod
    def export_to_json(articles: List[Dict], filepath: str, pretty: bool = True) -> bool:
        """Export articles to JSON format"""
        try:
            import json

            # Convert datetime objects to strings
            articles_copy = []
            for article in articles:
                article_copy = article.copy()
                if 'date_added' in article_copy and article_copy['date_added']:
                    if isinstance(article_copy['date_added'], datetime):
                        article_copy['date_added'] = article_copy['date_added'].isoformat()
                articles_copy.append(article_copy)

            with open(filepath, 'w', encoding='utf-8') as f:
                if pretty:
                    json.dump(articles_copy, f, indent=2, ensure_ascii=False)
                else:
                    json.dump(articles_copy, f, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return False

    @staticmethod
    def export_to_plain_text(articles: List[Dict], filepath: str, format_style: str = "APA") -> bool:
        """Export articles as formatted plain text references"""
        try:
            from ..services.citation_service import CitationService

            citation_service = CitationService(style=format_style)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# Literature References ({format_style} Style)\n")
                f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Total Articles: {len(articles)}\n\n")

                for i, article in enumerate(articles, 1):
                    citation = citation_service.format_citation(article)
                    f.write(f"{i}. {citation}\n\n")

            return True
        except Exception as e:
            print(f"Error exporting to plain text: {e}")
            return False

    @staticmethod
    def get_supported_formats() -> List[Dict[str, str]]:
        """Get list of supported export formats"""
        return [
            {'name': 'BibTeX', 'extension': '.bib', 'description': 'LaTeX bibliography format'},
            {'name': 'RIS', 'extension': '.ris', 'description': 'Reference Manager format'},
            {'name': 'EndNote XML', 'extension': '.xml', 'description': 'EndNote library format'},
            {'name': 'JSON', 'extension': '.json', 'description': 'JSON data format'},
            {'name': 'Plain Text', 'extension': '.txt', 'description': 'Formatted references'},
            {'name': 'CSV', 'extension': '.csv', 'description': 'Spreadsheet format'},
            {'name': 'Markdown', 'extension': '.md', 'description': 'Markdown format'},
            {'name': 'DOCX', 'extension': '.docx', 'description': 'Microsoft Word format'}
        ]
