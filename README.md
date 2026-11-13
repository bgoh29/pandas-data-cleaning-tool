# Pandas Data Cleaning Tool

## Project Overview

Raw data is rarely perfect. Before using it for data analysis or machine learning, it is often necessary to perform data preprocessing and cleaning.

This project provides a simple Python tool to assist with some common data-cleaning tasks, including handling missing values, converting negative numbers to positive values, identifying empty columns, and removing duplicate rows.

The tool is developed using Python and pandas as a practical exercise in data preprocessing and data quality management.

## Requirements

1. Python 3 installed.
2. Python package: `pandas`.
3. Input data must be provided as a pandas DataFrame.

## Installation

Clone this repository:

    git clone https://github.com/bgoh29/pandas-data-cleaning-tool.git

Navigate to the project directory:

    cd pandas-data-cleaning-tool

Install the required packages:

    python -m pip install -r requirements.txt

## Features

The tool provides the following data-cleaning capabilities:

1. **Replace missing numeric values** – Supports six different methods: interpolation, mode (most frequently occurring value), mean, median, next valid value, and previous valid value.
2. **Replace missing text values** – Replaces missing text values with a generic value specified by the user.
3. **Convert negative numbers to positive values** – Converts negative numeric values to their absolute values.
4. **Identify empty columns** – Reports columns that contain no values.
5. **Remove duplicate rows** – Identifies and removes duplicated rows, retaining the first occurrence.

The function also displays a summary of the cleaning operations performed, including the number of numeric and text cells updated, duplicate rows removed, and columns identified as empty or changed.

## Usage

The function is called using the following parameters:

```python
clean_data(
    df,
    filling_missing_numbers=True,
    convert_negatives=False,
    fill_missing_text=True,
    replace_text='TBD',
    remove_duplicates=True,
    option=3
)
```

### Function Parameters

| Parameter | Description | Default |
|---|---|---|
| `df` | The pandas DataFrame to be cleaned. | Required |
| `filling_missing_numbers` | Enables or disables replacement of missing numeric values. | `True` |
| `convert_negatives` | Converts negative numeric values to absolute values. | `False` |
| `fill_missing_text` | Enables or disables replacement of missing text values. | `True` |
| `replace_text` | The replacement value for missing text. Can be customised by the user. | `'TBD'` |
| `remove_duplicates` | Enables or disables removal of duplicate rows. | `True` |
| `option` | Selects the method used to replace missing numeric values. | `3` |

### Numeric Replacement Options

The `option` parameter determines how missing numeric values are handled.

| Option | Method | Description |
|---|---|---|
| 1 | Interpolation | Estimates missing values based on surrounding values. |
| 2 | Mode | Replaces missing values with the most frequently occurring value. |
| 3 | Mean | Replaces missing values with the column average. |
| 4 | Median | Replaces missing values with the middle value. |
| 5 | Next valid value | Uses the next available value to fill missing values, then fills remaining gaps using the previous available value. |
| 6 | Previous valid value | Uses the previous available value to fill missing values, then fills remaining gaps using the next available value. |

**Note:** Options 5 and 6 use pandas' backward-fill and forward-fill operations. The result depends on the order of rows in the DataFrame.

## Example

```python
import pandas as pd
from clean_data import clean_data

data = {
    'Age': [25, 30, None, 40, 45],
    'Salary': [5000, None, 6000, 7000, 8000],
    'Department': ['IT', 'HR', None, 'IT', 'HR'],
    'Score': [10, 20, -5, 30, 40]
}

df = pd.DataFrame(data)

# Clean the DataFrame using interpolation
cleaned_df = clean_data(
    df,
    option=1,
    convert_negatives=True
)

print(cleaned_df)
```
## Testing

The project uses pytest for automated testing.

To run the tests:

    python -m pytest -v

The tests cover:
- Original DataFrame numbers remain unchanged.
- Original DataFrame texts remain unchanged.
- Missing numeric values are replaced correctly.
- Negative numbers are converted when enabled.
- Missing text values are replaced.
- Duplicate rows are removed.
- missing numbers with interpolation.
- missing values with most frequently used number.
- missing values with median.
- missing value with next valid number.
- missing value with previous valid number. 
- Invalid options are handled.

## Important Notes

- The function creates a copy of the input DataFrame. The original DataFrame remains unchanged.
- Missing numeric values are processed only in numeric columns.
- Missing text values are processed in object and string columns.
- Columns containing only missing values are reported but are not automatically populated.
- Negative-value conversion applies to all numeric columns when enabled. Use this option carefully, as negative values may be meaningful in some datasets.
- If an invalid numeric replacement option is supplied, the function displays an error message and returns `None`.

## Project Status

This is an ongoing learning project. Further improvements may include more detailed cleaning reports, configurable cleaning methods for individual columns, and additional data-validation capabilities.
# pandas-data-cleaning-tool
