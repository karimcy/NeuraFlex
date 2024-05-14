import pandas as pd

# Function to load consumption data
def load_consumption_data(file_path):
    df = pd.read_csv(file_path, parse_dates=['DateTime'], dayfirst=True)
    df['KWH/hh (per half hour) '] = pd.to_numeric(df['KWH/hh (per half hour) '].replace('Null', '0'), errors='coerce')
    df['DateTime'] = df['DateTime'] + pd.DateOffset(years=8)
    df['LCLid'] = df['LCLid'].astype(str)
    # Retrieve a list of unique LCLids
    unique_lclids = df['LCLid'].unique()
    # Select LCLids from 1500th to 1550th
    selected_lclids = unique_lclids[1499:1550]  # Indexing starts at 0, hence 1499
    df = df[df['LCLid'].isin(selected_lclids)]
    return df

# Function to load price data
def load_price_data(file_path):
    price_df = pd.read_csv(file_path, parse_dates=['DateTime'], dayfirst=True)
    price_df['SpotPrice'].fillna(method='ffill', inplace=True)
    return price_df

# Function to align data based on 'DateTime'
def align_data(consumption_df, price_df):
    aligned_df = consumption_df.merge(price_df, on='DateTime')
    return aligned_df

# Function to calculate total cost for each household based on spot pricing
def calculate_total_cost(aligned_df):
    aligned_df['TotalCost'] = aligned_df['KWH/hh (per half hour) '] * aligned_df['SpotPrice']
    total_cost_per_household = aligned_df.groupby('LCLid')['TotalCost'].sum()
    return total_cost_per_household

# Function to compare total costs between spot pricing and a fixed price scheme
def compare_fixed_price(consumption_df, fixed_price):
    consumption_df['FixedCost'] = consumption_df['KWH/hh (per half hour) '] * fixed_price
    total_fixed_cost_per_household = consumption_df.groupby('LCLid')['FixedCost'].sum()
    return total_fixed_cost_per_household
