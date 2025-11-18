"""
Citation formatting service
Supports multiple citation styles (APA, MLA, Chicago, etc.)
"""

from typing import Dict, List
from datetime import datetime


class CitationService:
    """Service for formatting citations in various styles"""

    def __init__(self, style: str = "APA"):
        """Initialize citation service"""
        self.style = style

    def format_citation(self, article: Dict, style: str = None) -> str:
        """Format a single citation"""
        style = style or self.style

        if style.upper() == "APA":
            return self._format_apa(article)
        elif style.upper() == "MLA":
            return self._format_mla(article)
        elif style.upper() == "CHICAGO":
            return self._format_chicago(article)
        elif style.upper() == "IEEE":
            return self._format_ieee(article)
        else:
            return self._format_apa(article)  # Default to APA

    def format_bibliography(self, articles: List[Dict], style: str = None) -> str:
        """Format a complete bibliography"""
        style = style or self.style
        citations = []

        for article in articles:
            citation = self.format_citation(article, style)
            citations.append(citation)

        # Sort alphabetically by first author's last name
        citations.sort()

        if style.upper() == "APA":
            header = "# References\n\n"
        elif style.upper() == "MLA":
            header = "# Works Cited\n\n"
        else:
            header = "# Bibliography\n\n"

        return header + '\n\n'.join(citations)

    def _format_apa(self, article: Dict) -> str:
        """Format citation in APA style"""
        authors = article.get('authors', 'Unknown')
        year = article.get('year', 'n.d.')
        title = article.get('title', 'Untitled')
        journal = article.get('journal', '')
        doi = article.get('doi', '')

        # Format authors (APA style)
        author_list = [a.strip() for a in authors.split(',') if a.strip()]
        if len(author_list) == 1:
            formatted_authors = author_list[0]
        elif len(author_list) == 2:
            formatted_authors = f"{author_list[0]}, & {author_list[1]}"
        elif len(author_list) > 2:
            formatted_authors = ', '.join(author_list[:-1]) + f", & {author_list[-1]}"
        else:
            formatted_authors = "Unknown"

        # Build citation
        citation = f"{formatted_authors} ({year}). *{title}*."

        if journal:
            citation += f" *{journal}*."

        if doi:
            citation += f" https://doi.org/{doi}"

        return citation

    def _format_mla(self, article: Dict) -> str:
        """Format citation in MLA style"""
        authors = article.get('authors', 'Unknown')
        year = article.get('year', 'n.d.')
        title = article.get('title', 'Untitled')
        journal = article.get('journal', '')
        doi = article.get('doi', '')

        # Format authors (MLA style - Last, First)
        author_list = [a.strip() for a in authors.split(',') if a.strip()]
        if author_list:
            formatted_authors = author_list[0]
            if len(author_list) > 1:
                formatted_authors += ", et al."
        else:
            formatted_authors = "Unknown"

        # Build citation
        citation = f'{formatted_authors}. "{title}."'

        if journal:
            citation += f" *{journal}*,"

        citation += f" {year}."

        if doi:
            citation += f" https://doi.org/{doi}."

        return citation

    def _format_chicago(self, article: Dict) -> str:
        """Format citation in Chicago style"""
        authors = article.get('authors', 'Unknown')
        year = article.get('year', 'n.d.')
        title = article.get('title', 'Untitled')
        journal = article.get('journal', '')
        doi = article.get('doi', '')

        # Format authors
        author_list = [a.strip() for a in authors.split(',') if a.strip()]
        if author_list:
            formatted_authors = author_list[0]
            if len(author_list) > 1:
                formatted_authors += ", et al."
        else:
            formatted_authors = "Unknown"

        # Build citation
        citation = f'{formatted_authors}. "{title}."'

        if journal:
            citation += f" *{journal}*"

        citation += f" ({year})."

        if doi:
            citation += f" https://doi.org/{doi}."

        return citation

    def _format_ieee(self, article: Dict) -> str:
        """Format citation in IEEE style"""
        authors = article.get('authors', 'Unknown')
        year = article.get('year', 'n.d.')
        title = article.get('title', 'Untitled')
        journal = article.get('journal', '')
        doi = article.get('doi', '')

        # Format authors (IEEE uses initials)
        author_list = [a.strip() for a in authors.split(',') if a.strip()]
        if author_list:
            if len(author_list) <= 3:
                formatted_authors = ', '.join(author_list)
            else:
                formatted_authors = author_list[0] + ", et al."
        else:
            formatted_authors = "Unknown"

        # Build citation
        citation = f'{formatted_authors}, "{title},"'

        if journal:
            citation += f" *{journal}*,"

        citation += f" {year}."

        if doi:
            citation += f" DOI: {doi}."

        return citation

    def create_inline_citation(self, article: Dict, citation_number: int = None, style: str = None) -> str:
        """Create an inline citation"""
        style = style or self.style

        if citation_number is not None:
            # Numbered citation [1], [2], etc.
            return f"[{citation_number}]"
        else:
            # Author-year citation
            authors = article.get('authors', 'Unknown')
            year = article.get('year', 'n.d.')

            # Get first author's last name
            author_list = [a.strip() for a in authors.split(',') if a.strip()]
            if author_list:
                first_author = author_list[0].split()[-1]  # Get last name
                if len(author_list) > 2:
                    return f"({first_author} et al., {year})"
                elif len(author_list) == 2:
                    second_author = author_list[1].split()[-1]
                    return f"({first_author} & {second_author}, {year})"
                else:
                    return f"({first_author}, {year})"
            else:
                return f"(Unknown, {year})"

    def get_available_styles(self) -> List[str]:
        """Get list of available citation styles"""
        return ["APA", "MLA", "Chicago", "IEEE"]
