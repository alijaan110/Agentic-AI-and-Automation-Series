# 🧹 DataCleanser AI Agent

A production-grade AI-powered data cleaning tool that automatically detects and fixes data quality issues in CSV, Excel, and JSON files.

## ✨ Features

### Automated Issue Detection
- **Missing Values**: Detects empty cells, null values, "N/A", "Unknown", and other representations
- **Duplicate Records**: Identifies exact and fuzzy duplicate rows
- **Formatting Inconsistencies**:
  - Mixed date formats (ISO, US, European, etc.)
  - Inconsistent text case (UPPER, lower, Title, MiXeD)
  - Extra whitespace (leading, trailing, multiple spaces)
  - Phone numbers in various formats
  - Email address validation
  - Currency symbols mixed with numbers
- **Data Type Mismatches**: Numbers stored as text, dates as strings, etc.
- **Statistical Outliers**: IQR-based outlier detection in numerical columns

### Intelligent Data Cleaning
- **Missing Value Imputation**: Mean, median, mode, forward-fill, or zero strategies
- **Duplicate Handling**: Keep first, last, or most complete record
- **Format Standardization**:
  - Dates → ISO format (YYYY-MM-DD)
  - Phone numbers → E.164 format
  - Text → Title case
  - Whitespace normalization
- **Type Conversion**: Automatic casting to appropriate data types
- **Outlier Management**: Replace or remove statistical anomalies

### AI-Powered Features (Optional)
When OpenAI API key is provided:
- Intelligent column name standardization
- Smart data type inference
- Contextual missing value recommendations
- Anomaly explanation with business context

### Comprehensive Reporting
- Detailed cleaning report with before/after statistics
- Row-by-row change log
- Summary metrics and visualizations
- Timestamped outputs

## 🚀 Installation

### Google Colab

1. Upload the files to your Colab environment or clone from repository
2. Install dependencies:
```python
!pip install -r requirements.txt
```

3. Add your OpenAI API key (optional but recommended):
   - Click the 🔑 key icon in the left sidebar
   - Add a secret named `OPENAI_API_KEY`
   - Paste your API key as the value

4. Run the agent:
```python
!python data_cleanser_agent.py
```

### Local Installation

1. **Clone or download the files**
```bash
# If using git
git clone <repository-url>
cd data-cleanser-agent

# Or download and extract the files
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup OpenAI API Key (optional)**

Create a `.env` file in the same directory:
```env
OPENAI_API_KEY=your_api_key_here
```

Or export as environment variable:
```bash
# On macOS/Linux
export OPENAI_API_KEY=your_api_key_here

# On Windows (Command Prompt)
set OPENAI_API_KEY=your_api_key_here

# On Windows (PowerShell)
$env:OPENAI_API_KEY="your_api_key_here"
```

5. **Run the agent**
```bash
python data_cleanser_agent.py
```

## 📖 Usage

### Quick Start

1. **Run the application**
```bash
python data_cleanser_agent.py
```

2. **Choose an option**:
   - Option 1: Upload and clean your own file
   - Option 2: Generate sample data to test the agent
   - Option 3: Exit

3. **Configure cleaning preferences** (when cleaning a file):
   - Missing numeric values strategy
   - Missing categorical values strategy
   - Duplicate handling strategy
   - Date standardization (yes/no)
   - Text standardization (yes/no)
   - Outlier handling (yes/no)

4. **Review results**:
   - View data profile and detected issues
   - See cleaning summary
   - Access cleaned files in `cleaned_data/` directory

### Sample Data Generation

To test the agent's capabilities:

```python
python data_cleanser_agent.py
# Select option 2: Generate sample data with issues
```

This creates `sample_data_with_issues.csv` containing 50+ rows with:
- 15% missing values in various formats
- 5 exact duplicate rows
- 3 fuzzy duplicate rows
- Mixed date formats (4+ different styles)
- Inconsistent text case
- Extra whitespace issues
- Phone numbers in 5 different formats
- Valid and invalid email addresses
- Currency values with mixed symbols
- Numbers stored as text
- Statistical outliers

### Supported File Formats

- **CSV** (`.csv`)
- **Excel** (`.xlsx`, `.xls`)
- **JSON** (`.json`)

### Configuration Options

#### Missing Value Strategies

**Numeric columns**:
- `mean`: Fill with column mean
- `median`: Fill with column median (default)
- `mode`: Fill with most frequent value
- `zero`: Fill with 0
- `forward_fill`: Use previous row's value

**Categorical columns**:
- `mode`: Fill with most frequent value (default)
- `unknown`: Fill with "Unknown"
- `forward_fill`: Use previous row's value

#### Duplicate Strategies

- `first`: Keep first occurrence (default)
- `last`: Keep last occurrence
- `most_complete`: Keep row with fewest missing values

#### Standardization Options

- **Date formats**: Standardize to `YYYY-MM-DD`
- **Text case**: Convert to Title Case
- **Phone numbers**: Convert to E.164 format (`+1XXXXXXXXXX`)
- **Whitespace**: Remove leading/trailing, collapse multiple spaces

## 📁 Output Files

All cleaned files are saved to the `cleaned_data/` directory:

### Cleaned Dataset
```
cleaned_[original_filename]_[timestamp].csv
```
- Same format as input
- All issues fixed according to configuration
- Ready for analysis or downstream processing

### Cleaning Report
```
cleaning_report_[timestamp].csv
```
Contains:
- Column name
- Issue type detected
- Action taken
- Before/after counts
- Summary statistics

Example report entries:
```csv
column,issue,action,before,after
email,email_validation,Validated emails,50,47
purchase_date,date_format,Standardized to YYYY-MM-DD,success,success
amount,data_type,Converted to numeric,success,success
```

## 🔧 Environment Variables

### Required (for AI features)

```env
OPENAI_API_KEY=sk-...your-key-here
```

Get your API key from: https://platform.openai.com/api-keys

### Optional

The agent works without an API key using rule-based cleaning only.

## 💡 Examples

### Example 1: Clean a CSV file
```python
python data_cleanser_agent.py

# Select option 1
# Upload your CSV file
# Use default settings (press Enter for each prompt)
# Review cleaned file in cleaned_data/ directory
```

### Example 2: Custom cleaning configuration
```python
python data_cleanser_agent.py

# Select option 1
# Upload file
# Configure:
#   - Missing numeric: mean
#   - Missing categorical: unknown
#   - Duplicates: most_complete
#   - Standardize dates: yes
#   - Standardize text: no
#   - Handle outliers: yes
```

### Example 3: Test with sample data
```python
python data_cleanser_agent.py

# Select option 2 to generate sample data
# Select option 1 to clean the generated file
# Use default settings to see all cleaning features
```

## 🏗️ Architecture

### Class Structure

```python
DataCleanserAgent
├── __init__()           # Initialize agent with AI capabilities
├── upload_file()        # Handle file upload (Colab/Local)
├── load_data()          # Load CSV/Excel/JSON files
├── detect_issues()      # Detect all quality issues
├── clean_data()         # Execute cleaning operations
├── generate_report()    # Create comprehensive report
└── export_results()     # Save cleaned data and report
```

### AI Integration

The agent uses OpenAI GPT-4 for:
- Column name standardization
- Data type inference
- Missing value strategy recommendations
- Outlier explanation and context

**System Prompt Structure**:
```python
"You are an expert data quality analyst specializing in:
1. Data quality issue analysis
2. Data type conversions
3. Column name standardization
4. Missing value imputation strategies
5. Anomaly explanation with business context"
```

**User Prompts**: Dynamic prompts based on detected issues with context-specific information.

## 🛠️ Troubleshooting

### Common Issues

**1. File upload not working in Colab**
```python
# Make sure you're running in Colab environment
# The upload widget should appear automatically
# If not, restart runtime and try again
```

**2. OpenAI API errors**
```
✗ Error: Invalid API key
```
**Solution**: Check that your API key is correctly set in Colab secrets or .env file

**3. Module not found errors**
```bash
# Reinstall requirements
pip install -r requirements.txt --upgrade
```

**4. Date parsing issues**
```
Could not standardize dates in column X
```
**Solution**: Some date formats may not be recognized. The agent will skip those columns and log a warning.

**5. Memory errors with large files**
```
MemoryError: Unable to allocate array
```
**Solution**: 
- Process file in chunks
- Increase available RAM
- Filter data before cleaning

### Performance Tips

**For large datasets (>1M rows)**:
- Disable AI features for faster processing
- Process in batches
- Use simpler cleaning strategies

**For optimal AI performance**:
- Ensure stable internet connection
- Use specific, well-formed column names
- Provide context in data when possible

### Logging

Check `data_cleanser.log` for detailed operation logs:
```bash
tail -f data_cleanser.log
```

## 📊 Sample Data Issues

The generated sample data includes realistic examples of:

```csv
# Missing values in different formats
region: "", "N/A", "null", "Unknown"

# Inconsistent text case
first_name: "JOHN", "jane", "Bob Smith", "  alice  "

# Mixed date formats
purchase_date: "2024-01-15", "01/20/2024", "2-15-24"

# Mixed phone formats
phone: "555-123-4567", "(555) 234-5678", "5553456789"

# Currency with symbols
amount: "$1,250", "€1,800", "3200.75"

# Invalid emails
email: "test@example", "invalid-email", "user@domain.com"

# Statistical outlier
amount: 50000 (when others are 1000-3000)
```

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional data validation rules
- More intelligent fuzzy matching
- Support for more file formats
- Enhanced AI prompts
- Performance optimizations

## 📄 License

MIT License

Copyright (c) 2024 DataCleanser AI Agent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 📞 Support

For issues, questions, or suggestions:
- Check the troubleshooting section
- Review the log file (`data_cleanser.log`)
- Open an issue on the repository

## 🔄 Version History

### v1.0.0 (Current)
- Initial release
- AI-powered data cleaning
- Support for CSV, Excel, JSON
- Comprehensive issue detection
- Multi-environment support (Colab/Local)
- Detailed reporting

---

**Happy Cleaning! 🧹✨**
