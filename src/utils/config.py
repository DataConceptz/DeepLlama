"""
Configuration management
"""

import json
from pathlib import Path
from typing import Any, Dict


class Config:
    """Application configuration manager"""

    DEFAULT_CONFIG = {
        'ollama_url': 'http://localhost:11434',
        'default_model': '',
        'temperature': 0.7,
        'max_tokens': 2000,
        'theme': 'dark',
        'citation_style': 'APA',
        'default_search_sources': ['openalex', 'pubmed', 'arxiv', 'semantic_scholar'],
        'default_num_results': 50,
        'auto_save': True,
        'window_width': 1400,
        'window_height': 900,
        'font_family': 'Segoe UI',
        'font_size': 10
    }

    def __init__(self, config_path: str = "data/config.json"):
        """Initialize configuration"""
        self.config_path = Path(config_path)
        self.config = self.DEFAULT_CONFIG.copy()
        self.load()

    def load(self):
        """Load configuration from file"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                    self.config.update(loaded_config)
        except Exception as e:
            print(f"Error loading config: {e}")

    def save(self):
        """Save configuration to file"""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """Set configuration value"""
        self.config[key] = value
        self.save()

    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save()
