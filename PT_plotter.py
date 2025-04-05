import sys
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.lines import Line2D  # Import for creating custom legend handles

# File name and legend labels
output_dir = 'plot/PT/'
<<<<<<< HEAD
output_name = 'TOI_PT_profiles_A-I'
input_files = [
    'atm/toi270d_PT/A_TOI270d_Psurf_1bar_Tsurf_340K_Tstrat_260K.txt',
    'atm/toi270d_PT/B_TOI270d_Psurf_1bar_Tsurf_340K_Tstrat_270K.txt',
    'atm/toi270d_PT/C_TOI270d_Psurf_1bar_Tsurf_340K_Tstrat_280K.txt',
    'atm/toi270d_PT/D_TOI270d_Psurf_1bar_Tsurf_350K_Tstrat_260K.txt',
    'atm/toi270d_PT/E_TOI270d_Psurf_1bar_Tsurf_350K_Tstrat_270K.txt',
    'atm/toi270d_PT/F_TOI270d_Psurf_1bar_Tsurf_350K_Tstrat_280K.txt',
    'atm/toi270d_PT/G_TOI270d_Psurf_1bar_Tsurf_360K_Tstrat_270K.txt',
    'atm/toi270d_PT/H_TOI270d_Psurf_1bar_Tsurf_360K_Tstrat_280K.txt',
    'atm/toi270d_PT/I_TOI270d_Psurf_1bar_Tsurf_360K_Tstrat_290K.txt',
    'atm/toi270d_PT/AC1_TOI270d_Psurf_1bar_Tsurf_340K_Tstrat_200K_2e-2_turn.txt',
    
    
    
    #'atm/toi270d_PT/J_TOI270d_Psurf_1bar_Tsurf_320K_Tstrat_200K.txt',
    #'atm/toi270d_PT/K_TOI270d_Psurf_1bar_Tsurf_320K_Tstrat_210K.txt',
    #'atm/toi270d_PT/L_TOI270d_Psurf_1bar_Tsurf_320K_Tstrat_220K.txt',
    #'atm/toi270d_PT/M_TOI270d_Psurf_1bar_Tsurf_340K_Tstrat_200K.txt',
    #'atm/toi270d_PT/N_TOI270d_Psurf_1bar_Tsurf_340K_Tstrat_210K.txt',
    #'atm/toi270d_PT/O_TOI270d_Psurf_1bar_Tsurf_340K_Tstrat_220K.txt',
    #'atm/toi270d_PT/AC1_TOI270d_Psurf_1bar_Tsurf_340K_Tstrat_200K_2e-2_turn.txt'
    




    
    
    
]




# Legend labels
legend_labels = ['A','B','C','D','E','F','G','H','I','AC1'
   
=======
output_name = 'Hycean PT profiles'
input_files = [
    'atm/atm_K218b_Hy_M23_PT_100bar(PT3).txt',
    'atm/atm_K218b_Hy_WoganPT_10bar.txt',
    'atm/atm_K218b_Hy_PTA1.txt'
    
]

# Legend labels
legend_labels = [
    'M23, PT3',
    'W24',
    'New PT'
>>>>>>> defa297b8908fb28a979a07a58f1dfa4851e8ed4
]

def plot_atmospheric_profiles(input_files, output_dir, output_name, legend_labels):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
   
    # Create a new figure for plotting
    fig, ax1 = plt.subplots(figsize=(6, 5), constrained_layout=True)
    ax2 = ax1.twiny()  # Create secondary x-axis for k_zz

<<<<<<< HEAD
    # Use a colormap for more varied colors (viridis, plasma, etc.)
    cmap = plt.cm.plasma  # You can try other maps like 'plasma', 'cividis', etc.
    colors = [cmap(i / len(input_files)) for i in range(len(input_files))]
=======
    # Colors for different profiles
    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']  # List of colors
>>>>>>> defa297b8908fb28a979a07a58f1dfa4851e8ed4
    
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
<<<<<<< HEAD

    # Save plot
    output_path = os.path.join(output_dir, output_name + ".png")
=======
    
    #To make axes thicker
    def thick_axes(top = False, direction = 'in'):
        # Accessing the axes object and setting linewidth
        plt.gca().spines['top'].set_linewidth(2)  # Top axis
        plt.gca().spines['bottom'].set_linewidth(2)  # Bottom axis
        plt.gca().spines['left'].set_linewidth(2)  # Left axis
        plt.gca().spines['right'].set_linewidth(2)  # Right axis
        plt.tick_params(which = 'major', axis = 'both', direction = direction, labelsize = 12, length = 4, width = 2, right = True, top = top)
        plt.tick_params(which = 'minor',axis = 'both', direction = direction, labelsize = 12, length = 2, width = 1, right = True, top = top)
    thick_axes(top=True)
    output_path = os.path.join(output_dir, output_name + ".png")
    
    # Save plot
>>>>>>> defa297b8908fb28a979a07a58f1dfa4851e8ed4
    plt.savefig(output_path)
    plt.show()

plot_atmospheric_profiles(input_files, output_dir, output_name, legend_labels)