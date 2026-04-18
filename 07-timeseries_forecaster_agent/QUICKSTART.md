# 🚀 Quick Start Guide

Get started with TimeSeriesForecaster Agent in 5 minutes!

---

## ⚡ Installation (2 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set OpenAI API Key
```bash
# Create .env file
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

---

## 🎯 Run Your First Forecast (3 minutes)

### Option 1: Use Sample Data (Recommended for Testing)

```bash
python timeseries_forecaster_agent.py
```

When prompted:
1. **File path**: Enter `sample_timeseries_data.csv`
2. **Forecast horizon**: Press Enter (uses default 30)

### Option 2: Use Your Own Data

```bash
python timeseries_forecaster_agent.py
```

When prompted:
1. **File path**: Enter your CSV/Excel file path
2. **Forecast horizon**: Enter number of periods (e.g., 60)

---

## 📊 What You'll Get

After ~1-2 minutes of processing:

### Files Created:
✅ **forecast_results.csv** - Your predictions  
✅ **forecast_report.txt** - Detailed analysis  
✅ **trained_model.pkl** - Saved model  
✅ **model_metadata.json** - Configuration  

### Visualizations:
📈 **forecast_plot.png** - Main forecast chart  
📊 **decomposition_plot.png** - Trend analysis  
📉 **residuals_plot.png** - Model diagnostics  

---

## 🎨 Example Output Preview

### Console Output:
```
================================================================================
TIME SERIES FORECASTER AGENT
================================================================================

STAGE 1: File Loading
✓ File loaded successfully: 1096 rows, 2 columns

STAGE 2: Column Identification
✓ Date column: date
✓ Value column: sales

STAGE 3: Data Validation
✓ Data validated: 1096 observations
✓ Frequency: D (Daily)

...

STAGE 14: Output Formatting
✓ Saved: forecast_results.csv
✓ Saved: forecast_report.txt
✓ Saved: trained_model.pkl
✓ Saved: model_metadata.json

✅ SUCCESS!
```

### Key Insights:
```
KEY FORECAST INSIGHTS:
1. Sales show strong upward trend (+15% annually)
2. Weekend sales 25% higher than weekdays
3. Q4 sales surge 40% due to holiday seasonality

TOP RECOMMENDATIONS:
1. Increase Q4 inventory by 35-40%
2. Add weekend staff during peak periods
3. Monitor forecast accuracy weekly
```

---

## 📁 Your Data Format

Minimum requirements:

```csv
date,value
2022-01-01,100
2022-01-02,105
2022-01-03,98
...
```

**Requirements:**
- At least 50 rows
- Date column (any standard format)
- Numeric value column
- Less than 50% missing values

---

## 🔥 Pro Tips

### 1. **Choosing Forecast Horizon**
- **Short-term (7-30 days)**: Higher accuracy, tactical planning
- **Medium-term (30-90 days)**: Strategic planning, budgeting
- **Long-term (90+ days)**: Trend analysis, capacity planning

### 2. **Data Quality Matters**
- ✅ More data = better forecasts (aim for 2+ years)
- ✅ Consistent frequency (daily, weekly, monthly)
- ✅ Minimal missing values
- ❌ Avoid large gaps in dates

### 3. **Interpreting Results**
- Check MAPE (Mean Absolute Percentage Error):
  - < 5% = Excellent
  - 5-10% = Good
  - 10-20% = Acceptable
  - > 20% = Poor (review data quality)

### 4. **Model Selection**
The agent auto-selects the best model:
- **ARIMA**: No seasonality, stationary data
- **SARIMA**: Strong seasonal patterns
- **Prophet**: Multiple seasonalities, holidays
- **Exponential Smoothing**: Simple trend/seasonality

---

## 🆘 Quick Troubleshooting

### Problem: "File not found"
**Solution**: Use full file path or place file in same directory
```bash
# Good examples:
sample_timeseries_data.csv
/Users/yourname/data/sales.csv
C:\Users\yourname\data\sales.xlsx
```

### Problem: "API key not found"
**Solution**: 
```bash
# Quick fix - set in terminal
export OPENAI_API_KEY=sk-your-key-here
```

### Problem: "Insufficient data"
**Solution**: Need at least 50 observations. Combine data or reduce granularity.

---

## 📈 Next Steps

After your first forecast:

1. **Review** `forecast_report.txt` for detailed analysis
2. **Examine** plots to understand patterns
3. **Validate** predictions against domain knowledge
4. **Iterate** with different horizons or data subsets
5. **Deploy** trained model for production use

---

## 🎓 Learning Path

**Beginner**: Use sample data, default settings  
**Intermediate**: Try your own data, adjust forecast horizon  
**Advanced**: Modify CONFIG, batch process files, integrate model into apps  

---

## 📞 Need Help?

1. Check `timeseries_forecaster.log` for errors
2. Review README.md for detailed documentation
3. Verify your data format matches requirements

---

**Ready to forecast? Run the command and let AI do the work! 🚀**

```bash
python timeseries_forecaster_agent.py
```
