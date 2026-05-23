# energy_classes.py

class WaterHeater:
    """Hot water energy based on daily showers."""

    def __init__(self, showers_per_day=1, minutes_per_shower=8, gallons_per_minute=1.5):
        self.showers_per_day = showers_per_day
        self.minutes_per_shower = minutes_per_shower
        self.gallons_per_minute = gallons_per_minute

    def annual_kwh(self):
        # Simple estimate: ~2 kWh per 10-minute shower
        kwh_per_shower = 2.0
        return kwh_per_shower * self.showers_per_day * 365


class Refrigerator:
    def __init__(self, energy_star=True):
        self.energy_star = energy_star

    def annual_kwh(self):
        return 500 if self.energy_star else 700


class Lighting:
    """Light bulbs throughout the apartment."""

    def __init__(self, bulbs=10, watts_per_bulb=10, hours_per_day=4):
        self.bulbs = bulbs
        self.watts = watts_per_bulb
        self.hours_per_day = hours_per_day

    def annual_kwh(self):
        daily_wh = self.bulbs * self.watts * self.hours_per_day
        return (daily_wh * 365) / 1000


class Electronics:
    """TV, computer, router, chargers, etc."""

    def __init__(self, tv_hours=3, computer_hours=4, gaming=False):
        self.tv_hours = tv_hours
        self.computer_hours = computer_hours
        self.gaming = gaming

    def annual_kwh(self):
        tv_kwh = (0.1 * self.tv_hours * 365)  # 100W TV
        computer_kwh = (0.15 * self.computer_hours * 365)  # 150W computer
        gaming_extra = 300 if self.gaming else 0
        router_chargers = 200
        return tv_kwh + computer_kwh + gaming_extra + router_chargers


class Cooking:
    """Electric stove and oven usage."""

    def __init__(self, meals_per_day=1):
        self.meals_per_day = meals_per_day

    def annual_kwh(self):
        # ~1 kWh per meal on electric stove
        return self.meals_per_day * 365 * 1.0


class PhantomLoads:
    """Devices drawing power even when off."""

    def __init__(self, devices=10):
        self.devices = devices
        self.watts_per_device = 3

    def annual_kwh(self):
        daily_wh = self.devices * self.watts_per_device * 24
        return (daily_wh * 365) / 1000




# This file defines six classes that represent common sources of electricity use in an apartment: a water heater for
# showers, a refrigerator, lights, electronics like TVs and computers, an electric stove for cooking, and phantom loads
# from devices that draw power even when turned off. Each class calculates how many kilowatt-hours of electricity it
# uses over a full year based on typical usage patterns and settings like shower frequency or hours of TV watched. These
# annual energy values can then be added together to estimate a household's total electricity consumption and cost.

# Lighting / TV should be automated via microcontroller because people like myself often fall asleep for many hours having
# left the lights on, and also not noticing they are on during the day when the sunlight is present.