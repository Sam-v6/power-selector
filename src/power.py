"""
Purpose: Determmines best power plan based on past consumption (pull from powertochoose)
Author: Syam Evani
"""

# Standard imports
import os

# Additional imports
import numpy as np

# Local imports


# Class to init all power plan objects
class PowerPlan():

    # Init
    def __init__(self,consumption_list,range1,price1,range2,price2,range3,price3,base_charge,bill_credit_price,bill_credit_lower,bill_credit_higher):
        self.consumption_list = consumption_list
        self.range1 = range1
        self.price1 = price1
        self.range2 = range2
        self.price2 = price2
        self.range3 = range3
        self.price3 = price3
        self.base_charge = base_charge
        self.bill_credit_price = bill_credit_price
        self.bill_credit_lower = bill_credit_lower
        self.bill_credit_higher = bill_credit_higher

    # Calculate monthly bill
    def calcluate_monthly_bill(self,monthly_consumption):

        #--------------------------------------------------------
        # Calculate price based on ranges
        #--------------------------------------------------------

        # Less than range 1 upper band
        if monthly_consumption <= self.range1:
            monthly_bill = ((monthly_consumption * self.price1)/100)

            # First range calc
            monthly_bill = ((self.range1 * self.price1)/100)

        # Less than range 2 upper band
        elif monthly_consumption >  self.range1 and monthly_consumption <= self.range2:

            # First range calc
            monthly_bill = ((self.range1 * self.price1)/100)

            # Second range calc
            delta_power = monthly_consumption - self.range1
            monthly_bill = ((delta_power*self.price2)/100) + monthly_bill

        # Exceed range 2 upper band
        else:

            # First range calc
            monthly_bill = ((self.range1 * self.price1)/100)

            # Second range calc
            delta_power = self.range2 - self.range1
            monthly_bill = ((delta_power*self.price2)/100) + monthly_bill

            # Calculate final range amount
            delta_power = (monthly_consumption - self.range2)
            monthly_bill = ((delta_power*self.price3)/100) + monthly_bill

        # Add in base charge
        monthly_bill = monthly_bill + self.base_charge

        #--------------------------------------------------------
        # Calculate credits
        #--------------------------------------------------------
        # Subtract out monthly credit if it applies
        if monthly_consumption > self.bill_credit_lower and monthly_consumption <= self.bill_credit_higher:
            monthly_bill = monthly_bill-self.bill_credit_price

        #--------------------------------------------------------
        # Calculate distro costs
        #--------------------------------------------------------
        # $4.39 Centerpoint TDU charges per month July 28 2024
        # 4.041 cents per kWh Centerpoint charge
        monthly_bill = monthly_bill + 4.39 + ((monthly_consumption*4.041)/100)

        # Return (appears to be missing some additional billing charge, but would all be equal to plans)
        return monthly_bill

    # Calculate yearly consumption month by month
    def calculate_year_totals(self):

        # Init
        month_bill_list = []

        # Append monthly bill
        for monthly_consumption in self.consumption_list:
            month_bill = self.calcluate_monthly_bill(monthly_consumption)
            month_bill_list.append(month_bill)

        # Calculate year total
        year_sum = 0
        for i in range(0,len(month_bill_list)):
            year_sum = month_bill_list[i] + year_sum
        month_bill_list.append(year_sum)

        # Return
        return month_bill_list

# Main
if __name__ =="__main__":

    #-----------------------Define consumption list-----------------------
    consumption_history = [
        271,    # January
        368,    # February
        456,    # March
        1156,   # April
        2121,   # May
        2540,   # June
        2540,   # July
        2510,   # August
        2256,   # September
        1000,    # October
        394,    # November
        481     # December
        ]    
    consumption_list = []
    home_factor = 1
    for month in consumption_history:
        consumption_list.append(month*home_factor)

    # Init
    totals = {}

    #-----------------------Define power plan objects-----------------------
    # Coonsumption list, range 1 upper, range 1 price, range 2 upper, range 2 price, range 3 upper, range 3 price, base charge, bill credit price, bill credit lower, bill credit higher

    # Last year comparison - TXU Energy (also called TXU energy saver's discount 12)
    # savers_choice_12 = PowerPlan(consumption_list,
    #                           1200,         # [kWh]             First range ceiling
    #                           10.7,         # [cents/kWh]       First range cost
    #                           2000,         # [kWh]             Second range ceiling
    #                           5.4,          # [cents/kWh]       Second range cost
    #                           5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
    #                           11.2,         # [cents/kWh]       Third range cost 
    #                           9.95,         # [dollars/month]   Base charge per month 
    #                           30,           # [dollars/month]   Bill credit price
    #                           1200,         # [kWh]             Bill credit lower threshold (must be above this)
    #                           5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    # totals["savers_choice_12"] = savers_choice_12.calculate_year_totals()
    
   
   # sofed_better_rate_10
    sofed_better_rate_10 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              7.7745,       # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              7.7745,       # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              7.7745,       # [cents/kWh]       Third range cost 
                              4.95,         # [dollars/month]   Base charge per month 
                              0.00,         # [dollars/month]   Bill credit price (there's a usage charge that only applies if <1000 kWh so I apply it like this)
                              1000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["sofed_better_rate_10"] = sofed_better_rate_10.calculate_year_totals()

 # frontier_power_saver_8
    frontier_power_saver_8 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              5.15,       # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              5.15,       # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              5.15,       # [cents/kWh]       Third range cost 
                              0.00,         # [dollars/month]   Base charge per month 
                              0.00,         # [dollars/month]   Bill credit price (there's a usage charge that only applies if <1000 kWh so I apply it like this)
                              1000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["frontier_power_saver_8"] = frontier_power_saver_8.calculate_year_totals()

 # gexa_eco_choice_8
    gexa_eco_choice_8 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              5.25,       # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              5.25,       # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              5.25,       # [cents/kWh]       Third range cost 
                              0.00,         # [dollars/month]   Base charge per month 
                              0.00,         # [dollars/month]   Bill credit price (there's a usage charge that only applies if <1000 kWh so I apply it like this)
                              1000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["gexa_eco_choice_8"] = gexa_eco_choice_8.calculate_year_totals()

 # shell_standard_3
    shell_standard_3 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              5.4,       # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              5.4,       # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              5.4,       # [cents/kWh]       Third range cost 
                              0.00,         # [dollars/month]   Base charge per month 
                              0.00,         # [dollars/month]   Bill credit price (there's a usage charge that only applies if <1000 kWh so I apply it like this)
                              1000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["shell_standard_3"] = shell_standard_3.calculate_year_totals()

 # infuse_energy_3
    infuse_energy_3 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              5.175,       # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              5.175,       # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              5.175,       # [cents/kWh]       Third range cost 
                              4.00,         # [dollars/month]   Base charge per month 
                              0.00,         # [dollars/month]   Bill credit price (there's a usage charge that only applies if <1000 kWh so I apply it like this)
                              1000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["infuse_energy_3"] = infuse_energy_3.calculate_year_totals()

 # bkv_daisy_3
    bkv_daisy_3 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              5.62452,       # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              5.62452,       # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              5.62452,       # [cents/kWh]       Third range cost 
                              0.00,         # [dollars/month]   Base charge per month 
                              0.00,         # [dollars/month]   Bill credit price (there's a usage charge that only applies if <1000 kWh so I apply it like this)
                              1000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["bkv_daisy_3"] = bkv_daisy_3.calculate_year_totals()

 # gexa_eco_9
    gexa_eco_9 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              5.95,       # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              5.95,       # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              5.95,       # [cents/kWh]       Third range cost 
                              0.00,         # [dollars/month]   Base charge per month 
                              0.00,         # [dollars/month]   Bill credit price (there's a usage charge that only applies if <1000 kWh so I apply it like this)
                              1000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["gexa_eco_9"] = gexa_eco_9.calculate_year_totals()

# constellation_10
    constellation_10 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              6.0,       # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              6.0,       # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              6.0,       # [cents/kWh]       Third range cost 
                              0.00,         # [dollars/month]   Base charge per month 
                              0.00,         # [dollars/month]   Bill credit price (there's a usage charge that only applies if <1000 kWh so I apply it like this)
                              1000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["constellation_10"] = constellation_10.calculate_year_totals()

    #-----------------------Find optimal plan-----------------------
    # Initialize variables to track the smallest sum and corresponding key
    smallest_sum = float('inf')  # Set to positive infinity initially
    smallest_key = None

    # Iterate through each key-value pair in the dictionary
    for key, value in totals.items():
        # Extract the last element (sum) from the list
        sum_value = value[-1]
        
        # Compare the sum_value with the current smallest_sum
        if sum_value < smallest_sum:
            smallest_sum = sum_value
            smallest_key = key

    # Sort the plans by cost
    sorted_plans = sorted(totals.items(), key=lambda item: item[1][-1])

    # Print plans from least to most expensive
    for key, value in sorted_plans:
        print(f"Plan: {key} with cost: ${value[-1]}")
    print("Optimal power plan is:", smallest_key, "with an annual price of:", smallest_sum)