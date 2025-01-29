import numpy as np
from astropy.io import fits

# ========== USER CONFIGURABLE PARAMETERS ==========
star_name = "GJ163"  # Name of the star for filenames
distance_pc = 15.1351  # Distance to the star in parsecs
stellar_radius_solar = 0.405  # Stellar radius in solar radii
input_fits_filename = f'hlsp_muscles_multi_multi_{star_name.lower()}_broadband_v23_const-res-sed.fits'
output_flux_filename = f'sflux-{star_name}.txt'

# ========== CONSTANTS ==========
AU_CM = 1.4959787E13  # 1 AU in cm
R_SUN_CM = 6.957E10  # Solar radius in cm
PARSEC_CM = 3.085677581E18  # 1 parsec in cm

# Convert distance and stellar radius to cm
distance_cm = distance_pc * PARSEC_CM
stellar_radius_cm = stellar_radius_solar * R_SUN_CM

# ========== OPEN AND READ FITS FILE ==========
try:
    hdulist = fits.open(input_fits_filename)
    print(hdulist.info())
    spec = fits.getdata(input_fits_filename, 1)
except FileNotFoundError:
    print(f"Error: File '{input_fits_filename}' not found. Check the filename and path.")
    exit()

# ========== FLUX SCALING ==========
# Wavelength conversion from Ångstrom to nm, Flux scaled to surface of the star
new_str = '# WL(nm)\t Flux(ergs/cm**2/s/nm)\n'
scaling_factor = (distance_cm / stellar_radius_cm) ** 2

for n, wl in enumerate(spec['WAVELENGTH']):
    wl_nm = wl * 0.1  # Convert from Ångstrom to nm
    flux_scaled = float(spec['FLUX'][n] * 10. * scaling_factor)  # Scale and convert units
    new_str += '{:<12}'.format(wl_nm) + "{:>12.2E}".format(flux_scaled) + '\n'

# ========== SAVE OUTPUT ==========
with open(output_flux_filename, 'w+') as f:
    f.write(new_str)

print(f"Flux file saved as '{output_flux_filename}'")
