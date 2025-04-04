import sys
import numpy as np
import matplotlib.pyplot as plt
import vulcan_cfg  # Assuming it's in the top-level directory
import os
import pickle


# Setting input arguments
plot_spec = 'H2O,CH4,CO2,CO,NH3,CH3CL,HCN'  # Species to plot, separated by commas

plot_name = 'K2-18b_EQs' # Output plot name
plot_dir = vulcan_cfg.plot_dir if hasattr(vulcan_cfg, 'plot_dir') else 'path/to/your/plot/directory'  # Ensure plot_dir is set
error_bar_set = 'cb_1'
vul_files = [
             
             "output/K2-18b_EQ/K2-18b_1bar_100metal_1s_EQ.vul",
             "output/Albedo_Surface/EQ/UH_K2-18b_GJ176_25bar_100metal_PT3.vul",
             "output/Albedo_Surface/EQ/UH_K2-18b_GJ176_50bar_100metal_PT3.vul",
             "output/Albedo_Surface/EQ/UH_K2-18b_GJ176_75bar_100metal_PT3.vul",

            

             
             
           
             ]
titles = [ "1bar", "25bar", "50bar", "75bar"]
plot_title = ''

# Line styles for each dataset (extend as needed)
line_styles = ['-', '-.', '--', ':']  # Solid, dashed, dash-dot, dot

# Color setup (Tableau 20 colors)
tableau20 = [(31, 119, 180), (255, 127, 14), (44, 160, 44), (214, 39, 40), (148, 103, 189),
             (140, 86, 75), (227, 119, 194), (127, 127, 127), (188, 189, 34), (23, 190, 207)]
tableau20 = [(r / 255., g / 255., b / 255.) for r, g, b in tableau20]

# Species to TeX label mapping
tex_labels = {
    'H2O': 'H$_2$O', 'CH4': 'CH$_4$', 'CO2': 'CO$_2$', 'CO': 'CO',
    'NH3': 'NH$_3$', 'CH3CL': 'CH$_3$Cl', 'HCN': 'HCN'
}

# Error bar configurations
error_bar_sets = {
    'cb_1': {
        'CH4': {'x_center': -1.74, 'dx_pos': 0.59, 'dx_neg': 0.69, 'y': 0.5e-3},
        'CO2': {'x_center': -2.09, 'dx_pos': 0.51, 'dx_neg': 0.94, 'y': 1.2e-3},
        'H2O': {'x_center': -3.06, 'y': 0.5e-3},
        'NH3': {'x_center': -4.51, 'y': 1.6e-3},
        'CO': {'x_center': -3.5, 'y': 1.8e-3},
        'HCN': {'x_center': -2.92, 'y': 4e-3},
    },
}

# Use the selected error bar set
species_error_data = error_bar_sets[error_bar_set]

# Initialize plot
fig, ax = plt.subplots(figsize=(6, 5), constrained_layout=True)
species_plotted = set()

for idx, (vul_file, title) in enumerate(zip(vul_files, titles)):
    # Load VULCAN output
    try:
        with open(vul_file, 'rb') as handle:
            data = pickle.load(handle)
    except FileNotFoundError:
        print(f"File not found: {vul_file}, skipping.")
        continue
    except pickle.UnpicklingError:
        print(f"Error loading {vul_file}, ensure it's a valid VULCAN output.")
        continue

    # Ensure the data structure is valid
    if 'variable' not in data or 'atm' not in data:
        print(f"Invalid data format in {vul_file}, skipping.")
        continue

    vulcan_spec = data['variable'].get('species', [])
    if not vulcan_spec:
        print(f"No species found in {vul_file}, skipping.")
        continue

    # Select line style (default to solid if out of range)
    linestyle = line_styles[idx % len(line_styles)]

    # Loop over species to plot
    for color_index, sp in enumerate(plot_spec.split(',')):
        sp_label = tex_labels.get(sp, sp)

        if sp in vulcan_spec:
            species_index = vulcan_spec.index(sp)
            ax.plot(
                data['variable']['ymix'][:, species_index],
                data['atm']['pco'] / 1.e6,
                color=tableau20[color_index],
                linestyle=linestyle,
                alpha=0.9
            )

            # Add to legend if not already added
            if sp not in species_plotted:
                ax.plot([], [], color=tableau20[color_index], label=sp_label)
                species_plotted.add(sp)

            # Add error bars if available
            if sp in species_error_data:
                error_data = species_error_data[sp]
                x_center_10 = 10 ** (error_data['x_center'])

                if 'dx_pos' in error_data and 'dx_neg' in error_data:
                    x_high = 10 ** (error_data['x_center'] + abs(error_data['dx_pos']))
                    x_low = 10 ** (error_data['x_center'] - abs(error_data['dx_neg']))
                    ax.errorbar(
                        x_center_10,
                        error_data['y'],
                        xerr=[[abs(x_center_10 - x_low)], [abs(x_center_10 - x_high)]],
                        fmt='o',
                        color=tableau20[color_index],
                        markersize=5,
                        capsize=5,
                        elinewidth=2,
                        capthick=2
                    )
                elif 'x_center' in error_data:
                    ax.plot([x_center_10, x_center_10],
                            [error_data['y'] * 1.4, error_data['y'] / 1.4],
                            color=tableau20[color_index], lw=2)
                    ax.annotate('',
                                xy=(x_center_10 * 1.1, error_data['y']),
                                xytext=(x_center_10 * 0.15, error_data['y']),
                                arrowprops=dict(
                                    arrowstyle='<|-',
                                    lw=2,
                                    color=tableau20[color_index],
                                    mutation_scale=16,
                                )
                                )

    # Legend entry for each dataset
    ax.plot([], [], linestyle=linestyle, color='black', label=title)

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

# Axis setup
ax.set_xscale('log')
ax.set_yscale('log')
ax.invert_yaxis()
ax.set_xlim(1.E-10, 1)
ax.set_ylim(1, 1.E-8)
ax.legend(frameon=0, prop={'size': 10}, loc='best')
ax.set_title(plot_title)
ax.set_xlabel("Mixing Ratio")
ax.set_ylabel("Pressure (bar)")


# Save plot
output_path = os.path.join(plot_dir, plot_name + '.png')
plt.savefig(output_path)
plt.show()