# YouTube SEO Optimization Agent

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)](https://openai.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Workflow-orange.svg)](https://github.com/langchain-ai/langgraph)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-success.svg)]()

**Part 6/50 – Agentic AI & Automation Series**

An AI-powered YouTube SEO optimization engine that leverages multi-agent orchestration to generate ranking-focused metadata, titles, descriptions, tags, and chapters from video content.

---

## 📋 Project Overview

This production-grade system transforms raw video content into algorithmically-optimized YouTube assets using a three-agent architecture. It accepts YouTube URLs or local media files, transcribes audio, and generates SEO-optimized metadata through intelligent agent coordination with built-in validation and retry mechanisms.

### Architecture Diagram

```
Input (URL/File) → Audio Extraction → Transcription → Agent 1 (Content Brief)
                                                              ↓
                                       Agent 3 (SEO Assets) ← Agent 2 (Keywords)
                                                              ↓
                                                    Validation → Scoring → JSON Output
```

*See `docs/architecture-flowchart.png` for detailed visual representation*

---

## ✨ Features

- **Multi-Input Support**: YouTube URLs, audio files (mp3, wav, m4a), video files (mp4, mov, mkv)
- **Duration-Aware Processing**: Chapters automatically scaled to video length
- **Three-Agent Architecture**: Specialized agents for content analysis, keyword strategy, and asset generation
- **Validation Loops**: Pydantic schema validation with automatic retry on failure
- **SEO Scoring System**: 0-100 scores for titles, keywords, and CTR optimization
- **Production-Grade**: Tenacity retry logic, exponential backoff, structured logging
- **Cross-Platform**: Works in VS Code, Jupyter, and Google Colab
- **Ranking-Focused**: Algorithm-aware prompts optimized for YouTube discoverability

---

## 🔄 Workflow Overview

1. **Input Processing**
   - Accept YouTube URL or local file path
   - Download audio via yt-dlp (YouTube) or extract via ffmpeg (local files)
   - Extract video duration metadata

2. **Transcription**
   - Transcribe audio using OpenAI Whisper
   - Preprocess and normalize transcript
   - Compress if exceeds token limits

3. **Agent Orchestration**
   - **Agent 1**: Analyze content and extract video metadata
   - **Agent 2**: Generate ranking-focused keyword strategy
   - **Agent 3**: Create SEO-optimized titles, descriptions, tags, chapters

4. **Validation & Scoring**
   - Validate outputs against Pydantic schemas
   - Retry with corrective prompts if validation fails
   - Calculate SEO quality scores

5. **Output Generation**
   - Compile structured JSON output
   - Print to stdout (logs to stderr)

---

## 🤖 Agent Breakdown

### Agent 1: Content Brief Agent
**Temperature**: 0.2 (Factual Analysis)

**Mission**: Extract strategic metadata for algorithmic optimization

**Outputs**:
- `main_topic`: Rankable, searchable topic description
- `target_audience`: Detailed audience profile with search behavior
- `search_intent`: Classification (informational, tutorial, review, etc.)
- `content_category`: YouTube taxonomy alignment
- `duration_seconds`: Video duration

### Agent 2: Keyword Strategy Agent
**Temperature**: 0.4 (Balanced Creativity)

**Mission**: Generate ranking-focused keyword sets

**Outputs**:
- `primary`: Single high-value ranking keyword (2-5 words)
- `secondary`: 5-10 complementary keywords with modifiers
- `long_tail`: 5-10 question-based search phrases (4-8 words)

**Focus**: Uses ranking modifiers like "best", "top", "guide", "complete", numbers

### Agent 3: SEO Assets Agent
**Temperature**: 0.7 (Creative Variation)

**Mission**: Create click-optimized, algorithm-friendly assets

**Outputs**:
- **SEO Titles** (5): Keyword-optimized, 55-60 chars, 2+ with numbers, 3+ with primary keyword
- **High-CTR Titles** (3): Curiosity-driven, benefit-focused, 50-60 chars
- **Description**: Hook (120 chars with keyword), summary, 3-7 bullets
- **Tags**: 15-25 unique, deduplicated tags
- **Chapters**: 4-12 chapters, evenly distributed, duration-aware

---

## 🔁 Validation & Retry Logic

### Validation Layer
- **Pydantic Models**: Strict schema enforcement for all outputs
- **Field Validation**: Length limits, character counts, uniqueness checks
- **Timestamp Validation**: Strictly increasing, duration bounds, format normalization

### Retry Mechanism
```python
Max Retries: 3 attempts per agent
Backoff: Exponential (2s → 4s → 8s)
Triggers: API errors, rate limits, validation failures
Correction: Sends validation error + schema to LLM for fix
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.8+ |
| **LLM** | OpenAI GPT-4o-mini |
| **STT** | OpenAI Whisper |
| **Workflow** | LangGraph |
| **Validation** | Pydantic v2 |
| **Retry Logic** | Tenacity |
| **Media Processing** | yt-dlp, ffmpeg |
| **Environment** | python-dotenv, google-colab |

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- ffmpeg installed
- OpenAI API key

### Steps

**1. Install ffmpeg**

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows (Chocolatey)
choco install ffmpeg
```

**2. Install Python Dependencies**

```bash
pip install openai yt-dlp pydantic tenacity langgraph langchain-core python-dotenv
```

**3. Set Environment Variables**

Create `.env` file:
```env
OPENAI_API_KEY=your-api-key-here
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_STT_MODEL=whisper-1
```

**Google Colab Setup**:
```python
# Install system dependencies
!apt-get update && apt-get install -y ffmpeg

# Install Python packages
!pip install openai yt-dlp pydantic tenacity langgraph langchain-core python-dotenv

# Set API key in Colab Secrets (🔑 icon in sidebar)
# Name: OPENAI_API_KEY
# Value: your-api-key
```

---

## 🚀 Usage

### Command Line

```bash
# YouTube URL
python youtube_seo_agent.py

# When prompted:
Enter YouTube URL (or press Enter to upload file): https://youtu.be/VIDEO_ID

# Or upload local file
Enter YouTube URL (or press Enter to upload file): [press Enter]
Enter path to audio/video file: /path/to/video.mp4
```

### Python Script

```python
from youtube_seo_agent import process_video

result = process_video(
    input_source="youtube",
    youtube_url="https://youtu.be/VIDEO_ID",
    file_path=None
)

print(result)
```

### Output

JSON printed to stdout (logs to stderr):

```json
{
  "video_metadata": {
    "main_topic": "Best AI Tools for Content Creators",
    "target_audience": "Content creators, YouTubers aged 18-35...",
    "search_intent": "tutorial",
    "content_category": "Education",
    "duration_seconds": 847
  },
  "keywords": {
    "primary": "best AI tools for content creation",
    "secondary": [
      "top AI video editing tools",
      "complete guide to AI for creators",
      "best AI productivity tools 2024",
      "top 10 AI tools for YouTube",
      "AI content creation tutorial"
    ],
    "long_tail": [
      "how to use AI tools for video editing",
      "best AI tools for beginner content creators",
      "top AI productivity apps for YouTubers",
      "complete guide to AI video automation",
      "how to automate content creation with AI"
    ]
  },
  "assets": {
    "titles": {
      "seo_titles": [
        "Top 10 Best AI Tools for Content Creation 2024",
        "Best AI Tools for Content Creators: Complete Guide",
        "Ultimate Guide to Best AI Tools for Video Editing",
        "7 Best AI Productivity Tools Every Creator Needs",
        "Best AI Tools for Content Creation You Must Try"
      ],
      "high_ctr_titles": [
        "These AI Tools Changed How I Create Content Forever",
        "Stop Wasting Time: Best AI Tools for Creators Revealed",
        "AI Content Creation: The Tools Pros Don't Share"
      ]
    },
    "description": {
      "hook": "Looking for the best AI tools for content creation? Discover the top tools that will transform your workflow and boost productivity!",
      "summary": "In this comprehensive guide, we explore the best AI tools for content creation that every YouTuber and creator should know. From AI video editing to automated workflows, these best AI tools for content creation will save you hours and improve quality. Whether you're a beginner or pro, learn how to leverage the best AI tools for content creation to scale your output. Subscribe for more AI productivity tips!",
      "bullets": [
        "Discover the top 10 best AI tools for content creation",
        "Learn how AI can automate your video editing workflow",
        "Compare the best AI productivity tools for creators",
        "Step-by-step tutorial on using AI for content",
        "Find the perfect AI tools for your content niche"
      ]
    },
    "tags": [
      "best AI tools for content creation",
      "top AI video editing tools",
      "AI productivity tools",
      "content creation automation",
      "AI for YouTubers",
      "best AI tools 2024",
      "AI video editing",
      "content creator tools",
      "AI workflow automation",
      "top AI apps for creators",
      "AI content strategy",
      "video editing AI",
      "creator productivity",
      "AI tutorial",
      "content creation guide"
    ],
    "chapters": [
      {"timestamp": "00:00", "title": "Introduction to AI Content Creation"},
      {"timestamp": "01:30", "title": "Top 3 AI Video Editing Tools"},
      {"timestamp": "04:15", "title": "Best AI Writing Assistants"},
      {"timestamp": "06:45", "title": "AI Thumbnail Generation Tools"},
      {"timestamp": "09:20", "title": "Workflow Automation with AI"},
      {"timestamp": "12:00", "title": "Price Comparison and Recommendations"},
      {"timestamp": "13:45", "title": "Final Tips and Conclusion"}
    ]
  },
  "seo_score": {
    "overall": 95,
    "title_score": 100,
    "keyword_score": 90,
    "ctr_score": 95
  }
}
```

---

## 📁 Folder Structure

```
youtube-seo-agent/
├── youtube_seo_agent.py       # Main script
├── .env                        # Environment variables (gitignored)
├── .env.example                # Example environment file
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── LICENSE                     # MIT License
├── docs/
│   └── architecture-flowchart.png
└── examples/
    ├── example_output.json
    └── example_usage.py
```

---

## 🗺️ Roadmap

### Current Version (v1.0)
- ✅ Multi-input support (YouTube, audio, video)
- ✅ Three-agent architecture
- ✅ Duration-aware chapter generation
- ✅ SEO scoring system
- ✅ Production-grade validation

### Planned Features (v2.0)
- [ ] Multi-language transcription support
- [ ] Thumbnail analysis and recommendations
- [ ] Competitor video analysis
- [ ] Historical performance tracking
- [ ] A/B testing recommendations
- [ ] YouTube API integration for direct upload
- [ ] Batch processing for multiple videos
- [ ] Web interface (Gradio/Streamlit)
- [ ] Custom prompt templates
- [ ] Fine-tuned models for niche categories

---

## 🔮 Future Improvements

1. **Advanced Analytics**
   - Integration with YouTube Analytics API
   - Performance prediction based on historical data
   - Trend analysis for keyword timing

2. **Enhanced AI Capabilities**
   - GPT-4 Turbo support for longer videos
   - Custom fine-tuned models for specific niches
   - Multi-modal analysis (thumbnail + transcript)

3. **Workflow Extensions**
   - Script generation for new videos
   - Voiceover generation with ElevenLabs
   - Automated subtitle generation and formatting

4. **Enterprise Features**
   - Team collaboration workflows
   - Brand voice consistency enforcement
   - Multi-channel management
   - API endpoints for integration

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 👤 Author

**Part 6/50 – Agentic AI & Automation Series**

Building production-grade AI agents and automation systems. Follow the journey from concept to deployment.

Connect: [LinkedIn](#https://www.linkedin.com/in/ali-jaan-6a0b85274/) | [GitHub](#) | [Twitter](#)

---

**⭐ Star this repo if you found it helpful!**
