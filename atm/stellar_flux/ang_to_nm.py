import sys
import pandas as pd
import os

# Check if a filename argument was provided
if len(sys.argv) < 2:
    print("Usage: python3 ang_to_nm.py <filename>")
    sys.exit(1)

# Load the filename from the command line argument
filename = sys.argv[1]

# Load the text file into a DataFrame
try:
    data = pd.read_csv(filename, sep='\s+', usecols=[0, 1])
    print("Data loaded successfully:")
except FileNotFoundError:
    print(f"Error: The file '{filename}' was not found.")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)

# Extract wavelength and flux columns
wavelength_ang = data.iloc[:, 0]
flux_ang = data.iloc[:, 1]

# Convert wavelength and flux
wavelength_nm = wavelength_ang / 10
flux_nm = flux_ang * 10

# Create a new DataFrame with the converted data
new_data = pd.DataFrame({
    'WL(nm)': wavelength_nm,
    'Flux(ergs/cm**2/s/nm)': flux_nm
})

# Format the columns to two decimal places for wavelength and scientific notation for flux
new_data['WL(nm)'] = new_data['WL(nm)'].map(lambda x: f"{x:5.2f}")
new_data['Flux(ergs/cm**2/s/nm)'] = new_data['Flux(ergs/cm**2/s/nm)'].map(lambda x: f"{x:.6E}")

# Change filename
base, ext = os.path.splitext(filename)
new_filename = base + "_nm" + ext

# Save the new DataFrame to a space-delimited file with headers
new_data.to_csv(new_filename, sep=' ', index=False, header=True)

print("Converted data saved to " + new_filename)