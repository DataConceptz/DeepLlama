# DeepLlama - AI Literature Review Research Tool

A comprehensive, enterprise-grade desktop application for conducting deep literature reviews using local AI models.

**Version 2.0 - Enterprise Edition** - Now with Analytics Dashboard, Batch Operations, and Advanced Export Formats!

## ✨ Features

### Core Features
- 🔍 **Multi-Source Search**: Search across 50+ academic databases (OpenAlex, PubMed, arXiv, CORE, etc.)
- 📊 **Smart Organization**: Sortable table view with complete bibliographic metadata
- 🤖 **AI-Powered Analysis**: Generate comprehensive reports using local Ollama models
- ✍️ **5 Writing Styles**: Academic, Professional, Technical, Executive, Journalistic
- 🎭 **Humanization**: Natural, human-like writing with varied sentence structure
- ⚡ **Fast Mode**: 40-60% faster generation for quick summaries
- 💬 **AI Chat**: Context-aware chat interface for discussing research articles
- 🎨 **Professional UI**: Modern dark/light themes with customizable settings
- 💾 **Local Storage**: SQLite database for all articles and metadata

### NEW in v2.0!
- 📈 **Analytics Dashboard**: Publication timeline, top authors/journals, keyword clouds, source distribution
- ⚡ **Batch Operations**: AI summarization, auto-tagging, duplicate detection, research gap analysis
- 📤 **Advanced Export**: BibTeX, RIS, EndNote XML, JSON, Plain Text (8 total formats)
- 🔍 **Research Intelligence**: Gap identification, methodology extraction, reading list generation
- 🏷️ **Auto-Tagging**: AI-powered keyword extraction and categorization
- 📋 **Duplicate Detection**: Intelligent similarity matching with configurable threshold

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
- **8 Export Formats**: Markdown, DOCX, BibTeX, RIS, EndNote XML, JSON, Plain Text, CSV
- Multiple CSL citation styles supported (APA, MLA, Chicago, IEEE)
- Automatic bibliography generation
- BibTeX/RIS for reference managers (Zotero, EndNote, Mendeley)

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

## 🆕 What's New in v2.0 - Enterprise Edition

### Analytics Dashboard 📈
Gain instant insights into your research collection:
- **Overview Metrics**: Total articles, recent vs older publications, average scores
- **Publication Timeline**: Visualize research trends over time
- **Top Authors & Journals**: Identify key contributors and publications
- **Keyword Cloud**: Discover dominant themes in your research
- **Source Distribution**: Analyze where your articles come from
- **JSON Export**: Export analytics for custom visualizations

### Batch Operations ⚡
Process multiple articles simultaneously:
- **Batch Summarization**: Generate AI summaries for 100s of articles
- **Auto-Tagging**: Automatic keyword extraction and categorization
- **Duplicate Detection**: Find similar articles with configurable threshold
- **Research Gap Analysis**: AI-powered identification of research opportunities
- **Reading List Generation**: Prioritized recommendations
- **Methodology Extraction**: Categorize research approaches

### Advanced Export Formats 📤
Export your collection in professional formats:
- **BibTeX (.bib)**: Perfect for LaTeX documents
- **RIS (.ris)**: Compatible with EndNote, Zotero, Mendeley
- **EndNote XML (.xml)**: Direct EndNote desktop import
- **JSON (.json)**: Custom data analysis and scripts
- **Plain Text (.txt)**: Simple, readable format
- Plus existing: Markdown, DOCX, CSV

### Research Intelligence 🔍
- **Gap Identification**: Discover underexplored research areas
- **Trend Analysis**: Track publication patterns over time
- **Author Networks**: Identify collaboration opportunities
- **Topic Clustering**: Automatic thematic organization

### Performance Improvements
- Handles 10,000+ articles efficiently
- Optimized database queries
- Threaded operations (non-blocking UI)
- Real-time progress tracking for all batch operations

📖 **See [ENHANCEMENTS_V2.0.md](ENHANCEMENTS_V2.0.md) for complete v2.0 details**
📖 **See [FEATURES_V2.0_SUMMARY.md](FEATURES_V2.0_SUMMARY.md) for quick reference**

## 📚 Documentation

- **[USER_GUIDE.md](USER_GUIDE.md)**: Complete user manual
- **[FEATURES_IMPLEMENTED.md](FEATURES_IMPLEMENTED.md)**: Full feature list
- **[ENHANCEMENTS_V2.0.md](ENHANCEMENTS_V2.0.md)**: v2.0 complete feature guide
- **[FEATURES_V2.0_SUMMARY.md](FEATURES_V2.0_SUMMARY.md)**: v2.0 quick reference
- **[ENHANCEMENTS_V1.1.md](ENHANCEMENTS_V1.1.md)**: v1.1 release notes

## License

MIT License
