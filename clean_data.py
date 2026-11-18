from pathlib import Path
import pandas as pd

"""
Program: clean_data.py
Description: A simple pandas DataFrame cleaning utility.
Author: Ben Goh
Version: 1.1

Purpose:
    Handles missing values, negative numbers and duplicate rows.
"""


def clean_data(df, filling_missing_numbers = True, convert_negatives = False, fill_missing_text = True, replace_text = 'TBD', remove_duplicates = True, option = 3 ):

    # option 1 : replaces the missing number with interpolation 
    # option 2 : replaces the missing number with most frequently used number
    # option 3 : replaces the missing number with the mean 
    # option 4: replaces missing number with the median
    # option 5: replaces missing number with the next number 
    # option 6: replaces missing number withthe  previous number

    processingfile = False
    input_path = None

    if isinstance(df, pd.DataFrame) :
         #original dataframe is copied to a new dataframe to avoid changing the original dataframe
         # origianl design
        df_copy = df.copy()
        print("Input is a DataFrame. Proceeding with cleaning.")
        print(type(df_copy))

    elif isinstance(df, (str, Path)):
        # check if the file is a CSV
        input_path = Path(df)
        if input_path.suffix.lower() != ".csv":
            print("Error: File must be a CSV.")
            return None
        else:
            try:
                # read the CSV file into a DataFrame
                df_copy = pd.read_csv(input_path)
                # set a flag to indicate that we are processing a file
                processingfile = True

            except FileNotFoundError:
                print("Error: File not found.")
                return None

            except Exception as e:
                print(f"Error reading CSV file: {e}")
                return None


    # print error if option is not 1 to 6
    if option not in range(1, 7):
        print("Error: Option must be between 1 and 6.")
        return None
    

    # records of changes
    total_cells_updated = 0 
    duplicate_rows = 0  
    text_cells_changed = 0 
    columns_with_empty_values = []
    changed_columns = []

    # scanning for empty columns
    for col in df_copy.columns:
        if df_copy[col].isna().all():
            columns_with_empty_values.append(col)
 
    
    #scanning numeric columns 
    nc = df_copy.select_dtypes(include=['number']).columns
               
    for col in  nc: 
        
        if not (df_copy[col].isna().all()) :
                
            # replace missing number with the differences between previous and after numbers
            if df_copy[col].isna().any() and filling_missing_numbers:
                mnu = df_copy[col].isna()
               
                            
                # Estimate missing values using interpolation
                if option == 1 : 
                    missing_before = df_copy[col].isna().sum()
                    df_copy[col] = df_copy[col].interpolate(limit_direction="both")
                    missing_after = df_copy[col].isna().sum()
                    total_cells_updated += missing_before -  missing_after
                    changed_columns.append(col)
                    
                # replace missing number with most frequently used
                elif option == 2:
                    mode_values = df_copy[col].mode()
                    if not mode_values.empty:
                        missing_before = df_copy[col].isna().sum()
                        df_copy[col] = df_copy[col].fillna(mode_values.iloc[0])
                        missing_after = df_copy[col].isna().sum()
                        total_cells_updated += missing_before - missing_after
                        changed_columns.append(col)
                    
                # replace missing number with mean
                elif option == 3: 
                    missing_before = df_copy[col].isna().sum()
                    df_copy.loc[mnu,col] = df_copy[col].mean()
                    missing_after = df_copy[col].isna().sum()
                    total_cells_updated += missing_before - missing_after
                    changed_columns.append(col)
    
                # replace missing number with the median     
                elif option == 4: 
                    missing_before = df_copy[col].isna().sum()
                    df_copy.loc[mnu, col] = df_copy[col].median()
                    missing_after = df_copy[col].isna().sum()
                    total_cells_updated += missing_before - missing_after
                    changed_columns.append(col)
                
                # replace missing number with next number
                elif option == 5: 
                    missing_before = df_copy[col].isna().sum()
                    df_copy[col] = df_copy[col].bfill().ffill()
                    missing_after = df_copy[col].isna().sum()
                    total_cells_updated += missing_before - missing_after
                    changed_columns.append(col)
                # replace missing number with the previous number
                elif option == 6:
                    missing_before = df_copy[col].isna().sum()
                    df_copy[col] = df_copy[col].ffill().bfill()
                    missing_after = df_copy[col].isna().sum()
                    total_cells_updated += missing_before - missing_after
                    changed_columns.append(col)
                              
            # updating negative numbers to positivies
            if df_copy[col].lt(0).any() and convert_negatives:
                changed_columns.append(col)
                neg = df_copy[col].lt(0)
                negative_before = df_copy[col].lt(0).sum()
                df_copy.loc[neg, col] = df_copy.loc[neg, col].abs()
                negative_after = df_copy[col].lt(0).sum()
                total_cells_updated += negative_before - negative_after
            
    
    #scan text columns for missing values update them as set by the user in the configuration parameter      
    tc = df_copy.select_dtypes(include=['object', 'string']).columns
    for col in tc: 
        if not(df_copy[col].isna().all()): 
            if df_copy[col].isna().any() and fill_missing_text:
                changed_columns.append(col)
                missing_before = df_copy[col].isna().sum()
                df_copy[col] = df_copy[col].fillna(replace_text)
                missing_after = df_copy[col].isna().sum()
                text_cells_changed += missing_before - missing_after
    
    #scanning for duplicates 
    if df_copy.duplicated().any() and remove_duplicates :
        duplicate_rows = len(df_copy[df_copy.duplicated()])
        df_copy = df_copy.drop_duplicates()
          
   
    print("Data Cleaning Summary") 
    print('Numeric cells updated: ',total_cells_updated)
    print('Text cells updated: ', text_cells_changed)   
    print('The duplicated rows have been removed: ', duplicate_rows)
    print('Found empty columns:', columns_with_empty_values)
    print('Columns that have changed during data cleaning: ', list(dict.fromkeys(changed_columns)))

    # save the cleaned data to a new CSV file if the input was a file path
    if processingfile == True:
        output_file = input_path.with_name(input_path.stem + "_cleaned.csv")
        try:
            df_copy.to_csv(output_file, index=False)
            print(f"Cleaned file saved: {output_file}")
        except Exception as e:
            print(f"Error saving CSV file: {e}")
        return None

    # return the cleaned DataFrame if the input was a DataFrame
    return df_copy
