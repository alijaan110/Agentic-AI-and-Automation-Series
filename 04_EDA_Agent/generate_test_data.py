"""
Generate sample test data for EDA Agent testing
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data(n_rows: int = 1000, output_path: str = "sample_data.csv") -> None:
    """
    Generate realistic sample dataset for EDA testing.
    
    Args:
        n_rows: Number of rows to generate
        output_path: Where to save the CSV
    """
    np.random.seed(42)
    
    # Generate dates
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(n_rows)]
    
    # Generate data with intentional patterns
    data = {
        # Datetime column
        'transaction_date': dates,
        
        # Numeric columns with different distributions
        'age': np.random.normal(35, 12, n_rows).clip(18, 80).astype(int),
        'income': np.random.lognormal(10.5, 0.5, n_rows).astype(int),
        'transaction_amount': np.random.gamma(2, 50, n_rows).round(2),
        'credit_score': np.random.normal(700, 50, n_rows).clip(300, 850).astype(int),
        
        # Categorical columns
        'customer_segment': np.random.choice(
            ['Premium', 'Standard', 'Basic', 'New'], 
            n_rows, 
            p=[0.15, 0.35, 0.35, 0.15]
        ),
        'region': np.random.choice(
            ['North', 'South', 'East', 'West'], 
            n_rows,
            p=[0.3, 0.25, 0.25, 0.2]
        ),
        'product_category': np.random.choice(
            ['Electronics', 'Clothing', 'Food', 'Books', 'Home'], 
            n_rows
        ),
        
        # Boolean column
        'is_premium_member': np.random.choice([True, False], n_rows, p=[0.3, 0.7]),
        
        # Column with correlation to age
        'years_customer': (
            (np.random.normal(35, 12, n_rows) / 10) + 
            np.random.normal(0, 2, n_rows)
        ).clip(0, 20).round(1),
    }
    
    df = pd.DataFrame(data)
    
    # Add missing values (realistic pattern)
    # More missing in recent transactions
    missing_mask = np.random.random(n_rows) < 0.05
    df.loc[missing_mask, 'transaction_amount'] = np.nan
    
    # Random missing in income
    missing_mask = np.random.random(n_rows) < 0.08
    df.loc[missing_mask, 'income'] = np.nan
    
    # Add some duplicates
    n_dupes = int(n_rows * 0.02)  # 2% duplicates
    dupe_indices = np.random.choice(df.index, n_dupes, replace=False)
    df = pd.concat([df, df.loc[dupe_indices]], ignore_index=True)
    
    # Add outliers
    outlier_indices = np.random.choice(df.index, 20, replace=False)
    df.loc[outlier_indices, 'transaction_amount'] = np.random.uniform(5000, 10000, 20)
    
    # Save
    df.to_csv(output_path, index=False)
    print(f"✅ Generated {len(df):,} rows → {output_path}")
    print(f"   Columns: {', '.join(df.columns)}")
    print(f"   Missing values: {df.isna().sum().sum():,} cells")
    print(f"   Duplicates: {df.duplicated().sum():,} rows")
    
    return df


if __name__ == "__main__":
    # Generate test data
    generate_sample_data(n_rows=1000, output_path="sample_data.csv")
    
    # For larger testing
    # generate_sample_data(n_rows=50000, output_path="sample_data_large.csv")
