# DeepLlama - AI Literature Review Research Tool

A comprehensive, enterprise-grade desktop application for conducting deep literature reviews using local AI models.

**Version 1.1** - Now with advanced writing styles, humanization, and performance optimization!

## ✨ Features

- 🔍 **Multi-Source Search**: Search across 50+ academic databases (OpenAlex, PubMed, arXiv, CORE, etc.)
- 📊 **Smart Organization**: Sortable table view with complete bibliographic metadata
- 🤖 **AI-Powered Analysis**: Generate comprehensive reports using local Ollama models
- ✍️ **5 Writing Styles**: Academic, Professional, Technical, Executive, Journalistic
- 🎭 **Humanization**: Natural, human-like writing with varied sentence structure
- ⚡ **Fast Mode**: 40-60% faster generation for quick summaries
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

### 3. AI Report Generation (NEW v1.1!)
- **5 Writing Styles**: Academic, Professional, Technical, Executive Summary, Journalistic
- **Humanization Toggle**: Generate natural, human-like text
- **5 Report Types**: Comprehensive, Executive Summary, Detailed Analysis, Synthesis, Comparative
- **Fast Mode**: Optimized for speed (40-60% faster)
- **Real-Time Progress**: Live time tracking and word counting
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

## 🆕 What's New in v1.1

### Advanced Writing Styles
Choose from 5 professional writing styles tailored to your audience:
- **Academic**: Formal, scholarly tone for publications
- **Professional**: Business-appropriate, clear communication
- **Technical**: Detailed, methodology-focused
- **Executive Summary**: High-level, decision-maker focused
- **Journalistic**: Accessible, narrative-driven

### Humanization System
Enable natural, human-like writing that:
- Varies sentence structure and length
- Uses transitional phrases naturally
- Reduces robotic patterns
- Maintains professionalism

### Performance Optimization
- **Fast Mode**: Generate reports 40-60% faster
- **Configurable Timeout**: 30-600 seconds
- **Real-Time Tracking**: See elapsed time and word count
- **Enhanced Cancellation**: Stop generation anytime

### Enhanced UX
- Clear Report button with confirmation
- Reset All settings button
- Word and character counting
- Time estimates and completion tracking

📖 **See [ENHANCEMENTS_V1.1.md](ENHANCEMENTS_V1.1.md) for complete details**

## 📚 Documentation

- **[USER_GUIDE.md](USER_GUIDE.md)**: Complete user manual
- **[FEATURES_IMPLEMENTED.md](FEATURES_IMPLEMENTED.md)**: Full feature list
- **[ENHANCEMENTS_V1.1.md](ENHANCEMENTS_V1.1.md)**: v1.1 release notes

## License

MIT License
