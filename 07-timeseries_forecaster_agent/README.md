# TimeSeriesForecaster Agent

**Production-Grade Time Series Forecasting with LangGraph & AI**

An intelligent, autonomous agent that automatically analyzes time-series data, detects patterns, builds optimal forecasting models, and generates actionable business insights using LangGraph orchestration and OpenAI LLMs.

---

## 🌟 Features

### Automated Analysis
- **Smart Column Detection**: AI-powered identification of date and value columns
- **Pattern Recognition**: Automatic detection of trends, seasonality, and anomalies
- **Stationarity Testing**: ADF and KPSS tests for series characteristics
- **Time Series Decomposition**: Trend, seasonal, and residual component extraction

### Multiple Forecasting Models
- **ARIMA**: Auto-regressive integrated moving average
- **SARIMA**: Seasonal ARIMA for periodic patterns
- **Prophet**: Facebook's robust forecasting framework
- **Exponential Smoothing**: Holt-Winters method for trend and seasonality

### AI-Powered Insights
- **Model Recommendation**: LLM analyzes data characteristics to suggest optimal models
- **Business Insights**: Natural language explanations of patterns and forecasts
- **Strategic Recommendations**: Actionable advice based on forecast results

### Production Features
- **Multi-Format Support**: CSV, Excel, JSON file inputs
- **Error Handling**: Comprehensive validation and retry logic
- **Visualization**: Professional plots with confidence intervals
- **Dual Environment**: Works in Google Colab and local setups
- **File Selection**: GUI dialog or manual path input

---

## 📋 Requirements

### Python Version
- Python 3.9 or higher

### Dependencies
See `requirements.txt` for full list. Key packages:
- `langgraph>=0.2.45` - Workflow orchestration
- `openai>=1.54.5` - AI model integration
- `pandas>=2.1.4` - Data manipulation
- `statsmodels>=0.14.1` - Statistical models
- `prophet>=1.1.5` - Facebook Prophet
- `matplotlib>=3.8.2` - Visualization
- `scikit-learn>=1.4.0` - Metrics and utilities

---

## 🚀 Installation

### Local Setup

1. **Clone or download the project files**
```bash
# Create project directory
mkdir timeseries_forecaster
cd timeseries_forecaster

# Place the three files here:
# - timeseries_forecaster_agent.py
# - requirements.txt
# - sample_timeseries_data.csv
```


### Google Colab Setup

1. **Upload files to Colab**
```python
from google.colab import files
uploaded = files.upload()  # Upload the .py file
```

2. **Install dependencies**
```python
!pip install.... cell 1
```

3. **Set API key in Colab Secrets**
- Click the key icon (🔑) in the left sidebar
- Add secret: `OPENAI_API_KEY` = `your_api_key_here`

---

## 💻 Usage

### Basic Usage

1. **Run the agent**
```bash
python timeseries_forecaster_agent.py
```

2. **Select your data file**
   - A file dialog will open (if available)
   - Or enter the file path manually
   - Supported formats: `.csv`, `.xlsx`, `.xls`, `.json`

3. **Enter forecast horizon**
   - Specify how many periods to forecast (e.g., 30 days)
   - Press Enter to use default (30)

4. **Wait for analysis**
   - The agent will process through 14 stages
   - Progress is logged to console and `timeseries_forecaster.log`

5. **Review outputs**
   - Check generated files and visualizations
   - Read insights in `forecast_report.txt`

### Example Session

```bash
$ python timeseries_forecaster_agent.py

================================================================================
TIME SERIES FORECASTER AGENT
Powered by LangGraph & OpenAI
================================================================================

================================================================================
FILE SELECTION
================================================================================

Enter the path to your time-series data file: sample_timeseries_data.csv

--------------------------------------------------------------------------------
Enter forecast horizon (days/periods) [default: 30]: 60

================================================================================
STARTING ANALYSIS PIPELINE
================================================================================

[Processing stages 1-14...]

================================================================================
ANALYSIS COMPLETE
================================================================================

✅ SUCCESS!

Generated Files:
  1. forecast_results.csv - Forecast values with confidence intervals
  2. forecast_report.txt - Comprehensive analysis report
  3. trained_model.pkl - Trained forecasting model
  4. model_metadata.json - Model configuration and metadata

Generated Plots:
  - forecast_plot.png
  - decomposition_plot.png
  - residuals_plot.png

--------------------------------------------------------------------------------
KEY FORECAST INSIGHTS:
--------------------------------------------------------------------------------
1. The forecast indicates continued upward trend with seasonal variations
2. Q4 2025 is projected to show 35% increase compared to Q1 2025
3. Weekly patterns suggest higher sales on weekends consistently

--------------------------------------------------------------------------------
TOP RECOMMENDATIONS:
--------------------------------------------------------------------------------
1. Increase inventory 2 weeks before Q4 to meet projected demand surge
2. Optimize weekend staffing based on predicted 25% higher traffic
3. Monitor actual vs forecast weekly to detect early deviations
```

---

## 📊 Input Data Format

### Required Columns
Your time-series data must contain:
1. **Date/Time column**: Dates or timestamps
2. **Value column**: Numeric values to forecast

### Supported Formats

**CSV Example:**
```csv
date,sales
2022-01-01,1000
2022-01-02,1050
2022-01-03,980
...
```

**Excel Example:**
| date       | revenue |
|------------|---------|
| 2022-01-01 | 1000.00 |
| 2022-01-02 | 1050.50 |
| 2022-01-03 | 980.25  |

**JSON Example:**
```json
[
  {"date": "2022-01-01", "value": 1000},
  {"date": "2022-01-02", "value": 1050},
  {"date": "2022-01-03", "value": 980}
]
```

### Data Requirements
- **Minimum observations**: 50 data points
- **Maximum missing values**: 50% of total observations
- **Date formats**: Any standard format (YYYY-MM-DD, MM/DD/YYYY, etc.)
- **Frequency**: Daily, weekly, or monthly (auto-detected)

---

## 📁 Output Files

### 1. forecast_results.csv
Contains forecast values with confidence intervals:
```csv
date,forecast,lower_95,upper_95
2025-01-01,1500.50,1350.25,1650.75
2025-01-02,1520.30,1365.40,1675.20
...
```

### 2. forecast_report.txt
Comprehensive text report including:
- Data summary and statistics
- Pattern analysis (trend, seasonality)
- Model information and parameters
- Validation metrics (MAE, RMSE, MAPE)
- Forecast summary
- AI-generated insights and recommendations

### 3. trained_model.pkl
Serialized trained model for:
- Future predictions
- Model inspection
- Retraining with new data

### 4. model_metadata.json
Model configuration and metadata:
```json
{
  "model_type": "SARIMA",
  "parameters": {
    "order": [1, 1, 1],
    "seasonal_order": [0, 1, 0, 7]
  },
  "training_date": "2024-01-15T10:30:00",
  "validation_metrics": {
    "mae": 45.23,
    "rmse": 62.18,
    "mape": 3.45
  }
}
```

### 5. Visualizations

**forecast_plot.png**
- Historical data
- Forecast line
- 95% confidence intervals

**decomposition_plot.png**
- Original series
- Trend component
- Seasonal component
- Residual component

**residuals_plot.png**
- Residuals over time
- Residuals distribution

---

## 🎯 Use Cases

### Business Applications
- **Sales Forecasting**: Predict future sales for inventory planning
- **Demand Forecasting**: Anticipate product/service demand
- **Revenue Projection**: Financial planning and budgeting
- **Traffic Prediction**: Website/store traffic forecasting
- **Capacity Planning**: Resource allocation optimization

### Industry Examples
- **E-commerce**: Daily sales and order volume prediction
- **Retail**: Seasonal demand and inventory optimization
- **Finance**: Stock price trends and volatility analysis
- **Healthcare**: Patient admission and resource forecasting
- **Energy**: Power consumption and load prediction
- **Transportation**: Ridership and logistics forecasting

---

## 🔧 Configuration

Edit `CONFIG` dictionary in `timeseries_forecaster_agent.py`:

```python
CONFIG = {
    'min_observations': 50,          # Minimum data points required
    'max_missing_pct': 0.5,          # Max 50% missing values allowed
    'train_test_split': 0.8,         # 80% train, 20% test
    'max_model_retries': 3,          # Retry attempts for model training
    'confidence_levels': [80, 95],   # Confidence interval levels
    'default_horizon': 30,           # Default forecast periods
    'openai_model': 'gpt-4o-mini',   # OpenAI model to use
    'temperature': 0.7,              # LLM temperature (0-1)
    'max_tokens': 2000,              # Max tokens per LLM call
    'figure_size': (14, 8),          # Plot dimensions
    'dpi': 100                       # Plot resolution
}
```

---

## 🐛 Troubleshooting

### Common Issues

**1. ImportError: No module named 'X'**
```bash
# Solution: Install missing package
pip install -r requirements.txt
```

**2. API Key Error**
```
EnvironmentError: OPENAI_API_KEY not found
```
```bash
# Solution: Set your API key
export OPENAI_API_KEY=your_key_here  # macOS/Linux
set OPENAI_API_KEY=your_key_here     # Windows
```

**3. File Dialog Not Working**
```
File dialog not available
```
```bash
# Solution: Install tkinter
# Ubuntu/Debian:
sudo apt-get install python3-tk

# Or use manual file path input (fallback)
```

**4. Data Validation Error**
```
DataValidationError: Insufficient data: X rows (minimum 50 required)
```
**Solution**: Ensure your dataset has at least 50 observations

**5. Model Training Failed**
```
ModelTrainingError: Failed to train SARIMA
```
**Solution**: The agent automatically retries with ARIMA. If persists, check data quality

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check `timeseries_forecaster.log` for detailed execution logs.

---

## 🧪 Sample Data

Use the provided `sample_timeseries_data.csv` for testing:
- **Duration**: 3 years (2022-2024)
- **Frequency**: Daily
- **Observations**: 1096 rows
- **Features**:
  - Base sales: ~1000/day
  - Yearly growth: +15%
  - Weekly seasonality (weekend boost)
  - Yearly seasonality (Q4 spike)
  - Realistic noise and anomalies
  - ~2.5% missing values

---

## 📚 Advanced Usage

### Using Trained Model for New Predictions

```python
import pickle
import pandas as pd

# Load trained model
with open('trained_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Generate new forecast
new_forecast = model.forecast(steps=90)  # 90-day forecast
print(new_forecast)
```

### Batch Processing Multiple Files

```python
import glob
from timeseries_forecaster_agent import create_forecaster_graph

files = glob.glob('data/*.csv')
graph = create_forecaster_graph()

for filepath in files:
    state = TimeSeriesState(
        filepath=filepath,
        forecast_horizon=30,
        # ... other parameters
    )
    result = graph.invoke(state)
    print(f"Processed: {filepath}")
```

---

## 🤝 Contributing

### Extending the Agent

**Add New Model:**
1. Update `train_forecasting_model()` function
2. Add model-specific logic to `generate_forecast()`
3. Update model recommendation prompts

**Add New Metrics:**
1. Extend `model_evaluation_node()`
2. Update validation metrics dictionary
3. Include in report generation

**Custom Visualizations:**
1. Add plotting code to `visualization_node()`
2. Save to `state['plots']` dictionary
3. Reference in output formatter

---

## 📝 License

This project is provided as-is for educational and commercial use.

---

## 🙏 Acknowledgments

Built with:
- **LangGraph** - Workflow orchestration
- **OpenAI** - Large language models
- **Statsmodels** - Statistical analysis
- **Prophet** - Facebook's forecasting framework
- **Pandas & NumPy** - Data manipulation
- **Matplotlib & Seaborn** - Visualization

---

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review `timeseries_forecaster.log`
3. Examine error messages in console output

---

## 🗺️ Roadmap

Potential future enhancements:
- [ ] Support for multivariate time series
- [ ] Neural network models (LSTM, Transformer)
- [ ] Real-time streaming data support
- [ ] Interactive dashboard
- [ ] Automated hyperparameter tuning
- [ ] Model ensemble capabilities
- [ ] Custom holiday/event handling
- [ ] API deployment guide

---

**Happy Forecasting! 📈**
