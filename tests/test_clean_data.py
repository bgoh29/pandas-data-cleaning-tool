# Import the cleaning function
from clean_data import clean_data
import pandas as pd


# test 1
def test_original_dataframe_unchanged():

    original = pd.DataFrame({
        'Age': [25, 30, None, 40]
    })

    expected = original.copy()

    result = clean_data(original)

    pd.testing.assert_frame_equal(original, expected)

# test 2
def test_original_dataframe_text_unchanged():

    original = pd.DataFrame({
        'Name': ['Aaron', 'Bob', None, 'Daniel']
    })

    expected = pd.DataFrame({ 
        'Name': ['Aaron', 'Bob', None, 'Daniel']
    })

    result = clean_data(original,fill_missing_text=False)

    pd.testing.assert_frame_equal(original, expected)


# test 3
def test_missing_values_filled_with_mean():
    df = pd.DataFrame({
        'Age': [25, 30, None, 40, 45]
    })

    result = clean_data(df, option=3)

    expected = pd.DataFrame({
        'Age': [25.0, 30.0, 35.0, 40.0, 45.0]
    })

    pd.testing.assert_frame_equal(result, expected)

# test 4
def test_negative_numbers_converted():
    df = pd.DataFrame({
        'Score': [10, 20, -5, 30]
    })

    result = clean_data(df, convert_negatives=True)

    expected = pd.DataFrame({
        'Score': [10, 20, 5, 30]
    })

    pd.testing.assert_frame_equal(result, expected)


# test 5
def test_negative_numbers_converted_turned_off():
    df = pd.DataFrame({
        'Score': [10, 20, -5, 30]
    })

    result = clean_data(df, convert_negatives=False)

    expected = pd.DataFrame({
        'Score': [10, 20, - 5, 30]
    })

    pd.testing.assert_frame_equal(result, expected)




# test 6
def test_missing_text_replaced():
    df = pd.DataFrame({
        'Department': ['IT', None, 'HR']
    })

    result = clean_data(df, replace_text='Unknown')

    expected = pd.DataFrame({
        'Department': ['IT', 'Unknown', 'HR']
    })

    pd.testing.assert_frame_equal(result, expected)


# test 7
def test_duplicate_rows_removed():
    df = pd.DataFrame({
        'Name': ['John', 'Mary', 'John'],
        'Age': [25, 30, 25]
    })

    result = clean_data(df)

    expected = pd.DataFrame({
        'Name': ['John', 'Mary'],
        'Age': [25, 30]
    })

    pd.testing.assert_frame_equal(result, expected)



# test 8
def test_duplicate_rows_removed_disabled():
    df = pd.DataFrame({
        'Name': ['John', 'Mary', 'John'],
        'Age': [25, 30, 25]
    })

    result = clean_data(df, remove_duplicates=False)

    expected = pd.DataFrame({
        'Name': ['John', 'Mary', 'John'],
                'Age': [25, 30, 25]
    })

    pd.testing.assert_frame_equal(result, expected)


# test 9
def test_missing_value_with_interpolation():
    df = pd.DataFrame({
        'Score': [10, 20, None, 30]
    })

    result = clean_data(df, option=1)

    expected = pd.DataFrame({
        'Score': [10.0, 20.0, 25.0, 30.0]
    })

    pd.testing.assert_frame_equal(result, expected)


# test 10
def test_missing_values_filled_with_most_frequently_used_number():
    df = pd.DataFrame({
        'Score': [20, 20, None, 30],
        'Player':['Jess','Ben','Warren','Sandra']
    })

    result = clean_data(df, option=2)

    expected = pd.DataFrame({
        'Score': [20.0, 20.0, 20.0, 30.0],
        'Player':['Jess','Ben','Warren','Sandra']
    })

    pd.testing.assert_frame_equal(result, expected)


# test 11
def test_missing_values_filled_with_median():
    df = pd.DataFrame({
        'Salary': [85200, 92000, None, 130000],
        'Staff':['Jess','Ben','Warren','Sandra']
    })

    result = clean_data(df, option=4)

    expected = pd.DataFrame({
        'Salary': [85200.00, 92000.00, 92000.00, 130000.00],
        'Staff':['Jess','Ben','Warren','Sandra']
    })

    pd.testing.assert_frame_equal(result, expected)


# test 12
def test_missing_values_filled_with_next_valid_number():
    df = pd.DataFrame({
        'Salary': [85200, 50000, 92000, None, 130000], 
         'Staff':['Jess','Ben','Warren','Sandra','Ella']
        
     
    })

    result = clean_data(df, option=5)

    expected = pd.DataFrame({
        'Salary': [85200.00, 50000.00, 92000.00, 130000.00, 130000.00],
        'Staff':['Jess','Ben','Warren','Sandra','Ella']
        
    })

    pd.testing.assert_frame_equal(result, expected)


# test 13
def test_missing_values_filled_with_previous_valid_number():
    df = pd.DataFrame({
        'Salary': [85200, 50000, 92000, None, 130000], 
         'Staff':['Jess','Ben','Warren','Sandra','Ella']
        
     
    })

    result = clean_data(df, option=6)

    expected = pd.DataFrame({
        'Salary': [85200.00, 50000.00, 92000.00, 92000.00, 130000.00],
        'Staff':['Jess','Ben','Warren','Sandra','Ella']
        
    })

    pd.testing.assert_frame_equal(result, expected)


# test 14
def test_empty_values_column_unchanged():
    df = pd.DataFrame({
        'Score': [20, 20, None, 30],
        'Player':['Jess','Ben','Warren','Sandra'],
        'tournament':[None, None, None, None]
    })

    result = clean_data(df, option=2)

    expected = pd.DataFrame({
        'Score': [20.0, 20.0, 20.0, 30.0],
        'Player':['Jess','Ben','Warren','Sandra'],
        'tournament':[None, None, None, None]
    })

    pd.testing.assert_frame_equal(result, expected)



# test 15
def test_invalid_option():
    df = pd.DataFrame({
        'Age': [25, 30, None]
    })

    result = clean_data(df, option=7)

    assert result is None

# test 16
def test_invalid_option_lower_bound():
    df = pd.DataFrame({
        'Age': [25, 30, None]
    })

    result = clean_data(df, option=0)

    assert result is None

# test 17
def test_remove_duplicated_row_after_replacement():
    df = pd.DataFrame({
         'Score' : [25, None, 30, 40, 5]
    })

    result = clean_data(df)

    expected = pd.DataFrame({
        'Score': [25.0, 30.0, 40.0, 5.0]
    }, index=[0, 2, 3, 4])

    pd.testing.assert_frame_equal(result, expected)

