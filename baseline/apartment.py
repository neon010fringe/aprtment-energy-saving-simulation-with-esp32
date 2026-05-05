class Apartment:
    """Represents an apartment's thermal properties."""

    def __init__(self, area_m2, wall_r, ceiling_r, window_u, window_area_sqft):
        """
        Parameters:
        - area_m2: Floor area in square meters
        - wall_r: R-value of walls (US units)
        - ceiling_r: R-value of ceiling (US units)
        - window_u: U-factor of windows (US units)
        - window_area_sqft: Total window area in square feet
        """
        self.area_m2 = area_m2
        self.wall_r = wall_r
        self.ceiling_r = ceiling_r
        self.window_u = window_u
        self.window_area_sqft = window_area_sqft

        # Derived values (cached for performance)
        self.floor_ft2 = area_m2 * 10.764
        self.wall_area_sqft = self._calculate_wall_area()
        self.ceiling_area_sqft = self.floor_ft2

    def _calculate_wall_area(self):
        """Calculate wall area from floor area assuming 8 ft ceiling and square shape."""
        # Assume square room: side length = sqrt(floor_ft2)
        # Perimeter = 4 × side length
        # Wall area = perimeter × ceiling height (8 ft)
        side_ft = self.floor_ft2 ** 0.5
        perimeter_ft = 4 * side_ft
        ceiling_height_ft = 8
        return perimeter_ft * ceiling_height_ft

    def effective_ua(self):
        """Calculate effective UA (BTU/hr per FF) for the apartment.

        UA = sum of (Area / R) for each component, or (Area × U) for windows.
        This represents heat loss (or gain) per degree Fahrenheit per hour.
        """
        wall_ua = self.wall_area_sqft / self.wall_r
        ceiling_ua = self.ceiling_area_sqft / self.ceiling_r
        window_ua = self.window_area_sqft * self.window_u

        return wall_ua + ceiling_ua + window_ua

    def summary(self):
        """Print a summary of apartment properties."""
        print(" Apartment Summary ")
        print(f"Floor area: {self.area_m2} m^2 ({self.floor_ft2:.0f} ft^2)")
        print(f"Wall area: {self.wall_area_sqft:.0f} ft^2")
        print(f"Ceiling area: {self.ceiling_area_sqft:.0f} ft^2")
        print(f"Window area: {self.window_area_sqft} ft^2")
        print(f"Wall R-value: {self.wall_r}")
        print(f"Ceiling R-value: {self.ceiling_r}")
        print(f"Window U-factor: {self.window_u}")
        print(f"Effective UA: {self.effective_ua():.2f} BTU/hr per F")


# Test the class
if __name__ == "__main__":
    # NYC studio apartment from your specifications
    apt = Apartment(
        area_m2=91.44,
        wall_r=30,
        ceiling_r=49,
        window_u=0.27,
        window_area_sqft=20
    )

    apt.summary()


# This code defines what an apartment is in terms of heat and energy. It takes basic information about the apartment -
# the size, how well the walls and ceiling are insulated, and how many windows it has - and then calculates a single
# number called "effective UA" that represents how easily heat escapes from or enters the apartment. That number can then
# be used to figure out how much heating or air conditioning the apartment needs on any given day.