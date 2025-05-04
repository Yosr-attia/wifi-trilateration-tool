import numpy as np
import matplotlib.pyplot as plt
import subprocess
import re
from math import log10
from sympy import symbols, Eq, solve

ap_positions = {
    "AP1": (0, 0),
    "AP2": (4,0),
    "AP3": (0,4)
}


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
    P0 = -50 # Reference RSSI at 1 meter (in dBm)
    f = 2483.5  # Frequency in MHz (2.4 GHz band)
    n = 2.2 # Path loss exponent
    Fm = 12  

    c = (P0 - Fm - 10 * n * log10(f) + 30 * n - 32.44 - rssi) / (10 * n)
    distance = pow(10, c) * 1000  # Convert distance to meters
    return distance

def plot_trilateration(ap_positions, distances, ssid_names):
    fig, ax = plt.subplots()

    for ap_key, position in ap_positions.items():
        x, y = position
        distance = distances.get(ap_key, 0)
        ssid_name = ssid_names[ap_key]

        ax.plot(x, y, 'o', label=f'{ssid_name}', markersize=8)

        circle = plt.Circle(position, distance, fill=False, linestyle='--', alpha=0.6)
        ax.add_artist(circle)

        ax.text(x, y, ssid_name, fontsize=10, ha='center', va='center', fontweight='bold')

    ax.set_xlim(-5, 15)
    ax.set_ylim(-5, 15)
    ax.set_aspect('equal', 'box')
    plt.xlabel("X Position (m)")
    plt.ylabel("Y Position (m)")
    plt.grid(True)
    plt.legend()
    plt.title("Trilateration of Mobile Position Based on RSSI")

    # Display plot
    plt.show()

if __name__ == "__main__":
    distances = {}
    ssid_names = {} 

    # Collect SSID names and calculate distances
    for ap_key in ap_positions.keys():
        SSID = input(f"Enter the SSID for {ap_key}: ").strip()
        ssid_names[ap_key] = SSID  # Store the SSID name provided by the user
        rssi_value = get_signal_strength(SSID)
        if rssi_value is not None:
            distance = distance_wifi(rssi_value)
            distances[ap_key] = distance
            print(f"Estimated Distance to {SSID}: {distance:.2f} meters")
        else:
            print(f"Could not calculate distance for {SSID} due to missing RSSI value.")

    plot_trilateration(ap_positions, distances, ssid_names)

