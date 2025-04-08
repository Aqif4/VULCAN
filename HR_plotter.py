import matplotlib.pyplot as plt
import numpy as np
import os
def plot_HR_diagram(data, output_dir, filename):
    """
    Plots the Hertzsprung-Russell (HR) diagram with asymmetric uncertainties and saves the plot to a file.
    Parameters:
    data: list of tuples (star, t_eff, delta_plus_Teff, delta_negative_Teff, log_10_luminosity, delta_plus_L, delta_negative_L)
    output_dir: Directory where the plot image will be saved (default is the current directory).
    filename: Name of the file to save the plot (default is 'hr_diagram.png').
    """
    
    stars = []
    temperatures = []
    luminosities = []
    temp_errors_pos = []
    temp_errors_neg = []
    lum_errors_high = []
    lum_errors_low = []
    for star, t_eff, delta_plus_Teff, delta_negative_Teff, log_10_luminosity, delta_plus_L, delta_negative_L in data:
        stars.append(star)
        temperatures.append(t_eff)
        luminosities.append(log_10_luminosity)
        temp_errors_pos.append(delta_plus_Teff)
        temp_errors_neg.append(delta_negative_Teff)
        lum_errors_high.append(log_10_luminosity+delta_plus_L)
        lum_errors_low.append(log_10_luminosity+delta_negative_L)
    # Convert to numpy arrays for easier manipulation
    temperatures = np.array(temperatures)
    luminosities = np.array(luminosities)
    temp_errors_pos = np.array(temp_errors_pos)
    temp_errors_neg = np.array(temp_errors_neg)
    lum_errors_high = np.array(lum_errors_high)
    lum_errors_low = np.array(lum_errors_low)
    # Plotting the HR diagram
    plt.figure(figsize=(8, 6))
    plt.errorbar(temperatures, luminosities, 
                 xerr=[temp_errors_neg, temp_errors_pos], 
                 yerr=[abs(luminosities-lum_errors_low), abs(luminosities-lum_errors_high)], 
                 fmt='o', label="Stars", color='blue', capsize=5)
    plt.gca().invert_xaxis()  # Invert x-axis to have hotter stars on the left
    
    plt.xlabel(r"$T_{\text{eff}}$ (K)")  # Updated label with raw string
    plt.ylabel(r"$\log_{10}$ ($L/L_{\odot}$)")  # Updated label with raw string
    # Annotate stars with names
    for i, star in enumerate(stars):
        plt.text(temperatures[i], luminosities[i], star, fontsize=12, ha='right', va='bottom')
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Save the plot as an image file
    output_path = os.path.join(output_dir, filename)
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.xlim(3800,3300)
    # Show the plot
    plt.show()
    print(f"Plot saved to: {output_path}")
# Example input
# (Star, T_eff, T_eff_pos, T_eff_neg, log_L, log_L_pos, log_L_neg)
data = [
    ("K2-18", 3645, 53, 53, -1.6, 0.03, 0.04),
    ("TOI-270", 3506, 70, 70, -1.71, 0.04, 0.04),
    ("TOI-776", 3725, 60, 60, -1.3, 0.09, 0.11),
    ("GJ-176", 3703, 32, 32, -1.47, 0.09, 0.11),
    ("GJ-436", 3586, 36, 36 , -1.63, 0.09, 0.12),
    ("GJ-163", 3399, 157, 157, -1.69, 0.10, 0.12),
    ("GJ-832", 3681, 96, 96, -1.523, 0.602, 0.301),
]
# Specify directory and filename where the plot will be saved
output_dir = "plot/HR/"
filename = "Stellar_proxies_HR.png"
plot_HR_diagram(data, output_dir, filename)
