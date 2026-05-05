Apartment Energy Saving Simulation with ESP-32

Overview

This project simulates the annual energy consumption of a typical bachelor living in a New York City studio apartment. It calculates electricity usage for heating, cooling, and common appliances, then estimates the total cost based on real NYC electricity rates.

The goal is to establish a baseline energy model and then — in future development — simulate how an ESP-32 microcontroller can automate devices (lights, AC, heating) to save even more money.

Current Features

Outdoor temperature generator – Creates a full year of daily temperatures based on NYC monthly averages.
Apartment thermal model – Calculates heat loss and gain through walls, ceiling, and one window using NYC 2025 insulation codes (R-30 walls, R-49 ceiling, U-0.27 window).
Heating and cooling calculation – Determines daily energy needed to maintain comfort between 18°C (64°F) and 22°C (72°F).
Appliance energy estimates – Includes realistic averages for a single person:

Water heater (one shower per day)
Refrigerator (Energy Star)
Lighting (10 LED bulbs)
Electronics (TV, computer, router)
Cooking (one electric stove meal per day)
Phantom loads (idle devices)
Cost calculation – Uses NYC electricity rate of $0.31 per kWh (May 2026 data).
Project Structure

Apartment_Energy_Simulator/
- baseline/                    # Core energy model package
  - apartment.py               # Apartment thermal properties
  - energy_classes.py          # Appliance classes
  - outdoor_temps.py           # Outdoor temperature generator
- automation/                  # Future ESP-32 simulation (coming soon)
  - energy_simulation.py       # Main simulation runner


README.md
Sample Output:
HVAC energy: 2127 kWh
Appliance energy: 2532 kWh
Total annual energy: 4660 kWh
Annual energy cost: $1323.31
Future Development: ESP-32 Automation

A virtual ESP-32 microcontroller will be added to simulate smart automation that reduces energy use without sacrificing comfort.

Planned Automation Rules

Device	Automation Strategy	Estimated Savings
Heating / AC	Lower temperature when apartment is empty (9 hours/day). Start reheating 1 hour before returning home.	10-20% of HVAC energy
Lights	Turn off automatically when no motion detected for 15 minutes.	30-50% of lighting energy
Electronics	Cut power to TV, computer, and chargers during sleep hours (11 PM – 7 AM).	20-40% of electronics energy
Phantom loads	Automatically disconnect idle devices when not in use for extended periods.	33% of phantom energy
How the Virtual ESP-32 Will Work

Sensors – Simulated motion, light, temperature, and door/window sensors.
Rules Engine – If/then logic ("if window open, turn off AC").
Actuators – Virtual smart plugs and relays that cut power to devices.
Comparison – Run the same apartment with and without automation to see savings.
Expected Result

After adding ESP-32 automation, the simulation is expected to reduce total annual energy by approximately 15-25% , saving the resident 
200

200–300 per year.

Requirements

Python 3.9+
No external dependencies required (uses only standard library)

How to Run
python energy_simulation.py
Acknowledgments

NYC weather data based on historical monthly averages
Electricity rate from EnergySage (May 2026)
Insulation values from NYC 2025 Energy Code
License

This project is for educational and personal use.
