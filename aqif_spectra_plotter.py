import matplotlib.pyplot as plt 
import os

# Specify the input and output directories
input_dir = "atm/stellar_flux/"  # Change this to your actual input directory
output_dir = "plot/stellar_flux/"  # Change this to your actual output directory
output_filename = "GJ-176_vs_GJ-436_100-200nm.png"  # Name of the saved plot
plot_title = 'GJ-436 and GJ-176 between 100-200nm from MUSCLES'

# Define the wavelength range (in nm)
min_wavelength = 100  # Set lower limit
max_wavelength = 200  # Set upper limit

# List of input files, legend labels, and corresponding line styles
files = [
    ("sflux-GJ176_from_muscles.txt", "GJ-176", "-"),   # Solid line
    ("sflux-GJ436_from_muscles.txt", "GJ-436", "--")   # Dashed line
    # Add more files as needed, e.g., ("filename.txt", "label", "linestyle")
]

# Colors for each spectrum line
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

# Create figure
plt.figure(figsize=(8, 6))

# Loop through each file and plot it
for i, (filename, legend_label, line_style) in enumerate(files):
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
                wl = float(parts[0])
                f = float(parts[1])
                
                # Collect data within the specified range
                if min_wavelength <= wl <= max_wavelength:
                    wavelength.append(wl)
                    flux.append(f)
        
        # Check if data was collected in the range
        if not wavelength:
            print(f"No data in the specified range for {filename}. Skipping.")
            continue

        # Plot the current spectrum
        color = colors[i % len(colors)]  # Cycle through colors if more files than colors
        plt.plot(wavelength, flux, color=color, linestyle=line_style, label=legend_label)

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