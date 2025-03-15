import sys
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.lines import Line2D  # Import for creating custom legend handles

# File name and legend labels
output_dir = 'plot/PT/'
output_name = 'Wogan_2024'
input_files = [
    'atm/atm_K218b_Hy_WoganPT_10bar.txt', 
    'atm/atm_K218b_Hy_WoganPT.txt', 
    'atm/atm_K218b_Hy_M23_PT_100bar(PT3).txt'
]

# Legend labels
legend_labels = [
    'Profile 1',  # Replace with custom labels for each input file
    'Profile 2',
]

def plot_atmospheric_profiles(input_files, output_dir, output_name, legend_labels):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
   
    # Create a new figure for plotting
    fig, ax1 = plt.subplots(figsize=(6, 5), constrained_layout=True)
    ax2 = ax1.twiny()  # Create secondary x-axis for k_zz

    # Colors for different profiles
    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']  # List of colors
    
    # Lists for legends
    profile_legends = []  # For Temperature (PT)
    
    # Loop over each input file and plot its data
    for i, input_file in enumerate(input_files):
        # Load data from the input file, skipping any header row with non-numeric values
        try:
            data = np.genfromtxt(input_file, skip_header=1)  # Use genfromtxt to handle missing values or headers
        except ValueError:
            print(f"Error loading {input_file}, skipping this file.")
            continue
        
        pressure = data[:, 0] / 1e6  # Convert dyne/cm² to bar
        temperature = data[:, 1]  # Temperature in K
        k_zz = data[:, 2]  # Eddy diffusion coefficient
        
        # Choose color for the current profile
        color = colors[i % len(colors)]  # Cycle through colors if more than available
        
        # Plot temperature (solid line)
        ax1.plot(temperature, pressure, color=color)
        
        # Plot Kzz (dashed line, on logarithmic scale)
        ax2.plot(k_zz, pressure, color=color, linestyle='--')
        
        # Add profile legends for temperature
        profile_legends.append(f'{legend_labels[i] if i < len(legend_labels) else f"Profile {i+1}"}')
             
    # Set up labels and ticks
    ax1.set_xlabel("Temperature (K)", color='black')
    ax1.tick_params(axis='x', colors='black')
    ax2.set_xlabel("$K_{zz}$ (cm²/s)", color='black')
    ax2.tick_params(axis='x', colors='black')
    
    # Common Y-axis (Pressure)
    ax1.set_ylabel("Pressure (bar)", color='black')
    ax1.set_yscale('log')
    ax1.invert_yaxis()  # Invert to match atmospheric convention
    
    # Set logarithmic scale for k_zz (ax2)
    ax2.set_xscale('log')

    # Add legends
    ax1.legend(profile_legends, loc='upper right',bbox_to_anchor=(1, 0.9), fontsize=8)
    
    # Create custom legend handles
    legend_handles = [
        Line2D([0], [0], color='black', linestyle='--', lw=2),  # Dashed line for Kzz
        Line2D([0], [0], color='black', lw=2)  # Solid line for Temperature
    ]
    ax2.legend(legend_handles, ['$K_{zz}$', 'Temperature'], loc='upper right', fontsize=8)

    # Save plot
    output_path = os.path.join(output_dir, output_name + ".png")
    plt.savefig(output_path)
    plt.show()

plot_atmospheric_profiles(input_files, output_dir, output_name, legend_labels)