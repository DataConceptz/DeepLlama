"""
Batch Operations Service - AI Summarization, Tagging, Duplicate Detection
"""

from typing import List, Dict, Callable, Optional
from datetime import datetime
import difflib


class BatchService:
    """Service for batch operations on articles"""

    def __init__(self, ollama_service, db_manager):
        """Initialize batch service"""
        self.ollama_service = ollama_service
        self.db = db_manager

    def batch_summarize(self,
                       articles: List[Dict],
                       model: str,
                       callback: Optional[Callable[[int, int, str], None]] = None) -> List[Dict]:
        """
        Batch summarize multiple articles

        Args:
            articles: List of articles to summarize
            model: Ollama model to use
            callback: Progress callback (current, total, article_title)

        Returns:
            List of articles with summaries added
        """
        results = []
        total = len(articles)

        for i, article in enumerate(articles, 1):
            if callback:
                callback(i, total, article.get('title', 'Untitled'))

            try:
                # Skip if already has summary
                if article.get('summary') and len(article.get('summary', '')) > 50:
                    results.append(article)
                    continue

                # Generate summary
                summary = self.ollama_service.summarize_article(model, article)

                # Update article
                article['summary'] = summary

                # Save to database if has ID
                if article.get('id'):
                    from ..database.models import Article
                    article_obj = Article(**article)
                    self.db.update_article(article_obj)

                results.append(article)

            except Exception as e:
                print(f"Error summarizing article {article.get('title', 'Unknown')}: {e}")
                results.append(article)

        return results

    def auto_tag_articles(self,
                         articles: List[Dict],
                         model: str,
                         callback: Optional[Callable[[int, int, str], None]] = None) -> List[Dict]:
        """
        Auto-tag articles using AI

        Args:
            articles: List of articles to tag
            model: Ollama model to use
            callback: Progress callback

        Returns:
            List of articles with tags added
        """
        results = []
        total = len(articles)

        for i, article in enumerate(articles, 1):
            if callback:
                callback(i, total, article.get('title', 'Untitled'))

            try:
                # Generate tags
                tags = self._generate_tags(article, model)

                # Merge with existing keywords
                existing_keywords = article.get('keywords', '')
                if existing_keywords:
                    existing_tags = [k.strip() for k in existing_keywords.split(',')]
                    all_tags = list(set(existing_tags + tags))
                else:
                    all_tags = tags

                article['keywords'] = ', '.join(all_tags[:10])  # Limit to 10 tags

                # Save to database
                if article.get('id'):
                    from ..database.models import Article
                    article_obj = Article(**article)
                    self.db.update_article(article_obj)

                results.append(article)

            except Exception as e:
                print(f"Error tagging article: {e}")
                results.append(article)

        return results

    def _generate_tags(self, article: Dict, model: str) -> List[str]:
        """Generate tags for an article using AI"""
        system_prompt = "You are an expert at extracting key topics and themes from research papers. Generate 5-8 concise, relevant tags/keywords."

        user_prompt = f"""Extract key tags/keywords from this article:

Title: {article.get('title', 'Untitled')}
Abstract: {article.get('abstract', 'No abstract')}

Generate 5-8 relevant tags/keywords (single words or short phrases). Return only the tags, comma-separated."""

        response = self.ollama_service.generate(
            model=model,
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=100,
            stream=False
        )

        # Parse tags
        tags = [tag.strip() for tag in response.split(',')]
        return [tag for tag in tags if tag and len(tag) > 2][:8]

    def detect_duplicates(self,
                         articles: List[Dict],
                         threshold: float = 0.85) -> List[List[Dict]]:
        """
        Detect duplicate articles based on title and DOI similarity

        Args:
            articles: List of articles to check
            threshold: Similarity threshold (0.0 to 1.0)

        Returns:
            List of duplicate groups
        """
        duplicates = []
        checked = set()

        for i, article1 in enumerate(articles):
            if i in checked:
                continue

            duplicate_group = [article1]

            for j, article2 in enumerate(articles[i+1:], i+1):
                if j in checked:
                    continue

                # Check DOI match (exact)
                doi1 = article1.get('doi', '').strip().lower()
                doi2 = article2.get('doi', '').strip().lower()

                if doi1 and doi2 and doi1 == doi2:
                    duplicate_group.append(article2)
                    checked.add(j)
                    continue

                # Check title similarity
                title1 = article1.get('title', '').strip().lower()
                title2 = article2.get('title', '').strip().lower()

                if title1 and title2:
                    similarity = difflib.SequenceMatcher(None, title1, title2).ratio()

                    if similarity >= threshold:
                        duplicate_group.append(article2)
                        checked.add(j)

            if len(duplicate_group) > 1:
                duplicates.append(duplicate_group)
                checked.add(i)

        return duplicates

    def find_similar_articles(self,
                             article: Dict,
                             all_articles: List[Dict],
                             limit: int = 5) -> List[Dict]:
        """
        Find articles similar to the given article

        Args:
            article: Reference article
            all_articles: Pool of articles to search
            limit: Maximum number of similar articles to return

        Returns:
            List of similar articles with similarity scores
        """
        similar = []

        reference_text = self._article_to_text(article)

        for candidate in all_articles:
            # Skip the article itself
            if candidate.get('id') == article.get('id'):
                continue

            candidate_text = self._article_to_text(candidate)

            # Calculate similarity
            similarity = difflib.SequenceMatcher(None, reference_text, candidate_text).ratio()

            similar.append({
                'article': candidate,
                'similarity': similarity
            })

        # Sort by similarity
        similar.sort(key=lambda x: x['similarity'], reverse=True)

        return [s['article'] for s in similar[:limit]]

    def _article_to_text(self, article: Dict) -> str:
        """Convert article to text for similarity comparison"""
        parts = [
            article.get('title', '').lower(),
            article.get('abstract', '').lower(),
            article.get('keywords', '').lower()
        ]
        return ' '.join(parts)

    def identify_research_gaps(self,
                              articles: List[Dict],
                              model: str) -> str:
        """
        Identify research gaps from a collection of articles

        Args:
            articles: Articles to analyze
            model: Ollama model to use

        Returns:
            Research gaps analysis
        """
        # Build summary of articles
        articles_summary = ""
        for i, article in enumerate(articles[:50], 1):  # Limit to 50 articles
            articles_summary += f"{i}. {article.get('title', 'Untitled')} ({article.get('year', 'N/A')})\n"
            articles_summary += f"   Abstract: {article.get('abstract', 'No abstract')[:200]}...\n\n"

        system_prompt = """You are an expert research strategist. Analyze the provided literature collection and identify research gaps, underexplored areas, and future research directions."""

        user_prompt = f"""Analyze this collection of {len(articles)} research articles and identify:

1. Research Gaps (areas not well covered)
2. Underexplored Topics
3. Methodological Gaps
4. Future Research Directions
5. Emerging Trends

Articles:
{articles_summary}

Provide a comprehensive analysis with specific, actionable insights."""

        analysis = self.ollama_service.generate(
            model=model,
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=2000,
            stream=False
        )

        return analysis

    def generate_reading_list(self,
                             articles: List[Dict],
                             model: str,
                             criteria: str = "foundational") -> List[Dict]:
        """
        Generate a prioritized reading list

        Args:
            articles: Articles to prioritize
            model: Ollama model to use
            criteria: Prioritization criteria (foundational, recent, highly-cited, comprehensive)

        Returns:
            Prioritized list of articles
        """
        if criteria == "foundational":
            # Sort by year (older first) and score
            sorted_articles = sorted(
                articles,
                key=lambda x: (x.get('year', 9999), -x.get('score', 0))
            )

        elif criteria == "recent":
            # Sort by year (newer first)
            sorted_articles = sorted(
                articles,
                key=lambda x: -x.get('year', 0)
            )

        elif criteria == "highly-cited":
            # Sort by score/citations
            sorted_articles = sorted(
                articles,
                key=lambda x: -x.get('score', 0)
            )

        elif criteria == "comprehensive":
            # Sort by abstract length (more comprehensive)
            sorted_articles = sorted(
                articles,
                key=lambda x: -len(x.get('abstract', ''))
            )

        else:
            sorted_articles = articles

        return sorted_articles

    def extract_methodologies(self,
                             articles: List[Dict],
                             model: str) -> Dict[str, List[str]]:
        """
        Extract and categorize research methodologies from articles

        Args:
            articles: Articles to analyze
            model: Ollama model to use

        Returns:
            Dictionary of methodology categories and examples
        """
        methodologies = {
            'Quantitative': [],
            'Qualitative': [],
            'Mixed Methods': [],
            'Experimental': [],
            'Survey': [],
            'Case Study': [],
            'Meta-Analysis': [],
            'Other': []
        }

        # Extract from abstracts
        for article in articles[:30]:  # Limit for performance
            abstract = article.get('abstract', '').lower()
            title = article.get('title', '')

            if any(term in abstract for term in ['experiment', 'trial', 'randomized']):
                methodologies['Experimental'].append(title)
            if any(term in abstract for term in ['survey', 'questionnaire', 'poll']):
                methodologies['Survey'].append(title)
            if any(term in abstract for term in ['case study', 'case analysis']):
                methodologies['Case Study'].append(title)
            if any(term in abstract for term in ['meta-analysis', 'systematic review']):
                methodologies['Meta-Analysis'].append(title)
            if any(term in abstract for term in ['interview', 'focus group', 'ethnography']):
                methodologies['Qualitative'].append(title)
            if any(term in abstract for term in ['statistical', 'regression', 'correlation']):
                methodologies['Quantitative'].append(title)

        return {k: v for k, v in methodologies.items() if v}
