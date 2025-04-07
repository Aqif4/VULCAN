'''
Normally the observation like MUSCLES provides the flux observed from Earth.
So we need to scale it back to the surface of the star.
In SIMBAD, mas = 0.001 arcsec:
1 ly = 1000./ (X mas from SIMBAD) * 3.2616 
( 1 parsec = 1/p (arcsecond) , 1 ly = parsec * 3.2616 )

'''

#Input file
file='fits_files/hlsp_muscles_multi_multi_gj176_broadband_v22_adapt-const-res-sed.fits'
output='sflux-GJ176_adapt.txt'


stellar_radius= 0.478  #solar radii
stellar_distance_pc= 9.547   #pc

#Constants
lyr = 9.461e17  # cm
r_sun = 6.957E10 # cm
stellar_distance=stellar_distance_pc * 3.26 #pc to lyr

import numpy as np 
import scipy 
from astropy.io import fits 
from astropy.table import Table 

hdulist = fits.open(file)
print (hdulist.info())
spec = fits.getdata(file, 1)

# WAVELENGTH : midpoint of the wavelength bin in Angstroms
# WAVELENGTH0: left (blue) edge of the wavelength bin in Angstroms
# WAVELENGTH1: right (red) edge of the wavelength bin in Angstroms
# FLUX : average flux density in the wavelength bin in erg s-1 cm-2 Angstroms-1
# need to convert to ergs/cm**2/s/nm

new_str = '# WL(nm)\t Flux(ergs/cm**2/s/nm)\n'

for n,wl in enumerate(spec['WAVELENGTH']):
    new_str += '{:<12}'.format(wl*0.1) + "{:>12.2E}".format(float(spec['FLUX'][n]*10. *((stellar_distance*lyr)/(r_sun*stellar_radius))**2        )) + '\n'




# with open('VPL_solar.txt') as f:
#     for line in f.readlines():
#         if not line.startswith("#") and line.split():
#             li = line.split()
#             if float(li[0]) < 115.:
#                 new_str += '{:<12}'.format(li[0]) + "{:>12.2E}".format(float(li[1])) + '\n'
#             else: break
   
with open(output, 'w+') as f: f.write(new_str)   
