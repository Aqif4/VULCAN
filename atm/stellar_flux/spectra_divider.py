import numpy as np
import matplotlib.pyplot as plt

file1 = "sflux-GJ176_from_muscles.txt"  # Path to your first spectrum file
file2 = "sflux-GJ176_K2-18b.txt"   # Path to your second spectrum file

def divide_spectra(file1, file2):
    # Initialize lists for wavelength (WL) and flux for both files
    wavelength1 = []
    flux1 = []
    wavelength2 = []
    flux2 = []

    # Read data from the first file
    try:
        with open(file1, "r") as f1:
            for line in f1:
                if line.startswith("#"):  # Skip header lines
                    continue
                parts = line.split()
                wavelength1.append(float(parts[0]))
                flux1.append(float(parts[1]))

        # Read data from the second file
        with open(file2, "r") as f2:
            for line in f2:
                if line.startswith("#"):  # Skip header lines
                    continue
                parts = line.split()
                wavelength2.append(float(parts[0]))
                flux2.append(float(parts[1]))

    except FileNotFoundError:
        print("Error: One or both files not found.")
        return
    except Exception as e:
        print(f"Error: {e}")
        return

    # Check if wavelengths match
    if len(wavelength1) != len(wavelength2):
        print("Error: The wavelengths of the two spectra do not match.")
        return

    # Divide the flux of the two spectra
    flux_ratio = np.divide(flux1, flux2)

    # Calculate the mean multiple (average of the flux ratio)
    mean_multiple = np.mean(flux_ratio)
    print(f"Mean multiple: {mean_multiple:.4f}")

    # Plotting the ratio of the two spectra
    plt.plot(wavelength1, flux_ratio, label="Flux Ratio (File1 / File2)", color='b')
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Flux Ratio")
    plt.xscale('log')
    plt.yscale('log')
    plt.title("Mean mutiple="+str(mean_multiple))
    plt.grid(True)
     
    # Close the plot
    plt.show()

divide_spectra(file1, file2)