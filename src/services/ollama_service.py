"""
Ollama integration service for AI model interactions
"""

import requests
import json
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass


@dataclass
class OllamaModel:
    """Ollama model information"""
    name: str
    size: int = 0
    modified: str = ""
    digest: str = ""


class OllamaService:
    """Service for interacting with local Ollama models"""

    def __init__(self, base_url: str = "http://localhost:11434"):
        """Initialize Ollama service"""
        self.base_url = base_url
        self.timeout = 120  # Default timeout in seconds

    def is_available(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

    def get_models(self) -> List[OllamaModel]:
        """Get list of available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                models = []
                for model_data in data.get('models', []):
                    models.append(OllamaModel(
                        name=model_data.get('name', ''),
                        size=model_data.get('size', 0),
                        modified=model_data.get('modified_at', ''),
                        digest=model_data.get('digest', '')
                    ))
                return models
            return []
        except Exception as e:
            print(f"Error fetching models: {e}")
            return []

    def generate(self,
                 model: str,
                 prompt: str,
                 system_prompt: str = "",
                 temperature: float = 0.7,
                 max_tokens: int = 2000,
                 stream: bool = False,
                 callback: Optional[Callable[[str], None]] = None) -> str:
        """Generate text using Ollama model"""
        try:
            url = f"{self.base_url}/api/generate"

            payload = {
                "model": model,
                "prompt": prompt,
                "stream": stream,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }

            if system_prompt:
                payload["system"] = system_prompt

            if stream:
                response = requests.post(url, json=payload, stream=True, timeout=self.timeout)
                full_response = ""

                for line in response.iter_lines():
                    if line:
                        data = json.loads(line.decode('utf-8'))
                        chunk = data.get('response', '')
                        full_response += chunk

                        if callback:
                            callback(chunk)

                        if data.get('done', False):
                            break

                return full_response
            else:
                response = requests.post(url, json=payload, timeout=self.timeout)
                if response.status_code == 200:
                    return response.json().get('response', '')
                else:
                    return f"Error: {response.status_code} - {response.text}"

        except requests.exceptions.Timeout:
            return "Error: Request timed out. The model may be taking too long to respond."
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def chat(self,
             model: str,
             messages: List[Dict[str, str]],
             temperature: float = 0.7,
             max_tokens: int = 2000,
             stream: bool = False,
             callback: Optional[Callable[[str], None]] = None) -> str:
        """Chat with Ollama model"""
        try:
            url = f"{self.base_url}/api/chat"

            payload = {
                "model": model,
                "messages": messages,
                "stream": stream,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }

            if stream:
                response = requests.post(url, json=payload, stream=True, timeout=self.timeout)
                full_response = ""

                for line in response.iter_lines():
                    if line:
                        data = json.loads(line.decode('utf-8'))
                        message = data.get('message', {})
                        chunk = message.get('content', '')
                        full_response += chunk

                        if callback:
                            callback(chunk)

                        if data.get('done', False):
                            break

                return full_response
            else:
                response = requests.post(url, json=payload, timeout=self.timeout)
                if response.status_code == 200:
                    message = response.json().get('message', {})
                    return message.get('content', '')
                else:
                    return f"Error: {response.status_code} - {response.text}"

        except requests.exceptions.Timeout:
            return "Error: Request timed out. The model may be taking too long to respond."
        except Exception as e:
            return f"Error in chat: {str(e)}"

    def generate_report(self,
                       model: str,
                       articles: List[Dict],
                       query: str,
                       temperature: float = 0.7,
                       callback: Optional[Callable[[str], None]] = None) -> str:
        """Generate a literature review report from articles"""

        # Build context from articles
        articles_context = ""
        for i, article in enumerate(articles, 1):
            articles_context += f"\n\n[{i}] {article.get('title', 'Untitled')}\n"
            articles_context += f"Authors: {article.get('authors', 'Unknown')}\n"
            articles_context += f"Year: {article.get('year', 'N/A')}\n"
            articles_context += f"Journal: {article.get('journal', 'N/A')}\n"
            articles_context += f"DOI: {article.get('doi', 'N/A')}\n"
            articles_context += f"Abstract: {article.get('abstract', 'No abstract available')}\n"

        system_prompt = """You are an expert academic researcher and writer. Your task is to generate a comprehensive, well-structured literature review report based on the provided articles.

Your report should:
1. Use proper markdown formatting with clear headings (# ## ###)
2. Include an executive summary at the beginning
3. Organize findings thematically
4. Use inline citations in the format [Author, Year] or [1], [2], etc.
5. Provide critical analysis and synthesis of the literature
6. Highlight key findings, methodologies, and conclusions
7. Include a proper reference section at the end
8. Be written in professional academic style
9. Use proper spacing and formatting for readability

Format the references in APA style at the end of the report."""

        user_prompt = f"""Generate a comprehensive literature review report on the topic: "{query}"

Based on the following {len(articles)} articles:
{articles_context}

Please provide:
1. Executive Summary
2. Introduction
3. Methodology Overview
4. Key Findings (organized thematically)
5. Discussion
6. Conclusions
7. References

Ensure all claims are properly cited with inline citations."""

        return self.generate(
            model=model,
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=4000,
            stream=True,
            callback=callback
        )

    def generate_enhanced_report(self,
                                 model: str,
                                 articles: List[Dict],
                                 query: str,
                                 temperature: float = 0.7,
                                 writing_style: str = "Academic",
                                 humanize: bool = True,
                                 report_type: str = "Comprehensive Literature Review",
                                 fast_mode: bool = False,
                                 timeout: int = 180,
                                 callback: Optional[Callable[[str], None]] = None) -> str:
        """Generate an enhanced literature review report with custom styling and humanization"""

        # Build context from articles
        articles_context = ""
        for i, article in enumerate(articles, 1):
            articles_context += f"\n\n[{i}] {article.get('title', 'Untitled')}\n"
            articles_context += f"Authors: {article.get('authors', 'Unknown')}\n"
            articles_context += f"Year: {article.get('year', 'N/A')}\n"
            articles_context += f"Journal: {article.get('journal', 'N/A')}\n"
            articles_context += f"DOI: {article.get('doi', 'N/A')}\n"
            articles_context += f"Abstract: {article.get('abstract', 'No abstract available')}\n"

        # Define writing style prompts
        style_prompts = {
            "Academic": "Use formal, scholarly tone with technical terminology appropriate for peer-reviewed publications. Employ precise academic language and maintain objectivity throughout.",
            "Professional": "Use business-appropriate language that is clear, concise, and accessible to professionals across different fields. Balance technical accuracy with readability.",
            "Technical": "Focus on detailed methodological descriptions, technical specifications, and precise terminology. Emphasize technical rigor and replicability.",
            "Executive Summary": "Write in a high-level, strategic style appropriate for decision-makers. Focus on key insights, implications, and actionable conclusions. Be concise and impactful.",
            "Journalistic": "Use an accessible, narrative-driven style that engages general readers while maintaining accuracy. Tell the story of the research in a compelling way."
        }

        # Define humanization instructions
        humanize_instruction = ""
        if humanize:
            humanize_instruction = """
IMPORTANT - Natural Writing Guidelines:
• Vary sentence structure and length naturally (mix short punchy sentences with longer, more complex ones)
• Use transitional phrases to connect ideas smoothly (however, furthermore, in contrast, notably, etc.)
• Avoid repetitive sentence patterns and mechanical phrasing
• Incorporate natural flow with varied vocabulary
• Use active voice where appropriate
• Create a conversational yet professional tone
• Avoid overly formal or stilted constructions
• Make the text feel written by a human expert, not generated by AI
"""

        # Define report type structures
        report_structures = {
            "Comprehensive Literature Review": """
1. Executive Summary
2. Introduction and Background
3. Methodology and Approach
4. Thematic Analysis of Literature
5. Key Findings and Insights
6. Critical Discussion
7. Research Gaps and Future Directions
8. Conclusions
9. References""",
            "Executive Summary": """
1. Key Findings (bullet points)
2. Strategic Implications
3. Recommendations
4. Supporting References""",
            "Detailed Analysis": """
1. Introduction
2. Detailed Methodological Analysis
3. Comprehensive Findings by Theme
4. Critical Evaluation
5. Synthesis and Interpretation
6. Limitations and Considerations
7. Conclusions
8. References""",
            "Synthesis Report": """
1. Overview
2. Synthesis of Major Themes
3. Convergent Findings
4. Divergent Perspectives
5. Integrated Conclusions
6. References""",
            "Comparative Study": """
1. Introduction
2. Comparison Framework
3. Comparative Analysis by Criteria
4. Similarities and Differences
5. Synthesis and Insights
6. Conclusions
7. References"""
        }

        # Adjust max tokens based on mode
        max_tokens = 2000 if fast_mode else 4000

        # Build system prompt
        system_prompt = f"""You are an expert academic researcher and writer specializing in literature review synthesis.

WRITING STYLE: {style_prompts.get(writing_style, style_prompts['Academic'])}

REPORT TYPE: {report_type}
{humanize_instruction}

Your report must:
1. Use proper markdown formatting with clear headings (# ## ###)
2. Follow the structure outlined for this report type
3. Use inline citations in the format [Author, Year] or [1], [2], etc.
4. Provide critical analysis and synthesis of the literature
5. Highlight key findings, methodologies, and conclusions
6. Include a proper reference section at the end
7. Format references in APA style
8. Demonstrate deep understanding and insight{' (be concise and focused)' if fast_mode else ''}

Structure your report as follows:
{report_structures.get(report_type, report_structures['Comprehensive Literature Review'])}
"""

        user_prompt = f"""Generate a {report_type.lower()} on the topic: "{query}"

Based on the following {len(articles)} articles:
{articles_context}

Apply the {writing_style} writing style and ensure all claims are properly cited with inline citations.
{'Focus on conciseness and key points for rapid generation.' if fast_mode else 'Provide comprehensive analysis with detailed insights.'}
"""

        # Set timeout for the service
        original_timeout = self.timeout
        self.timeout = timeout

        try:
            result = self.generate(
                model=model,
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
                callback=callback
            )
            return result
        finally:
            # Restore original timeout
            self.timeout = original_timeout

    def summarize_article(self, model: str, article: Dict, callback: Optional[Callable[[str], None]] = None) -> str:
        """Generate a summary for a single article"""

        system_prompt = "You are an expert at summarizing academic research papers. Provide concise, accurate summaries that capture the key points, methodology, and findings."

        user_prompt = f"""Summarize the following research article in 2-3 sentences:

Title: {article.get('title', 'Untitled')}
Authors: {article.get('authors', 'Unknown')}
Year: {article.get('year', 'N/A')}
Abstract: {article.get('abstract', 'No abstract available')}

Provide a clear, concise summary focusing on the main contribution and findings."""

        return self.generate(
            model=model,
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.5,
            max_tokens=500,
            stream=False,
            callback=callback
        )
