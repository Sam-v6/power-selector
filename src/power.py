"""
Purpose: Determmines best power plan based on past consumption
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

        monthly_bill = ((self.range1*self.price1)/100)
        delta_power = monthly_consumption - self.range1

        # Less than range 1 upper band
        if monthly_consumption < self.range1:
            return monthly_bill

        # Less than range 2 upper band
        elif monthly_consumption < self.range2:
            monthly_bill = ((delta_power*self.price2)/100)+monthly_bill+self.base_charge

        # Exceed range 2 upper band
        else:
            monthly_bill = (((self.range2-self.range1)*self.price2)/100)+monthly_bill
            delta_power = (monthly_consumption - self.range2)
            monthly_bill = ((delta_power*self.price3)/100)+monthly_bill+self.base_charge

        # Subtract out monthly credit if it applies
        if monthly_consumption > self.bill_credit_lower and monthly_consumption < self.bill_credit_higher:
            monthly_bill = monthly_bill-self.bill_credit_price

        # Return 
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
    consumption_history = [900,1100,600,500,500,500,800,1000,600,600,400,650]
    consumption_list = []
    home_factor = 2.5
    for month in consumption_history:
        consumption_list.append(month*home_factor)

    # Init
    totals = {}

    #-----------------------Define power plan objects-----------------------
    # Coonsumption list, range 1 upper, range 1 price, range 2 upper, range 2 price, range 3 upper, range 3 price, base charge, bill credit price, bill credit lower, bill credit higher

    # TXU Energy
    smart_deal_12 = PowerPlan(consumption_list,1200,10.7,2000,5.4,5000,11.2,9.95,30,1200,5000) # also called TXU energy saver's discount 12
    totals["smart deal 12"] = smart_deal_12.calculate_year_totals()
    
    # Cirro
    cirro_smart_value = PowerPlan(consumption_list,1000,10.4972,2000,10.4972,5000,10.4972,0,30,1000,2000)
    totals["cirro smart value"] = cirro_smart_value.calculate_year_totals()

    # Gexa
    gexa_eco_saver = PowerPlan(consumption_list,1000,14.67,2000,14.67,5000,14.67,0,100,1500,5000)
    totals["gexa eco saver"] = gexa_eco_saver.calculate_year_totals()

    # Constellation New Energy
    constellation = PowerPlan(consumption_list,1000,12,2000,12,5000,12,0,50,1000,5000)
    totals["constellation"] = constellation.calculate_year_totals()

    # Change Power Saver
    change = PowerPlan(consumption_list,1000,11.099,2000,11.099,5000,11.099,4.95,100,2000,5000)
    totals["change"] = change.calculate_year_totals()

    #Constellation Current Plan
    currentconstellation = PowerPlan(consumption_list,1000,10.6,2000,10.6,5000,10.6,0,0,1000,5000)
    totals["currentconstellation"] = currentconstellation.calculate_year_totals()

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

    # Print winner winner chicken dinner
    for key in totals:
        print(key, totals[key][12])
    print("Optimal power plan is:", smallest_key, "with an annual price of:", smallest_sum)