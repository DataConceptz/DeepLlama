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
