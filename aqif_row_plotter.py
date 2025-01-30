import sys
import numpy as np
import matplotlib.pyplot as plt
import vulcan_cfg  # Assuming it's in the top-level directory

try:
    from PIL import Image
except ImportError:
    vulcan_cfg.use_PIL = False

import os
import pickle

# Setting input arguments
plot_spec = 'H2O,CH4,CO2,CO,NH3'  # Species to plot, separated by commas
plot_name = 'mtol investigation, original'  # Output plot name
plot_dir = vulcan_cfg.plot_dir  # Assume it's defined correctly

# Path to input files
vul_files =['output/mtol_test/K2-18b_GJ176_nz250_1e12s_greg.vul',
             'output/mtol_test/K2-18b_GJ176_nz250_1e12s_q.vul',
             'output/mtol_test/K2-18b_GJ176_nz250_1e12s_10q.vul']
             #'output/vih_botpressure/K2-18b_GJ176_nz250_1e17s_pb_5bar.vul',
             #'output/vih_botpressure/K2-18b_GJ176_nz250_1e17s_pb_10bar.vul']

# Titles and axis limits for each plot
titles = ['1e-18', '1e-17', '1e-16']# '5 bar', '10 bar'
axis_limits = [
    {'x_min': 1.E-10, 'x_max': 1, 'y_min': 0.5, 'y_max': 1.E-11},  # Custom limits for plot 1
    {'x_min': 1.E-10, 'x_max': 1, 'y_min': 0.5, 'y_max': 1.E-11},  # Custom limits for plot 2
    {'x_min': 1.E-10, 'x_max': 1, 'y_min': 0.5, 'y_max': 1.E-11}#,   # Custom limits for plot 3
    #{'x_min': 1.E-10, 'x_max': 1, 'y_min': 5, 'y_max': 1.E-11},  # Custom limits for plot 4
    #{'x_min': 1.E-10, 'x_max': 1, 'y_min': 10, 'y_max': 1.E-11},  # Custom limits for plot 5
]

# Color setup
tableau20 = [(31, 119, 180), (255, 127, 14), (44, 160, 44), (214, 39, 40), (148, 103, 189),
             (140, 86, 75), (227, 119, 194), (127, 127, 127), (188, 189, 34), (23, 190, 207)]
tableau20 = [(r / 255., g / 255., b / 255.) for r, g, b in tableau20]

# Species labels
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
