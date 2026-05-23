import serial
import serial.tools.list_ports
import time


def find_esp32_port():
    """Automatically find the ESP32's COM port."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if any(keyword in port.description.upper() for keyword in
               ["CP210", "CH340", "UART", "USB", "SERIAL"]):
            return port.device
    return None


def get_real_temp(port=None, baud=9600, timeout=10):
    """
    Connect to ESP32 and read one real temperature from the DS18B20.
    Returns temperature in Celsius as a float, or None if failed.
    """
    if port is None:
        port = find_esp32_port()

    if port is None:
        print("Could not find ESP32. Is it plugged in?")
        print("Available ports:")
        for p in serial.tools.list_ports.comports():
            print(f"  {p.device} — {p.description}")
        return None

    print(f"Connecting to ESP32 on {port}...")

    try:
        with serial.Serial(port, baud, timeout=2) as ser:
            time.sleep(2)  # Wait for ESP32 to boot
            ser.reset_input_buffer()

            start = time.time()
            while time.time() - start < timeout:
                line = ser.readline().decode("utf-8", errors="ignore").strip()

                if not line:
                    continue

                # Parse lines like: "Temp: 25.62 C  /  78.12 F"
                if line.startswith("Temp:"):
                    parts = line.split()
                    temp_c = float(parts[1])
                    print(f"Live sensor reading: {temp_c}°C / {(temp_c * 9/5) + 32:.2f}°F")
                    return temp_c

                elif "Error" in line:
                    print(f"Sensor error: {line}")
                    return None

        print("Timed out waiting for temperature reading.")
        return None

    except serial.SerialException as e:
        print(f"Serial connection failed: {e}")
        return None


def get_real_temp_or_default(default_c=20.0, port=None):
    """
    Try to get a real temp reading. If ESP32 isn't connected,
    fall back to a default so the simulation still runs.
    """
    temp = get_real_temp(port=port)
    if temp is None:
        print(f"Falling back to default indoor temp: {default_c}°C")
        return default_c
    return temp


if __name__ == "__main__":
    temp = get_real_temp_or_default()
    print(f"\nIndoor temperature to use in simulation: {temp}°C")


# This program acts as the bridge between the physical hardware and the Python simulation. It automatically detects
# the ESP32 plugged into the computer's USB port, connects to it, and reads the live temperature from the DS18B20
# sensor. If the ESP32 is not available, it falls back to a default temperature so the rest of the simulation can still
# run uninterrupted