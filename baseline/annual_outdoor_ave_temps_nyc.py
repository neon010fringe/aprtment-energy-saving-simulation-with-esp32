import random

def get_outdoor_temps():
    """Returns a list of daily outdoor temperatures in Celsius for the year."""

    # Outdoor temperature data
    external_january_temps = [random.randint(-3, 4) for _ in range(31)]
    external_february_temps = [random.randint(-3, 5) for _ in range(28)]
    external_march_temps = [random.randint(1, 8) for _ in range(31)]
    external_april_temps = [random.randint(6, 16) for _ in range(30)]
    external_may_temps = [random.randint(11, 21) for _ in range(31)]
    external_june_temps = [random.randint(17, 27) for _ in range(30)]
    external_july_temps = [random.randint(18, 29) for _ in range(31)]
    external_august_temps = [random.randint(19, 28) for _ in range(31)]
    external_september_temps = [random.randint(15, 24) for _ in range(30)]
    external_october_temps = [random.randint(9, 18) for _ in range(31)]
    external_november_temps = [random.randint(4, 12) for _ in range(30)]
    external_december_temps = [random.randint(0, 6) for _ in range(30)]

    all_temps = (
            external_january_temps + external_february_temps + external_march_temps +
            external_april_temps + external_may_temps + external_june_temps +
            external_july_temps + external_august_temps + external_september_temps +
            external_october_temps + external_november_temps + external_december_temps
    )

    return all_temps

def main():
    temps = get_outdoor_temps()
    print(f"Generated {len(temps)} daily temperatures for NYC")
    print(f"Sample: {temps[:5]}...")

if __name__ == "__main__":
    main()


# This code generates a full year of fake daily outdoor temperatures for New York City. It uses the monthly temperature
# ranges you provided (like January between -3°C and 4°C) and randomly picks a temperature for each day of that month,
# then collects all 365 days into one list that can be used for energy calculations.