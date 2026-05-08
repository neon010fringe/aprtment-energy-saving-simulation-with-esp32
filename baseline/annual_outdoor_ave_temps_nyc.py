import random


def get_outdoor_temps():
    """Returns a list of daily outdoor temperatures in Celsius for the year."""

    # Define normal ranges for each month
    month_ranges = [
        ("January", 31, -3, 4),
        ("February", 28, -3, 5),
        ("March", 31, 1, 8),
        ("April", 30, 6, 16),
        ("May", 31, 11, 21),
        ("June", 30, 17, 27),
        ("July", 31, 18, 29),
        ("August", 31, 19, 28),
        ("September", 30, 15, 24),
        ("October", 31, 9, 18),
        ("November", 30, 4, 12),
        ("December", 30, 0, 6)
    ]

    # Define extreme outliers (unseasonably cold/hot)
    # Each tuple: (month_index, cold_temp, hot_temp)
    extremes = [
        (0, -12, 12),  # January: extreme cold -12C, extreme warm 12C
        (1, -10, 14),  # February: extreme cold -10C, extreme warm 14C
        (2, -8, 18),  # March: extreme cold -8C, extreme warm 18C
        (3, -2, 26),  # April: extreme cold -2C, extreme warm 26C
        (4, 4, 30),  # May: extreme cold 4C, extreme warm 30C
        (5, 10, 35),  # June: extreme cold 10C, extreme warm 35C
        (6, 14, 38),  # July: extreme cold 14C, extreme warm 38C
        (7, 15, 37),  # August: extreme cold 15C, extreme warm 37C
        (8, 9, 33),  # September: extreme cold 9C, extreme warm 33C
        (9, 2, 28),  # October: extreme cold 2C, extreme warm 28C
        (10, -4, 22),  # November: extreme cold -4C, extreme warm 22C
        (11, -8, 16)  # December: extreme cold -8C, extreme warm 16C
    ]

    all_temps = []

    for i, (month_name, days, min_temp, max_temp) in enumerate(month_ranges):
        # Generate normal temperatures
        month_temps = [random.randint(min_temp, max_temp) for _ in range(days)]

        # Add 1-2 extreme days
        num_extremes = random.choice([1, 2])  # Randomly 1 or 2 extremes per month

        for _ in range(num_extremes):
            # Pick a random day in the month
            day_index = random.randint(0, days - 1)

            # Decide if extreme cold or extreme hot (50/50 chance)
            if random.choice([True, False]):
                # Extreme cold day
                extreme_temp = extremes[i][1]  # Cold extreme
            else:
                # Extreme hot day
                extreme_temp = extremes[i][2]  # Hot extreme

            # Replace the normal temp with extreme temp
            month_temps[day_index] = extreme_temp

        all_temps.extend(month_temps)

    return all_temps


def main():
    temps = get_outdoor_temps()
    print(f"Generated {len(temps)} daily temperatures for NYC")

    # Show the extreme days by month
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    print("\nExtreme days detected:")
    idx = 0
    for i, month in enumerate(month_names):
        month_temps = temps[idx:idx + [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 30][i]]
        normal_min = [-3, -3, 1, 6, 11, 17, 18, 19, 15, 9, 4, 0][i]
        normal_max = [4, 5, 8, 16, 21, 27, 29, 28, 24, 18, 12, 6][i]

        extremes = [t for t in month_temps if t < normal_min or t > normal_max]
        if extremes:
            print(f"  {month}: {extremes}")

        idx += len(month_temps)

    print(f"\nSample first 10 temps: {temps[:10]}...")


if __name__ == "__main__":
    main()


# This code generates a full year of fake daily outdoor temperatures for New York City. It uses the monthly temperature
# ranges you provided (like January between -3°C and 4°C) and randomly picks a temperature for each day of that month,
# then collects all 365 days into one list that can be used for energy calculations. Generates 1-2 extreme temperatures
# per month, cold in the winter and hot in the summer.