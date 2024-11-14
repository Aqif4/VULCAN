import matplotlib.pyplot as plt
import sys

# Check if at least one file is provided
if len(sys.argv) < 2:
    print("Usage: python script.py file1.txt file2.txt ...")
    sys.exit(1)

# Colors for each spectrum line
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

# Loop through each file provided in the command line
for i, filename in enumerate(sys.argv[1:]):
    # Initialize lists for wavelength (WL) and flux data for each file
    wavelength = []
    flux = []
    
    # Read data from the current file and skip the first line
    try:
        with open(filename, "r") as file:
            next(file)  # Skip the first line
            for line in file:
                # Split each line into WL and flux, convert to float, and store in lists
                parts = line.split()
                wavelength.append(float(parts[0]))
                flux.append(float(parts[1]))
        
        # Plotting the current spectrum
        color = colors[i % len(colors)]  # Cycle through colors if more files than colors
        plt.plot(wavelength, flux, color=color, linestyle='-', label=f"{filename}")

    except FileNotFoundError:
        print(f"File {filename} not found. Skipping.")
        continue

# Adding labels, title, legend, and grid
plt.xlabel("Wavelength (nm)")
plt.ylabel("Flux (ergs/cm²/s/nm)")
plt.title("Multiple Spectra")
plt.legend(loc="best")
plt.grid(True)

# Show plot
plt.show()