
input_file = "sflux-GJ176_K2-18b.txt"  # Path to your input file
output_file = "sflux-GJ176_K2-18b_0.9_albedo.txt"  # Path to save the output file
A = 0.9 # Albedo (1 - A), modify this value as needed

def adjust_flux(input_file, output_file, A):
    # Initialize lists for wavelength (WL) and flux
    wavelength = []
    flux = []

    # Read data from the input file
    try:
        with open(input_file, "r") as file:
            for line in file:
                if line.startswith("#"):  # Skip header line
                    continue
                parts = line.split()
                wavelength.append(float(parts[0]))
                flux.append(float(parts[1]))

        # Multiply flux by (1 - A)
        adjusted_flux = [f * (1 - A) for f in flux]

        # Save the adjusted data to the output file
        with open(output_file, 'w') as out_file:
            out_file.write('# WL(nm)\t Flux(ergs/cm**2/s/nm)\n')
            for wl, adjusted_f in zip(wavelength, adjusted_flux):
                out_file.write(f"{wl:.6f}\t {adjusted_f:.2E}\n")
        
        print(f"File saved to {output_file}")

    except FileNotFoundError:
        print(f"File {input_file} not found.")
    except Exception as e:
        print(f"Error: {e}")


adjust_flux(input_file, output_file, A)