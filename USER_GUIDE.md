# DeepLlama User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Installation](#installation)
3. [Features Overview](#features-overview)
4. [Search Tab](#search-tab)
5. [Literature Database Tab](#literature-database-tab)
6. [Report Generation Tab](#report-generation-tab)
7. [AI Chat Tab](#ai-chat-tab)
8. [Settings Tab](#settings-tab)
9. [Tips & Best Practices](#tips--best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Getting Started

DeepLlama is a comprehensive desktop application for conducting deep literature reviews using local AI models powered by Ollama.

### Prerequisites
- Python 3.8 or higher
- Ollama installed and running locally
- At least one Ollama model pulled (recommended: `llama2`, `mistral`, or `mixtral`)

### Quick Start
1. Install Ollama from https://ollama.ai
2. Pull a model: `ollama pull llama2`
3. Run DeepLlama: `./run.sh` (Linux/Mac) or `run.bat` (Windows)

---

## Installation

### Method 1: Using Run Scripts (Recommended)

**Linux/macOS:**
```bash
chmod +x run.sh
./run.sh
```

**Windows:**
```
run.bat
```

The run scripts automatically:
- Create a virtual environment
- Install all dependencies
- Check if Ollama is running
- Launch the application

### Method 2: Manual Installation

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate.bat  # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

---

## Features Overview

### 🔍 Multi-Source Search
Search across 50+ academic databases including:
- OpenAlex (comprehensive multidisciplinary)
- PubMed (biomedical literature)
- arXiv (preprints in physics, math, CS)
- Semantic Scholar (AI-powered search)
- CORE (open access research)

### 📊 Smart Organization
- Sortable spreadsheet-style table
- Full abstract display (no truncation)
- Comprehensive metadata storage
- Personal notes and annotations
- CSV import/export

### 🤖 AI-Powered Analysis
- Generate comprehensive literature review reports
- Multiple Ollama model support
- Customizable temperature and parameters
- Streaming output with real-time updates

### 📝 Export Options
- Markdown export with metadata headers
- DOCX export with proper formatting
- Multiple citation styles (APA, MLA, Chicago, IEEE)
- Automatic bibliography generation

### 💬 Context-Aware Chat
- Ask questions about your articles
- Compare methodologies
- Identify research gaps
- Get AI-powered insights

---

## Search Tab

### Basic Search

1. Enter your query in the search box
   - Keywords: `machine learning`, `climate change`
   - Phrases: `"deep neural networks"`, `"renewable energy"`
   - Topics: `artificial intelligence in healthcare`

2. Set the number of articles to retrieve (1-1000)

3. Select data sources
   - Check/uncheck individual sources
   - Use "Select All" / "Deselect All" buttons

4. Click "🔍 Search"

### Search Results

- Results appear in the status area
- Shows count by source
- Articles are automatically saved to the database
- You're switched to the Literature Database tab

### Tips
- Start with 50 articles for quick results
- Use multiple sources for comprehensive coverage
- More specific queries yield better results
- PubMed is best for medical/biomedical topics
- arXiv is ideal for physics, math, and CS preprints

---

## Literature Database Tab

### Viewing Articles

The table displays all articles with columns:
- **✓**: Checkbox for selection
- **Title**: Article title (click to sort)
- **Authors**: Author names
- **Year**: Publication year
- **Journal**: Publication venue
- **DOI**: Digital Object Identifier
- **Keywords**: Article keywords/topics
- **Abstract**: Full abstract (NO TRUNCATION)
- **Source**: Database source
- **Score**: Relevance score
- **Date Added**: When added to database

### Article Selection

1. **Select Individual Articles**: Check boxes next to articles
2. **Select All**: Click "☑️ Select All" button
3. **Deselect All**: Click "☐ Deselect All" button

Selected articles are used for:
- Report generation
- AI chat context
- Batch operations

### Viewing Full Details

**Double-click** any row to open a detailed view with:
- Complete bibliographic information
- Full abstract
- AI-generated summary (if available)
- Personal notes
- Direct link to source

### Sorting

Click any column header to sort:
- Click once: Ascending order
- Click again: Descending order
- Useful for organizing by year, relevance, etc.

### CSV Import/Export

**Import CSV:**
1. Click "📥 Import CSV"
2. Select your CSV file
3. Articles are added to database

**CSV Format:**
```csv
title,authors,year,journal,doi,keywords,abstract,source,score,url,notes
"Article Title","Author 1, Author 2",2023,"Journal Name","10.1234/example","keyword1, keyword2","Abstract text...","Source",1.0,"https://...",""
```

**Export CSV:**
1. Click "📤 Export CSV"
2. Choose save location
3. All articles exported with full metadata

### Clear All

1. Click "🗑️ Clear All"
2. Confirm the action
3. All articles removed from database

**⚠️ Warning**: This action cannot be undone!

---

## Report Generation Tab

### Generating Reports

1. **Select Articles**: Choose articles in Literature Database tab
2. **Choose Model**: Select an Ollama model from dropdown
3. **Adjust Temperature**:
   - Low (0.0-0.3): Focused, factual
   - Medium (0.4-0.8): Balanced
   - High (0.9-2.0): Creative, varied
4. **Select Citation Style**: APA, MLA, Chicago, or IEEE
5. **Click "✨ Generate Report"**

### Report Structure

Generated reports include:
- **Executive Summary**: Overview of findings
- **Introduction**: Context and scope
- **Methodology Overview**: Research methods from articles
- **Key Findings**: Organized thematically
- **Discussion**: Analysis and synthesis
- **Conclusions**: Main takeaways
- **References**: Properly formatted citations

### Real-Time Generation

- Report streams in real-time
- Watch as the AI writes
- Stop anytime with "⏹️ Stop" button

### Export Options

**Markdown Export:**
- Click "📥 Export Markdown"
- Includes metadata header
- Perfect for version control
- Can be converted to other formats

**DOCX Export:**
- Click "📥 Export DOCX"
- Professional formatting
- Compatible with Microsoft Word
- Includes title page and proper spacing

### Tips for Better Reports

1. **Select 5-20 articles** for focused reports
2. **Use higher temperature (0.7-0.8)** for creative synthesis
3. **Lower temperature (0.3-0.5)** for factual summaries
4. **Larger models** (70B+) produce more sophisticated analysis
5. **Review and edit** the generated report as needed

---

## AI Chat Tab

### Chat Modes

**With Article Context:**
1. Select articles in Literature Database
2. Check "Use selected articles as context"
3. Ask questions about your articles

**General Chat:**
1. Uncheck "Use selected articles as context"
2. General AI assistance

### Sample Questions

**Analysis:**
- "What are the main findings across these articles?"
- "Summarize the key contributions of each paper"
- "What methodologies were used?"

**Comparison:**
- "Compare the approaches in these papers"
- "How do the results differ between studies?"
- "Which paper has the strongest evidence?"

**Synthesis:**
- "What are the common themes?"
- "Identify research gaps"
- "What are the contradictions or disagreements?"

**Methodology:**
- "What sample sizes were used?"
- "What statistical methods appear?"
- "Are there experimental design issues?"

### Chat Features

- **Streaming Responses**: See AI typing in real-time
- **Context-Aware**: AI references your selected articles
- **Chat History**: Maintains conversation context
- **Clear History**: Start fresh anytime
- **Model Selection**: Use any installed Ollama model

---

## Settings Tab

### Ollama Configuration

**Ollama URL:**
- Default: `http://localhost:11434`
- Change if Ollama runs on different host/port

**Default Model:**
- Set your preferred model
- Used for chat and reports
- Can override per operation

**Temperature:**
- Global default temperature
- Range: 0.0 to 2.0

**Max Tokens:**
- Maximum response length
- Range: 100 to 10,000

### Search Configuration

**Default # of Results:**
- How many articles to fetch per search
- Range: 1 to 1,000

**Citation Style:**
- Default citation format
- Options: APA, MLA, Chicago, IEEE

### User Interface

**Theme:**
- **Dark**: Default dark theme (easy on eyes)
- **Light**: Clean white background
- **High Contrast**: For accessibility
- **Academic**: Professional scholarly theme

**Font Settings:**
- Choose font family
- Adjust font size (8-20pt)

### Database

**Auto-save articles:**
- Automatically save search results
- Recommended: Keep enabled

### Saving Settings

1. Make your changes
2. Click "💾 Save Settings"
3. Settings persist between sessions

### Reset to Defaults

1. Click "🔄 Reset to Defaults"
2. Confirm action
3. All settings restored to original values

---

## Tips & Best Practices

### Search Strategy

1. **Start Broad, Then Narrow**
   - Initial search: 100+ articles
   - Review and select relevant ones
   - Generate reports on curated set

2. **Use Multiple Sources**
   - Different databases have different coverage
   - OpenAlex + PubMed + arXiv = comprehensive

3. **Refine Your Query**
   - Too many irrelevant results? Use more specific terms
   - Too few results? Broaden your keywords

### Article Management

1. **Regular Exports**
   - Export CSV backups of your database
   - Save important reports

2. **Use Notes**
   - Add personal annotations
   - Flag important articles

3. **Organize by Projects**
   - Clear database between major projects
   - Or export/import for different topics

### Report Generation

1. **Quality Over Quantity**
   - 10 highly relevant articles > 100 marginally related

2. **Experiment with Models**
   - Try different Ollama models
   - Larger models = more sophisticated analysis
   - Smaller models = faster responses

3. **Adjust Temperature**
   - Literature reviews: 0.5-0.7
   - Creative synthesis: 0.7-0.9
   - Summaries: 0.3-0.5

4. **Iterate**
   - Generate initial report
   - Review and note gaps
   - Search for additional articles
   - Regenerate with complete set

### AI Chat Usage

1. **Be Specific**
   - "What are the sample sizes?" > "Tell me about the studies"

2. **Reference Articles**
   - Chat knows which articles you selected
   - Ask comparative questions

3. **Build on Responses**
   - Use chat history for follow-up questions
   - AI maintains context

---

## Troubleshooting

### Ollama Not Available

**Problem**: "❌ Ollama not running" message

**Solutions**:
1. Install Ollama from https://ollama.ai
2. Start Ollama: `ollama serve`
3. Verify: `curl http://localhost:11434/api/tags`
4. Check Settings tab for correct URL

### No Models Available

**Problem**: "No models available" in dropdown

**Solutions**:
1. Pull a model: `ollama pull llama2`
2. Verify: `ollama list`
3. Click "🔄 Refresh" button
4. Restart application

### Search Returns No Results

**Possible Causes**:
- Too specific query
- Source databases may be down
- Network connectivity issues

**Solutions**:
1. Try broader keywords
2. Test with simple query: "machine learning"
3. Check different sources
4. Verify internet connection

### Import CSV Fails

**Problem**: CSV import shows errors

**Solutions**:
1. Check CSV format matches expected columns
2. Ensure UTF-8 encoding
3. Remove special characters from file
4. Verify file not corrupted

### Report Generation Slow

**Problem**: Report takes very long to generate

**Solutions**:
1. Use smaller model (e.g., llama2 vs llama2:70b)
2. Reduce number of selected articles
3. Increase Ollama timeout in settings
4. Check system resources (RAM, CPU)

### Theme Not Changing

**Problem**: Theme toggle doesn't work

**Solutions**:
1. Go to Settings tab
2. Select theme explicitly
3. Click "💾 Save Settings"
4. Restart application if needed

### Application Crashes

**Problem**: Application closes unexpectedly

**Solutions**:
1. Check Python version (3.8+ required)
2. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
3. Check error logs
4. Clear database: `rm data/literature.db`
5. Reset settings: `rm data/config.json`

### Database Locked Error

**Problem**: "Database is locked" message

**Solutions**:
1. Close other instances of DeepLlama
2. Restart application
3. If persists, delete lock file

---

## Keyboard Shortcuts

- **Search Tab**: `Enter` to start search
- **Chat Tab**: `Enter` to send message
- **Double-click**: View article details
- **Ctrl+A** (in tables): Select all rows

---

## Support & Feedback

For issues, feature requests, or contributions:
- GitHub: [Your Repository URL]
- Documentation: Check README.md
- Ollama Help: https://ollama.ai/docs

---

## Version Information

**Current Version**: 1.0.0

**Last Updated**: 2024

**License**: MIT License

---

Happy researching! 📚🔬
