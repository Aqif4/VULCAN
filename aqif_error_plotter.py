import sys
import numpy as np
import matplotlib.pyplot as plt
import vulcan_cfg  # Assuming it's in the top-level directory
import os
import pickle

# Setting input arguments
plot_spec = 'H2O,CH4,CO2,CO,NH3,CH3CL,HCN'  # Species to plot, separated by commas
plot_name = 'vih_pt -25 to +75'  # Output plot name
plot_dir = vulcan_cfg.plot_dir  # Assume it's defined correctly

# Path to input files
vul_files = ['output/vih_pt/K2-18b_GJ176_nz250_1e17s_minus25K.vul',
'output/vih_pt/K2-18b_GJ176_nz250_5e16s_plus25K.vul',
'output/vih_pt/K2-18b_GJ176_nz250_1e17s_plus50K.vul',
'output/vih_pt/K2-18b_GJ176_nz250_1e17s_plus75K.vul',
			 
			 ]

# Titles and axis limits for each plot
titles = ['-25K', '+25K', '+50K', '+75K']
axis_limits = [{'x_min': 1.E-10, 'x_max': 1, 'y_min': 0.5, 'y_max': 1.E-11}] * len(vul_files)

# Color setup
tableau20 = [(31, 119, 180), (255, 127, 14), (44, 160, 44), (214, 39, 40), (148, 103, 189),
			 (140, 86, 75), (227, 119, 194), (127, 127, 127), (188, 189, 34), (23, 190, 207)]
tableau20 = [(r / 255., g / 255., b / 255.) for r, g, b in tableau20]

# Define error bar sets with central x and dx values in log scale, dx values should be positive
error_bar_sets = {
	'benneke_toi270d': { #Benneke et al. one offset
		'CH4': {'x_center': -1.64, 'dx_pos': 0.38, 'dx_neg': 0.36, 'y': 0.05}, 
		'CO2': {'x_center': -1.67, 'dx_pos': 0.40, 'dx_neg': 0.60, 'y': 0.1},
		'H2O': {'x_center': -1.10, 'dx_pos': 0.31, 'dx_neg': 0.92, 'y': 0.01},
		'CO': {'x_center': -1.46,'y': 0.02},
		'NH3': {'x_center': -4.27,'y': 0.03}#,
		#'SO2': {'x_center': 0.25e-2, 'y': 0.05},
		#'CS2': {'x_center': 0.25e-2, 'y': 0.05}

	},
	'madhu_toi270d': { #Madhu Holmberg 2023 one offset
		'CH4': {'x_center': -2.44, 'dx_pos': 0.34, 'dx_neg': 0.46, 'y': 0.03}, 
		'CO2': {'x_center': -1.96, 'dx_pos': 0.49, 'dx_neg': 0.79, 'y': 0.02},
		'H2O': {'x_center': -1.56, 'y': 0.03},  
		'NH3': {'x_center': -5.75, 'y': 0.05},
		#'CS2': {'x_center': 0.25e-2, 'dx_pos': 0.1e-2, 'dx_neg': 0.05e-2, 'y': 0.05},
		'C2H6': {'x_center': 0.25e-2, 'dx_pos': 0.1e-2, 'dx_neg': 0.05e-2, 'y': 0.05},
		'CO': {'x_center': -1.63, 'y': 0.05}
	},
	'cb_1': { #Carbon-bearing 2023 Madhu et al. one offset
			  #y values from photosphere which is between 1e-2, 1e-4 (Cooke Considerations)
		'CH4': {'x_center': -1.74, 'dx_pos': 0.59, 'dx_neg': 0.69, 'y': 0.5e-3}, 
		'CO2': {'x_center': -2.09, 'dx_pos': 0.51, 'dx_neg': 0.94, 'y': 1.2e-3},
		'H2O': {'x_center': -3.06, 'y': 0.5e-3},  
		'NH3': {'x_center': -4.51, 'y': 1.6e-3},
		'CO': {'x_center': -3.5, 'y': 1.8e-3},
		#'DMS':{'x_center': -6.35, 'dx_pos': 1.59, 'dx_neg': -3.60, 'y': 0.05},
		#'CH3CL':{'x_center': -3.80, 'y': 0.05},
		'HCN':{'x_center': -2.92, 'y': 4e-3},
		
	},
	# You can add more sets here
}

# Error bar set
error_bar_set = 'cb_1'  

# Use the selected error bar set
species_error_data = error_bar_sets[error_bar_set]

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
		capsize = 5  # For arrows and error bars

		if sp in species_error_data:
			error_data = species_error_data[sp]

			# Go back to base 10 for center
			x_center_10 = 10**(error_data['x_center'])  
			
			if 'x_center' in error_data and 'dx_pos' in error_data and 'dx_neg' in error_data:
				# Go back to base 10 for bounds
				x_high = 10**(error_data['x_center']+abs(error_data['dx_pos']))  
				x_low =  10**(error_data['x_center']-abs(error_data['dx_neg']))  
				# Add asymmetric error bars using the transformed values
				ax.errorbar(
					x_center_10,  # Plot the log-transformed central x value
					error_data['y'],
					xerr=[[abs(x_center_10-x_low)], [abs(x_center_10-x_high)]],  
					fmt='o',  # No markers
					color=tableau20[color_index], 
					markersize=5,
					capsize=capsize, 
					elinewidth=2,
					capthick=2
				)
			elif 'x_center' in error_data:
				# Draw a small line at the tail with a cap
				ax.plot([x_center_10, x_center_10], 
						[error_data['y'] * 1.4, error_data['y'] / 1.4], 
						color=tableau20[color_index], 
						lw=2)  # Tail line with a round cap
				# Draw arrow for upper bound only without legend label
				ax.annotate('', 
							xy=(x_center_10 * 1.1, error_data['y']), 
							xytext=(x_center_10 * 0.15, error_data['y']),
							arrowprops=dict(
								arrowstyle='<|-',  
								lw=2,               # Line width
								color=tableau20[color_index],  # Arrow color
								mutation_scale=16,   # Size of the arrow
							)
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
