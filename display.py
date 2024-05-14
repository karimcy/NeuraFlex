import pandas as pd
import matplotlib.pyplot as plt

# Function to prompt for new fixed price and adjust the fixed cost accordingly
def adjust_fixed_price(results_df, original_fixed_price):
    new_fixed_price = float(input("Enter the new fixed price per KWH for adjustment: "))
    adjustment_factor = new_fixed_price / original_fixed_price
    results_df['Fixed Price'] *= adjustment_factor
    results_df['Agile (Spot) Price'] /= 100  # Adjusting the Spot Price to be on the same scale
    return results_df

# Function to calculate the percentage difference between spot and fixed prices
def calculate_percentage_difference(df):
    df['Percentage Difference'] = ((df['Agile (Spot) Price'] - df['Fixed Price']) / df['Fixed Price']) * 100
    return df

# Function to plot the data on a bar chart
def plot_data(df):
    # Define the percentage range bins and labels
    bins = [-50, -40, -30, -20, -10, 0, 10, 20, 30, 40]
    labels = ['-50% to -40%', '-40% to -30%', '-30% to -20%', '-20% to -10%', '-10% to 0%', '0% to 10%', '10% to 20%', '20% to 30%', '30% to 40%']
    df['Percentage Range'] = pd.cut(df['Percentage Difference'], bins=bins, labels=labels, include_lowest=True)

    # Group by the percentage range and count the number of houses in each
    count_per_range = df['Percentage Range'].value_counts().sort_index()

    # Plot the bar chart
    plt.bar(count_per_range.index.astype(str), count_per_range.values)
    plt.xlabel('Percentage Difference Range')
    plt.ylabel('Number of Houses')
    plt.title('Comparison of Spot Price Savings Against Fixed Price')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Main execution
if __name__ == '__main__':
    # Load the results CSV file
    results_path = '/Users/karimcy/Downloads/household_costs_comparison.csv'
    results_df = pd.read_csv(results_path)

    # Assume the original fixed price was asked during the previous step (e.g., 0.25)
    original_fixed_price = 0.25  # Update this if needed

    # Adjust the fixed prices based on new user input
    adjusted_results_df = adjust_fixed_price(results_df, original_fixed_price)

    # Calculate the percentage difference between spot and fixed prices
    percentage_df = calculate_percentage_difference(adjusted_results_df)

    # Plot the data
    plot_data(percentage_df)
