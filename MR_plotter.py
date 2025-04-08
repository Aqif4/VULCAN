import matplotlib.pyplot as plt
import numpy as np
import os
def plot_MR_diagram(data, output_dir, filename):
    """
  
    Parameters:
    output_dir: Directory where the plot image will be saved (default is the current directory).
    """
    
    stars = []
    mass = []
    radius = []
    mass_errors_pos = []
    mass_errors_neg = []
    radius_errors_high = []
    radius_errors_low = []
    for star, t_eff, delta_plus_Teff, delta_negative_Teff, log_10_luminosity, delta_plus_L, delta_negative_L in data:
        stars.append(star)
        mass.append(t_eff)
        radius.append(log_10_luminosity)
        mass_errors_pos.append(delta_plus_Teff)
        mass_errors_neg.append(delta_negative_Teff)
        radius_errors_high.append(delta_plus_L)
        radius_errors_low.append(delta_negative_L)
    # Convert to numpy arrays for easier manipulation
    mass = np.array(mass)
    radius = np.array(radius)
    mass_errors_pos = np.array(mass_errors_pos)
    mass_errors_neg = np.array(mass_errors_neg)
    radius_errors_high = np.array(radius_errors_high)
    radius_errors_low = np.array(radius_errors_low)
    # Plotting the HR diagram
    plt.figure(figsize=(8, 6))
    plt.errorbar(mass, radius, 
                 xerr=[mass_errors_neg, mass_errors_pos], 
                 yerr=[radius_errors_low, radius_errors_high], 
                 fmt='o', label="Stars", color='blue', capsize=5)
    
    plt.xlabel(r"$M/M_{\odot}$")  # Updated label with raw string
    plt.ylabel(r"$R/R_{\odot}$")  # Updated label with raw string
    # Annotate stars with names
    for i, star in enumerate(stars):
        plt.text(mass[i], radius[i], star, fontsize=12, ha='right', va='bottom')
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Save the plot as an image file
    output_path = os.path.join(output_dir, filename)
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    # Show the plot
    plt.show()
    print(f"Plot saved to: {output_path}")
# Example input
# (Star, mass, mass_pos, mass_neg, radius, radius_pos, radius_neg)
data = [
    ("K2-18", 0.495, 0.004, 0.004, 0.445, 0.015, 0.015),
    ("TOI-270", 0.386, 0.008, 0.008, 0.378, 0.011, 0.011),
    ("TOI-776", 0.542, 0.04, 0.039, 0.547, 0.017, 0.017),
    ("GJ-176", 0.509, 0.01, 0.01, 0.478, 0.007, 0.007),
    ("GJ-436", 0.441, 0.009, 0.009 , 0.417, 0.008, 0.008),
    ("GJ-163", 0.402, 0.02, 0.02, 0.410, 0.012, 0.012),
    ("GJ-832", 0.437, 0.02, 0.02, 0.442, 0.01, 0.01),
]
# Specify directory and filename where the plot will be saved
output_dir = "plot/MR/"
filename = "Stellar_proxies_MR.png"
plot_MR_diagram(data, output_dir, filename)
