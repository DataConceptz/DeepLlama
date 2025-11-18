# DeepLlama - AI Literature Review Research Tool

A comprehensive desktop application for conducting deep literature reviews using local AI models.

## Features

- 🔍 **Multi-Source Search**: Search across 50+ academic databases (OpenAlex, PubMed, arXiv, CORE, etc.)
- 📊 **Smart Organization**: Sortable table view with complete bibliographic metadata
- 🤖 **AI-Powered Analysis**: Generate comprehensive reports using local Ollama models
- 📝 **Export Options**: Export to Markdown or DOCX with proper citations (CSL styles)
- 💬 **AI Chat**: Context-aware chat interface for discussing research articles
- 🎨 **Professional UI**: Modern dark/light themes with customizable settings
- 💾 **Local Storage**: SQLite database for all articles and metadata

## Installation

```bash
pip install -r requirements.txt
```

## Prerequisites

- Python 3.8+
- Ollama installed locally (https://ollama.ai)
- At least one Ollama model pulled (e.g., `ollama pull llama2`)

## Usage

```bash
python main.py
```

## Key Features

### 1. Literature Search
- Search by keywords, phrases, or topics
- Specify exact number of articles to retrieve
- Filter by year, journal, or source

### 2. Article Management
- View and sort articles in spreadsheet-style table
- Add personal notes and annotations
- Full abstract display (no truncation)
- PDF linking and storage

### 3. AI Report Generation
- Select multiple articles for analysis
- Choose any installed Ollama model
- Generate fully-cited academic reports
- Professional formatting with proper structure

### 4. Export & Citations
- Markdown export with inline citations
- DOCX export with formatted references
- Multiple CSL citation styles supported
- Automatic bibliography generation

### 5. AI Chat Interface
- Article-based discussions
- Research methodology assistance
- Literature comparison and synthesis

## License

MIT License
