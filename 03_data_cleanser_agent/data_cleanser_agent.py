"""
DataCleanser AI Agent
=====================
A production-grade AI-powered data cleaning tool that automatically detects and fixes
data quality issues in CSV, Excel, and JSON files.

Author: Data Engineering Team
Version: 1.0.0
License: MIT
"""

import sys
import os
import json
import re
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Union
import warnings

warnings.filterwarnings('ignore')

# Environment detection
IN_COLAB = 'google.colab' in sys.modules

# Core dependencies
import pandas as pd
import numpy as np
from dateutil import parser
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.panel import Panel
from rich import print as rprint

# Optional dependencies with fallbacks
try:
    import phonenumbers
    PHONE_AVAILABLE = True
except ImportError:
    PHONE_AVAILABLE = False

try:
    from email_validator import validate_email, EmailNotValidError
    EMAIL_AVAILABLE = True
except ImportError:
    EMAIL_AVAILABLE = False

try:
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

# AI capabilities
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Environment-specific imports
if IN_COLAB:
    from google.colab import userdata, files as colab_files
else:
    from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_cleanser.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Rich console
console = Console()


class DataCleanserConfig:
    """Configuration constants for the DataCleanser Agent"""
    
    # Missing value representations
    MISSING_VALUES = ['', ' ', 'NA', 'N/A', 'n/a', 'null', 'NULL', 'None', 
                      'NONE', 'nan', 'NaN', 'NAN', 'Unknown', 'unknown', 
                      'UNKNOWN', '-', '--', '?', 'N.A.', 'n.a.']
    
    # Numeric fill strategies
    NUMERIC_STRATEGIES = ['mean', 'median', 'mode', 'forward_fill', 'zero']
    
    # Categorical fill strategies
    CATEGORICAL_STRATEGIES = ['mode', 'unknown', 'forward_fill']
    
    # Duplicate handling strategies
    DUPLICATE_STRATEGIES = ['first', 'last', 'most_complete']
    
    # Date format standardization
    TARGET_DATE_FORMAT = '%Y-%m-%d'
    
    # Text case standardization
    TEXT_CASE_OPTIONS = ['title', 'lower', 'upper', 'original']
    
    # Outlier detection (IQR multiplier)
    OUTLIER_IQR_MULTIPLIER = 3.0
    
    # Fuzzy duplicate threshold (0-1)
    FUZZY_MATCH_THRESHOLD = 0.85
    
    # Output directory
    OUTPUT_DIR = 'cleaned_data'
    
    # OpenAI model
    OPENAI_MODEL = 'gpt-4o-mini'
    
    # AI System Prompt
    AI_SYSTEM_PROMPT = """You are an expert data quality analyst and data engineer specializing in data cleaning and standardization.

Your role is to:
1. Analyze data quality issues and provide intelligent recommendations
2. Suggest appropriate data type conversions based on content patterns
3. Standardize column names to be clean, consistent, and meaningful
4. Provide context-aware missing value imputation strategies
5. Explain detected anomalies and outliers with business context
6. Recommend optimal cleaning strategies based on data patterns

Guidelines:
- Be concise and actionable in your recommendations
- Consider the business context when making suggestions
- Prioritize data integrity and consistency
- Explain your reasoning clearly
- Provide specific examples when helpful
- Focus on practical, implementable solutions

Always respond in JSON format when requested for structured outputs."""

    # AI User Prompts
    @staticmethod
    def get_column_standardization_prompt(columns: List[str]) -> str:
        return f"""Analyze these column names and suggest standardized versions:

Columns: {columns}

Requirements:
- Convert to snake_case
- Use clear, descriptive names
- Fix abbreviations and typos
- Ensure consistency across similar columns
- Keep names concise but meaningful

Return a JSON object mapping original to standardized names:
{{"original_name": "standardized_name", ...}}"""

    @staticmethod
    def get_data_type_inference_prompt(column_name: str, sample_values: List[str]) -> str:
        return f"""Analyze this data column and suggest the appropriate data type:

Column: {column_name}
Sample values: {sample_values}

Suggest the most appropriate data type from:
- int64 (integers)
- float64 (decimal numbers)
- datetime (dates/timestamps)
- bool (boolean)
- string (text)
- category (categorical with limited unique values)

Return JSON: {{"recommended_type": "type_name", "confidence": "high/medium/low", "reasoning": "explanation"}}"""

    @staticmethod
    def get_missing_value_strategy_prompt(column_name: str, data_type: str, 
                                         missing_percent: float, context: str) -> str:
        return f"""Recommend the best strategy for handling missing values:

Column: {column_name}
Data Type: {data_type}
Missing Percentage: {missing_percent:.1f}%
Context: {context}

Available strategies:
- For numeric: mean, median, mode, forward_fill, zero
- For categorical: mode, unknown, forward_fill

Return JSON: {{"strategy": "chosen_strategy", "reasoning": "explanation"}}"""

    @staticmethod
    def get_anomaly_explanation_prompt(column_name: str, outlier_values: List[Any], 
                                       stats: Dict[str, float]) -> str:
        return f"""Analyze these statistical outliers and provide business context:

Column: {column_name}
Statistics: {stats}
Outlier Values: {outlier_values}

Provide:
1. Possible reasons for these outliers
2. Whether they should be kept or removed
3. Business implications

Return JSON: {{"likely_causes": ["cause1", "cause2"], "recommendation": "keep/remove/investigate", "explanation": "detailed explanation"}}"""


class DataCleanserAgent:
    """
    Main DataCleanser Agent class for automated data quality improvement.
    
    This agent detects and fixes common data quality issues including:
    - Missing values
    - Duplicate records
    - Formatting inconsistencies
    - Data type mismatches
    - Statistical outliers
    """
    
    def __init__(self, use_ai: bool = True):
        """
        Initialize the DataCleanser Agent.
        
        Args:
            use_ai: Whether to use AI-powered features (requires OpenAI API key)
        """
        self.config = DataCleanserConfig()
        self.console = console
        self.df_original: Optional[pd.DataFrame] = None
        self.df_cleaned: Optional[pd.DataFrame] = None
        self.cleaning_report: List[Dict[str, Any]] = []
        self.issues_found: Dict[str, Any] = {}
        self.filename: Optional[str] = None
        
        # Setup OpenAI client
        self.use_ai = use_ai and OPENAI_AVAILABLE
        self.ai_client: Optional[OpenAI] = None
        
        if self.use_ai:
            self._setup_openai()
        
        # Create output directory
        Path(self.config.OUTPUT_DIR).mkdir(exist_ok=True)
    
    def _setup_openai(self) -> None:
        """Setup OpenAI client with API key from environment"""
        try:
            if IN_COLAB:
                api_key = userdata.get('OPENAI_API_KEY')
            else:
                load_dotenv()
                api_key = os.getenv('OPENAI_API_KEY')
            
            if api_key:
                self.ai_client = OpenAI(api_key=api_key)
                self.console.print("✓ AI features enabled", style="green")
            else:
                self.use_ai = False
                self.console.print("⚠ AI features disabled (no API key)", style="yellow")
        except Exception as e:
            self.use_ai = False
            logger.warning(f"Could not setup OpenAI: {e}")
            self.console.print("⚠ AI features disabled", style="yellow")
    
    def _call_openai(self, user_prompt: str, response_format: str = "json") -> Optional[Dict]:
        """
        Call OpenAI API with error handling.
        
        Args:
            user_prompt: The user message/prompt
            response_format: Expected response format
            
        Returns:
            Parsed JSON response or None if failed
        """
        if not self.use_ai or not self.ai_client:
            return None
        
        try:
            response = self.ai_client.chat.completions.create(
                model=self.config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": self.config.AI_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"} if response_format == "json" else None,
                temperature=0.3,
                max_tokens=1000
            )
            
            result = response.choices[0].message.content
            if response_format == "json":
                return json.loads(result)
            return {"response": result}
        
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return None
    
    def upload_file(self) -> Optional[str]:
        """
        Handle file upload based on environment (Colab vs Local).
        
        Returns:
            Path to uploaded file or None if cancelled
        """
        try:
            if IN_COLAB:
                self.console.print("\n📁 Please select a file to upload...", style="cyan bold")
                uploaded = colab_files.upload()
                if not uploaded:
                    return None
                filename = list(uploaded.keys())[0]
                self.console.print(f"✓ File uploaded: {filename}", style="green")
                return filename
            else:
                from tkinter import Tk, filedialog
                root = Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                
                filename = filedialog.askopenfilename(
                    title="Select data file to clean",
                    filetypes=[
                        ("All Supported Files", "*.csv;*.xlsx;*.xls;*.json"),
                        ("CSV Files", "*.csv"),
                        ("Excel Files", "*.xlsx;*.xls"),
                        ("JSON Files", "*.json"),
                        ("All Files", "*.*")
                    ]
                )
                root.destroy()
                
                if filename:
                    self.console.print(f"✓ File selected: {filename}", style="green")
                    return filename
                return None
        
        except Exception as e:
            logger.error(f"File upload error: {e}")
            self.console.print(f"✗ Error uploading file: {e}", style="red")
            return None
    
    def load_data(self, filepath: str) -> bool:
        """
        Load data from CSV, Excel, or JSON file.
        
        Args:
            filepath: Path to the data file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.filename = Path(filepath).name
            file_ext = Path(filepath).suffix.lower()
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task("Loading data...", total=None)
                
                if file_ext == '.csv':
                    self.df_original = pd.read_csv(filepath, na_values=self.config.MISSING_VALUES)
                elif file_ext in ['.xlsx', '.xls']:
                    self.df_original = pd.read_excel(filepath, na_values=self.config.MISSING_VALUES)
                elif file_ext == '.json':
                    self.df_original = pd.read_json(filepath)
                else:
                    raise ValueError(f"Unsupported file format: {file_ext}")
                
                progress.update(task, completed=True)
            
            # Create a copy for cleaning
            self.df_cleaned = self.df_original.copy()
            
            # Display data profile
            self._display_data_profile()
            
            return True
        
        except Exception as e:
            logger.error(f"Data loading error: {e}")
            self.console.print(f"✗ Error loading data: {e}", style="red")
            return False
    
    def _display_data_profile(self) -> None:
        """Display initial data profile"""
        if self.df_original is None:
            return
        
        table = Table(title="📊 Data Profile", show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Rows", f"{len(self.df_original):,}")
        table.add_row("Columns", f"{len(self.df_original.columns):,}")
        table.add_row("Total Cells", f"{self.df_original.size:,}")
        table.add_row("Memory Usage", f"{self.df_original.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        table.add_row("Duplicate Rows", f"{self.df_original.duplicated().sum():,}")
        table.add_row("Missing Cells", f"{self.df_original.isna().sum().sum():,}")
        
        self.console.print(table)
    
    def detect_issues(self) -> Dict[str, Any]:
        """
        Detect all data quality issues.
        
        Returns:
            Dictionary containing all detected issues
        """
        if self.df_original is None:
            return {}
        
        self.console.print("\n🔍 Detecting data quality issues...", style="cyan bold")
        
        issues = {
            'missing_values': self._detect_missing_values(),
            'duplicates': self._detect_duplicates(),
            'formatting': self._detect_formatting_issues(),
            'data_types': self._detect_data_type_issues(),
            'outliers': self._detect_outliers()
        }
        
        self.issues_found = issues
        self._display_issues_summary(issues)
        
        return issues
    
    def _detect_missing_values(self) -> Dict[str, Any]:
        """Detect missing values in all columns"""
        missing_info = {}
        
        for col in self.df_original.columns:
            missing_count = self.df_original[col].isna().sum()
            if missing_count > 0:
                missing_info[col] = {
                    'count': int(missing_count),
                    'percentage': float(missing_count / len(self.df_original) * 100),
                    'data_type': str(self.df_original[col].dtype)
                }
        
        return missing_info
    
    def _detect_duplicates(self) -> Dict[str, Any]:
        """Detect exact and fuzzy duplicate rows"""
        exact_dupes = self.df_original.duplicated(keep=False).sum()
        
        duplicate_info = {
            'exact_count': int(exact_dupes),
            'exact_rows': self.df_original[self.df_original.duplicated(keep=False)].index.tolist()
        }
        
        return duplicate_info
    
    def _detect_formatting_issues(self) -> Dict[str, List[str]]:
        """Detect formatting inconsistencies"""
        issues = {
            'inconsistent_case': [],
            'whitespace_issues': [],
            'mixed_date_formats': [],
            'mixed_phone_formats': [],
            'invalid_emails': []
        }
        
        for col in self.df_original.columns:
            if self.df_original[col].dtype == 'object':
                # Check text case inconsistency
                non_null = self.df_original[col].dropna()
                if len(non_null) > 0:
                    has_upper = non_null.str.isupper().any()
                    has_lower = non_null.str.islower().any()
                    has_title = non_null.str.istitle().any()
                    
                    if sum([has_upper, has_lower, has_title]) > 1:
                        issues['inconsistent_case'].append(col)
                
                # Check whitespace issues
                if non_null.str.contains(r'^\s|\s$|\s{2,}', regex=True).any():
                    issues['whitespace_issues'].append(col)
                
                # Check date format variations
                if self._could_be_dates(non_null):
                    issues['mixed_date_formats'].append(col)
                
                # Check phone number variations
                if self._could_be_phones(non_null):
                    issues['mixed_phone_formats'].append(col)
                
                # Check email validity
                if self._could_be_emails(non_null):
                    issues['invalid_emails'].append(col)
        
        return issues
    
    def _detect_data_type_issues(self) -> Dict[str, str]:
        """Detect columns with incorrect data types"""
        type_issues = {}
        
        for col in self.df_original.columns:
            current_type = str(self.df_original[col].dtype)
            
            # Check if numeric columns are stored as strings
            if current_type == 'object':
                non_null = self.df_original[col].dropna()
                if len(non_null) > 0:
                    # Try to convert to numeric
                    sample = non_null.head(100).astype(str).str.replace(',', '').str.replace('$', '').str.replace('€', '')
                    try:
                        pd.to_numeric(sample, errors='raise')
                        type_issues[col] = f"Should be numeric, currently {current_type}"
                    except:
                        # Try to parse as dates
                        if self._could_be_dates(non_null):
                            type_issues[col] = f"Should be datetime, currently {current_type}"
        
        return type_issues
    
    def _detect_outliers(self) -> Dict[str, List[float]]:
        """Detect statistical outliers in numeric columns"""
        outliers = {}
        
        numeric_cols = self.df_original.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            Q1 = self.df_original[col].quantile(0.25)
            Q3 = self.df_original[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - self.config.OUTLIER_IQR_MULTIPLIER * IQR
            upper_bound = Q3 + self.config.OUTLIER_IQR_MULTIPLIER * IQR
            
            outlier_values = self.df_original[
                (self.df_original[col] < lower_bound) | 
                (self.df_original[col] > upper_bound)
            ][col].tolist()
            
            if outlier_values:
                outliers[col] = outlier_values[:10]  # Limit to first 10
        
        return outliers
    
    def _could_be_dates(self, series: pd.Series) -> bool:
        """Check if a series could contain dates"""
        sample = series.head(10).astype(str)
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',
            r'\d{2}/\d{2}/\d{4}',
            r'\d{1,2}-\d{1,2}-\d{2,4}',
            r'\d{1,2}/\d{1,2}/\d{2,4}'
        ]
        
        for pattern in date_patterns:
            if sample.str.contains(pattern, regex=True).any():
                return True
        return False
    
    def _could_be_phones(self, series: pd.Series) -> bool:
        """Check if a series could contain phone numbers"""
        sample = series.head(10).astype(str)
        return sample.str.contains(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', regex=True).any()
    
    def _could_be_emails(self, series: pd.Series) -> bool:
        """Check if a series could contain emails"""
        sample = series.head(10).astype(str)
        return sample.str.contains(r'@', regex=False).any()
    
    def _display_issues_summary(self, issues: Dict[str, Any]) -> None:
        """Display summary of detected issues"""
        table = Table(title="⚠️  Issues Detected", show_header=True, header_style="bold red")
        table.add_column("Issue Type", style="yellow")
        table.add_column("Count", style="red", justify="right")
        table.add_column("Details", style="white")
        
        # Missing values
        if issues['missing_values']:
            count = len(issues['missing_values'])
            cols = ', '.join(list(issues['missing_values'].keys())[:3])
            if count > 3:
                cols += f", ... (+{count-3} more)"
            table.add_row("Missing Values", str(count), cols)
        
        # Duplicates
        if issues['duplicates']['exact_count'] > 0:
            table.add_row("Exact Duplicates", str(issues['duplicates']['exact_count']), "Full row matches")
        
        # Formatting issues
        for issue_type, columns in issues['formatting'].items():
            if columns:
                display_name = issue_type.replace('_', ' ').title()
                cols_str = ', '.join(columns[:3])
                if len(columns) > 3:
                    cols_str += f", ... (+{len(columns)-3} more)"
                table.add_row(display_name, str(len(columns)), cols_str)
        
        # Data type issues
        if issues['data_types']:
            count = len(issues['data_types'])
            table.add_row("Data Type Mismatches", str(count), f"{count} columns need type conversion")
        
        # Outliers
        if issues['outliers']:
            count = len(issues['outliers'])
            cols = ', '.join(list(issues['outliers'].keys())[:3])
            if count > 3:
                cols += f", ... (+{count-3} more)"
            table.add_row("Statistical Outliers", str(count), cols)
        
        if not any([issues['missing_values'], issues['duplicates']['exact_count'], 
                   any(issues['formatting'].values()), issues['data_types'], issues['outliers']]):
            table.add_row("✓ No Issues Found", "0", "Data quality looks good!")
        
        self.console.print(table)
    
    def clean_data(self, 
                   numeric_strategy: str = 'median',
                   categorical_strategy: str = 'mode',
                   duplicate_strategy: str = 'first',
                   standardize_dates: bool = True,
                   standardize_text: bool = True,
                   remove_outliers: bool = False) -> bool:
        """
        Clean the data based on detected issues.
        
        Args:
            numeric_strategy: Strategy for numeric missing values
            categorical_strategy: Strategy for categorical missing values
            duplicate_strategy: Strategy for handling duplicates
            standardize_dates: Whether to standardize date formats
            standardize_text: Whether to standardize text formatting
            remove_outliers: Whether to remove statistical outliers
            
        Returns:
            True if successful, False otherwise
        """
        if self.df_cleaned is None:
            return False
        
        try:
            self.console.print("\n🔧 Cleaning data...", style="cyan bold")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                console=self.console
            ) as progress:
                
                # Clean missing values
                task = progress.add_task("Handling missing values...", total=100)
                self._clean_missing_values(numeric_strategy, categorical_strategy)
                progress.update(task, completed=100)
                
                # Remove duplicates
                task = progress.add_task("Removing duplicates...", total=100)
                self._clean_duplicates(duplicate_strategy)
                progress.update(task, completed=100)
                
                # Fix formatting
                task = progress.add_task("Standardizing formatting...", total=100)
                if standardize_dates:
                    self._standardize_dates()
                if standardize_text:
                    self._standardize_text()
                self._clean_whitespace()
                self._standardize_phone_numbers()
                self._validate_emails()
                progress.update(task, completed=100)
                
                # Fix data types
                task = progress.add_task("Converting data types...", total=100)
                self._fix_data_types()
                progress.update(task, completed=100)
                
                # Handle outliers
                if remove_outliers:
                    task = progress.add_task("Handling outliers...", total=100)
                    self._handle_outliers()
                    progress.update(task, completed=100)
            
            self.console.print("✓ Data cleaning completed!", style="green bold")
            return True
        
        except Exception as e:
            logger.error(f"Data cleaning error: {e}")
            self.console.print(f"✗ Error during cleaning: {e}", style="red")
            return False
    
    def _clean_missing_values(self, numeric_strategy: str, categorical_strategy: str) -> None:
        """Clean missing values based on strategies"""
        for col in self.df_cleaned.columns:
            if self.df_cleaned[col].isna().any():
                if pd.api.types.is_numeric_dtype(self.df_cleaned[col]):
                    # Numeric column
                    if numeric_strategy == 'mean':
                        fill_value = self.df_cleaned[col].mean()
                    elif numeric_strategy == 'median':
                        fill_value = self.df_cleaned[col].median()
                    elif numeric_strategy == 'mode':
                        fill_value = self.df_cleaned[col].mode()[0] if not self.df_cleaned[col].mode().empty else 0
                    elif numeric_strategy == 'zero':
                        fill_value = 0
                    elif numeric_strategy == 'forward_fill':
                        self.df_cleaned[col].fillna(method='ffill', inplace=True)
                        continue
                    
                    before_count = self.df_cleaned[col].isna().sum()
                    self.df_cleaned[col].fillna(fill_value, inplace=True)
                    after_count = self.df_cleaned[col].isna().sum()
                    
                    self.cleaning_report.append({
                        'column': col,
                        'issue': 'missing_values',
                        'action': f'Filled with {numeric_strategy}',
                        'before': int(before_count),
                        'after': int(after_count)
                    })
                else:
                    # Categorical column
                    if categorical_strategy == 'mode':
                        fill_value = self.df_cleaned[col].mode()[0] if not self.df_cleaned[col].mode().empty else 'Unknown'
                    elif categorical_strategy == 'unknown':
                        fill_value = 'Unknown'
                    elif categorical_strategy == 'forward_fill':
                        self.df_cleaned[col].fillna(method='ffill', inplace=True)
                        continue
                    
                    before_count = self.df_cleaned[col].isna().sum()
                    self.df_cleaned[col].fillna(fill_value, inplace=True)
                    after_count = self.df_cleaned[col].isna().sum()
                    
                    self.cleaning_report.append({
                        'column': col,
                        'issue': 'missing_values',
                        'action': f'Filled with {categorical_strategy}',
                        'before': int(before_count),
                        'after': int(after_count)
                    })
    
    def _clean_duplicates(self, strategy: str) -> None:
        """Remove duplicate rows"""
        before_count = len(self.df_cleaned)
        
        if strategy == 'first':
            self.df_cleaned.drop_duplicates(keep='first', inplace=True)
        elif strategy == 'last':
            self.df_cleaned.drop_duplicates(keep='last', inplace=True)
        elif strategy == 'most_complete':
            # Keep row with fewest missing values
            self.df_cleaned['_missing_count'] = self.df_cleaned.isna().sum(axis=1)
            self.df_cleaned.sort_values('_missing_count', inplace=True)
            self.df_cleaned.drop_duplicates(subset=self.df_cleaned.columns.difference(['_missing_count']), 
                                           keep='first', inplace=True)
            self.df_cleaned.drop('_missing_count', axis=1, inplace=True)
        
        after_count = len(self.df_cleaned)
        removed = before_count - after_count
        
        if removed > 0:
            self.cleaning_report.append({
                'column': 'ALL',
                'issue': 'duplicates',
                'action': f'Removed duplicates (keep {strategy})',
                'before': before_count,
                'after': after_count,
                'removed': removed
            })
    
    def _standardize_dates(self) -> None:
        """Standardize date formats"""
        for col in self.df_cleaned.columns:
            if self._could_be_dates(self.df_cleaned[col].dropna()):
                try:
                    # Try to parse dates
                    self.df_cleaned[col] = pd.to_datetime(
                        self.df_cleaned[col], 
                        errors='coerce',
                        infer_datetime_format=True
                    )
                    
                    # Format to standard
                    self.df_cleaned[col] = self.df_cleaned[col].dt.strftime(self.config.TARGET_DATE_FORMAT)
                    
                    self.cleaning_report.append({
                        'column': col,
                        'issue': 'date_format',
                        'action': f'Standardized to {self.config.TARGET_DATE_FORMAT}',
                        'status': 'success'
                    })
                except Exception as e:
                    logger.warning(f"Could not standardize dates in {col}: {e}")
    
    def _standardize_text(self) -> None:
        """Standardize text case to title case"""
        for col in self.df_cleaned.columns:
            if self.df_cleaned[col].dtype == 'object':
                # Check if it's likely a name/text field (not IDs, codes, etc.)
                sample = self.df_cleaned[col].dropna().head(5).astype(str)
                if sample.str.contains(' ').any():  # Multi-word fields
                    try:
                        self.df_cleaned[col] = self.df_cleaned[col].str.title()
                        
                        self.cleaning_report.append({
                            'column': col,
                            'issue': 'text_case',
                            'action': 'Standardized to title case',
                            'status': 'success'
                        })
                    except:
                        pass
    
    def _clean_whitespace(self) -> None:
        """Remove extra whitespace"""
        for col in self.df_cleaned.columns:
            if self.df_cleaned[col].dtype == 'object':
                # Remove leading/trailing whitespace and collapse multiple spaces
                self.df_cleaned[col] = self.df_cleaned[col].str.strip().str.replace(r'\s+', ' ', regex=True)
    
    def _standardize_phone_numbers(self) -> None:
        """Standardize phone number formats"""
        if not PHONE_AVAILABLE:
            return
        
        for col in self.df_cleaned.columns:
            if self._could_be_phones(self.df_cleaned[col].dropna()):
                def format_phone(phone):
                    if pd.isna(phone):
                        return phone
                    try:
                        # Parse and format to E.164
                        parsed = phonenumbers.parse(str(phone), "US")
                        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
                    except:
                        return phone
                
                self.df_cleaned[col] = self.df_cleaned[col].apply(format_phone)
                
                self.cleaning_report.append({
                    'column': col,
                    'issue': 'phone_format',
                    'action': 'Standardized to E.164 format',
                    'status': 'success'
                })
    
    def _validate_emails(self) -> None:
        """Validate and clean email addresses"""
        if not EMAIL_AVAILABLE:
            return
        
        for col in self.df_cleaned.columns:
            if self._could_be_emails(self.df_cleaned[col].dropna()):
                def clean_email(email):
                    if pd.isna(email):
                        return email
                    try:
                        validated = validate_email(str(email), check_deliverability=False)
                        return validated.normalized
                    except EmailNotValidError:
                        return None
                
                before_valid = self.df_cleaned[col].notna().sum()
                self.df_cleaned[col] = self.df_cleaned[col].apply(clean_email)
                after_valid = self.df_cleaned[col].notna().sum()
                
                self.cleaning_report.append({
                    'column': col,
                    'issue': 'email_validation',
                    'action': 'Validated emails',
                    'before': int(before_valid),
                    'after': int(after_valid),
                    'invalid_removed': int(before_valid - after_valid)
                })
    
    def _fix_data_types(self) -> None:
        """Convert columns to appropriate data types"""
        for col in self.df_cleaned.columns:
            if self.df_cleaned[col].dtype == 'object':
                # Try numeric conversion
                cleaned = self.df_cleaned[col].astype(str).str.replace(',', '').str.replace('$', '').str.replace('€', '').str.replace('USD', '').str.strip()
                
                try:
                    self.df_cleaned[col] = pd.to_numeric(cleaned, errors='raise')
                    self.cleaning_report.append({
                        'column': col,
                        'issue': 'data_type',
                        'action': 'Converted to numeric',
                        'status': 'success'
                    })
                    continue
                except:
                    pass
    
    def _handle_outliers(self) -> None:
        """Handle statistical outliers"""
        numeric_cols = self.df_cleaned.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            Q1 = self.df_cleaned[col].quantile(0.25)
            Q3 = self.df_cleaned[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - self.config.OUTLIER_IQR_MULTIPLIER * IQR
            upper_bound = Q3 + self.config.OUTLIER_IQR_MULTIPLIER * IQR
            
            before_count = len(self.df_cleaned)
            outlier_mask = (self.df_cleaned[col] < lower_bound) | (self.df_cleaned[col] > upper_bound)
            outlier_count = outlier_mask.sum()
            
            if outlier_count > 0:
                # Replace outliers with median
                median_val = self.df_cleaned[col].median()
                self.df_cleaned.loc[outlier_mask, col] = median_val
                
                self.cleaning_report.append({
                    'column': col,
                    'issue': 'outliers',
                    'action': f'Replaced {outlier_count} outliers with median',
                    'median_value': float(median_val),
                    'count': int(outlier_count)
                })
    
    def generate_report(self) -> pd.DataFrame:
        """
        Generate comprehensive cleaning report.
        
        Returns:
            DataFrame containing the cleaning report
        """
        if not self.cleaning_report:
            return pd.DataFrame()
        
        report_df = pd.DataFrame(self.cleaning_report)
        
        # Add summary statistics
        summary = {
            'total_rows_before': len(self.df_original),
            'total_rows_after': len(self.df_cleaned),
            'total_columns': len(self.df_cleaned.columns),
            'total_changes': len(self.cleaning_report),
            'timestamp': datetime.now().isoformat()
        }
        
        # Display summary
        self._display_cleaning_summary(summary)
        
        return report_df
    
    def _display_cleaning_summary(self, summary: Dict[str, Any]) -> None:
        """Display cleaning summary"""
        table = Table(title="📋 Cleaning Summary", show_header=True, header_style="bold green")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Original Rows", f"{summary['total_rows_before']:,}")
        table.add_row("Cleaned Rows", f"{summary['total_rows_after']:,}")
        table.add_row("Rows Removed", f"{summary['total_rows_before'] - summary['total_rows_after']:,}")
        table.add_row("Total Columns", f"{summary['total_columns']:,}")
        table.add_row("Operations Performed", f"{summary['total_changes']:,}")
        
        self.console.print(table)
    
    def export_results(self) -> Tuple[str, str]:
        """
        Export cleaned data and report.
        
        Returns:
            Tuple of (cleaned_data_path, report_path)
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_name = Path(self.filename).stem if self.filename else 'data'
        
        # Export cleaned data
        cleaned_path = Path(self.config.OUTPUT_DIR) / f"cleaned_{base_name}_{timestamp}.csv"
        self.df_cleaned.to_csv(cleaned_path, index=False)
        
        # Export report
        report_path = Path(self.config.OUTPUT_DIR) / f"cleaning_report_{timestamp}.csv"
        report_df = pd.DataFrame(self.cleaning_report)
        report_df.to_csv(report_path, index=False)
        
        self.console.print(f"\n✓ Cleaned data saved to: {cleaned_path}", style="green")
        self.console.print(f"✓ Cleaning report saved to: {report_path}", style="green")
        
        return str(cleaned_path), str(report_path)


def main():
    """Main execution function"""
    console.print(Panel.fit(
        "[bold cyan]DataCleanser AI Agent[/bold cyan]\n"
        "[yellow]Automated Data Quality Improvement[/yellow]\n\n"
        "Detects and fixes:\n"
        "• Missing values • Duplicates • Formatting issues\n"
        "• Data type mismatches • Statistical outliers",
        border_style="cyan"
    ))
    
    # Initialize agent
    agent = DataCleanserAgent(use_ai=True)
    
    while True:
        console.print("\n[bold cyan]Select a file to clean:[/bold cyan]")
        
        # Upload file
        filepath = agent.upload_file()
        if not filepath:
            console.print("\nNo file selected.", style="yellow")
            
            retry = console.input("\n[bold yellow]Try again? (y/n):[/bold yellow] ").strip().lower()
            if retry != 'y':
                console.print("\n👋 Goodbye!", style="cyan")
                break
            continue
        
        # Load data
        if not agent.load_data(filepath):
            continue
        
        # Detect issues
        issues = agent.detect_issues()
        
        if not any([issues['missing_values'], issues['duplicates']['exact_count'],
                   any(issues['formatting'].values()), issues['data_types'], issues['outliers']]):
            console.print("\n✓ No data quality issues detected! Your data looks clean.", style="green bold")
            
            another = console.input("\n[bold yellow]Clean another file? (y/n):[/bold yellow] ").strip().lower()
            if another != 'y':
                console.print("\n👋 Goodbye!", style="cyan")
                break
            continue
        
        # Ask for cleaning preferences
        console.print("\n[bold cyan]Cleaning Configuration:[/bold cyan]")
        
        numeric_strategy = console.input(
            f"Missing numeric values strategy [median/mean/mode/zero/forward_fill] (default: median): "
        ).strip().lower() or 'median'
        
        categorical_strategy = console.input(
            f"Missing categorical values strategy [mode/unknown/forward_fill] (default: mode): "
        ).strip().lower() or 'mode'
        
        duplicate_strategy = console.input(
            f"Duplicate handling strategy [first/last/most_complete] (default: first): "
        ).strip().lower() or 'first'
        
        standardize_dates = console.input(
            "Standardize date formats? [y/n] (default: y): "
        ).strip().lower() != 'n'
        
        standardize_text = console.input(
            "Standardize text case? [y/n] (default: y): "
        ).strip().lower() != 'n'
        
        remove_outliers = console.input(
            "Handle statistical outliers? [y/n] (default: n): "
        ).strip().lower() == 'y'
        
        # Clean data
        if agent.clean_data(
            numeric_strategy=numeric_strategy,
            categorical_strategy=categorical_strategy,
            duplicate_strategy=duplicate_strategy,
            standardize_dates=standardize_dates,
            standardize_text=standardize_text,
            remove_outliers=remove_outliers
        ):
            # Generate report
            agent.generate_report()
            
            # Export results
            cleaned_path, report_path = agent.export_results()
            
            # Download in Colab
            if IN_COLAB:
                console.print("\n📥 Downloading files...", style="cyan")
                colab_files.download(cleaned_path)
                colab_files.download(report_path)
                console.print("✓ Files downloaded!", style="green")
        
        # Ask if user wants to clean another file
        another = console.input("\n[bold yellow]Clean another file? (y/n):[/bold yellow] ").strip().lower()
        if another != 'y':
            console.print("\n👋 Goodbye!", style="cyan")
            break


if __name__ == "__main__":
    main()
