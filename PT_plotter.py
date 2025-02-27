import numpy as np
import matplotlib.pyplot as plt
import sys

def read_PT_file(filename):
    """Reads a P-T profile file and returns pressure (in bars) and temperature arrays."""
    try:
        data = np.genfromtxt(filename, skip_header=1)  # Skip the first row (header)
        pressure_dyn = data[:, 0]  # First column: Pressure in dyn/cm²
        temp = data[:, 1]  # Second column: Temperature in K
        
        pressure_bar = pressure_dyn * 1e-6  # Convert dyn/cm² to bars
        return pressure_bar, temp
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        sys.exit(1)

def plot_PT_profiles(filenames):
    """Plots multiple P-T profiles with pressure in bars."""
    plt.figure(figsize=(6, 8))  # Set figure size
    
    for filename in filenames:
        pressure, temp = read_PT_file(filename)
        plt.plot(temp, pressure, label=filename)  # Plot temperature vs. pressure
    
    plt.yscale("log")  # Log scale for pressure
    plt.gca().invert_yaxis()  # Invert y-axis so high pressure is at the bottom
    plt.xlabel("Temperature (K)")
    plt.ylabel("Pressure (bar)")
    plt.legend()
    plt.title("P-T Profiles")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python PT_plotter.py file1.txt file2.txt ...")
        sys.exit(1)
    
    plot_PT_profiles(sys.argv[1:])
