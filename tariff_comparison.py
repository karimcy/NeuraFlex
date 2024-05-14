import pandas as pd

# Assuming these functions are defined in your 'data_processing' module
from data_processing import load_consumption_data, load_price_data, align_data, calculate_total_cost, compare_fixed_price

# Importing battery operations
from battery_optimization import optimize_battery_usage, get_battery_capacity

# Prompt for user input for the fixed price and battery capacity
fixed_price = float(input("Enter the fixed price per KWH: "))
battery_capacity = get_battery_capacity()

# Load the data
consumption_df = load_consumption_data('/Users/karimcy/Downloads/167m row UKPN household data.csv')
price_df = load_price_data('/Users/karimcy/Downloads/Octopus agile pricing.csv')

# Calculate total consumption per household
total_consumption_per_household = consumption_df.groupby('LCLid')['KWH/hh (per half hour) '].sum()

# Align data and calculate costs
aligned_df = align_data(consumption_df, price_df)
total_cost_spot = calculate_total_cost(aligned_df)
total_cost_fixed = compare_fixed_price(consumption_df, fixed_price)

# Calculate costs with the battery
optimized_df = optimize_battery_usage(aligned_df.copy(), battery_capacity)
total_cost_with_battery = optimized_df['CostWithBattery'].groupby(optimized_df['LCLid']).sum()

# Ensure all Series are aligned by reindexing based on the comprehensive set of LCLids
all_lclids = consumption_df['LCLid'].unique()
total_cost_spot = total_cost_spot.reindex(all_lclids, fill_value=0)
total_cost_fixed = total_cost_fixed.reindex(all_lclids, fill_value=0)
total_cost_with_battery = total_cost_with_battery.reindex(all_lclids, fill_value=0)
total_consumption_per_household = total_consumption_per_household.reindex(all_lclids, fill_value=0)

# Combine results into a DataFrame
results_df = pd.DataFrame({
    'House (LCLid)': all_lclids,
    'Total Consumption (KWH)': total_consumption_per_household.values,
    'Agile (Spot) Price': total_cost_spot.values,
    'Fixed Price': total_cost_fixed.values,
    'Cost With Battery': total_cost_with_battery.values
})

# Save the DataFrame to a CSV file
results_df.to_csv('/Users/karimcy/Downloads/household_costs_comparison.csv', index=False)
print("Results have been saved to /Users/karimcy/Downloads/household_costs_comparison.csv")
