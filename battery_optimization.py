import pandas as pd

def get_battery_capacity():
    """ Prompt the user for the battery capacity in kWh. """
    capacity = float(input("Enter the battery capacity (in kWh): "))
    return capacity

def optimize_battery_usage(df, capacity):
    charge_rate = capacity / 2  # kWh per hour for a 2-hour battery
    depth_of_discharge = 0.9 * capacity
    battery_storage = depth_of_discharge  # Start fully charged

    # Initialize columns
    df['BatteryCharge_kWh'] = 0.0
    df['BatteryDischarge_kWh'] = 0.0
    df['BatteryStorage_kWh'] = battery_storage
    df['CostWithBattery'] = 0.0

    # Group by day to identify low cost charging hours
    df['date'] = df['DateTime'].dt.date
    for date, day_group in df.groupby('date'):
        # Find the hours with the lowest prices to charge the battery
        min_price_hours = day_group.nsmallest(int(charge_rate * 2), 'SpotPrice')  # Assumes 2 hours needed for full recharge
        for index, row in min_price_hours.iterrows():
            if battery_storage < depth_of_discharge:
                charge_needed = min(charge_rate, depth_of_discharge - battery_storage)
                df.at[index, 'BatteryCharge_kWh'] = charge_needed
                battery_storage += charge_needed * 0.95  # Accounting for round trip efficiency

        # Discharge during high price hours if beneficial
        max_price_hours = day_group.nlargest(int(charge_rate * 2), 'SpotPrice')
        for index, row in max_price_hours.iterrows():
            if battery_storage > 0:
                discharge_amount = min(charge_rate, battery_storage, row['KWH/hh (per half hour) '])
                df.at[index, 'BatteryDischarge_kWh'] = discharge_amount
                battery_storage -= discharge_amount / 0.95  # Discharge considering efficiency loss

    # Update the cost considering the battery usage
    df['CostWithBattery'] = (df['KWH/hh (per half hour) '] - df['BatteryDischarge_kWh']) * df['SpotPrice']
    df['BatteryStorage_kWh'] = battery_storage  # Update final battery storage level

    return df

# This function can be imported and used in tariff_comparison.py to augment the DataFrame with battery optimization details.
