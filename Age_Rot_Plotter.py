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
    
    plt.xlabel("Rotation period/Days")  # Updated label with raw string
    plt.ylabel("Age/ Gyrs")  # Updated label with raw string
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
    ("K2-18", 39.55, 0.65, 0.65, 3, 0.1, 0.1),
    #("TOI-270", 0.386, 0.008, 0.008, 0.378, 0.011, 0.011),
    ("TOI-776", 33, 1, 1, 6.1, 7, 5.5),
    ("GJ-176", 40, 0.11, 0.11, 8.8, 2.5, 2.8),
    ("GJ-436", 44.09, 0.08, 0.08 , 6, 4, 5),
    ("GJ-163", 61.3, 0.3, 0.3, 6, 4, 4),
    ("GJ-832", 45.7, 9.3, 9.3, 8.1, 4.2, 4.2),
]
# Specify directory and filename where the plot will be saved
output_dir = "plot/AR/"
filename = "Stellar_proxies_AR.png"
plot_MR_diagram(data, output_dir, filename)
