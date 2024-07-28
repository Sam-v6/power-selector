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
        1178,   # September
        383,    # October
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
    
    # TXU Energy Smart Edge 12
    savers_choice_12 = PowerPlan(consumption_list,
                              1200,         # [kWh]             First range ceiling
                              14.0,         # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              22.8,         # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              22.8,         # [cents/kWh]       Third range cost 
                              9.95,         # [dollars/month]   Base charge per month 
                              30,           # [dollars/month]   Bill credit price
                              800,          # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["txu_smart_edge_12"] = savers_choice_12.calculate_year_totals()

     # TXU energy price saver 18
    txu_energy_price_saver_18 = PowerPlan(consumption_list,
                              1200,         # [kWh]             First range ceiling
                              15.5,         # [cents/kWh]       First range cost
                              2000,         # [kWh]             Second range ceiling
                              7.8,          # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              16.3,         # [cents/kWh]       Third range cost 
                              9.95,         # [dollars/month]   Base charge per month 
                              30,           # [dollars/month]   Bill credit price
                              1200,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["txu_energy_price_saver_18"] = txu_energy_price_saver_18.calculate_year_totals()

    # txu_simple_rate_12
    txu_simple_rate_12 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              14.8,         # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              14.8,         # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              14.8,         # [cents/kWh]       Third range cost 
                              9.95,         # [dollars/month]   Base charge per month 
                              0,            # [dollars/month]   Bill credit price
                              800,          # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["txu_simple_rate_12"] = txu_simple_rate_12.calculate_year_totals()

    # txu_simple_rate_24
    txu_smart_deal_24 = PowerPlan(consumption_list,
                              1200,         # [kWh]             First range ceiling
                              17.8,         # [cents/kWh]       First range cost
                              2000,         # [kWh]             Second range ceiling
                              8.9,          # [cents/kWh]       Second range cost
                              2000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              18.7,         # [cents/kWh]       Third range cost 
                              9.95,         # [dollars/month]   Base charge per month 
                              30,           # [dollars/month]   Bill credit price
                              1200,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["txu_smart_deal_24"] = txu_smart_deal_24.calculate_year_totals()

    # txu_energy_price_saver_24
    txu_energy_price_saver_24 = PowerPlan(consumption_list,
                              1200,         # [kWh]             First range ceiling
                              17.2,         # [cents/kWh]       First range cost
                              2000,         # [kWh]             Second range ceiling
                              8.6,          # [cents/kWh]       Second range cost
                              2000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              18.1,         # [cents/kWh]       Third range cost 
                              9.95,         # [dollars/month]   Base charge per month 
                              30,           # [dollars/month]   Bill credit price
                              1200,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["txu_energy_price_saver_24"] = txu_energy_price_saver_24.calculate_year_totals()


    # Gexa Energy Eco Saver Plus 12
    gexa_eco_saver_plus_12 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              19.18,        # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              19.18,        # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              19.18,        # [cents/kWh]       Third range cost 
                              0,            # [dollars/month]   Base charge per month 
                              125,          # [dollars/month]   Bill credit price
                              1000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["gexa_eco_saver_plus_12"] = gexa_eco_saver_plus_12.calculate_year_totals()

    # gexa_save_ev_choice_12
    gexa_save_ev_choice_12 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              11.2,         # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              11.2,         # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              11.2,         # [cents/kWh]       Third range cost 
                              0,            # [dollars/month]   Base charge per month 
                              0,            # [dollars/month]   Bill credit price
                              1000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["gexa_save_ev_choice_12"] = gexa_save_ev_choice_12.calculate_year_totals()

    # Gexa Energy prime preferred plus 12 (100% Renewable)
    gexa_prime_preferred_plus_12 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              19.42,        # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              19.18,        # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              19.18,        # [cents/kWh]       Third range cost 
                              0,            # [dollars/month]   Base charge per month 
                              125,          # [dollars/month]   Bill credit price
                              2000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["gexa_prime_preferred_plus_12"] = gexa_prime_preferred_plus_12.calculate_year_totals()

    # 4Change Energy Maxx Saver Select 12
    four_change_energy_maxx_saver_select_12 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              16.6721,      # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              16.6721,      # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              16.6721,      # [cents/kWh]       Third range cost 
                              0,            # [dollars/month]   Base charge per month 
                              100,          # [dollars/month]   Bill credit price
                              1000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["four_change_energy_maxx_saver_select_12"] = four_change_energy_maxx_saver_select_12.calculate_year_totals()
    
    # Frontier Utilities Saver Plus 12
    frontier_saver_plus_12 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              19.18,        # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              19.18,        # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              19.18,        # [cents/kWh]       Third range cost 
                              0,            # [dollars/month]   Base charge per month 
                              125,          # [dollars/month]   Bill credit price
                              1000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["frontier_saver_plus_12"] = frontier_saver_plus_12.calculate_year_totals()

    # frontier_power_saver_9 (similar to cleank sky embrace green 10)
    frontier_power_saver_9 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              8.290,        # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              8.290,        # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              8.290,        # [cents/kWh]       Third range cost 
                              0,            # [dollars/month]   Base charge per month 
                              0,            # [dollars/month]   Bill credit price
                              1000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["frontier_power_saver_9"] = frontier_power_saver_9.calculate_year_totals()
   
    # express_energy_flash_12
    express_energy_flash_12 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              16.6821,      # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              16.6821,      # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              16.6821,      # [cents/kWh]       Third range cost 
                              0,            # [dollars/month]   Base charge per month 
                              100,          # [dollars/month]   Bill credit price
                              1000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["express_energy_flash_12"] = express_energy_flash_12.calculate_year_totals()

    # Vetern energy
    vetern_energy_valor_24 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              14.7911,      # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              14.7911,      # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              14.7911,      # [cents/kWh]       Third range cost 
                              0,            # [dollars/month]   Base charge per month 
                              50,           # [dollars/month]   Bill credit price
                              1000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["vetern_energy_valor_24"] = vetern_energy_valor_24.calculate_year_totals()

    # Reliant power savings 24
    reliant_power_savings_24 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              15.3894,      # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              15.3894,      # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              15.3894,      # [cents/kWh]       Third range cost 
                              0,            # [dollars/month]   Base charge per month 
                              50,           # [dollars/month]   Bill credit price
                              1000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["reliant_power_savings_24"] = reliant_power_savings_24.calculate_year_totals()

    # Reliant basic power plan 24
    reliant_basic_power_plan_24 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              11.2894,      # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              11.2894,      # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              11.2894,      # [cents/kWh]       Third range cost 
                              9.95,         # [dollars/month]   Base charge per month 
                              9.95,         # [dollars/month]   Bill credit price (there's a usage charge that only applies if <1000 kWh so I apply it like this)
                              1000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["reliant_basic_power_plan_24"] = reliant_basic_power_plan_24.calculate_year_totals()

    # Reliant power on 36 plan
    reliant_power_on_36_plan = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              10.1394,      # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              10.1394,      # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              10.1394,      # [cents/kWh]       Third range cost 
                              5.00,         # [dollars/month]   Base charge per month 
                              0.00,         # [dollars/month]   Bill credit price (there's a usage charge that only applies if <1000 kWh so I apply it like this)
                              1000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["reliant_power_on_36_plan"] = reliant_power_on_36_plan.calculate_year_totals()

    # Reliant secure advantage 24 plan
    reliant_secure_advantage_24 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              12.6894,      # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              12.6894,      # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              12.6894,      # [cents/kWh]       Third range cost 
                              9.95,         # [dollars/month]   Base charge per month 
                              9.95,         # [dollars/month]   Bill credit price (there's a usage charge that only applies if <1000 kWh so I apply it like this)
                              800,          # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["reliant_secure_advantage_24"] = reliant_secure_advantage_24.calculate_year_totals()

    # Reliant conservation 12
    reliant_conservation_12 = PowerPlan(consumption_list,
                              1000,         # [kWh]             First range ceiling
                              13.5394,      # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              15.539,       # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              15.539,       # [cents/kWh]       Third range cost 
                              5.00,         # [dollars/month]   Base charge per month 
                              0.00,         # [dollars/month]   Bill credit price (there's a usage charge that only applies if <1000 kWh so I apply it like this)
                              1000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["reliant_conservation_12"] = reliant_conservation_12.calculate_year_totals()

    # Lantana 36
    lantana_fixed_36 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              12.40491,     # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              12.40491,     # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              12.40491,     # [cents/kWh]       Third range cost 
                              0,            # [dollars/month]   Base charge per month 
                              0.00,         # [dollars/month]   Bill credit price (there's a usage charge that only applies if <1000 kWh so I apply it like this)
                              1000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["lantana_fixed_36"] = lantana_fixed_36.calculate_year_totals()

    # ranchero_smart_fixed_24
    ranchero_smart_fixed_24 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              8.2745,       # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              8.2745,       # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              8.2745,       # [cents/kWh]       Third range cost 
                              4.95,         # [dollars/month]   Base charge per month 
                              0.00,         # [dollars/month]   Bill credit price (there's a usage charge that only applies if <1000 kWh so I apply it like this)
                              1000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["ranchero_smart_fixed_24"] = ranchero_smart_fixed_24.calculate_year_totals()

     # sofed_better_rate_24
    sofed_better_rate_24 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              8.1745,       # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              8.1745,       # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              8.1745,       # [cents/kWh]       Third range cost 
                              4.95,         # [dollars/month]   Base charge per month 
                              0.00,         # [dollars/month]   Bill credit price (there's a usage charge that only applies if <1000 kWh so I apply it like this)
                              1000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["sofed_better_rate_24"] = sofed_better_rate_24.calculate_year_totals()

     # cleansky_embrace_green_24
    cleansky_embrace_green_24 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              8.8,          # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              8.8,          # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              8.8,          # [cents/kWh]       Third range cost 
                              0.00,         # [dollars/month]   Base charge per month 
                              0.00,         # [dollars/month]   Bill credit price (there's a usage charge that only applies if <1000 kWh so I apply it like this)
                              1000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["cleansky_embrace_green_24"] = cleansky_embrace_green_24.calculate_year_totals()

    # Revolution_stars_and_stripes_12
    Revolution_stars_and_stripes_12 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              8.764,        # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              8.764,        # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              8.764,        # [cents/kWh]       Third range cost 
                              2.00,         # [dollars/month]   Base charge per month 
                              0.00,         # [dollars/month]   Bill credit price (there's a usage charge that only applies if <1000 kWh so I apply it like this)
                              1000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["Revolution_stars_and_stripes_12"] = Revolution_stars_and_stripes_12.calculate_year_totals()\
    
    # infuse_essential_infusion_12
    infuse_essential_infusion_12 = PowerPlan(consumption_list,
                              5000,         # [kWh]             First range ceiling
                              8.564,        # [cents/kWh]       First range cost
                              5000,         # [kWh]             Second range ceiling
                              8.564,        # [cents/kWh]       Second range cost
                              5000,         # [kwH]             Third range ceiling, (arbritraily high upper ceiling)
                              8.564,        # [cents/kWh]       Third range cost 
                              4.00,         # [dollars/month]   Base charge per month 
                              0.00,         # [dollars/month]   Bill credit price (there's a usage charge that only applies if <1000 kWh so I apply it like this)
                              1000,         # [kWh]             Bill credit lower threshold (must be above this)
                              5000)         # [kWh]             Bill credit higher threshold (arbritraily high upper ceiling)
    totals["infuse_essential_infusion_12"] = infuse_essential_infusion_12.calculate_year_totals()
   
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