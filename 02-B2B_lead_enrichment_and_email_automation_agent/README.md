# 🚀 AI-Powered B2B Lead Generation Agent

Production-ready lead enrichment pipeline with **elite-level AI prompts** using LangGraph + OpenAI GPT-4.

## ⚡ Quick Overview

Automatically enriches B2B leads with:
- ✅ Company intelligence & market research
- ✅ Lead qualification scoring (1-10 scale)
- ✅ Personalized outreach emails
- ✅ Industry classification & insights

**AI Frameworks:** BANT, MEDDIC, CHAMP (scoring) | AIDA, PAS, BAB (email copywriting)

---

## 🎯 How It Works

```
Input: CSV/Excel/JSON → AI Enrichment → Qualification Scoring → Email Generation → Output
```

1. Upload leads (name, company, email)
2. AI researches each company
3. Scores lead quality (1-10)
4. Generates personalized emails
5. Exports enriched data (JSON + CSV)

**Processing:** 10-15 seconds per lead | **Cost:** ~$0.03 per lead (GPT-4-mini)

---

## 🚀 Quick Start (2 Minutes)

### **Google Colab (Easiest)**

```python
# STEP 1: Add API Key
# Click 🔑 icon → Add secret → Name: OPENAI_API_KEY → Paste your key

# STEP 2: Cell 1 - Install Dependencies
!pip install -r requirements.txt

# STEP 3: Cell 2 - Run Pipeline
# Copy-paste cell_2_lead_generation_pipeline.py
# Upload your CSV when prompted
# Wait ~2 minutes → Download results
```

### **Local Jupyter**

```bash
# Terminal setup
echo "OPENAI_API_KEY=sk-your-key-here" > .env
jupyter notebook

# Cell 1: Install dependencies
!pip install -r requirements.txt

# Cell 2: Run pipeline
# Copy-paste cell_2_lead_generation_pipeline.py
# Enter file path when prompted
# Results saved automatically
```

---

## 📁 Files

```
lead-generation-agent/
├── cell_1_install_dependencies.py    # Dependencies installation
├── cell_2_lead_generation_pipeline.py # Complete pipeline (897 lines)
├── requirements.txt                   # Package dependencies
├── sample_leads.csv                   # Example data
├── .env.example                       # API key template
└── TWO_CELL_GUIDE.md                 # Complete documentation
```

---

## 📊 Input Format

**Required columns:** `name`, `company`  
**Optional columns:** `title`, `email`, `website`, `industry`, `company_size`, `location`

**Example CSV:**
```csv
name,company,title,email,website
Sarah Chen,Stripe,VP Product,sarah@stripe.com,stripe.com
James Wilson,Shopify,Head of Engineering,james@shopify.com,shopify.com
```

**Supported formats:** `.csv`, `.xlsx`, `.xls`, `.json`

---

## 📤 Output

**enriched_leads.json:**
```json
{
  "lead_id": 1,
  "name": "Sarah Chen",
  "company": "Stripe",
  "score": 9.2,
  "company_summary": "Stripe is a financial infrastructure platform...",
  "fit_reasons": ["VP-level decision-maker...", "High-growth fintech..."],
  "email_generated": {
    "subject": "Product Development at Stripe",
    "body": "Hi Sarah,\n\nI've been following Stripe's growth..."
  }
}
```

**enriched_leads.csv:** Flattened spreadsheet version

---

## ⚙️ Configuration

### **API Key Setup**

**Colab:** Add to Secrets (🔑 icon)  
**Local:** Create `.env` file
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### **Dependencies**
```
openai>=1.12.0
langgraph>=0.0.30
pydantic>=2.5.0
pandas>=2.0.0
openpyxl>=3.1.0
requests>=2.31.0
beautifulsoup4>=4.12.0
python-dotenv>=1.0.0
nest-asyncio>=1.5.0
```

---

## 🎯 Elite AI Agents

### **Agent 1: Company Enrichment**
- **Persona:** 15+ years B2B research analyst
- **Output:** C-level executive summaries with market positioning

### **Agent 2: Industry Classification**
- **Frameworks:** GICS, NAICS standards
- **Output:** Precise industry categories (15+ predefined)

### **Agent 3: Lead Scoring**
- **Frameworks:** BANT, MEDDIC, CHAMP
- **Methodology:** Weighted evaluation across 4 dimensions
- **Output:** Decimal scores (e.g., 9.2/10) with reasoning

### **Agent 4: Email Generation**
- **Frameworks:** AIDA, PAS, BAB copywriting
- **Features:** Tone calibration by seniority
- **Output:** 125-175 word personalized emails

---

## 💡 Customization

### **For Your Product**

Edit `cell_2_lead_generation_pipeline.py` at line ~720:

```python
# Add your product context
Product: [YOUR PRODUCT]
Target Titles: [VP Sales, CTO, etc.]
Target Company Size: [100-1000 employees]
Target Industries: [SaaS, FinTech, etc.]
```

See [TWO_CELL_GUIDE.md](TWO_CELL_GUIDE.md) for detailed customization guide.

---

## 📈 Performance

| Metric | Value |
|--------|-------|
| Speed | 10-15 sec/lead |
| Cost | $0.02-0.05/lead |
| Model | GPT-4o-mini |
| Success Rate | >95% enrichment |
| Quality | Production-grade |

---

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| "No module named..." | Run Cell 1 first |
| "Invalid API key" | Check Secrets (Colab) or .env (Local) |
| "No file uploaded" | Upload CSV/Excel/JSON when prompted |
| "File not found" | Use full path: `/path/to/leads.csv` |

---

## 📚 Documentation

- **[TWO_CELL_GUIDE.md](TWO_CELL_GUIDE.md)** - Complete usage guide
- **[PROMPTS_DOCUMENTATION.md](PROMPTS_DOCUMENTATION.md)** - AI prompts explained
- **[GITHUB_DEPLOY.md](GITHUB_DEPLOY.md)** - Deployment instructions

---

## 🔒 Security

- ✅ Never commit `.env` files
- ✅ Use `.env.example` as template
- ✅ Keep API keys in Secrets (Colab) or `.env` (Local)
- ✅ `.gitignore` includes sensitive files

---

## 📊 Example Results

**Input:** 5 leads (name, company, website)

**Output after 2 minutes:**
- ✅ Company summaries for all 5
- ✅ Industry classifications
- ✅ Qualification scores (1-10)
- ✅ Personalized emails
- ✅ Exported JSON + CSV

**High-scoring lead (9.2/10):**
- VP-level at $50B+ company
- Perfect ICP match
- Personalized 150-word email
- 3 data-driven qualification reasons

---

## 🎓 Use Cases

- **Sales Teams:** Qualify inbound leads automatically
- **Marketing:** Enrich contact lists with intelligence
- **Business Development:** Prioritize outreach targets
- **Account-Based Marketing:** Research target accounts
- **Lead Generation Agencies:** Scale client deliverables

---

## ⭐ Key Features

- ✅ **Two-cell setup** - Simple dependency + pipeline
- ✅ **Elite AI prompts** - 650+ lines of expert instructions
- ✅ **Auto-detection** - Colab vs Local environments
- ✅ **File upload interface** - Interactive prompts
- ✅ **Multi-format support** - CSV, Excel, JSON
- ✅ **Production-ready** - Error handling, logging, validation
- ✅ **Cost-optimized** - GPT-4o-mini for efficiency
- ✅ **Zero external APIs** - Uses free DuckDuckGo search

---

## 🚀 Get Started

1. **Get OpenAI API Key:** https://platform.openai.com/api-keys
2. **Choose environment:** Colab (easiest) or Local Jupyter
3. **Run Cell 1:** Install dependencies
4. **Run Cell 2:** Upload file and process leads
5. **Download results:** enriched_leads.json + enriched_leads.csv

**Total time:** 2 minutes setup + 2 minutes per 10 leads

---

## 📞 Support

- **Issues:** Check [TWO_CELL_GUIDE.md](TWO_CELL_GUIDE.md) troubleshooting section
- **Customization:** See prompt customization guide in documentation
- **Questions:** Review [PROMPTS_DOCUMENTATION.md](PROMPTS_DOCUMENTATION.md)

---

## 📄 License

MIT License - Free for commercial and personal use

---

## 🎯 Quick Links

- [Complete Usage Guide →](TWO_CELL_GUIDE.md)
- [AI Prompts Explained →](PROMPTS_DOCUMENTATION.md)
- [Deploy to GitHub →](GITHUB_DEPLOY.md)
- [Example Output →](example_output.json)

---

**Built with:** LangGraph • OpenAI GPT-4 • Python • Pydantic  
**Version:** 2.0 (Two-Cell Architecture)  
**Status:** Production-Ready ✅

---

**⚡ Start enriching leads in 2 minutes!**
