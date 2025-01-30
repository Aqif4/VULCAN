
import sys
import numpy as np
import matplotlib.pyplot as plt
import vulcan_cfg  # Assuming it's in the top-level directory
import os
import pickle

# Setting input arguments
plot_spec = 'H2O,CH4,CO2,CO,NH3'  # Species to plot, separated by commas
plot_name = 'mtol investigation with errors and upper bounds'  # Output plot name
plot_dir = vulcan_cfg.plot_dir  # Assume it's defined correctly

# Path to input files
vul_files = ['output/mtol_test/K2-18b_GJ176_nz250_1e12s_greg.vul',
             'output/mtol_test/K2-18b_GJ176_nz250_1e12s_q.vul',
             'output/mtol_test/K2-18b_GJ176_nz250_1e12s_10q.vul']

# Titles and axis limits for each plot
titles = ['1e-18', '1e-17', '1e-16']
axis_limits = [{'x_min': 1.E-10, 'x_max': 1, 'y_min': 0.5, 'y_max': 1.E-11}] * len(vul_files)

# Color setup
tableau20 = [(31, 119, 180), (255, 127, 14), (44, 160, 44), (214, 39, 40), (148, 103, 189),
             (140, 86, 75), (227, 119, 194), (127, 127, 127), (188, 189, 34), (23, 190, 207)]
tableau20 = [(r / 255., g / 255., b / 255.) for r, g, b in tableau20]

# Species labels and their corresponding error bars
species_error_data = {
    'H2O': {'x': 1e-6, 'y': 0.01, 'x_err_low': 0.4e-6, 'x_err_high': 0.6e-6},
    'CH4': {'x': 1e-4, 'y': 0.05, 'x_upper_bound': 1.2e-4},  # Upper bound only
    'CO2': {'x': 1e-2, 'y': 0.1, 'x_err_low': 0.2e-2, 'x_err_high': 0.5e-2}
}

# Species color mapping
tex_labels = {
    'H': 'H', 'H2': 'H$_2$', 'O': 'O', 'OH': 'OH', 'H2O': 'H$_2$O',
    'CH': 'CH', 'C': 'C', 'CH2': 'CH$_2$', 'CH3': 'CH$_3$', 'CH4': 'CH$_4$',
    'HCO': 'HCO', 'H2CO': 'H$_2$CO', 'C4H2': 'C$_4$H$_2$', 'C2': 'C$_2$', 'C2H2': 'C$_2$H$_2$',
    'CO': 'CO', 'CO2': 'CO$_2$', 'He': 'He', 'O2': 'O$_2$'
}

# Plot setup
fig, axes = plt.subplots(1, len(vul_files), figsize=(len(vul_files) * 6, 5), constrained_layout=True)

for idx, (vul_file, title) in enumerate(zip(vul_files, titles)):
    with open(vul_file, 'rb') as handle:
        data = pickle.load(handle)

    ax = axes[idx] if len(vul_files) > 1 else axes
    vulcan_spec = data['variable']['species']

    # Use custom axis limits or fallback to default values
    limits = axis_limits[idx] if idx < len(axis_limits) else {'x_min': 1.E-10, 'x_max': 1, 'y_min': 1, 'y_max': 1.E-11}
    
    for color_index, sp in enumerate(plot_spec.split(',')):
        if color_index == len(tableau20):  # Generate random colors if limit exceeded
            tableau20.append(tuple(np.random.rand(3)))
        sp_label = tex_labels.get(sp, sp)
        if sp in vulcan_spec:
            ax.plot(
                data['variable']['ymix'][:, vulcan_spec.index(sp)],
                data['atm']['pco'] / 1.e6,
                color=tableau20[color_index],
                label=sp_label,
                alpha=0.9
            )

        # Add error bars or upper-bound arrows matching species plot color
        if sp in species_error_data:
            error_data = species_error_data[sp]
            if 'x_upper_bound' in error_data:
                # Draw arrow for upper bound
                ax.annotate('', xy=(error_data['x_upper_bound'], error_data['y']),
                             xytext=(error_data['x_upper_bound'] * 0.7, error_data['y']),
                             arrowprops=dict(arrowstyle='->', lw=2, color=tableau20[color_index]),
                             label=f"{sp} Upper Bound")
            else:
                # Add asymmetric error bars
                ax.errorbar(
                    error_data['x'], error_data['y'],
                    xerr=[[error_data.get('x_err_low', 0)], [error_data.get('x_err_high', 0)]],
                    fmt='o', color=tableau20[color_index], markersize=8,
                    capsize=5, elinewidth=1.5, label=f"{sp} Error"
                )

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.invert_yaxis()
    ax.set_xlim(limits['x_min'], limits['x_max'])
    ax.set_ylim(limits['y_min'], limits['y_max'])
    ax.legend(frameon=0, prop={'size': 10}, loc='best')
    ax.set_title(title)
    ax.set_xlabel("Mixing Ratio")
    ax.set_ylabel("Pressure (bar)")

# Save as PNG output file
output_path = os.path.join(plot_dir, plot_name + '.png')
plt.savefig(output_path)
plt.show()
