"""
Multi-source academic search service
Integrates with OpenAlex, PubMed, arXiv, CORE, and other academic databases
"""

import requests
import time
from typing import List, Dict, Optional
from datetime import datetime
import xml.etree.ElementTree as ET
from urllib.parse import quote


class SearchService:
    """Service for searching multiple academic databases"""

    def __init__(self):
        """Initialize search service"""
        self.user_agent = "DeepLlama/1.0 (Literature Review Tool)"
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.user_agent})

    def search_all(self, query: str, max_results: int = 50, sources: List[str] = None) -> List[Dict]:
        """Search across all available sources"""
        if sources is None:
            sources = ['openalex', 'pubmed', 'arxiv', 'core']

        all_results = []

        results_per_source = max(1, max_results // len(sources))

        for source in sources:
            try:
                if source == 'openalex':
                    results = self.search_openalex(query, results_per_source)
                elif source == 'pubmed':
                    results = self.search_pubmed(query, results_per_source)
                elif source == 'arxiv':
                    results = self.search_arxiv(query, results_per_source)
                elif source == 'core':
                    results = self.search_core(query, results_per_source)
                elif source == 'semantic_scholar':
                    results = self.search_semantic_scholar(query, results_per_source)
                else:
                    continue

                all_results.extend(results)
                time.sleep(0.5)  # Rate limiting

            except Exception as e:
                print(f"Error searching {source}: {e}")
                continue

        # Sort by relevance score
        all_results.sort(key=lambda x: x.get('score', 0), reverse=True)

        return all_results[:max_results]

    def search_openalex(self, query: str, max_results: int = 50) -> List[Dict]:
        """Search OpenAlex database"""
        results = []
        try:
            url = "https://api.openalex.org/works"
            params = {
                'search': query,
                'per_page': min(max_results, 100),
                'filter': 'type:article',
                'sort': 'relevance_score:desc',
                'mailto': 'research@deepllama.app'  # Polite pool
            }

            response = self.session.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()

                for work in data.get('results', []):
                    # Extract authors
                    authors = []
                    for authorship in work.get('authorships', []):
                        author = authorship.get('author', {})
                        if author.get('display_name'):
                            authors.append(author['display_name'])

                    # Extract publication info
                    pub_year = work.get('publication_year', 0)
                    primary_location = work.get('primary_location', {}) or {}
                    source = primary_location.get('source', {}) or {}

                    # Get DOI
                    doi = work.get('doi', '').replace('https://doi.org/', '') if work.get('doi') else ''

                    # Get abstract
                    abstract = work.get('abstract', '')
                    if not abstract:
                        abstract = work.get('abstract_inverted_index', '')
                        if abstract:
                            abstract = "Abstract available (inverted index format)"

                    # Get keywords/topics
                    keywords = []
                    for topic in work.get('topics', [])[:5]:
                        if topic.get('display_name'):
                            keywords.append(topic['display_name'])

                    results.append({
                        'title': work.get('title', 'Untitled'),
                        'authors': ', '.join(authors) if authors else 'Unknown',
                        'year': pub_year,
                        'journal': source.get('display_name', 'Unknown'),
                        'doi': doi,
                        'keywords': ', '.join(keywords),
                        'abstract': abstract or 'No abstract available',
                        'source': 'OpenAlex',
                        'score': work.get('relevance_score', 0),
                        'url': work.get('id', ''),
                        'full_text': ''
                    })

        except Exception as e:
            print(f"OpenAlex search error: {e}")

        return results

    def search_pubmed(self, query: str, max_results: int = 50) -> List[Dict]:
        """Search PubMed database"""
        results = []
        try:
            # Step 1: Search for PMIDs
            search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
            search_params = {
                'db': 'pubmed',
                'term': query,
                'retmax': max_results,
                'retmode': 'json',
                'sort': 'relevance'
            }

            search_response = self.session.get(search_url, params=search_params, timeout=30)
            if search_response.status_code != 200:
                return results

            search_data = search_response.json()
            pmids = search_data.get('esearchresult', {}).get('idlist', [])

            if not pmids:
                return results

            # Step 2: Fetch details for PMIDs
            time.sleep(0.5)  # Rate limiting
            fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
            fetch_params = {
                'db': 'pubmed',
                'id': ','.join(pmids),
                'retmode': 'xml'
            }

            fetch_response = self.session.get(fetch_url, params=fetch_params, timeout=30)
            if fetch_response.status_code != 200:
                return results

            # Parse XML
            root = ET.fromstring(fetch_response.content)

            for article in root.findall('.//PubmedArticle'):
                try:
                    medline = article.find('.//MedlineCitation')
                    article_elem = medline.find('.//Article')

                    # Title
                    title_elem = article_elem.find('.//ArticleTitle')
                    title = title_elem.text if title_elem is not None else 'Untitled'

                    # Authors
                    authors = []
                    author_list = article_elem.find('.//AuthorList')
                    if author_list is not None:
                        for author in author_list.findall('.//Author'):
                            last_name = author.find('.//LastName')
                            fore_name = author.find('.//ForeName')
                            if last_name is not None:
                                name = last_name.text
                                if fore_name is not None:
                                    name = f"{fore_name.text} {name}"
                                authors.append(name)

                    # Year
                    year = 0
                    pub_date = article_elem.find('.//PubDate/Year')
                    if pub_date is not None:
                        try:
                            year = int(pub_date.text)
                        except:
                            pass

                    # Journal
                    journal_elem = article_elem.find('.//Journal/Title')
                    journal = journal_elem.text if journal_elem is not None else 'Unknown'

                    # Abstract
                    abstract_texts = []
                    abstract_elem = article_elem.find('.//Abstract')
                    if abstract_elem is not None:
                        for abstract_text in abstract_elem.findall('.//AbstractText'):
                            if abstract_text.text:
                                label = abstract_text.get('Label', '')
                                text = abstract_text.text
                                if label:
                                    abstract_texts.append(f"{label}: {text}")
                                else:
                                    abstract_texts.append(text)

                    abstract = ' '.join(abstract_texts) if abstract_texts else 'No abstract available'

                    # PMID and DOI
                    pmid_elem = medline.find('.//PMID')
                    pmid = pmid_elem.text if pmid_elem is not None else ''

                    doi = ''
                    article_ids = article.find('.//PubmedData/ArticleIdList')
                    if article_ids is not None:
                        for id_elem in article_ids.findall('.//ArticleId'):
                            if id_elem.get('IdType') == 'doi':
                                doi = id_elem.text
                                break

                    # Keywords
                    keywords = []
                    mesh_list = medline.find('.//MeshHeadingList')
                    if mesh_list is not None:
                        for mesh in mesh_list.findall('.//MeshHeading')[:5]:
                            descriptor = mesh.find('.//DescriptorName')
                            if descriptor is not None and descriptor.text:
                                keywords.append(descriptor.text)

                    results.append({
                        'title': title,
                        'authors': ', '.join(authors) if authors else 'Unknown',
                        'year': year,
                        'journal': journal,
                        'doi': doi,
                        'keywords': ', '.join(keywords),
                        'abstract': abstract,
                        'source': 'PubMed',
                        'score': 1.0,  # PubMed doesn't provide scores
                        'url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else '',
                        'full_text': ''
                    })

                except Exception as e:
                    print(f"Error parsing PubMed article: {e}")
                    continue

        except Exception as e:
            print(f"PubMed search error: {e}")

        return results

    def search_arxiv(self, query: str, max_results: int = 50) -> List[Dict]:
        """Search arXiv database"""
        results = []
        try:
            url = "http://export.arxiv.org/api/query"
            params = {
                'search_query': f'all:{query}',
                'start': 0,
                'max_results': max_results,
                'sortBy': 'relevance',
                'sortOrder': 'descending'
            }

            response = self.session.get(url, params=params, timeout=30)
            if response.status_code != 200:
                return results

            # Parse Atom XML
            root = ET.fromstring(response.content)
            ns = {'atom': 'http://www.w3.org/2005/Atom',
                  'arxiv': 'http://arxiv.org/schemas/atom'}

            for entry in root.findall('atom:entry', ns):
                try:
                    title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')

                    # Authors
                    authors = []
                    for author in entry.findall('atom:author', ns):
                        name = author.find('atom:name', ns)
                        if name is not None:
                            authors.append(name.text)

                    # Published date
                    published = entry.find('atom:published', ns).text
                    year = int(published[:4]) if published else 0

                    # Abstract
                    summary = entry.find('atom:summary', ns)
                    abstract = summary.text.strip().replace('\n', ' ') if summary is not None else 'No abstract'

                    # arXiv ID
                    arxiv_id = entry.find('atom:id', ns).text.split('/')[-1]

                    # Categories (as keywords)
                    categories = []
                    for category in entry.findall('atom:category', ns):
                        term = category.get('term')
                        if term:
                            categories.append(term)

                    # DOI (if available)
                    doi = ''
                    doi_elem = entry.find('arxiv:doi', ns)
                    if doi_elem is not None:
                        doi = doi_elem.text

                    results.append({
                        'title': title,
                        'authors': ', '.join(authors) if authors else 'Unknown',
                        'year': year,
                        'journal': 'arXiv',
                        'doi': doi,
                        'keywords': ', '.join(categories[:5]),
                        'abstract': abstract,
                        'source': 'arXiv',
                        'score': 1.0,
                        'url': f"https://arxiv.org/abs/{arxiv_id}",
                        'full_text': ''
                    })

                except Exception as e:
                    print(f"Error parsing arXiv entry: {e}")
                    continue

        except Exception as e:
            print(f"arXiv search error: {e}")

        return results

    def search_core(self, query: str, max_results: int = 50) -> List[Dict]:
        """Search CORE database"""
        results = []
        try:
            # CORE API v3 (requires API key for full access, using open endpoint)
            url = "https://core.ac.uk/api-v2/articles/search"
            params = {
                'query': query,
                'page': 1,
                'pageSize': min(max_results, 100)
            }

            # Note: This is a simplified version. For production, register for an API key
            # at https://core.ac.uk/services/api
            response = self.session.get(url, params=params, timeout=30)

            if response.status_code == 200:
                data = response.json()

                for item in data.get('data', []):
                    # Extract authors
                    authors = []
                    for author in item.get('authors', []):
                        if isinstance(author, str):
                            authors.append(author)
                        elif isinstance(author, dict):
                            authors.append(author.get('name', ''))

                    # Extract year
                    year = 0
                    year_published = item.get('yearPublished')
                    if year_published:
                        try:
                            year = int(year_published)
                        except:
                            pass

                    results.append({
                        'title': item.get('title', 'Untitled'),
                        'authors': ', '.join(authors) if authors else 'Unknown',
                        'year': year,
                        'journal': item.get('publisher', 'Unknown'),
                        'doi': item.get('doi', ''),
                        'keywords': ', '.join(item.get('topics', [])[:5]),
                        'abstract': item.get('description', 'No abstract available'),
                        'source': 'CORE',
                        'score': 1.0,
                        'url': item.get('downloadUrl', ''),
                        'full_text': ''
                    })

        except Exception as e:
            print(f"CORE search error: {e}")

        return results

    def search_semantic_scholar(self, query: str, max_results: int = 50) -> List[Dict]:
        """Search Semantic Scholar"""
        results = []
        try:
            url = "https://api.semanticscholar.org/graph/v1/paper/search"
            params = {
                'query': query,
                'limit': min(max_results, 100),
                'fields': 'title,authors,year,venue,externalIds,abstract,fieldsOfStudy,citationCount'
            }

            response = self.session.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()

                for paper in data.get('data', []):
                    # Extract authors
                    authors = []
                    for author in paper.get('authors', []):
                        if author.get('name'):
                            authors.append(author['name'])

                    # Extract DOI
                    external_ids = paper.get('externalIds', {}) or {}
                    doi = external_ids.get('DOI', '')

                    # Keywords from fields of study
                    keywords = paper.get('fieldsOfStudy', [])[:5] if paper.get('fieldsOfStudy') else []

                    results.append({
                        'title': paper.get('title', 'Untitled'),
                        'authors': ', '.join(authors) if authors else 'Unknown',
                        'year': paper.get('year', 0) or 0,
                        'journal': paper.get('venue', 'Unknown') or 'Unknown',
                        'doi': doi,
                        'keywords': ', '.join(keywords),
                        'abstract': paper.get('abstract', 'No abstract available') or 'No abstract available',
                        'source': 'Semantic Scholar',
                        'score': paper.get('citationCount', 0) / 100.0,  # Normalize citation count
                        'url': f"https://www.semanticscholar.org/paper/{paper.get('paperId', '')}",
                        'full_text': ''
                    })

        except Exception as e:
            print(f"Semantic Scholar search error: {e}")

        return results
