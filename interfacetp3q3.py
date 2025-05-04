
import matplotlib.pyplot as plt
import subprocess
from math import log10, sqrt
import re
import tkinter as tk
from tkinter import messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def read_data_from_cmd():
    p = subprocess.Popen("netsh wlan show networks mode=bssid", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, _ = p.communicate()
    output = out.decode('unicode_escape').strip()
    return output

def get_available_access_points():
    data = read_data_from_cmd()
    aps = re.findall(r'SSID\s*\d+\s*:\s*(.*?)\s*Network type.*?Signal\s*:\s*([0-9]+)%', data, re.DOTALL)
    return {ssid.strip(): int(signal) for ssid, signal in aps}

def distance_wifi(signal_percent):
    rssi = -90 + (signal_percent / 100) * 60
    P0 = -50  
    f = 2483.5  
    n = 2.5
    Fm = 12

    c = (P0 - Fm - 10 * n * log10(f) + 30 * n - 32.44 - rssi) / (10 * n)
    distance = pow(10, c) * 1000
    return distance

def circle_intersections(x0, y0, r0, x1, y1, r1):
    d = sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    if d > r0 + r1 or d < abs(r0 - r1) or (d == 0 and r0 == r1):
        return None

    a = (r0**2 - r1**2 + d**2) / (2 * d)
    h = sqrt(r0**2 - a**2)

    x2 = x0 + a * (x1 - x0) / d
    y2 = y0 + a * (y1 - y0) / d

    intersection1 = (x2 + h * (y1 - y0) / d, y2 - h * (x1 - x0) / d)
    intersection2 = (x2 - h * (y1 - y0) / d, y2 + h * (x1 - x0) / d)
    

    midpoint = ((intersection1[0] + intersection2[0]) / 2, (intersection1[1] + intersection2[1]) / 2)
    return midpoint

class TrilaterationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trilateration Estimator")
        self.root.geometry("600x700")
        
        self.available_aps = get_available_access_points()

        self.ap_frame = ttk.LabelFrame(self.root, text="Available Access Points")
        self.ap_frame.pack(fill="x", padx=10, pady=10)

        self.ap_listbox = tk.Listbox(self.ap_frame, selectmode=tk.MULTIPLE, height=10, width=50)
        self.ap_listbox.pack(side="left", padx=5, pady=5)
        self.update_ap_listbox()

        self.refresh_button = ttk.Button(self.ap_frame, text="Refresh", command=self.refresh_ap_list)
        self.refresh_button.pack(side="right", padx=5, pady=5)

        # Selection confirmation and coordinate entry
        self.select_button = ttk.Button(self.root, text="Select APs", command=self.select_aps)
        self.select_button.pack(pady=10)

        self.coord_frame = ttk.LabelFrame(self.root, text="Coordinates Entry")
        self.coord_frame.pack(fill="x", padx=10, pady=10)

        # Coordinate input fields
        self.coord_entries = {}
        self.selected_aps = []

        # Trilateration calculation
        self.calculate_button = ttk.Button(self.root, text="Calculate Trilateration", command=self.calculate_trilateration)
        self.calculate_button.pack(pady=10)

        # Output and plot
        self.output_frame = ttk.LabelFrame(self.root, text="Output")
        self.output_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.output_text = tk.Text(self.output_frame, width=60, height=8)
        self.output_text.pack(padx=5, pady=5)

        self.canvas_frame = ttk.Frame(self.root)
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas = None

    def update_ap_listbox(self):
        self.ap_listbox.delete(0, tk.END)
        for ap in self.available_aps:
            self.ap_listbox.insert(tk.END, ap)

    def refresh_ap_list(self):
        self.available_aps = get_available_access_points()
        self.update_ap_listbox()
        self.output_text.insert(tk.END, "AP list refreshed.\n")

    def select_aps(self):
        self.selected_aps = [self.ap_listbox.get(i) for i in self.ap_listbox.curselection()]
        
        if len(self.selected_aps) != 3:
            messagebox.showerror("Selection Error", "Please select exactly 3 access points.")
            return

        for widget in self.coord_frame.winfo_children():
            widget.destroy()

        self.coord_entries.clear()
        for i, ap in enumerate(self.selected_aps):
            ttk.Label(self.coord_frame, text=f"Coordinates for {ap} (x, y):").grid(row=i, column=0, padx=5, pady=5)
            x_entry = ttk.Entry(self.coord_frame, width=10)
            y_entry = ttk.Entry(self.coord_frame, width=10)
            x_entry.grid(row=i, column=1, padx=5, pady=5)
            y_entry.grid(row=i, column=2, padx=5, pady=5)
            self.coord_entries[ap] = (x_entry, y_entry)

    def calculate_trilateration(self):
        ap_positions = {}
        distances = {}

        self.output_text.delete(1.0, tk.END)

        for ap in self.selected_aps:
            try:
                x = float(self.coord_entries[ap][0].get().strip())
                y = float(self.coord_entries[ap][1].get().strip())
                ap_positions[ap] = (x, y)
            except ValueError:
                self.output_text.insert(tk.END, f"Please enter valid coordinates for {ap}.\n")
                return

            rssi_value = self.available_aps[ap]
            distance = distance_wifi(rssi_value)
            distances[ap] = distance
            self.output_text.insert(tk.END, f"Estimated Distance to {ap}: {distance:.2f} meters\n")

        # Calculate the approximate intersection point of the circles
        aps = list(ap_positions.items())
        intersection_point = circle_intersections(aps[0][1][0], aps[0][1][1], distances[aps[0][0]], 
                                                  aps[1][1][0], aps[1][1][1], distances[aps[1][0]])

        if intersection_point:
            self.output_text.insert(tk.END, f"Estimated Position: {intersection_point}\n")
        else:
            self.output_text.insert(tk.END, "No intersection found.\n")

        self.plot_trilateration(ap_positions, distances, intersection_point)

    def plot_trilateration(self, ap_positions, distances, intersection_point):
        fig, ax = plt.subplots()

        for ap, (x, y) in ap_positions.items():
            distance = distances[ap]
            ax.plot(x, y, 'o', label=f'{ap}', markersize=8)
            circle = plt.Circle((x, y), distance, fill=False, linestyle='--', alpha=0.6)
            ax.add_artist(circle)
            ax.text(x, y, ap, fontsize=10, ha='center', va='center', fontweight='bold')

        if intersection_point:
            ax.plot(intersection_point[0], intersection_point[1], 'x', color='red', label="Estimated Position", markersize=10)

        ax.set_xlim(-5, 15)
        ax.set_ylim(-5, 15)
        ax.set_aspect('equal', 'box')
        plt.xlabel("X Position (m)")
        plt.ylabel("Y Position (m)")
        plt.grid(True)
        plt.legend()
        plt.title("Trilateration of Mobile Position Based on RSSI")

        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        self.canvas = FigureCanvasTkAgg(fig, self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

root = tk.Tk()
app = TrilaterationApp(root)
root.mainloop()
