# TimeSeriesForecaster Agent - Architecture & Structure

## 📐 Project Structure

```
timeseries_forecaster/
├── timeseries_forecaster_agent.py  # Main agent (62KB)
├── requirements.txt                 # Python dependencies
├── sample_timeseries_data.csv       # Sample dataset (1096 rows)
├── test_agent.py                    # Validation test suite
├── README.md                        # Complete documentation
├── QUICKSTART.md                    # Quick start guide
├── .env                            # API key (create this)
└── outputs/                        # Generated outputs
    ├── forecast_results.csv        # Forecast values
    ├── forecast_report.txt         # Analysis report
    ├── trained_model.pkl           # Saved model
    ├── model_metadata.json         # Model config
    ├── forecast_plot.png           # Main forecast chart
    ├── decomposition_plot.png      # Pattern analysis
    ├── residuals_plot.png          # Model diagnostics
    └── timeseries_forecaster.log   # Execution logs
```

---

## 🏗️ Architecture Overview

### LangGraph Workflow (14 Nodes)

```
┌─────────────────────────────────────────────────────────────────┐
│                    TimeSeriesForecaster Agent                    │
│                    LangGraph State Machine                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  File Loader     │ ◄── User selects file
                    │  Node 1          │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Column ID       │ ◄── LLM identifies columns
                    │  Node 2 (LLM)    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Data Validator  │ ◄── Validation & cleaning
                    │  Node 3          │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Exploratory     │ ◄── Trend, seasonality
                    │  Analysis        │     detection
                    │  Node 4          │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Stationarity    │ ◄── ADF/KPSS tests
                    │  Test Node 5     │     Decomposition
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Model Rec.      │ ◄── LLM recommends models
                    │  Node 6 (LLM)    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Model Selection │ ◄── Parameter optimization
                    │  Node 7          │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Data Splitting  │ ◄── Train/test split
                    │  Node 8          │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Model Training  │ ◄── Fit forecasting model
                    │  Node 9          │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Model Eval.     │ ◄── Calculate metrics
                    │  Node 10         │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Forecasting     │ ◄── Generate predictions
                    │  Node 11         │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Insights Gen.   │ ◄── LLM creates insights
                    │  Node 12 (LLM)   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Visualization   │ ◄── Create plots
                    │  Node 13         │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Output Format   │ ◄── Save all outputs
                    │  Node 14         │
                    └────────┬─────────┘
                             │
                             ▼
                          [END]
```

---

## 🧩 Component Architecture

### 1. State Management

**TimeSeriesState** (TypedDict with 30 fields):
```python
{
    # Input
    raw_data, filepath, date_column, value_column,
    forecast_horizon, frequency,
    
    # Analysis
    data_profile, trend_analysis, seasonality_analysis,
    stationarity_test, decomposition,
    
    # Modeling
    recommended_models, selected_model_type, model_parameters,
    train_data, test_data, trained_model,
    
    # Evaluation
    validation_metrics, residual_analysis,
    
    # Forecasting
    forecast_values, confidence_intervals, forecast_dates,
    
    # Insights
    pattern_insights, forecast_insights, recommendations,
    
    # Output
    plots, processing_stage, errors, warnings, retry_count
}
```

### 2. LLM Integration Points

**Three Strategic LLM Calls:**

1. **Column Identification** (Node 2)
   - Input: Column metadata, sample values
   - Output: Date and value column names
   - Handles various naming conventions automatically

2. **Model Recommendation** (Node 6)
   - Input: Data characteristics, pattern analysis
   - Output: Ranked model recommendations
   - Selects optimal forecasting approach

3. **Insights Generation** (Node 12)
   - Input: Analysis results, forecast summary
   - Output: Business insights and recommendations
   - Translates technical results to actionable advice

### 3. Forecasting Models

**Model Selection Logic:**
```
Has Seasonality?
    ├─ Yes → SARIMA (seasonal ARIMA)
    └─ No → Is Stationary?
            ├─ Yes → ExponentialSmoothing
            └─ No → ARIMA
            
Fallback: Prophet (handles all patterns)
```

**Model Implementations:**
- **ARIMA(p,d,q)**: Auto-regressive integrated moving average
- **SARIMA(p,d,q)(P,D,Q,s)**: Seasonal ARIMA
- **Prophet**: Additive model with trend + seasonality
- **Exponential Smoothing**: Holt-Winters method

---

## 🔄 Data Flow

### Input Processing
```
User File → Load → Parse → Validate → Clean
                                        │
                                        ▼
                                   Time Series
                                        │
                                        ▼
                          Exploratory Analysis
                                        │
                                        ▼
                              Pattern Detection
                                        │
                                        ▼
                              Model Selection
```

### Model Training
```
Clean Data → Split (80/20) → Train Model → Validate
                                              │
                                              ▼
                                         Calculate:
                                         - MAE
                                         - RMSE
                                         - MAPE
```

### Forecasting
```
Trained Model → Generate Forecast → Confidence Intervals
                                             │
                                             ▼
                                    Future Predictions
```

### Output Generation
```
Results → Format → Save Files + Plots → Report
```

---

## 🎯 Design Patterns

### 1. State Pattern
- LangGraph manages workflow state
- Each node transforms state immutably
- Clear progression through pipeline

### 2. Strategy Pattern
- Multiple forecasting algorithms
- Selected dynamically based on data
- Consistent interface across models

### 3. Observer Pattern
- Comprehensive logging throughout
- Error tracking and warnings
- Progress monitoring

### 4. Template Method
- Standardized node structure
- Consistent error handling
- Uniform state updates

---

## 🔐 Error Handling Strategy

### Three-Level Error Handling:

**Level 1: Custom Exceptions**
```python
TimeSeriesError          # Base exception
├─ DataValidationError   # Data issues
└─ ModelTrainingError    # Training failures
```

**Level 2: Retry Logic**
- Max 3 retries for model training
- Fallback to simpler models
- Graceful degradation

**Level 3: State Tracking**
- Errors array in state
- Warnings array for non-critical issues
- Processing stage tracking

---

## 📊 Performance Characteristics

### Memory Usage
- Small datasets (<1MB): ~100MB RAM
- Medium datasets (1-10MB): ~200-500MB RAM
- Large datasets (>10MB): ~500MB-1GB RAM

### Processing Time
- File loading: <1 second
- Analysis: 2-5 seconds
- Model training: 5-30 seconds (varies by model)
- Forecasting: <1 second
- Visualization: 2-5 seconds
- **Total**: ~15-45 seconds for typical dataset

### Scalability
- **Data points**: Handles 50 to 100,000+ observations
- **Forecast horizon**: 1 to 365+ periods
- **Memory**: O(n) where n = data points
- **Time**: O(n log n) for most operations

---

## 🔧 Configuration System

### CONFIG Dictionary
```python
{
    'min_observations': 50,       # Minimum data validation
    'max_missing_pct': 0.5,       # Maximum missing values
    'train_test_split': 0.8,      # 80/20 split
    'max_model_retries': 3,       # Retry attempts
    'confidence_levels': [80, 95], # CI percentiles
    'default_horizon': 30,        # Default forecast
    'openai_model': 'gpt-4o-mini', # LLM model
    'temperature': 0.7,           # LLM creativity
    'max_tokens': 2000,           # LLM response size
    'figure_size': (14, 8),       # Plot dimensions
    'dpi': 100                    # Plot resolution
}
```

### Environment Variables
```bash
OPENAI_API_KEY=sk-...          # Required
LOG_LEVEL=INFO                 # Optional
PLOT_STYLE=seaborn-darkgrid   # Optional
```

---

## 📈 Metrics & Validation

### Model Evaluation Metrics

**MAE (Mean Absolute Error)**
```
MAE = (1/n) Σ |actual - predicted|
Lower is better, same units as data
```

**RMSE (Root Mean Squared Error)**
```
RMSE = √[(1/n) Σ (actual - predicted)²]
Penalizes large errors more
```

**MAPE (Mean Absolute Percentage Error)**
```
MAPE = (1/n) Σ |(actual - predicted)/actual| × 100
Percentage-based, scale-independent
```

### Quality Thresholds
- **Excellent**: MAPE < 5%
- **Good**: MAPE 5-10%
- **Acceptable**: MAPE 10-20%
- **Poor**: MAPE > 20%

---

## 🎨 Visualization System

### Plot Types

**1. Forecast Plot**
- Historical data (blue line)
- Forecast (red dashed line)
- 95% confidence interval (shaded)
- Grid and labels

**2. Decomposition Plot**
- Original series
- Trend component
- Seasonal component
- Residual component

**3. Residuals Plot**
- Residuals over time
- Residuals distribution (histogram)
- Zero reference line

### Styling
- Seaborn darkgrid theme
- Professional color palette
- High DPI for clarity
- Consistent sizing

---

## 🔄 Extensibility Points

### Adding New Models
```python
# 1. Add to train_forecasting_model()
elif model_type == 'NewModel':
    model = NewModel(**parameters)
    fitted_model = model.fit(train_clean)

# 2. Add to generate_forecast()
elif model_type == 'NewModel':
    forecast = model.predict(horizon)
```

### Adding New Metrics
```python
# In model_evaluation_node()
new_metric = calculate_new_metric(test_data, predictions)
state['validation_metrics']['new_metric'] = new_metric
```

### Custom Visualizations
```python
# In visualization_node()
fig, ax = plt.subplots()
# ... plotting code ...
plt.savefig('custom_plot.png')
plots['custom'] = 'custom_plot.png'
```

---

## 🧪 Testing Strategy

### Test Coverage

**Unit Tests** (test_agent.py):
- ✅ Package installation
- ✅ API key configuration
- ✅ Sample data validity
- ✅ Import functionality
- ✅ File loading
- ✅ Basic analysis

**Integration Tests**:
- Full pipeline execution
- Model training
- Forecast generation
- Output creation

**Validation Tests**:
- Input data validation
- Model parameter validation
- Output format validation

---

## 📦 Deployment Options

### 1. Local Development
```bash
python timeseries_forecaster_agent.py
```

### 2. Google Colab
```python
!pip install -r requirements.txt
!python timeseries_forecaster_agent.py
```

### 3. Docker (Future)
```dockerfile
FROM python:3.9
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "timeseries_forecaster_agent.py"]
```

### 4. API Service (Future)
```python
from fastapi import FastAPI
app = FastAPI()

@app.post("/forecast")
def forecast(file: UploadFile, horizon: int):
    # Run agent
    return results
```

---

## 🔍 Code Quality

### Standards
- **PEP 8**: Python style guide compliance
- **Type Hints**: TypedDict for state
- **Docstrings**: Comprehensive documentation
- **Comments**: Inline explanations
- **Logging**: Detailed execution tracking

### Best Practices
- ✅ Single Responsibility Principle
- ✅ DRY (Don't Repeat Yourself)
- ✅ Error handling everywhere
- ✅ Configuration externalization
- ✅ Modular design

---

## 📚 Dependencies Rationale

| Package | Purpose | Why This Version |
|---------|---------|------------------|
| pandas 2.1.4 | Data manipulation | Latest stable, performance improvements |
| numpy 1.26.3 | Numerical computing | Compatible with pandas 2.1.x |
| statsmodels 0.14.1 | Statistical models | Latest ARIMA/SARIMA implementations |
| prophet 1.1.5 | Facebook forecasting | Production-ready, stable |
| scikit-learn 1.4.0 | Metrics, utilities | Latest features, compatible |
| langgraph 0.2.45 | Workflow orchestration | Production-grade state management |
| openai 1.54.5 | LLM integration | Latest API features |
| matplotlib 3.8.2 | Visualization | Modern plotting features |
| seaborn 0.13.1 | Enhanced plots | Professional styling |

---

## 🎓 Learning Resources

### Understanding Time Series
- Trend: Long-term direction
- Seasonality: Regular patterns
- Stationarity: Statistical properties don't change
- Autocorrelation: Relationship with past values

### Model Selection Guide
- **ARIMA**: No seasonality, needs differencing
- **SARIMA**: Has seasonal patterns
- **Prophet**: Multiple seasonalities, holidays
- **Exp. Smoothing**: Simple trend/seasonality

### Interpretation
- **Confidence Intervals**: Prediction uncertainty
- **Residuals**: Model error patterns
- **Metrics**: Accuracy measurements

---

**This architecture supports both simple forecasting tasks and complex production deployments.**
