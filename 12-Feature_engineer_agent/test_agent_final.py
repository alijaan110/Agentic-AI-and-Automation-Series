"""
FOOLPROOF Test Script for Feature Engineer Agent (AgentGrid Format)
This script handles ALL dependency conflicts properly.

USAGE:
1. Upload feature_engineer_agent_agentgrid.py to Colab
2. Add OPENAI_API_KEY to Colab Secrets (🔑 icon)
3. Run this script
4. When prompted, RESTART RUNTIME
5. Run this script again
"""

import sys
import os

# ============================================================================
# CHECK IF THIS IS FIRST RUN OR AFTER RESTART
# ============================================================================

# Create a flag file to detect if we need to restart
FLAG_FILE = '/tmp/feature_engineer_setup_complete.flag'

if not os.path.exists(FLAG_FILE):
    # FIRST RUN - Install dependencies
    print("=" * 80)
    print("FIRST RUN - INSTALLING DEPENDENCIES")
    print("=" * 80)
    print("\nThis will install all required packages...")
    print("You will need to RESTART RUNTIME after this completes.\n")
    
    # Comprehensive cleanup
    print("Step 1/4: Cleaning up conflicting packages...")
    import subprocess
    subprocess.run([
        'pip', 'uninstall', '-y', '-q',
        'langchain', 'langchain-openai', 'langgraph', 'langchain-core',
        'langchain-community', 'langsmith', 'langgraph-checkpoint', 'langgraph-prebuilt'
    ], stderr=subprocess.DEVNULL)
    
    # Install compatible numpy/pandas first (Colab compatible versions)
    print("Step 2/4: Installing compatible numpy and pandas...")
    subprocess.run(['pip', 'install', '-q', 'numpy==1.26.4', 'pandas==2.2.2'], check=True)
    
    # Install langchain packages with no-deps
    print("Step 3/4: Installing LangChain packages...")
    subprocess.run(['pip', 'install', '-q', '--no-deps', 'langchain-core==0.1.10'], check=True)
    subprocess.run(['pip', 'install', '-q', '--no-deps', 'langchain==0.1.0'], check=True)
    subprocess.run(['pip', 'install', '-q', '--no-deps', 'langchain-openai==0.0.2'], check=True)
    subprocess.run(['pip', 'install', '-q', '--no-deps', 'langgraph==0.0.20'], check=True)
    
    # Install remaining dependencies
    print("Step 4/4: Installing other dependencies...")
    subprocess.run(['pip', 'install', '-q', 'scipy', 'scikit-learn', 'openpyxl'], check=True)
    subprocess.run(['pip', 'install', '-q', 'pydantic', 'requests', 'aiohttp', 'tiktoken'], check=True)
    subprocess.run(['pip', 'install', '-q', 'langsmith==0.0.87', 'langchain-community==0.0.13'], check=True)
    
    # Create flag file
    with open(FLAG_FILE, 'w') as f:
        f.write('setup_complete')
    
    print("\n" + "=" * 80)
    print("✓ INSTALLATION COMPLETE!")
    print("=" * 80)
    print("\n🔄 NEXT STEP - MANDATORY:")
    print("   1. Go to: Runtime → Restart runtime")
    print("   2. After restart, run this script again")
    print("   3. Do NOT skip the restart - it's required for numpy!")
    print("\n" + "=" * 80)
    
    sys.exit(0)

else:
    # AFTER RESTART - Run the actual tests
    print("=" * 80)
    print("SETUP VERIFIED - RUNNING TESTS")
    print("=" * 80 + "\n")

# ============================================================================
# IMPORT LIBRARIES (After restart)
# ============================================================================
print("Loading libraries...")

import base64
import json
import pandas as pd
import numpy as np
from io import BytesIO, StringIO
from google.colab import userdata

print("✓ Libraries imported successfully\n")

# ============================================================================
# MOCK AGENTGRID COMPONENTS
# ============================================================================
print("Setting up mock AgentGrid environment...")

# Mock BaseAgent
class AgentInput:
    def __init__(self, name, type, description):
        self.name = name
        self.type = type
        self.description = description

class AgentOutput:
    def __init__(self, name, type, description):
        self.name = name
        self.type = type
        self.description = description

class BaseAgent:
    pass

# Mock registry
AGENT_REGISTRY = {}

def register_agent(agent_id):
    def decorator(cls):
        AGENT_REGISTRY[agent_id] = cls
        return cls
    return decorator

# Create mock app.agents module
from types import ModuleType

app = ModuleType('app')
agents = ModuleType('agents')
base = ModuleType('base')
registry = ModuleType('registry')

base.BaseAgent = BaseAgent
base.AgentInput = AgentInput
base.AgentOutput = AgentOutput
registry.register_agent = register_agent

agents.base = base
agents.registry = registry
app.agents = agents

sys.modules['app'] = app
sys.modules['app.agents'] = agents
sys.modules['app.agents.base'] = base
sys.modules['app.agents.registry'] = registry

print("✓ Mock AgentGrid environment created\n")

# ============================================================================
# LOAD THE AGENT
# ============================================================================
print("Loading Feature Engineer Agent...")

try:
    from feature_engineer_agent_agentgrid import FeatureEngineerAgent
    print("✓ Agent loaded successfully\n")
except ImportError as e:
    print(f"\n❌ ERROR: Could not import agent!")
    print(f"Error: {e}")
    print("\n⚠️  Make sure 'feature_engineer_agent_agentgrid.py' is uploaded to Colab!")
    sys.exit(1)

# ============================================================================
# CREATE TEST DATA
# ============================================================================
print("Creating test dataset...")

test_data = pd.DataFrame({
    'age': [25, 30, 35, 40, 45, 28, 33, 38, 42, 29],
    'income': [50000, 60000, 75000, 90000, 85000, 55000, 65000, 80000, 95000, 58000],
    'city': ['NYC', 'LA', 'NYC', 'SF', 'LA', 'NYC', 'SF', 'LA', 'NYC', 'SF'],
    'purchase_date': pd.date_range('2024-01-01', periods=10, freq='D'),
    'sales': [100, 150, 200, 250, 220, 120, 160, 210, 240, 130]
})

print("Test Data Preview:")
print(test_data.head())
print(f"\nShape: {test_data.shape}")
print(f"Columns: {list(test_data.columns)}\n")

# ============================================================================
# ENCODING FUNCTIONS
# ============================================================================

def encode_dataframe_csv(df):
    """Encode DataFrame to base64 CSV"""
    csv_content = df.to_csv(index=False)
    encoded = base64.b64encode(csv_content.encode()).decode()
    return encoded

def encode_dataframe_excel(df):
    """Encode DataFrame to base64 Excel"""
    buffer = BytesIO()
    df.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)
    encoded = base64.b64encode(buffer.read()).decode()
    return encoded

def encode_dataframe_json(df):
    """Encode DataFrame to base64 JSON"""
    json_content = df.to_json(orient='records', indent=2)
    encoded = base64.b64encode(json_content.encode()).decode()
    return encoded

# ============================================================================
# GET API KEY
# ============================================================================
print("=" * 80)
print("API KEY SETUP")
print("=" * 80)

try:
    openai_api_key = userdata.get('OPENAI_API_KEY')
    print("✓ Using API key from Colab Secrets\n")
except:
    from getpass import getpass
    openai_api_key = getpass("Enter your OpenAI API Key: ")
    print("✓ API key entered manually\n")

# ============================================================================
# TEST FUNCTION
# ============================================================================

def test_csv_format():
    """Test agent with CSV format"""
    print("=" * 80)
    print("TEST: CSV FORMAT")
    print("=" * 80)
    
    encoded_csv = encode_dataframe_csv(test_data)
    
    inputs = {
        "file_content": encoded_csv,
        "file_format": "csv",
        "target_variable": "sales",
        "max_features": 30,
        "openai_api_key": openai_api_key
    }
    
    print("Running agent... (this may take 30-60 seconds)")
    agent = FeatureEngineerAgent()
    result = agent.run(inputs)
    
    print(f"\n✓ Status: {result['status']}")
    print(f"✓ Message: {result['message']}\n")
    
    if result['status'] == 'success':
        enhanced_csv = base64.b64decode(result['enhanced_data']).decode()
        enhanced_df = pd.read_csv(StringIO(enhanced_csv))
        
        print(f"✅ Original columns: {len(test_data.columns)}")
        print(f"✅ Enhanced columns: {len(enhanced_df.columns)}")
        print(f"✅ New features: {len(enhanced_df.columns) - len(test_data.columns)}")
        
        print("\n📊 Enhanced columns:")
        for i, col in enumerate(enhanced_df.columns, 1):
            print(f"  {i:2d}. {col}")
        
        print("\n📋 Feature Report Summary:")
        summary = result['feature_report']['feature_engineering_summary']
        print(f"  • Total features generated: {summary['total_features_generated']}")
        print(f"  • Features selected: {summary['total_features_selected']}")
        print(f"  • Summary: {summary['summary']}")
        print(f"  • Recommendations: {summary['recommendations']}")
        
        return True
    else:
        print(f"❌ Test failed: {result['message']}")
        return False

# ============================================================================
# RUN TEST
# ============================================================================

print("\n" + "=" * 80)
print("STARTING AGENT TEST")
print("=" * 80 + "\n")

try:
    success = test_csv_format()
    
    print("\n" + "=" * 80)
    if success:
        print("🎉 TEST PASSED! Agent is working correctly!")
    else:
        print("❌ TEST FAILED! Check errors above.")
    print("=" * 80)
    
except Exception as e:
    print("\n" + "=" * 80)
    print("❌ TEST FAILED WITH EXCEPTION")
    print("=" * 80)
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Clean up flag for next run
if os.path.exists(FLAG_FILE):
    os.remove(FLAG_FILE)

print("\n✓ Test complete!")
