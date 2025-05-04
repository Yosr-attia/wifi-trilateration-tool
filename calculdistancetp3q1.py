import subprocess
import re
from math import log10

def read_data_from_cmd():
    p = subprocess.Popen("netsh wlan show networks mode=bssid", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, _ = p.communicate()
    output = out.decode('unicode_escape').strip()
    return output

def get_signal_strength(SSID):
    data = read_data_from_cmd()
    network_data = re.findall(r'SSID\s*\d+\s*:\s*(.*?)\s*Network type.*?Signal\s*:\s*([0-9]+)%', data, re.DOTALL)
    for ssid, signal in network_data:
        if ssid.strip().lower() == SSID.lower():
            return int(signal)
    return None


def distance_wifi(signal_percent):
    # Convert percentage to dBm 
    rssi = -90+ (signal_percent / 100) * 60  
    P0 = -50# Reference RSSI at 1 meter (in dBm)
    f = 2483.5  # Frequency in MHz (2.4 GHz band)
    n = 2.5 # Path loss exponent
    Fm = 12  

    c = (P0 - Fm - 10 * n * log10(f) + 30 * n - 32.44 - rssi) / (10 * n)
    distance = pow(10, c) * 1000  # Convert distance to meters
    return distance

# SSID you are trying to detect
SSID = input("SSID: ")
signal_strength_percent = get_signal_strength(SSID)

if signal_strength_percent is not None:
    # Convert signal strength percentage to dBm
    rssi = -90 + (signal_strength_percent / 100) * 60  
    # Calculate distance based on RSSI
    distance = distance_wifi(signal_strength_percent)
    print(f"Signal strength for {SSID}: {signal_strength_percent}%")
    print(f"Estimated distance to {SSID}: {distance:.2f} meters")
else:
    print("SSID not found or no signal detected.")
