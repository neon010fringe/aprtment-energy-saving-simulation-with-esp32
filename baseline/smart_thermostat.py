class DumbThermostat:
    def __init__(self, apartment, heater_btu_hr=7500, cooler_btu_hr=6000):
        self.apartment = apartment
        self.heater_btu_hr = heater_btu_hr
        self.cooler_btu_hr = cooler_btu_hr
        self.setpoint_heating_c = 18
        self.setpoint_cooling_c = 22
        self.indoor_temp_c = 20.0
        self.heater_on = False
        self.cooler_on = False
        self.total_heating_kwh = 0
        self.total_cooling_kwh = 0
        self.thermal_mass_btu_per_f = 950

    def calculate_net_btu_per_hour(self, outside_temp_c):
        delta_f = (outside_temp_c - self.indoor_temp_c) * 1.8
        ua = self.apartment.effective_ua()
        heat_flow_btu = ua * delta_f
        if self.heater_on:
            heat_flow_btu += self.heater_btu_hr
        if self.cooler_on:
            heat_flow_btu -= self.cooler_btu_hr
        return heat_flow_btu

    def update_temperature(self, outside_temp_c, hours=1):
        net_btu = self.calculate_net_btu_per_hour(outside_temp_c)
        temp_change_f = net_btu * hours / self.thermal_mass_btu_per_f
        temp_change_c = temp_change_f / 1.8
        self.indoor_temp_c += temp_change_c
        self.indoor_temp_c = max(10, min(35, self.indoor_temp_c))
        return self.indoor_temp_c

    def decide(self, outside_temp_c):
        if self.indoor_temp_c < self.setpoint_heating_c:
            self.heater_on = True
            self.cooler_on = False
        elif self.indoor_temp_c > self.setpoint_cooling_c:
            self.heater_on = False
            self.cooler_on = True
        else:
            self.heater_on = False
            self.cooler_on = False

    def record_energy(self, hours=1):
        if self.heater_on:
            self.total_heating_kwh += self.heater_btu_hr * hours * 0.000293071
        if self.cooler_on:
            self.total_cooling_kwh += self.cooler_btu_hr * hours * 0.000293071

    def run_hour(self, outside_temp_c):
        self.decide(outside_temp_c)
        self.update_temperature(outside_temp_c, 1)
        self.record_energy(1)

    def total_kwh(self):
        return self.total_heating_kwh + self.total_cooling_kwh


class SmartThermostat:
    def __init__(self, apartment, heater_btu_hr=7500, cooler_btu_hr=6000):
        self.apartment = apartment
        self.heater_btu_hr = heater_btu_hr
        self.cooler_btu_hr = cooler_btu_hr
        self.setpoint_heating_c = 18
        self.setpoint_cooling_c = 22
        self.away_heating_c = 14
        self.away_cooling_c = 26
        self.indoor_temp_c = 20.0
        self.heater_on = False
        self.cooler_on = False
        self.total_heating_kwh = 0
        self.total_cooling_kwh = 0
        self.thermal_mass_btu_per_f = 950

    def calculate_net_btu_per_hour(self, outside_temp_c):
        delta_f = (outside_temp_c - self.indoor_temp_c) * 1.8
        ua = self.apartment.effective_ua()
        heat_flow_btu = ua * delta_f
        if self.heater_on:
            heat_flow_btu += self.heater_btu_hr
        if self.cooler_on:
            heat_flow_btu -= self.cooler_btu_hr
        return heat_flow_btu

    def update_temperature(self, outside_temp_c, hours=1):
        net_btu = self.calculate_net_btu_per_hour(outside_temp_c)
        temp_change_f = net_btu * hours / self.thermal_mass_btu_per_f
        temp_change_c = temp_change_f / 1.8
        self.indoor_temp_c += temp_change_c
        self.indoor_temp_c = max(10, min(35, self.indoor_temp_c))
        return self.indoor_temp_c

    def decide(self, outside_temp_c, is_home, hour_of_day):
        if is_home:
            if self.indoor_temp_c < self.setpoint_heating_c:
                self.heater_on = True
                self.cooler_on = False
            elif self.indoor_temp_c > self.setpoint_cooling_c:
                self.heater_on = False
                self.cooler_on = True
            else:
                self.heater_on = False
                self.cooler_on = False
        else:
            if self.indoor_temp_c < self.away_heating_c:
                self.heater_on = True
                self.cooler_on = False
            elif self.indoor_temp_c > self.away_cooling_c:
                self.heater_on = False
                self.cooler_on = True
            else:
                self.heater_on = False
                self.cooler_on = False

    def record_energy(self, hours=1):
        if self.heater_on:
            self.total_heating_kwh += self.heater_btu_hr * hours * 0.000293071
        if self.cooler_on:
            self.total_cooling_kwh += self.cooler_btu_hr * hours * 0.000293071

    def run_hour(self, outside_temp_c, is_home, hour_of_day):
        self.decide(outside_temp_c, is_home, hour_of_day)
        self.update_temperature(outside_temp_c, 1)
        self.record_energy(1)

    def total_kwh(self):
        return self.total_heating_kwh + self.total_cooling_kwh
