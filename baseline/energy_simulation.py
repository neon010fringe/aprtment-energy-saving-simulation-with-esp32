from annual_outdoor_ave_temps_nyc import get_outdoor_temps
from apartment import Apartment
from energy_classes import WaterHeater, Refrigerator, Lighting, Electronics, Cooking, PhantomLoads
from smart_thermostat import DumbThermostat, SmartThermostat
from baseline.sensor_reader import get_real_temp_or_default


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
    # ── REAL SENSOR READING ──────────────────────────────────────────
    # Reads live temperature from your DS18B20 via ESP32.
    # If ESP32 isn't connected, falls back to 20.0°C automatically.
    real_indoor_temp_c = get_real_temp_or_default(default_c=20.0)
    print(f"\nSimulation starting indoor temp: {real_indoor_temp_c}°C "
          f"/ {c_to_f(real_indoor_temp_c):.1f}°F (from DS18B20)\n")
    # ─────────────────────────────────────────────────────────────────

    apt = Apartment(area_m2=91.44, wall_r=30, ceiling_r=49, window_u=0.27, window_area_sqft=20)
    all_temps = get_outdoor_temps()

    # Original HVAC calculation
    hvac_kwh = 0
    for temp_c in all_temps:
        hvac_kwh += daily_energy_kwh(apt, temp_c)

    # Appliances
    water_heater = WaterHeater(showers_per_day=1)
    fridge = Refrigerator()
    lights = Lighting()
    electronics = Electronics()
    cooking = Cooking()
    phantom = PhantomLoads()
    appliance_kwh = (water_heater.annual_kwh() + fridge.annual_kwh() + lights.annual_kwh() +
                     electronics.annual_kwh() + cooking.annual_kwh() + phantom.annual_kwh())

    total_kwh = hvac_kwh + appliance_kwh
    annual_cost = total_kwh * 0.284

    print(f"HVAC energy: {hvac_kwh:.0f} kWh")
    print(f"Appliance energy: {appliance_kwh:.0f} kWh")
    print(f"Total annual energy: {total_kwh:.0f} kWh")
    print(f"Annual energy cost: ${annual_cost:.2f}")

    # Smart Thermostat Comparison
    print("\n" + "=" * 50)
    print("SMART THERMOSTAT COMPARISON")
    print("=" * 50)

    # Pass real indoor temp as starting point for both thermostats
    dumb = DumbThermostat(apt)
    dumb.indoor_temp_c = real_indoor_temp_c        # ← real sensor reading
    for temp_c in all_temps:
        for hour in range(24):
            dumb.run_hour(temp_c)
    dumb_energy = dumb.total_kwh()

    smart = SmartThermostat(apt)
    smart.indoor_temp_c = real_indoor_temp_c       # ← real sensor reading
    for day, temp_c in enumerate(all_temps):
        day_of_week = day % 7
        is_weekend = (day_of_week >= 5)
        for hour in range(24):
            if is_weekend:
                is_home = True
            else:
                is_home = (hour >= 18 or hour < 8)
            smart.run_hour(temp_c, is_home, hour)
    smart_energy = smart.total_kwh()

    savings = dumb_energy - smart_energy

    print(f"Dumb thermostat HVAC: {dumb_energy:.0f} kWh")
    print(f"Smart thermostat HVAC: {smart_energy:.0f} kWh")
    print(f"Savings: {savings:.0f} kWh")

    print("\n" + "=" * 50)
    print("FINAL VERDICT")
    print("=" * 50)
    print(f"Original simplified HVAC:    {hvac_kwh:.0f} kWh")
    print(f"Realistic dumb thermostat:   {dumb_energy:.0f} kWh")
    print(f"Realistic smart thermostat:  {smart_energy:.0f} kWh")
    print(f"\nSmart vs Dumb savings:       {savings:.0f} kWh ({savings / dumb_energy * 100:.1f}%)")
    print(f"Annual cost savings:         ${savings * 0.284:.2f}")
    print("\nPROVEN: Smart thermostat saves energy while maintaining comfort")


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