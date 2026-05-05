from annual_outdoor_ave_temps_nyc import get_outdoor_temps
from apartment import Apartment
from energy_classes import WaterHeater, Refrigerator, Lighting, Electronics, Cooking, PhantomLoads

def c_to_f(c):
    return (c * 9 / 5) + 32

def daily_energy_kwh(apartment, t_outside_c):
    t_outside_f = c_to_f(t_outside_c)
    heating_setpoint_f = c_to_f(18)
    cooling_setpoint_f = c_to_f(22)

    if t_outside_f < heating_setpoint_f:
        delta_f = heating_setpoint_f - t_outside_f
    elif t_outside_f > cooling_setpoint_f:
        delta_f = t_outside_f - cooling_setpoint_f
    else:
        delta_f = 0

    ua = apartment.effective_ua()
    kwh_per_day = (ua * delta_f * 24) / 3412
    return kwh_per_day


def main():
    # Create apartment using your class
    apt = Apartment(area_m2=91.44, wall_r=30, ceiling_r=49, window_u=0.27, window_area_sqft=20)

    # Get outdoor temperatures
    all_temps = get_outdoor_temps()

    # Calculate HVAC energy
    hvac_kwh = 0
    for temp_c in all_temps:
        hvac_kwh += daily_energy_kwh(apt, temp_c)

    # Create appliance instances
    water_heater = WaterHeater(showers_per_day=1)
    fridge = Refrigerator()
    lights = Lighting()
    electronics = Electronics()
    cooking = Cooking()
    phantom = PhantomLoads()

    # Calculate appliance energy
    appliance_kwh = (
            water_heater.annual_kwh() +
            fridge.annual_kwh() +
            lights.annual_kwh() +
            electronics.annual_kwh() +
            cooking.annual_kwh() +
            phantom.annual_kwh()
    )

    # Calculate totals
    total_kwh = hvac_kwh + appliance_kwh
    electricity_cost_per_kwh = 0.284
    annual_cost = total_kwh * electricity_cost_per_kwh

    print(f"HVAC energy: {hvac_kwh:.0f} kWh")
    print(f"Appliance energy: {appliance_kwh:.0f} kWh")
    print(f"Total annual energy: {total_kwh:.0f} kWh")
    print(f"Annual energy cost: ${annual_cost:.2f}")


if __name__ == "__main__":
    main()

# It calculates how much electricity the NYC apartment needs to stay comfortable all year long. It looks at the outside
# temperature each day, figures out how much heating (when it's cold) or air conditioning (when it's hot) is needed to
# keep the home between 64-72°F, then adds up the total energy cost for the entire year. The calculation accounts for
# your apartment's size, insulation, and that one window.


# NYC Average temperature by month in C
# January: -3, 4
# February: -3, 5
# March: 1, 8
# April: 6, 16
# May: 11, 21
# June: 17, 27
# July: 18, 29
# August: 19, 28
# September: 15, 24
# October: 9, 18
# November: 4, 12
# December: 0, 6

# Standard Comfort Zone: 18–22°C
# Condition	                Temperature (°C)
# Winter (heating season)	18–20°C
# Summer (cooling season)	22–24°C
# Ideal year-round average	20–21°C
# Sleeping	                16–19°C

# Studio Apartment in NYC 300 sq/ft | 91.44 sq/m

# Heat loss = (Area × (T_inside - T_outside)) / R_value

# T_heating_setpoint = 18°C (winter comfort)
# T_cooling_setpoint = 22°C (summer comfort)
# Area_total = effective surface area of the apartment (walls + ceiling + window adjusted)
# R_effective = combined thermal resistance

# For Your NYC Studio Apartment (91.44 m^2, 1 window)
# Component	    Area (sq ft)	R or U value
# Walls	        936	            R-30
# Ceiling	    984	            R-49
# Window	    20	            U-0.27


# This file represents a typical single person living alone in a New York City studio apartment who is reasonably careful
# about energy use but not obsessive. It assumes normal habits like taking one shower per day, having the lights on for
# a few hours, watching some TV, cooking one meal, and leaving a few things plugged in. These are not extreme
# conservation numbers, nor wasteful numbers, just a realistic middle ground for someone trying to be mindful of their
# electric bill.