import matplotlib.pyplot as plt # type: ignore
import os

# Specify the input and output directories
input_dir = "atm/stellar_flux/"  # Change this to your actual input directory
output_dir = "plot/stellar_flux/"  # Change this to your actual output directory
output_filename = "GJ-176_0.3_albedo_var_vs_const.png"  # Name of the saved plot
plot_title=''

# List of input files and corresponding legend labels
files = [
    ("sflux-GJ176_from_muscles_var_0.3_albedo.txt", "var"),
    ("sflux-GJ176_from_muscles_0.3_albedo.txt", "const"),
    # Add more files as needed
]

# Colors for each spectrum line
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

# Create figure
plt.figure(figsize=(8, 6))

# Loop through each file and plot it
for i, (filename, legend_label) in enumerate(files):
    filepath = os.path.join(input_dir, filename)

    # Initialize lists for wavelength (WL) and flux data for each file
    wavelength = []
    flux = []

    # Read data from the file and skip the first line
    try:
        with open(filepath, "r") as file:
            next(file)  # Skip the first line
            for line in file:
                parts = line.split()
                wavelength.append(float(parts[0]))
                flux.append(float(parts[1]))
        
        # Plot the current spectrum
        color = colors[i % len(colors)]  # Cycle through colors if more files than colors
        plt.plot(wavelength, flux, color=color, linestyle='-', label=legend_label)

    except FileNotFoundError:
        print(f"File {filepath} not found. Skipping.")
        continue

# Add labels, title, legend, and grid
plt.xlabel("Wavelength (nm)")
plt.xscale('log')
plt.yscale('log')
plt.ylabel("Flux (ergs/cm²/s/nm)")
plt.title(plot_title)
plt.legend(loc="best")
plt.grid(True)

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Save the plot
output_path = os.path.join(output_dir, output_filename)
plt.savefig(output_path, dpi=300)
print(f"Plot saved to {output_path}")

# Close the figure to free memory
plt.show()