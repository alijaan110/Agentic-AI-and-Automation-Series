# Google Colab Setup Guide for EDA Agent

"""
COMPLETE GOOGLE COLAB SETUP
Copy-paste these cells in order into Google Colab
"""

# ============================================================
# CELL 1: Installation (Run First, Then Restart Runtime)
# ============================================================
print("📦 Installing dependencies...")

# Uninstall conflicting packages
!pip uninstall -y openai httpx langchain langchain-openai langgraph langchain-core

# Install compatible versions
!pip install -U --force-reinstall \
  "httpx==0.27.2" \
  "openai>=1.55.3,<2" \
  "langchain==0.2.14" \
  "langchain-core==0.2.38" \
  "langchain-openai==0.1.22" \
  "langgraph==0.2.22" \
  "pandas>=2.0.0" \
  "numpy>=1.24.0" \
  "matplotlib>=3.7.0" \
  "openpyxl>=3.1.0" \
  "python-dotenv>=1.0.0"

print("\n✅ Installation complete!")
print("⚠️  IMPORTANT: Click 'Runtime' → 'Restart runtime' before continuing")


# ============================================================
# CELL 2: Verify Installation (After Restart)
# ============================================================
print("🔍 Verifying installation...")

import httpx
print(f"✓ httpx version: {httpx.__version__}")
assert httpx.__version__ == "0.27.2", "Wrong httpx version!"

import openai
print(f"✓ openai version: {openai.__version__}")

import langchain
print(f"✓ langchain version: {langchain.__version__}")

import langgraph
print(f"✓ langgraph version: {langgraph.__version__}")

import pandas as pd
print(f"✓ pandas version: {pd.__version__}")

print("\n✅ All dependencies verified!")


# ============================================================
# CELL 3: Setup OpenAI API Key
# ============================================================
"""
OPTION A: Use Colab Secrets (Recommended)
1. Click 🔑 icon in left sidebar
2. Click "+ Add new secret"
3. Name: OPENAI_API_KEY
4. Value: sk-your-key-here
5. Toggle "Notebook access" ON

OPTION B: Set directly (NOT recommended - visible in notebook)
"""

# Option B (if not using secrets):
# import os
# os.environ["OPENAI_API_KEY"] = "sk-your-key-here"

# Test if key is available
from google.colab import userdata

try:
    api_key = userdata.get("OPENAI_API_KEY")
    print("✅ OpenAI API key found in Colab Secrets")
except Exception as e:
    print("❌ OpenAI API key not found!")
    print("   → Add OPENAI_API_KEY to Colab Secrets (🔑 icon)")


# ============================================================
# CELL 4: Generate Sample Data (Optional)
# ============================================================
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("📊 Generating sample dataset...")

np.random.seed(42)
n_rows = 1000

# Generate dates
start_date = datetime(2023, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(n_rows)]

# Generate realistic data
data = {
    'transaction_date': dates,
    'age': np.random.normal(35, 12, n_rows).clip(18, 80).astype(int),
    'income': np.random.lognormal(10.5, 0.5, n_rows).astype(int),
    'transaction_amount': np.random.gamma(2, 50, n_rows).round(2),
    'credit_score': np.random.normal(700, 50, n_rows).clip(300, 850).astype(int),
    'customer_segment': np.random.choice(['Premium', 'Standard', 'Basic'], n_rows),
    'region': np.random.choice(['North', 'South', 'East', 'West'], n_rows),
    'is_premium_member': np.random.choice([True, False], n_rows, p=[0.3, 0.7]),
}

df = pd.DataFrame(data)

# Add missing values
missing_mask = np.random.random(n_rows) < 0.05
df.loc[missing_mask, 'transaction_amount'] = np.nan

# Save
df.to_csv('/content/sample_data.csv', index=False)
print(f"✅ Generated {len(df):,} rows → /content/sample_data.csv")


# ============================================================
# CELL 5: Upload Your Own Data (Alternative to Cell 4)
# ============================================================
from google.colab import files

print("📁 Upload your CSV/Excel/JSON file...")
uploaded = files.upload()

# Get the uploaded filename
filename = list(uploaded.keys())[0]
print(f"✅ Uploaded: {filename}")
print(f"   Saved to: /content/{filename}")


# ============================================================
# CELL 6: Configure EDA Agent
# ============================================================
# ⚙️ CONFIGURATION - Edit these settings

NOTEBOOK_MODE = True
DISPLAY_CHARTS_IN_NOTEBOOK = True
INPUT_PATH = "/content/sample_data.csv"  # Change if you uploaded different file
OUTPUT_DIR = "/content/output"  # Main output directory
OUTPUT_PATH = "/content/output/eda_report.json"  # Report location
CHARTS_SUBDIR = "charts"  # Subdirectory for charts

print("⚙️ Configuration:")
print(f"   Input: {INPUT_PATH}")
print(f"   Output directory: {OUTPUT_DIR}")
print(f"   Report: {OUTPUT_PATH}")
print(f"   Charts: {OUTPUT_DIR}/{CHARTS_SUBDIR}")
print(f"   Display charts: {DISPLAY_CHARTS_IN_NOTEBOOK}")


# ============================================================
# CELL 7: Paste the Full EDA Agent Code Here
# ============================================================
# Copy the entire eda_agent_production.py content here
# (from "from __future__ import annotations" to the end)

# NOTE: Make sure the configuration section uses the variables from Cell 6:
# NOTEBOOK_MODE = True  # from Cell 6
# DISPLAY_CHARTS_IN_NOTEBOOK = True  # from Cell 6
# INPUT_PATH = "/content/sample_data.csv"  # from Cell 6
# OUTPUT_DIR = "/content/output"  # from Cell 6
# OUTPUT_PATH = "/content/output/eda_report.json"  # from Cell 6
# CHARTS_SUBDIR = "charts"  # from Cell 6


# ============================================================
# CELL 8: View Results
# ============================================================
import json

# Load the report
with open(OUTPUT_PATH, 'r') as f:
    report = json.load(f)

# Display key insights
print("=" * 60)
print("📊 EDA REPORT SUMMARY")
print("=" * 60)

metadata = report['metadata']
print(f"\n📈 Dataset: {metadata['rows']:,} rows × {metadata['columns']} columns")
print(f"⏰ Generated: {metadata['generated_at']}")

print("\n🔍 Key Patterns:")
for i, pattern in enumerate(report['insights']['key_patterns'][:5], 1):
    print(f"   {i}. {pattern}")

print("\n⚠️  Anomalies:")
for i, anomaly in enumerate(report['insights']['anomalies'][:5], 1):
    print(f"   {i}. {anomaly}")

print("\n💡 Business Insights:")
for i, insight in enumerate(report['insights']['business_insights'][:5], 1):
    print(f"   {i}. {insight}")

print("\n📋 Recommended Next Steps:")
for i, step in enumerate(report['insights']['recommended_next_steps'][:5], 1):
    print(f"   {i}. {step}")

# Display data quality metrics
dq = report['data_quality']
print(f"\n📊 Data Quality:")
print(f"   Missing cells: {dq['missing_values']['total_missing_cells']:,}")
print(f"   Duplicate rows: {dq['duplicates']['duplicate_rows']:,}")

# Show chart count
charts = report['visual_analysis']['charts']
print(f"\n📈 Generated {len(charts)} visualizations")


# ============================================================
# CELL 9: Download Results
# ============================================================
from google.colab import files

# Download the JSON report
files.download(OUTPUT_PATH)

# Optional: Download charts as ZIP
import shutil
import os

chart_dir = report['visual_analysis']['chart_storage']['directory']
if os.path.exists(chart_dir):
    # Create ZIP of all charts
    shutil.make_archive('/content/eda_charts', 'zip', chart_dir)
    files.download('/content/eda_charts.zip')
    print("✅ Downloaded charts.zip")


# ============================================================
# TROUBLESHOOTING
# ============================================================
"""
Common Issues:

1. "unexpected keyword argument 'proxies'" 
   → Restart runtime after installation (Cell 1)
   → Verify httpx==0.27.2 (Cell 2)

2. "OPENAI_API_KEY is missing"
   → Add key to Colab Secrets (🔑 icon)
   → Enable notebook access

3. Charts not displaying
   → Set DISPLAY_CHARTS_IN_NOTEBOOK = True
   → Ensure matplotlib backend is working

4. Memory error
   → Use smaller dataset
   → Increase MAX_ROWS_FOR_CORRELATION in agent code

5. DeprecationWarning
   → Safe to ignore (code uses modern methods)
   → Or update to production version above
"""

# ============================================================
# QUICK TEST
# ============================================================
# Run this to verify everything works before full execution

def quick_test():
    """Quick test to verify setup"""
    import pandas as pd
    from langchain_openai import ChatOpenAI
    
    # Test pandas
    df = pd.DataFrame({'a': [1, 2, 3]})
    assert len(df) == 3, "Pandas not working"
    print("✓ Pandas OK")
    
    # Test OpenAI connection
    try:
        llm = ChatOpenAI(model="gpt-4o-mini", max_tokens=10)
        response = llm.invoke("Say 'OK'")
        print(f"✓ OpenAI OK: {response.content}")
    except Exception as e:
        print(f"✗ OpenAI Error: {e}")
        return False
    
    print("\n✅ All systems ready!")
    return True

# Uncomment to run test:
# quick_test()
