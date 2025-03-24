#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Mon Nov  4 15:30:09 2024

@author: gregcooke
"""

'''
Instructions to user:
    
    filename is the config file that is produced
    file_path is the file path of the atmospheric file you want get spectra from
    filout is the output config file
    changing these three to the correct inputs and running the script should work
    provided your conda environment is set up correctly
    
    Star options include the Sun, K2-18, and TOI-270
    
    Other changes can be made
    
'''

'''
Aqif amendments

Commented out lines:
184
220
235

config filepath
spectra output filepath
name
'''

#%% Set file and observation parameters

# Set auto_upload = True if you want to upload to PSG from the command line
# Set auto_upload = False if you want to upload to PSG manually
auto_upload = True

overall_name='W24_VIH_spectra'
file_path = "output/VIH_K2-18b_standard_GJ176_nz250_1e17s_3.vul"

filename = 'PSG/'+overall_name+'_cfg.txt'
fileout = 'PSG/'+overall_name+'.txt'

#Includes sulfur molecules for observations
sulfur = False

#define atmospheric mean molecular weight 
mmw = 3.2

# Decide on telescope, note that some options have been user defined, others
# are defined by PSG. The options are as follows:
telescopes = ['LUVOIR HDI', 'LUVOIR A-UV', 'LUVOIR B-UV', 'LUVOIR A-VIS', 'LUVOIR B-VIS',
              'LUVOIR A-NIR', 'LUVOIR B-NIR', 'JWST NIRSpec', 'JWST MIRI', 
              'Keck HIRES', 'Keck NIRSpec', 'Ideal']

Telescope = 'JWST NIRSpec' #LUVOIR HDI #LUVOIR HDI 6m #LUVOIR A-NIR'
#Name of simulation
name = 'K2-18 b Inhabited Hycean'
#Decide on observation type, geometry and distance
transit = True
phase = 180 #For edge on, 180 is transit, 90 or 270 is max seperation, 0 is secondary eclipse
planet_distance = 38 #distance in pc
Object = 'Exoplanet'
Star = 'K2-18'
object_name = 'K2-18 b'
albedo = False
surface_P = '1' #surface pressure in bar
semi_major_axis = str(0.06) # semi-major axis in AU

if (albedo == True): transit = False
if (transit == False): unit = 'Wm2um'
    
# define solar latitude and longitude
sollon='0'
sollat='0'

if (albedo == True):
    unit = 'rif'

#Telescope exposures
exposure_time = 60 #in seconds
exposure_number = 10 

if (transit == True):
    if (Star == 'K2-18'):
        exposure_time = 60 #in seconds
        exposure_number = 53 
    phase = 180
    unit = 'rkm'
    #for transit unit, can also do ppm
    
total_T = exposure_time * exposure_number / (60**2)

#%%  Wavelength ranges for an 'ideal' telescope. 
# This is to be used for mission planning, or estimating what capabilities
# Note the noise data for Ideal is probably nonsense. This is more for just
# producing a spectrum and certain wavelengths with a specific spectral resolution, R

Ideal_wav_start = '0.1'
Ideal_wav_end = '20'
Ideal_R = '250'
  
#%% Star properties
if (Star == 'Sun'):
    #Values for Earth
    stellar_type = 'G' #stellar type
    stellar_temp = '5777' #stellar effective temperature
    stellar_radius = '1' #radius of star
    Metallicity = '0.0' #metallicity of star
    period = '365' #orbital period
    eccentricity = '0.01670' #orbital eccentricity
    diameter = '12742' #planet diameter
    gravity = '9.81' #gravity on the planet
elif (Star == 'TOI-270'):
    #Values for TOI-270 star
    stellar_type = 'M'
    stellar_temp = '3506'
    stellar_radius = '0.378'
    Metallicity = '-0.20'
    period = '11.379573'
    eccentricity = '0.0'
    diameter = str(int(12742*2.133)) #planet diameter
    gravity = '9.06'   
    total_T = round(total_T, 3)
    planet_distance = 22.477 #in parsec
    semi_major_axis = str(0.07210) # semi-major axis in AU
elif (Star == 'K2-18'):
    #Values for K218 star
    stellar_type = 'M'
    stellar_temp = '3503'
    stellar_radius = '	0.469'
    Metallicity = '0.123'
    period = '32.94' #in days
    eccentricity = '0.0'
    diameter = str(int(12742*2.61)) #planet diameter
    gravity = '12.2'   
    total_T = round(total_T, 3)
    planet_distance = 38 #in parsec
    semi_major_axis = str(0.15910) # semi-major axis in AU
    
# Clouds (It think you can specify a distribution too)
cloud_sizes = '5,100' #cloud sizes for liquid and ice particles, respectively

#Create a string of the distance
distance = str(planet_distance) #distance in pc
#%% imports

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

#import scipy
from matplotlib import rcParams
rcParams['font.weight'] = 'bold' 
def thick_axes(top = False, direction = 'in'):
    # Accessing the axes object and setting linewidth
    plt.gca().spines['top'].set_linewidth(2)  # Top axis
    plt.gca().spines['bottom'].set_linewidth(2)  # Bottom axis
    plt.gca().spines['left'].set_linewidth(2)  # Left axis
    plt.gca().spines['right'].set_linewidth(2)  # Right axis
    plt.tick_params(which = 'major', axis = 'both', direction = direction, labelsize = 15, length = 4, width = 2, right = True, top = top)
    plt.tick_params(which = 'minor',axis = 'both', direction = direction, labelsize = 15, length = 2, width = 1, right = True, top = top)
#%% return subscript number or text
def sub(num):
    return r'$_{'+str(num)+'}$'

#%% return superscript number or text
def sup(num):
    return r'$^{'+str(num)+'}$'

dpi = 200
#%% colour bar definition

def cbar(model, label = True, clabel = 'O'+ sub(3) +' column [DU]', orientation='vertical', tick = False, ticks = [2,3], shrink = 1):
    cbar = plt.colorbar(model, orientation = orientation, shrink = shrink)
    if (label == True):
        clabel = clabel
        cbar.set_label(clabel,size=15, weight = 'bold')
    cbar.ax.tick_params(labelsize=15)
    if (tick == True):
        cbar.set_ticks(ticks)
        
#%% Read in VULCAN data

import pickle
# from scipy.integrate import trapz
def read_pickle_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
            return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the pickle file: {e}")
        return None
    
#%% Save array function
def save_array(data, species_name = 'H'):
    species = data['variable']['species']
    return data['variable']['ymix'][:,species.index(species_name)]

#%% Read in file specified at top of script

data = read_pickle_file(file_path)

#%% Now arrange arrays

temp = data['atm']['Tco']
press = data['atm']['pco']/1e6 # conversion to bar
H = save_array(data, species_name = 'H')
H2 = save_array(data, species_name = 'H2')
H2O = save_array(data, species_name = 'H2O')
CO2 = save_array(data, species_name = 'CO2')
CO = save_array(data, species_name = 'CO')
CH4 = save_array(data, species_name = 'CH4')
N2 = save_array(data, species_name = 'N2')
NH3 = save_array(data, species_name = 'NH3')
HCN = save_array(data, species_name = 'HCN')
O2 = save_array(data, species_name = 'O2')
#O3 = save_array(data, species_name = 'O3')
N2O = save_array(data, species_name = 'N2O')

# Dictionary of molecule data (assuming more molecules in the actual dataset)
molecules = {
    'P': press,
    'T': temp,
    'H2': H2,
    'H2O': H2O,
    'CH4': CH4,
    'CO2': CO2,
    'N2': N2,
    'NH3': NH3,
    'O2': O2,
    #'O3': O3,
    'N2O': N2O,
    # Add other molecules here
}

GASES='H2,H2O,CH4,CO2,N2,NH3,O2,O3,N2O'
HIT='HIT[45],HIT[2],HIT[6],HIT[2],HIT[22],HIT[11],HIT[7],HIT[3],HIT[4]'
ABUN='1,1,1,1,1,1,1,1,1'
ATM_UNIT='scl,scl,scl,scl,scl,scl,scl,scl,scl'

if (sulfur == True):
    SO2 = save_array(data, species_name = 'SO2')
    CS2 = save_array(data, species_name = 'CS2')
    H2S = save_array(data, species_name = 'H2S')
    
    # Dictionary of molecule data (assuming more molecules in the actual dataset)
    molecules = {
        'P': press,
        'T': temp,
        'H2': H2,
        'H2O': H2O,
        'CH4': CH4,
        'CO2': CO2,
        'N2': N2,
        'NH3': NH3,
        'O2': O2,
        'O3': O3,
        'N2O': N2O,
        'SO2': SO2,
        'CS2': CS2,
        'H2S': H2S,
        # Add other molecules here
    }

    GASES='H2,H2O,CH4,CO2,N2,NH3,SO2,CS2,H2S'
    HIT='HIT[45],HIT[2],HIT[6],HIT[2],HIT[22],HIT[11],HIT[9],HIT[53],HIT[22]'
    ABUN='1,1,1,1,1,1,1,1,1'
    ATM_UNIT='scl,scl,scl,scl,scl,scl,scl,scl,scl'

layers = str(len(press))

NGAS=len(molecules)-2

#%% And write to a PSG file

# Specify output file
output_file = "/Users/aqifchoudhury/Documents/VULCAN/"+filename

#%%
velocity = '0'
periapsis = 0
season = phase
# Save object parameters
newf = []
newf.append('<OBJECT>'+Object)
newf.append('<OBJECT-NAME>'+object_name)
newf.append('<OBJECT-DATE>2024 00:00')
newf.append('<OBJECT-DIAMETER>'+diameter)
newf.append('<OBJECT-GRAVITY>'+gravity)
newf.append('<OBJECT-GRAVITY-UNIT>g')
newf.append('<OBJECT-STAR-DISTANCE>'+semi_major_axis)
newf.append('<OBJECT-STAR-VELOCITY>'+velocity)
newf.append('<OBJECT-SOLAR-LONGITUDE>'+sollon)
newf.append('<OBJECT-SOLAR-LATITUDE>'+sollat)
if (transit == True):
    newf.append('<OBJECT-SEASON>180')
else:
    newf.append('<OBJECT-SEASON>'+str(season))
newf.append('<OBJECT-STAR-TYPE>'+stellar_type)
newf.append('<OBJECT-STAR-TEMPERATURE>'+stellar_temp)
newf.append('<OBJECT-STAR-RADIUS>'+stellar_radius)
newf.append('<OBJECT-OBS-LONGITUDE>'+sollon)
newf.append('<OBJECT-OBS-LATITUDE>'+sollat)
newf.append('<OBJECT-STAR-METALLICITY>'+Metallicity)
newf.append('<OBJECT-PERIOD>'+period)
newf.append('<OBJECT-PERIAPSIS>'+str(periapsis))
newf.append('<OBJECT-OBS-VELOCITY>29.0')
newf.append('<OBJECT-INCLINATION>90.00')
newf.append('<OBJECT-ECCENTRICITY>'+eccentricity)
# Save geometry parameters
newf.append('<GEOMETRY>Observatory')
newf.append('<GEOMETRY-OFFSET-NS>0.0')
newf.append('<GEOMETRY-OFFSET-EW>0.0')
newf.append('<GEOMETRY-OFFSET-UNIT>arcsec')
newf.append('<GEOMETRY-OBS-ALTITUDE>'+distance)
newf.append('<GEOMETRY-ALTITUDE-UNIT>pc')
newf.append('<GEOMETRY-USER-PARAM>0.0')
newf.append('<GEOMETRY-STELLAR-TYPE>G')
newf.append('<GEOMETRY-STELLAR-TEMPERATURE>'+stellar_temp)
newf.append('<GEOMETRY-STELLAR-MAGNITUDE>0')
newf.append('<GEOMETRY-SOLAR-ANGLE>90.000')
newf.append('<GEOMETRY-OBS-ANGLE>90')
newf.append('<GEOMETRY-PLANET-FRACTION>1.000e+00')
if (transit == True): 
    newf.append('<GEOMETRY-STAR-DISTANCE>0')
else:
    G_S_D = abs((1.49e11*np.sin(season*np.pi/180) / (planet_distance * 3.086e16))/4.8481e-6)
    newf.append('<GEOMETRY-STAR-DISTANCE>'+str(G_S_D))
if (transit == True):
    newf.append('<GEOMETRY-STAR-FRACTION>'+str(8.38086e-05))
    newf.append('<GEOMETRY-PHASE>180')
else:
    newf.append('<GEOMETRY-STAR-FRACTION>0')
    newf.append('<GEOMETRY-PHASE>'+str(season))
newf.append('<GEOMETRY-REF>User')
newf.append('<GEOMETRY-DISK-ANGLES>1')
newf.append('<GEOMETRY-ROTATION>-0.00,0.00')
newf.append('<GEOMETRY-AZIMUTH>0.000')
newf.append('<GEOMETRY-BRDFSCALER>1.000')


if (Telescope == 'LUVOIR HDI'):
    newf.append('<GENERATOR-INSTRUMENT>LUVOIR_HDI: The HDI design provides a 2 x 3 arcminute field-of-view with two channels simultaneously (via beamsplitter), an ultraviolet/visible (UVIS) channel covering the range 0.2-1.0 um and a near-infrared (NIR) channel covering the range 0.8-2.5um. The UVIS channel employs a CMOS detector and the NIR a HgCdTe detector. Dozens of filters and several grisms provide spectroscopic capabilities up to RP=500 in both channels.')
    newf.append('<GENERATOR-RANGE1>0.2')
    newf.append('<GENERATOR-RANGE2>2.5')
    newf.append('<GENERATOR-RANGEUNIT>um')
    newf.append('<GENERATOR-RESOLUTION>500')
    newf.append('<GENERATOR-RESOLUTIONUNIT>RP')
    newf.append('<GENERATOR-TELESCOPE>SINGLE')
    newf.append('<GENERATOR-DIAMTELE>15.0')
    newf.append('<GENERATOR-BEAM>1')
    newf.append('<GENERATOR-BEAM-UNIT>diffrac')
    newf.append('<GENERATOR-TELESCOPE1>1')
    newf.append('<GENERATOR-TELESCOPE2>2.0')
    newf.append('<GENERATOR-TELESCOPE3>1.0')
    newf.append('<GENERATOR-NOISE>CCD')
    newf.append('<GENERATOR-NOISE1>0.2@0.2,0.2@1,2.5@1.01,2.5@2.5')
    newf.append('<GENERATOR-NOISE2>3e-5@0.2,3e-5@1,2e-3@1.01,2e-3@2.5')
    newf.append('<GENERATOR-NOISEOTEMP>270')
    newf.append('<GENERATOR-NOISEOEFF>0.100@2.25e-1,0.112@2.75e-1,0.175@3.36e-1,0.211@4.75e-1,0.211@6.06e-1,0.211@7.75e-1,0.298@8.00e-1,0.342@1.26e+0,0.342@1.60e+0,0.335@2.22e+0,0.335@2.5')
    newf.append('<GENERATOR-NOISEOEMIS>0.1')
    newf.append('<GENERATOR-NOISETIME>'+str(exposure_time))
    newf.append('<GENERATOR-NOISEFRAMES>'+str(exposure_number))
    newf.append('<GENERATOR-NOISEPIXELS>8')
    newf.append('<GENERATOR-TRANS-APPLY>N')
    newf.append('<GENERATOR-TRANS-SHOW>N')
    newf.append('<GENERATOR-TRANS>03-01')
    newf.append('<GENERATOR-LOGRAD>N')
    newf.append('<GENERATOR-GAS-MODEL>Y')
    newf.append('<GENERATOR-CONT-MODEL>Y')
    newf.append('<GENERATOR-CONT-STELLAR>Y')
    newf.append('<GENERATOR-RADUNITS>'+unit)
    newf.append('<GENERATOR-NOISE2>3e-5@0.2,3e-5@1,2e-3@1.01,2e-3@2.0')
    newf.append('<GENERATOR-RESOLUTIONKERNEL>N')
    
if (Telescope == 'LUVOIR HDI 6m'):
    newf.append('<GENERATOR-INSTRUMENT>user')
    newf.append('<GENERATOR-RANGE1>0.2')
    newf.append('<GENERATOR-RANGE2>2.5')
    newf.append('<GENERATOR-RANGEUNIT>um')
    newf.append('<GENERATOR-RESOLUTION>500')
    newf.append('<GENERATOR-RESOLUTIONUNIT>RP')
    newf.append('<GENERATOR-TELESCOPE>SINGLE')
    newf.append('<GENERATOR-DIAMTELE>6')
    newf.append('<GENERATOR-BEAM>1')
    newf.append('<GENERATOR-BEAM-UNIT>diffrac')
    newf.append('<GENERATOR-TELESCOPE1>1')
    newf.append('<GENERATOR-TELESCOPE2>2.0')
    newf.append('<GENERATOR-TELESCOPE3>1.0')
    newf.append('<GENERATOR-NOISE>CCD')
    newf.append('<GENERATOR-NOISE1>0.2@0.2,0.2@1,2.5@1.01,2.5@2.5')
    newf.append('<GENERATOR-NOISE2>3e-5@0.2,3e-5@1,2e-3@1.01,2e-3@2.5')
    newf.append('<GENERATOR-NOISEOTEMP>270')
    newf.append('<GENERATOR-NOISEOEFF>0.100@2.25e-1,0.112@2.75e-1,0.175@3.36e-1,0.211@4.75e-1,0.211@6.06e-1,0.211@7.75e-1,0.298@8.00e-1,0.342@1.26e+0,0.342@1.60e+0,0.335@2.22e+0,0.335@2.5')
    newf.append('<GENERATOR-NOISEOEMIS>0.1')
    newf.append('<GENERATOR-NOISETIME>'+str(exposure_time))
    newf.append('<GENERATOR-NOISEFRAMES>'+str(exposure_number))
    newf.append('<GENERATOR-NOISEPIXELS>8')
    newf.append('<GENERATOR-TRANS-APPLY>N')
    newf.append('<GENERATOR-TRANS-SHOW>N')
    newf.append('<GENERATOR-TRANS>03-01')
    newf.append('<GENERATOR-LOGRAD>N')
    newf.append('<GENERATOR-GAS-MODEL>Y')
    newf.append('<GENERATOR-CONT-MODEL>Y')
    newf.append('<GENERATOR-CONT-STELLAR>Y')
    newf.append('<GENERATOR-RADUNITS>'+unit)
    newf.append('<GENERATOR-NOISE2>3e-5@0.2,3e-5@1,2e-3@1.01,2e-3@2.0')
    newf.append('<GENERATOR-RESOLUTIONKERNEL>N')


if (Telescope == 'LUVOIR A-UV'):
    newf.append('<GENERATOR-INSTRUMENT>LUVOIR_A-UV: The Extreme Coronagraph for Living Planetary Systems (ECLIPS) delivers continuous spectral coverage from 200 nm to 2.5 um via three channels, UV (200 to 525 nm), VIS (515 nm to 1030 nm), and NIR (1 to 2 microns). The UV channel is effectively an imager and provides a maximum resolution of RP=7, while the VIS channel RP=140, and NIR=70. The core coronagraph throughput is practically twice for LUVOIR-B than A.')
    newf.append('<GENERATOR-RANGE1>0.2')
    newf.append('<GENERATOR-RANGE2>0.515')
    newf.append('<GENERATOR-RANGEUNIT>um')
    newf.append('<GENERATOR-RESOLUTION>7')
    newf.append('<GENERATOR-RESOLUTIONUNIT>RP')
    newf.append('<GENERATOR-TELESCOPE>CORONA')
    newf.append('<GENERATOR-DIAMTELE>15.0')
    newf.append('<GENERATOR-BEAM>1')
    newf.append('<GENERATOR-BEAM-UNIT>diffrac')
    newf.append('<GENERATOR-TELESCOPE1>1E-10')
    newf.append('<GENERATOR-TELESCOPE2>4.5')
    newf.append('<GENERATOR-TELESCOPE3>2.700e-11@0.000,2.700e-11@0.217,2.700e-11@1.410,2.110e-03@2.278,6.329e-03@2.767,1.688e-02@3.092,5.063e-02@3.418,1.097e-01@3.797,1.477e-01@4.014,1.751e-01@4.231,1.920e-01@4.557,2.004e-01@5.371,2.004e-01@6.130,2.131e-01@6.618,2.532e-01@7.215,2.679e-01@9.005,2.700e-01@12.640,2.700e-01@17.631,2.700e-01@20.561,2.700e-01@24.304,2.700e-01@27.288,2.700e-01@29.349')
    newf.append('<GENERATOR-NOISE>CCD')
    newf.append('<GENERATOR-NOISE1>0@0.2,0@1,2.5@1.01,2.5@2.0')
    newf.append('<GENERATOR-NOISEOTEMP>270')
    newf.append('<GENERATOR-NOISEOEFF>0.0317@0.2000,0.0437@0.2261,0.0589@0.2580,0.0742@0.2986,0.0851@0.3377,0.0917@0.3667,0.0971@0.4029,0.1015@0.4493,0.1004@0.4971,0.1004@0.5140,0.1670@0.5150,0.1659@0.5377,0.1506@0.6304,0.1255@0.7087,0.0939@0.7986,0.0884@0.8435,0.1146@0.9058,0.1419@0.9594,0.1594@0.9942,0.1821@1.2200,0.1958@1.4100,0.2049@1.6200,0.2094@1.8700,0.2140@2.0000')
    newf.append('<GENERATOR-NOISEOEMIS>0.1')
    newf.append('<GENERATOR-NOISETIME>'+str(exposure_time))
    newf.append('<GENERATOR-NOISEFRAMES>'+str(exposure_number))
    newf.append('<GENERATOR-NOISEPIXELS>10')
    newf.append('<GENERATOR-TRANS-APPLY>N')
    newf.append('<GENERATOR-TRANS-SHOW>N')
    newf.append('<GENERATOR-TRANS>03-01')
    newf.append('<GENERATOR-LOGRAD>N')
    newf.append('<GENERATOR-GAS-MODEL>Y')
    newf.append('<GENERATOR-CONT-MODEL>Y')
    newf.append('<GENERATOR-CONT-STELLAR>Y')
    newf.append('<GENERATOR-RADUNITS>'+unit)
    newf.append('<GENERATOR-NOISE2>3e-5@0.2,3e-5@1,2e-3@1.01,2e-3@2.0')
    newf.append('<GENERATOR-RESOLUTIONKERNEL>N')
    
if (Telescope == 'LUVOIR B-UV'):
    newf.append('<GENERATOR-INSTRUMENT>LUVOIR_B-UV: The Extreme Coronagraph for Living Planetary Systems (ECLIPS) delivers continuous spectral coverage from 200 nm to 2.5 um via three channels, UV (200 to 525 nm), VIS (515 nm to 1030 nm), and NIR (1 to 2 microns). The UV channel is effectively an imager and provides a maximum resolution of RP=7, while the VIS channel RP=140, and NIR=70. The core coronagraph throughput is practically twice for LUVOIR-B than A.')
    newf.append('<GENERATOR-RANGE1>0.2')
    newf.append('<GENERATOR-RANGE2>0.515')
    newf.append('<GENERATOR-RANGEUNIT>um')
    newf.append('<GENERATOR-RESOLUTION>7')
    newf.append('<GENERATOR-RESOLUTIONUNIT>RP')
    newf.append('<GENERATOR-TELESCOPE>CORONA')
    newf.append('<GENERATOR-DIAMTELE>6.0')
    newf.append('<GENERATOR-BEAM>1')
    newf.append('<GENERATOR-BEAM-UNIT>diffrac')
    newf.append('<GENERATOR-TELESCOPE1>1E-10')
    newf.append('<GENERATOR-TELESCOPE2>4.5')
    newf.append('<GENERATOR-TELESCOPE3>4.578000e-11@0.000,4.578000e-11@0.216,4.578000e-11@0.649,2.110e-03@0.973,1.266e-02@1.459,8.228e-02@2.108,1.709e-01@2.973,2.658e-01@4.486,3.418e-01@6.757,3.945e-01@10.216,4.219e-01@14.108,4.409e-01@19.459,4.536e-01@23.622,4.578e-01@27.784,4.578e-01@29.459')
    newf.append('<GENERATOR-NOISE>CCD')
    newf.append('<GENERATOR-NOISE1>0@0.2,0@1,2.5@1.01,2.5@2.0')
    newf.append('<GENERATOR-NOISEOTEMP>270')
    newf.append('<GENERATOR-NOISEOEFF>0.0317@0.2000,0.0437@0.2261,0.0589@0.2580,0.0742@0.2986,0.0851@0.3377,0.0917@0.3667,0.0971@0.4029,0.1015@0.4493,0.1004@0.4971,0.1004@0.5140,0.1670@0.5150,0.1659@0.5377,0.1506@0.6304,0.1255@0.7087,0.0939@0.7986,0.0884@0.8435,0.1146@0.9058,0.1419@0.9594,0.1594@0.9942,0.1821@1.2200,0.1958@1.4100,0.2049@1.6200,0.2094@1.8700,0.2140@2.0000')
    newf.append('<GENERATOR-NOISEOEMIS>0.1')
    newf.append('<GENERATOR-NOISETIME>'+str(exposure_time))
    newf.append('<GENERATOR-NOISEFRAMES>'+str(exposure_number))
    newf.append('<GENERATOR-NOISEPIXELS>10')
    newf.append('<GENERATOR-TRANS-APPLY>N')
    newf.append('<GENERATOR-TRANS-SHOW>N')
    newf.append('<GENERATOR-TRANS>03-01')
    newf.append('<GENERATOR-LOGRAD>N')
    newf.append('<GENERATOR-GAS-MODEL>Y')
    newf.append('<GENERATOR-CONT-MODEL>Y')
    newf.append('<GENERATOR-CONT-STELLAR>Y')
    newf.append('<GENERATOR-RADUNITS>'+unit)
    newf.append('<GENERATOR-NOISE2>3e-5@0.2,3e-5@1,2e-3@1.01,2e-3@2.0')
    newf.append('<GENERATOR-RESOLUTIONKERNEL>N')
    
if (Telescope == 'LUVOIR A-UV no coronagraph'):
    print('LUVOIR A-UV no coronagraph')
    newf.append('<GENERATOR-INSTRUMENT>LUVOIR_A-UV: The Extreme Coronagraph for Living Planetary Systems (ECLIPS) delivers continuous spectral coverage from 200 nm to 2.5 um via three channels, UV (200 to 525 nm), VIS (515 nm to 1030 nm), and NIR (1 to 2 microns). The UV channel is effectively an imager and provides a maximum resolution of RP=7, while the VIS channel RP=140, and NIR=70. The core coronagraph throughput is practically twice for LUVOIR-B than A.')
    newf.append('<GENERATOR-RANGE1>0.2')
    newf.append('<GENERATOR-RANGE2>0.515')
    newf.append('<GENERATOR-RANGEUNIT>um')
    newf.append('<GENERATOR-RESOLUTION>7')
    newf.append('<GENERATOR-RESOLUTIONUNIT>RP')
    newf.append('<GENERATOR-TELESCOPE>SINGLE')
    newf.append('<GENERATOR-DIAMTELE>15.0')
    newf.append('<GENERATOR-BEAM>1')
    newf.append('<GENERATOR-BEAM-UNIT>diffrac')
    newf.append('<GENERATOR-TELESCOPE2>4.5')
    newf.append('<GENERATOR-TELESCOPE3>2.700e-11@0.000,2.700e-11@0.217,2.700e-11@1.410,2.110e-03@2.278,6.329e-03@2.767,1.688e-02@3.092,5.063e-02@3.418,1.097e-01@3.797,1.477e-01@4.014,1.751e-01@4.231,1.920e-01@4.557,2.004e-01@5.371,2.004e-01@6.130,2.131e-01@6.618,2.532e-01@7.215,2.679e-01@9.005,2.700e-01@12.640,2.700e-01@17.631,2.700e-01@20.561,2.700e-01@24.304,2.700e-01@27.288,2.700e-01@29.349')
    newf.append('<GENERATOR-NOISE>CCD')
    newf.append('<GENERATOR-NOISE1>0@0.2,0@1,2.5@1.01,2.5@2.0')
    newf.append('<GENERATOR-NOISEOTEMP>270')
    newf.append('<GENERATOR-NOISEOEFF>0.0317@0.2000,0.0437@0.2261,0.0589@0.2580,0.0742@0.2986,0.0851@0.3377,0.0917@0.3667,0.0971@0.4029,0.1015@0.4493,0.1004@0.4971,0.1004@0.5140,0.1670@0.5150,0.1659@0.5377,0.1506@0.6304,0.1255@0.7087,0.0939@0.7986,0.0884@0.8435,0.1146@0.9058,0.1419@0.9594,0.1594@0.9942,0.1821@1.2200,0.1958@1.4100,0.2049@1.6200,0.2094@1.8700,0.2140@2.0000')
    newf.append('<GENERATOR-NOISEOEMIS>0.1')
    newf.append('<GENERATOR-NOISETIME>'+str(exposure_time))
    newf.append('<GENERATOR-NOISEFRAMES>'+str(exposure_number))
    newf.append('<GENERATOR-NOISEPIXELS>10')
    newf.append('<GENERATOR-TRANS-APPLY>N')
    newf.append('<GENERATOR-TRANS-SHOW>N')
    newf.append('<GENERATOR-TRANS>03-01')
    newf.append('<GENERATOR-LOGRAD>N')
    newf.append('<GENERATOR-GAS-MODEL>Y')
    newf.append('<GENERATOR-CONT-MODEL>Y')
    newf.append('<GENERATOR-CONT-STELLAR>Y')
    newf.append('<GENERATOR-RADUNITS>'+unit)
    newf.append('<GENERATOR-NOISE2>3e-5@0.2,3e-5@1,2e-3@1.01,2e-3@2.0')
    newf.append('<GENERATOR-RESOLUTIONKERNEL>N')
    
if (Telescope == 'LUVOIR A-VIS'):
    newf.append('<GENERATOR-INSTRUMENT>LUVOIR_A-VIS: The Extreme Coronagraph for Living Planetary Systems (ECLIPS) delivers continuous spectral coverage from 200 nm to 2.5 um via three channels, UV (200 to 525 nm), VIS (515 nm to 1030 nm), and NIR (1 to 2 microns). The UV channel is effectively an imager and provides a maximum resolution of RP=7, while the VIS channel RP=140, and NIR=70. The core coronagraph throughput is practically twice for LUVOIR-B than A.')
    newf.append('<GENERATOR-RANGE1>0.515')
    newf.append('<GENERATOR-RANGE2>1.0')
    newf.append('<GENERATOR-RANGEUNIT>um')
    newf.append('<GENERATOR-RESOLUTION>140')
    newf.append('<GENERATOR-RESOLUTIONUNIT>RP')
    newf.append('<GENERATOR-TELESCOPE>CORONA')
    newf.append('<GENERATOR-DIAMTELE>15.0')
    newf.append('<GENERATOR-BEAM>1')
    newf.append('<GENERATOR-BEAM-UNIT>diffrac')
    newf.append('<GENERATOR-TELESCOPE1>1E-10')
    newf.append('<GENERATOR-TELESCOPE2>4.5')
    newf.append('<GENERATOR-TELESCOPE3>2.700e-11@0.000,2.700e-11@0.217,2.700e-11@1.410,2.110e-03@2.278,6.329e-03@2.767,1.688e-02@3.092,5.063e-02@3.418,1.097e-01@3.797,1.477e-01@4.014,1.751e-01@4.231,1.920e-01@4.557,2.004e-01@5.371,2.004e-01@6.130,2.131e-01@6.618,2.532e-01@7.215,2.679e-01@9.005,2.700e-01@12.640,2.700e-01@17.631,2.700e-01@20.561,2.700e-01@24.304,2.700e-01@27.288,2.700e-01@29.349')
    newf.append('<GENERATOR-NOISE>CCD')
    newf.append('<GENERATOR-NOISE1>0@0.2,0@1,2.5@1.01,2.5@2.0')
    newf.append('<GENERATOR-NOISEOTEMP>270')
    newf.append('<GENERATOR-NOISEOEFF>0.0317@0.2000,0.0437@0.2261,0.0589@0.2580,0.0742@0.2986,0.0851@0.3377,0.0917@0.3667,0.0971@0.4029,0.1015@0.4493,0.1004@0.4971,0.1004@0.5140,0.1670@0.5150,0.1659@0.5377,0.1506@0.6304,0.1255@0.7087,0.0939@0.7986,0.0884@0.8435,0.1146@0.9058,0.1419@0.9594,0.1594@0.9942,0.1821@1.2200,0.1958@1.4100,0.2049@1.6200,0.2094@1.8700,0.2140@2.0000')
    newf.append('<GENERATOR-NOISEOEMIS>0.1')
    newf.append('<GENERATOR-NOISETIME>'+str(exposure_time))
    newf.append('<GENERATOR-NOISEFRAMES>'+str(exposure_number))
    newf.append('<GENERATOR-NOISEPIXELS>10')
    newf.append('<GENERATOR-TRANS-APPLY>N')
    newf.append('<GENERATOR-TRANS-SHOW>N')
    newf.append('<GENERATOR-TRANS>03-01')
    newf.append('<GENERATOR-LOGRAD>N')
    newf.append('<GENERATOR-GAS-MODEL>Y')
    newf.append('<GENERATOR-CONT-MODEL>Y')
    newf.append('<GENERATOR-CONT-STELLAR>Y')
    newf.append('<GENERATOR-RADUNITS>'+unit)
    newf.append('<GENERATOR-NOISE2>3e-5@0.2,3e-5@1,2e-3@1.01,2e-3@2.0')
    newf.append('<GENERATOR-RESOLUTIONKERNEL>N')
    
if (Telescope == 'LUVOIR B-VIS'):
    newf.append('<GENERATOR-INSTRUMENT>LUVOIR_B-VIS: The Extreme Coronagraph for Living Planetary Systems (ECLIPS) delivers continuous spectral coverage from 200 nm to 2.5 um via three channels, UV (200 to 525 nm), VIS (515 nm to 1030 nm), and NIR (1 to 2 microns). The UV channel is effectively an imager and provides a maximum resolution of RP=7, while the VIS channel RP=140, and NIR=70. The core coronagraph throughput is practically twice for LUVOIR-B than A.')
    newf.append('<GENERATOR-RANGE1>0.515')
    newf.append('<GENERATOR-RANGE2>1.0')
    newf.append('<GENERATOR-RANGEUNIT>um')
    newf.append('<GENERATOR-RESOLUTION>140')
    newf.append('<GENERATOR-RESOLUTIONUNIT>RP')
    newf.append('<GENERATOR-TELESCOPE>CORONA')
    newf.append('<GENERATOR-DIAMTELE>6.0')
    newf.append('<GENERATOR-BEAM>1')
    newf.append('<GENERATOR-BEAM-UNIT>diffrac')
    newf.append('<GENERATOR-TELESCOPE1>1E-10')
    newf.append('<GENERATOR-TELESCOPE2>4.5')
    newf.append('<GENERATOR-TELESCOPE3>4.578000e-11@0.000,4.578000e-11@0.216,4.578000e-11@0.649,2.110e-03@0.973,1.266e-02@1.459,8.228e-02@2.108,1.709e-01@2.973,2.658e-01@4.486,3.418e-01@6.757,3.945e-01@10.216,4.219e-01@14.108,4.409e-01@19.459,4.536e-01@23.622,4.578e-01@27.784,4.578e-01@29.459')
    newf.append('<GENERATOR-NOISE>CCD')
    newf.append('<GENERATOR-NOISE1>0@0.2,0@1,2.5@1.01,2.5@2.0')
    newf.append('<GENERATOR-NOISEOTEMP>270')
    newf.append('<GENERATOR-NOISEOEFF>0.0317@0.2000,0.0437@0.2261,0.0589@0.2580,0.0742@0.2986,0.0851@0.3377,0.0917@0.3667,0.0971@0.4029,0.1015@0.4493,0.1004@0.4971,0.1004@0.5140,0.1670@0.5150,0.1659@0.5377,0.1506@0.6304,0.1255@0.7087,0.0939@0.7986,0.0884@0.8435,0.1146@0.9058,0.1419@0.9594,0.1594@0.9942,0.1821@1.2200,0.1958@1.4100,0.2049@1.6200,0.2094@1.8700,0.2140@2.0000')
    newf.append('<GENERATOR-NOISEOEMIS>0.1')
    newf.append('<GENERATOR-NOISETIME>'+str(exposure_time))
    newf.append('<GENERATOR-NOISEFRAMES>'+str(exposure_number))
    newf.append('<GENERATOR-NOISEPIXELS>10')
    newf.append('<GENERATOR-TRANS-APPLY>N')
    newf.append('<GENERATOR-TRANS-SHOW>N')
    newf.append('<GENERATOR-TRANS>03-01')
    newf.append('<GENERATOR-LOGRAD>N')
    newf.append('<GENERATOR-GAS-MODEL>Y')
    newf.append('<GENERATOR-CONT-MODEL>Y')
    newf.append('<GENERATOR-CONT-STELLAR>Y')
    newf.append('<GENERATOR-RADUNITS>'+unit)
    newf.append('<GENERATOR-NOISE2>3e-5@0.2,3e-5@1,2e-3@1.01,2e-3@2.0')
    newf.append('<GENERATOR-RESOLUTIONKERNEL>N')
    
if (Telescope == 'LUVOIR A-NIR'):
    newf.append('<GENERATOR-INSTRUMENT>LUVOIR_A-VIS: The Extreme Coronagraph for Living Planetary Systems (ECLIPS) delivers continuous spectral coverage from 200 nm to 2.5 um via three channels, UV (200 to 525 nm), VIS (515 nm to 1030 nm), and NIR (1 to 2 microns). The UV channel is effectively an imager and provides a maximum resolution of RP=7, while the VIS channel RP=140, and NIR=70. The core coronagraph throughput is practically twice for LUVOIR-B than A.')
    newf.append('<GENERATOR-RANGE1>1.01')
    newf.append('<GENERATOR-RANGE2>2.0')
    newf.append('<GENERATOR-RANGEUNIT>um')
    newf.append('<GENERATOR-RESOLUTION>70')
    newf.append('<GENERATOR-RESOLUTIONUNIT>RP')
    newf.append('<GENERATOR-TELESCOPE>CORONA')
    newf.append('<GENERATOR-DIAMTELE>15.0')
    newf.append('<GENERATOR-BEAM>1')
    newf.append('<GENERATOR-BEAM-UNIT>diffrac')
    newf.append('<GENERATOR-TELESCOPE1>1E-10')
    newf.append('<GENERATOR-TELESCOPE2>4.5')
    newf.append('<GENERATOR-TELESCOPE3>2.700e-11@0.000,2.700e-11@0.217,2.700e-11@1.410,2.110e-03@2.278,6.329e-03@2.767,1.688e-02@3.092,5.063e-02@3.418,1.097e-01@3.797,1.477e-01@4.014,1.751e-01@4.231,1.920e-01@4.557,2.004e-01@5.371,2.004e-01@6.130,2.131e-01@6.618,2.532e-01@7.215,2.679e-01@9.005,2.700e-01@12.640,2.700e-01@17.631,2.700e-01@20.561,2.700e-01@24.304,2.700e-01@27.288,2.700e-01@29.349')
    newf.append('<GENERATOR-NOISE>CCD')
    newf.append('<GENERATOR-NOISE1>0@0.2,0@1,2.5@1.01,2.5@2.0')
    newf.append('<GENERATOR-NOISEOTEMP>270')
    newf.append('<GENERATOR-NOISEOEFF>0.0317@0.2000,0.0437@0.2261,0.0589@0.2580,0.0742@0.2986,0.0851@0.3377,0.0917@0.3667,0.0971@0.4029,0.1015@0.4493,0.1004@0.4971,0.1004@0.5140,0.1670@0.5150,0.1659@0.5377,0.1506@0.6304,0.1255@0.7087,0.0939@0.7986,0.0884@0.8435,0.1146@0.9058,0.1419@0.9594,0.1594@0.9942,0.1821@1.2200,0.1958@1.4100,0.2049@1.6200,0.2094@1.8700,0.2140@2.0000')
    newf.append('<GENERATOR-NOISEOEMIS>0.1')
    newf.append('<GENERATOR-NOISETIME>'+str(exposure_time))
    newf.append('<GENERATOR-NOISEFRAMES>'+str(exposure_number))
    newf.append('<GENERATOR-NOISEPIXELS>10')
    newf.append('<GENERATOR-TRANS-APPLY>N')
    newf.append('<GENERATOR-TRANS-SHOW>N')
    newf.append('<GENERATOR-TRANS>03-01')
    newf.append('<GENERATOR-LOGRAD>N')
    newf.append('<GENERATOR-GAS-MODEL>Y')
    newf.append('<GENERATOR-CONT-MODEL>Y')
    newf.append('<GENERATOR-CONT-STELLAR>Y')
    newf.append('<GENERATOR-RADUNITS>'+unit)
    newf.append('<GENERATOR-NOISE2>3e-5@0.2,3e-5@1,2e-3@1.01,2e-3@2.0')
    newf.append('<GENERATOR-RESOLUTIONKERNEL>N')
    
if (Telescope == 'LUVOIR B-NIR'):
    newf.append('<GENERATOR-INSTRUMENT>LUVOIR_B-NIR: The Extreme Coronagraph for Living Planetary Systems (ECLIPS) delivers continuous spectral coverage from 200 nm to 2.5 um via three channels, UV (200 to 525 nm), VIS (515 nm to 1030 nm), and NIR (1 to 2 microns). The UV channel is effectively an imager and provides a maximum resolution of RP=7, while the VIS channel RP=140, and NIR=70. The core coronagraph throughput is practically twice for LUVOIR-B than A.')
    newf.append('<GENERATOR-RANGE1>1.01')
    newf.append('<GENERATOR-RANGE2>2.0')
    newf.append('<GENERATOR-RANGEUNIT>um')
    newf.append('<GENERATOR-RESOLUTION>70')
    newf.append('<GENERATOR-RESOLUTIONUNIT>RP')
    newf.append('<GENERATOR-TELESCOPE>CORONA')
    newf.append('<GENERATOR-DIAMTELE>6.0')
    newf.append('<GENERATOR-BEAM>1')
    newf.append('<GENERATOR-BEAM-UNIT>diffrac')
    newf.append('<GENERATOR-TELESCOPE1>1E-10')
    newf.append('<GENERATOR-TELESCOPE2>4.5')
    newf.append('<GENERATOR-TELESCOPE3>4.578000e-11@0.000,4.578000e-11@0.216,4.578000e-11@0.649,2.110e-03@0.973,1.266e-02@1.459,8.228e-02@2.108,1.709e-01@2.973,2.658e-01@4.486,3.418e-01@6.757,3.945e-01@10.216,4.219e-01@14.108,4.409e-01@19.459,4.536e-01@23.622,4.578e-01@27.784,4.578e-01@29.459')
    newf.append('<GENERATOR-NOISE>CCD')
    newf.append('<GENERATOR-NOISE1>0@0.2,0@1,2.5@1.01,2.5@2.0')
    newf.append('<GENERATOR-NOISEOTEMP>270')
    newf.append('<GENERATOR-NOISEOEFF>0.0317@0.2000,0.0437@0.2261,0.0589@0.2580,0.0742@0.2986,0.0851@0.3377,0.0917@0.3667,0.0971@0.4029,0.1015@0.4493,0.1004@0.4971,0.1004@0.5140,0.1670@0.5150,0.1659@0.5377,0.1506@0.6304,0.1255@0.7087,0.0939@0.7986,0.0884@0.8435,0.1146@0.9058,0.1419@0.9594,0.1594@0.9942,0.1821@1.2200,0.1958@1.4100,0.2049@1.6200,0.2094@1.8700,0.2140@2.0000')
    newf.append('<GENERATOR-NOISEOEMIS>0.1')
    newf.append('<GENERATOR-NOISETIME>'+str(exposure_time))
    newf.append('<GENERATOR-NOISEFRAMES>'+str(exposure_number))
    newf.append('<GENERATOR-NOISEPIXELS>10')
    newf.append('<GENERATOR-TRANS-APPLY>N')
    newf.append('<GENERATOR-TRANS-SHOW>N')
    newf.append('<GENERATOR-TRANS>03-01')
    newf.append('<GENERATOR-LOGRAD>N')
    newf.append('<GENERATOR-GAS-MODEL>Y')
    newf.append('<GENERATOR-CONT-MODEL>Y')
    newf.append('<GENERATOR-CONT-STELLAR>Y')
    newf.append('<GENERATOR-RADUNITS>'+unit)
    newf.append('<GENERATOR-NOISE2>3e-5@0.2,3e-5@1,2e-3@1.01,2e-3@2.0')
    newf.append('<GENERATOR-RESOLUTIONKERNEL>N')
    
    
if (Telescope == 'HabEx SS-UV'):
    newf.append('<GENERATOR-INSTRUMENT>HabEx_SS-UV: The HabEx StarShade (SS) will provide extraordinary high-contrast capabilities from the UV (0.2 to 0.45 um), to the visible (0.45 to 1um), and to the infrared (0.975 to 1.8 um). By limiting the number of optical surfaces, this configuration provides high optical throughput (0.2 to 0.4) across this broad of wavelengths, while the quantum efficiency (QE) is expected to be 0.9 for the VU and visible detectors and 0.6 for the infrared detector. The UV channel provides a resolution (RP) of 7, visible channel a maximum of 140 and the infrared 40.')
    newf.append('<GENERATOR-RANGE1>0.2')
    newf.append('<GENERATOR-RANGE2>0.45')
    newf.append('<GENERATOR-RANGEUNIT>um')
    newf.append('<GENERATOR-RESOLUTION>7')
    newf.append('<GENERATOR-RESOLUTIONUNIT>RP')
    newf.append('<GENERATOR-TELESCOPE>CORONA')
    newf.append('<GENERATOR-DIAMTELE>4.0')
    newf.append('<GENERATOR-BEAM>1.0')
    newf.append('<GENERATOR-BEAM-UNIT>diffrac')
    newf.append('<GENERATOR-TELESCOPE1>1E-10')
    newf.append('<GENERATOR-TELESCOPE2>4.5')
    newf.append('<GENERATOR-TELESCOPE3>7e-11@-0.000e+00,7e-11@-7.483e-03,7e-11@-1.436e-02,3.544e-03@-2.040e-02,1.949e-02@-2.547e-02,3.367e-02@-2.788e-02,6.734e-02@-2.993e-02,1.241e-01@-3.210e-02,2.091e-01@-3.416e-02,2.818e-01@-3.572e-02,3.332e-01@-3.657e-02,3.987e-01@-3.802e-02,4.661e-01@-3.947e-02,5.352e-01@-4.031e-02,6.008e-01@-4.164e-02,6.344e-01@-4.236e-02,6.699e-01@-4.333e-02,6.911e-01@-4.441e-02,7.000e-01@-4.791e-02,7.000e-01@-5.853e-02,7.000e-01@-7.314e-02,7.000e-01@-8.340e-02,7.000e-01@-8.810e-02')
    newf.append('<GENERATOR-NOISE>CCD')
    newf.append('<GENERATOR-NOISE1>0.008@0.2,0.008@0.975,0.32@0.976,0.32@1.8')
    newf.append('<GENERATOR-NOISE2>3e-5@0.2,3e-5@0.975,0.005@0.976,0.005@1.8')
    newf.append('<GENERATOR-NOISEOTEMP>270')
    newf.append('<GENERATOR-NOISEOEFF>0.2260@0.2000,0.2201@0.2112,0.2182@0.2224,0.2300@0.2587,0.2536@0.3035,0.2673@0.3399,0.2791@0.3874,0.2830@0.4294,0.2850@0.4490,0.1796@0.4500,0.1848@0.5161,0.1749@0.6503,0.1474@0.7734,0.1415@0.8434,0.1592@0.9021,0.1926@0.9608,0.1988@0.9750,0.1988@0.9760,0.2162@1.0587,0.2339@1.2462,0.2437@1.4503,0.2516@1.6657,0.2594@1.8000')
    newf.append('<GENERATOR-NOISEOEMIS>0.10')
    newf.append('<GENERATOR-NOISETIME>'+str(exposure_time))
    newf.append('<GENERATOR-NOISEFRAMES>'+str(exposure_number))
    newf.append('<GENERATOR-NOISEPIXELS>10')
    newf.append('<GENERATOR-TRANS-APPLY>N')
    newf.append('<GENERATOR-TRANS-SHOW>N')
    newf.append('<GENERATOR-LOGRAD>N')
    newf.append('<GENERATOR-GAS-MODEL>Y')
    newf.append('<GENERATOR-CONT-MODEL>Y')
    newf.append('<GENERATOR-CONT-STELLAR>N')
    newf.append('<GENERATOR-RADUNITS>'+unit)
    newf.append('<GENERATOR-RESOLUTIONKERNEL>N')
    newf.append('<GENERATOR-TRANS>02-01')
    
if (Telescope == 'HabEx SS-VIS'):
    newf.append('<GENERATOR-INSTRUMENT>HabEx_SS-VIS: The HabEx StarShade (SS) will provide extraordinary high-contrast capabilities from the UV (0.2 to 0.45 um), to the visible (0.45 to 1um), and to the infrared (0.975 to 1.8 um). By limiting the number of optical surfaces, this configuration provides high optical throughput (0.2 to 0.4) across this broad of wavelengths, while the quantum efficiency (QE) is expected to be 0.9 for the VU and visible detectors and 0.6 for the infrared detector. The UV channel provides a resolution (RP) of 7, visible channel a maximum of 140 and the infrared 40.')
    newf.append('<GENERATOR-RANGE1>0.45')
    newf.append('<GENERATOR-RANGE2>0.975')
    newf.append('<GENERATOR-RANGEUNIT>um')
    newf.append('<GENERATOR-RESOLUTION>140')
    newf.append('<GENERATOR-RESOLUTIONUNIT>RP')
    newf.append('<GENERATOR-TELESCOPE>CORONA')
    newf.append('<GENERATOR-DIAMTELE>4.0')
    newf.append('<GENERATOR-BEAM>1.0')
    newf.append('<GENERATOR-BEAM-UNIT>diffrac')
    newf.append('<GENERATOR-TELESCOPE1>1E-10')
    newf.append('<GENERATOR-TELESCOPE2>4.5')
    newf.append('<GENERATOR-TELESCOPE3>7e-11@-0.000e+00,7e-11@-1.113e-02,7e-11@-2.136e-02,3.544e-03@-3.033e-02,1.949e-02@-3.787e-02,3.367e-02@-4.146e-02,6.734e-02@-4.451e-02,1.241e-01@-4.774e-02,2.091e-01@-5.079e-02,2.818e-01@-5.313e-02,3.332e-01@-5.438e-02,3.987e-01@-5.654e-02,4.661e-01@-5.869e-02,5.352e-01@-5.995e-02,6.008e-01@-6.192e-02,6.344e-01@-6.300e-02,6.699e-01@-6.444e-02,6.911e-01@-6.605e-02,7.000e-01@-7.126e-02,7.000e-01@-8.705e-02,7.000e-01@-1.088e-01,7.000e-01@-1.240e-01,7.000e-01@-1.310e-01')
    newf.append('<GENERATOR-NOISE>CCD')
    newf.append('<GENERATOR-NOISE1>0.008@0.2,0.008@0.975,0.32@0.976,0.32@1.8')
    newf.append('<GENERATOR-NOISE2>3e-5@0.2,3e-5@0.975,0.005@0.976,0.005@1.8')
    newf.append('<GENERATOR-NOISEOTEMP>270')
    newf.append('<GENERATOR-NOISEOEFF>0.2260@0.2000,0.2201@0.2112,0.2182@0.2224,0.2300@0.2587,0.2536@0.3035,0.2673@0.3399,0.2791@0.3874,0.2830@0.4294,0.2850@0.4490,0.1796@0.4500,0.1848@0.5161,0.1749@0.6503,0.1474@0.7734,0.1415@0.8434,0.1592@0.9021,0.1926@0.9608,0.1988@0.9750,0.1988@0.9760,0.2162@1.0587,0.2339@1.2462,0.2437@1.4503,0.2516@1.6657,0.2594@1.8000')
    newf.append('<GENERATOR-NOISEOEMIS>0.10')
    newf.append('<GENERATOR-NOISETIME>'+str(exposure_time))
    newf.append('<GENERATOR-NOISEFRAMES>'+str(exposure_number))
    newf.append('<GENERATOR-NOISEPIXELS>10')
    newf.append('<GENERATOR-TRANS-APPLY>N')
    newf.append('<GENERATOR-TRANS-SHOW>N')
    newf.append('<GENERATOR-LOGRAD>N')
    newf.append('<GENERATOR-GAS-MODEL>Y')
    newf.append('<GENERATOR-CONT-MODEL>Y')
    newf.append('<GENERATOR-CONT-STELLAR>N')
    newf.append('<GENERATOR-RADUNITS>'+unit)
    newf.append('<GENERATOR-RESOLUTIONKERNEL>N')
    newf.append('<GENERATOR-TRANS>02-01')
    
if (Telescope == 'HabEx SS-NIR'):
    newf.append('<GENERATOR-INSTRUMENT>HabEx_SS-NIR: The HabEx StarShade (SS) will provide extraordinary high-contrast capabilities from the UV (0.2 to 0.45 um), to the visible (0.45 to 1um), and to the infrared (0.975 to 1.8 um). By limiting the number of optical surfaces, this configuration provides high optical throughput (0.2 to 0.4) across this broad of wavelengths, while the quantum efficiency (QE) is expected to be 0.9 for the VU and visible detectors and 0.6 for the infrared detector. The UV channel provides a resolution (RP) of 7, visible channel a maximum of 140 and the infrared 40.')
    newf.append('<GENERATOR-RANGE1>0.975')
    newf.append('<GENERATOR-RANGE2>1.80')
    newf.append('<GENERATOR-RANGEUNIT>um')
    newf.append('<GENERATOR-RESOLUTION>40')
    newf.append('<GENERATOR-RESOLUTIONUNIT>RP')
    newf.append('<GENERATOR-TELESCOPE>CORONA')
    newf.append('<GENERATOR-DIAMTELE>4.0')
    newf.append('<GENERATOR-BEAM>1.0')
    newf.append('<GENERATOR-BEAM-UNIT>diffrac')
    newf.append('<GENERATOR-TELESCOPE1>1E-10')
    newf.append('<GENERATOR-TELESCOPE2>4.5')
    newf.append('<GENERATOR-TELESCOPE3>7e-11@-0.000e+00,7e-11@-1.995e-02,7e-11@-3.830e-02,3.544e-03@-5.439e-02,1.949e-02@-6.791e-02,3.367e-02@-7.434e-02,6.734e-02@-7.982e-02,1.241e-01@-8.561e-02,2.091e-01@-9.108e-02,2.818e-01@-9.526e-02,3.332e-01@-9.752e-02,3.987e-01@-1.014e-01,4.661e-01@-1.052e-01,5.352e-01@-1.075e-01,6.008e-01@-1.110e-01,6.344e-01@-1.130e-01,6.699e-01@-1.155e-01,6.911e-01@-1.184e-01,7.000e-01@-1.278e-01,7.000e-01@-1.561e-01,7.000e-01@-1.950e-01,7.000e-01@-2.224e-01,7.000e-01@-2.349e-01')
    newf.append('<GENERATOR-NOISE>CCD')
    newf.append('<GENERATOR-NOISE1>0.008@0.2,0.008@0.975,0.32@0.976,0.32@1.8')
    newf.append('<GENERATOR-NOISE2>3e-5@0.2,3e-5@0.975,0.005@0.976,0.005@1.8')
    newf.append('<GENERATOR-NOISEOTEMP>270')
    newf.append('<GENERATOR-NOISEOEFF>0.2260@0.2000,0.2201@0.2112,0.2182@0.2224,0.2300@0.2587,0.2536@0.3035,0.2673@0.3399,0.2791@0.3874,0.2830@0.4294,0.2850@0.4490,0.1796@0.4500,0.1848@0.5161,0.1749@0.6503,0.1474@0.7734,0.1415@0.8434,0.1592@0.9021,0.1926@0.9608,0.1988@0.9750,0.1988@0.9760,0.2162@1.0587,0.2339@1.2462,0.2437@1.4503,0.2516@1.6657,0.2594@1.8000')
    newf.append('<GENERATOR-NOISEOEMIS>0.10')
    newf.append('<GENERATOR-NOISETIME>'+str(exposure_time))
    newf.append('<GENERATOR-NOISEFRAMES>'+str(exposure_number))
    newf.append('<GENERATOR-NOISEPIXELS>10')
    newf.append('<GENERATOR-TRANS-APPLY>N')
    newf.append('<GENERATOR-TRANS-SHOW>N')
    newf.append('<GENERATOR-LOGRAD>N')
    newf.append('<GENERATOR-GAS-MODEL>Y')
    newf.append('<GENERATOR-CONT-MODEL>Y')
    newf.append('<GENERATOR-CONT-STELLAR>N')
    newf.append('<GENERATOR-RADUNITS>'+unit)
    newf.append('<GENERATOR-RESOLUTIONKERNEL>N')
    newf.append('<GENERATOR-TRANS>02-01')
        
if (Telescope == 'LIFE'):
    newf.append('<GENERATOR-INSTRUMENT>user')
    newf.append('<GENERATOR-RANGE1>3')
    newf.append('<GENERATOR-RANGE2>20')
    newf.append('<GENERATOR-RANGEUNIT>um')
    newf.append('<GENERATOR-RESOLUTION>100')
    newf.append('<GENERATOR-RESOLUTIONUNIT>RP')
    newf.append('<GENERATOR-TELESCOPE>ARRAY')
    newf.append('<GENERATOR-DIAMTELE>3.5')
    newf.append('<GENERATOR-BEAM>0.006')
    newf.append('<GENERATOR-BEAM-UNIT>arcsec')
    newf.append('<GENERATOR-TELESCOPE1>4')
    newf.append('<GENERATOR-TELESCOPE2>2.0')
    newf.append('<GENERATOR-TELESCOPE3>1.0')
    newf.append('<GENERATOR-NOISE>CCD')
    newf.append('<GENERATOR-NOISE1>20.0')
    newf.append('<GENERATOR-NOISE2>0.005')
    newf.append('<GENERATOR-NOISEOTEMP>40')
    newf.append('<GENERATOR-NOISEOEFF>0.4')
    newf.append('<GENERATOR-NOISEOEMIS>0.10')
    newf.append('<GENERATOR-NOISETIME>'+str(exposure_time))
    newf.append('<GENERATOR-NOISEFRAMES>'+str(exposure_number))
    newf.append('<GENERATOR-NOISEPIXELS>8')
    newf.append('<GENERATOR-TRANS-APPLY>N')
    newf.append('<GENERATOR-TRANS-SHOW>N')
    newf.append('<GENERATOR-LOGRAD>Y')
    newf.append('<GENERATOR-GAS-MODEL>Y')
    newf.append('<GENERATOR-CONT-MODEL>Y')
    newf.append('<GENERATOR-CONT-STELLAR>Y')
    newf.append('<GENERATOR-RADUNITS>'+unit)
    newf.append('<GENERATOR-RESOLUTIONKERNEL>N')
    newf.append('<GENERATOR-TRANS>02-01')
    
if (Telescope == 'Keck HIRES'):
    newf.append('<GENERATOR-INSTRUMENT>Keck_HIRES: HIRES is the High Resolution Echelle Spectrometer at the Keck observatory on Manuakea (4200m), Hawaii. It is a grating cross-dispersed, echelle spectrograph capable of operating between 0.3 and 1.0 microns at high resolutions (up to RP 85,000). Several slits are available in width and length, since order separation varies between 6 and 43 arcseconds. Typical throughput is 0.15, yet it drops substantially (below 0.05) beyond 0.8 um.')
#    newf.append('<GENERATOR-RANGE1>'+HIRES_wav_start)
#    newf.append('<GENERATOR-RANGE2>'+HIRES_wav_end)
    newf.append('<GENERATOR-RANGEUNIT>um')
#    newf.append('<GENERATOR-RESOLUTION>'+HIRES_R)
    newf.append('<GENERATOR-RESOLUTIONUNIT>RP')
    newf.append('<GENERATOR-TELESCOPE>SINGLE')
    newf.append('<GENERATOR-DIAMTELE>10')
    newf.append('<GENERATOR-BEAM>0.5')
    newf.append('<GENERATOR-BEAM-UNIT>arcsec')
    newf.append('<GENERATOR-TELESCOPE1>1')
    newf.append('<GENERATOR-TELESCOPE2>2.0')
    newf.append('<GENERATOR-TELESCOPE3>1.0')
    newf.append('<GENERATOR-NOISE>CCD')
    newf.append('<GENERATOR-NOISE1>3.0')
    newf.append('<GENERATOR-NOISE2>0.8')
    newf.append('<GENERATOR-NOISEOTEMP>273')
    newf.append('<GENERATOR-NOISEOEFF>0.15')
    newf.append('<GENERATOR-NOISEOEMIS>0.05')
    newf.append('<GENERATOR-NOISETIME>'+str(exposure_time))
    newf.append('<GENERATOR-NOISEFRAMES>'+str(exposure_number))
    newf.append('<GENERATOR-NOISEPIXELS>8')
    newf.append('<GENERATOR-TRANS-APPLY>N')
    newf.append('<GENERATOR-TRANS-SHOW>Y')
    newf.append('<GENERATOR-LOGRAD>Y')
    newf.append('<GENERATOR-GAS-MODEL>Y')
    newf.append('<GENERATOR-CONT-MODEL>Y')
    newf.append('<GENERATOR-CONT-STELLAR>Y')
    newf.append('<GENERATOR-RADUNITS>'+unit)
    newf.append('<GENERATOR-RESOLUTIONKERNEL>N')
    newf.append('<GENERATOR-TRANS>02-01')
    
if (Telescope == 'Keck NIRSpec'):
    newf.append('<GENERATOR-INSTRUMENT>Keck_NIRSpec: NIRSpec is the 2nd generation of the Near Infrared Spectrometer at the Keck observatory on Manuakea (4200m), Hawaii. It is a cryogenic cross-dispersed echelle spectrograph which features spectroscopy over the 0.95-5.5 micron range at resolutions up to 40,000 with a 2048x2048 H2RG Teledyne detector. The instrument samples this broad spectral range by employing an array of cross-dispersers and filter configurations.')
    newf.append('<GENERATOR-RANGE1>0.96')
    newf.append('<GENERATOR-RANGE2>5')
    newf.append('<GENERATOR-RANGEUNIT>um')
    newf.append('<GENERATOR-RESOLUTION>25000')
    newf.append('<GENERATOR-RESOLUTIONUNIT>RP')
    newf.append('<GENERATOR-TELESCOPE>SINGLE')
    newf.append('<GENERATOR-DIAMTELE>10')
    newf.append('<GENERATOR-BEAM>0.5')
    newf.append('<GENERATOR-BEAM-UNIT>arcsec')
    newf.append('<GENERATOR-TELESCOPE1>1')
    newf.append('<GENERATOR-TELESCOPE2>2.0')
    newf.append('<GENERATOR-TELESCOPE3>1.0')
    newf.append('<GENERATOR-NOISE>CCD')
    newf.append('<GENERATOR-NOISE1>10')
    newf.append('<GENERATOR-NOISE2>0.67')
    newf.append('<GENERATOR-NOISEOTEMP>273')
    newf.append('<GENERATOR-NOISEOEFF>0.18')
    newf.append('<GENERATOR-NOISEOEMIS>0.05')
    newf.append('<GENERATOR-NOISETIME>'+str(exposure_time))
    newf.append('<GENERATOR-NOISEFRAMES>'+str(exposure_number))
    newf.append('<GENERATOR-NOISEPIXELS>8')
    newf.append('<GENERATOR-TRANS-APPLY>Y')
    newf.append('<GENERATOR-TRANS-SHOW>Y')
    newf.append('<GENERATOR-LOGRAD>N')
    newf.append('<GENERATOR-GAS-MODEL>Y')
    newf.append('<GENERATOR-CONT-MODEL>Y')
    newf.append('<GENERATOR-CONT-STELLAR>Y')
    newf.append('<GENERATOR-RADUNITS>'+unit)
    newf.append('<GENERATOR-RESOLUTIONKERNEL>N')
    newf.append('<GENERATOR-TRANS>02-01')
#    newf.append('<GENERATOR-GCM-BINNING>'+Binning)  

if (Telescope == 'E-ELT HIRES'):
    newf.append('<GENERATOR-INSTRUMENT>user')
#    newf.append('<GENERATOR-RANGE1>'+HIRES_wav_start)
#    newf.append('<GENERATOR-RANGE2>'+HIRES_wav_end)
    newf.append('<GENERATOR-RANGEUNIT>um')
#    newf.append('<GENERATOR-RESOLUTION>'+HIRES_R)
    newf.append('<GENERATOR-RESOLUTIONUNIT>RP')
    newf.append('<GENERATOR-TELESCOPE>SINGLE')
    newf.append('<GENERATOR-DIAMTELE>39.1')
    newf.append('<GENERATOR-BEAM>0.5')
    newf.append('<GENERATOR-BEAM-UNIT>arcsec')
    newf.append('<GENERATOR-TELESCOPE1>1')
    newf.append('<GENERATOR-TELESCOPE2>2.0')
    newf.append('<GENERATOR-TELESCOPE3>1.0')
    newf.append('<GENERATOR-NOISE>CCD')
    newf.append('<GENERATOR-NOISE1>3.0')
    newf.append('<GENERATOR-NOISE2>0.8')
    newf.append('<GENERATOR-NOISEOTEMP>273')
    newf.append('<GENERATOR-NOISEOEFF>0.15')
    newf.append('<GENERATOR-NOISEOEMIS>0.05')
    newf.append('<GENERATOR-NOISETIME>'+str(exposure_time))
    newf.append('<GENERATOR-NOISEFRAMES>'+str(exposure_number))
    newf.append('<GENERATOR-NOISEPIXELS>8')
    newf.append('<GENERATOR-TRANS-APPLY>N')
    newf.append('<GENERATOR-TRANS-SHOW>Y')
    newf.append('<GENERATOR-LOGRAD>Y')
    newf.append('<GENERATOR-GAS-MODEL>Y')
    newf.append('<GENERATOR-CONT-MODEL>Y')
    newf.append('<GENERATOR-CONT-STELLAR>Y')
    newf.append('<GENERATOR-RADUNITS>'+unit)
    newf.append('<GENERATOR-RESOLUTIONKERNEL>N')
    newf.append('<GENERATOR-TRANS>02-01')

if (Telescope == 'E-ELT METIS'):
    newf.append('<GENERATOR-INSTRUMENT>user')
    newf.append('<GENERATOR-RANGE1>3')
    newf.append('<GENERATOR-RANGE2>13')
    newf.append('<GENERATOR-RANGEUNIT>um')
    newf.append('<GENERATOR-RESOLUTION>50000')
    newf.append('<GENERATOR-RESOLUTIONUNIT>RP')
    newf.append('<GENERATOR-TELESCOPE>SINGLE')
    newf.append('<GENERATOR-DIAMTELE>39.1')
    newf.append('<GENERATOR-BEAM>0.5')
    newf.append('<GENERATOR-BEAM-UNIT>arcsec')
    newf.append('<GENERATOR-TELESCOPE1>1')
    newf.append('<GENERATOR-TELESCOPE2>2.0')
    newf.append('<GENERATOR-TELESCOPE3>1.0')
    newf.append('<GENERATOR-NOISE>CCD')
    newf.append('<GENERATOR-NOISE1>10')
    newf.append('<GENERATOR-NOISE2>0.67')
    newf.append('<GENERATOR-NOISEOTEMP>273')
    newf.append('<GENERATOR-NOISEOEFF>0.18')
    newf.append('<GENERATOR-NOISEOEMIS>0.05')
    newf.append('<GENERATOR-NOISETIME>'+str(exposure_time))
    newf.append('<GENERATOR-NOISEFRAMES>'+str(exposure_number))
    newf.append('<GENERATOR-NOISEPIXELS>8')
    newf.append('<GENERATOR-TRANS-APPLY>Y')
    newf.append('<GENERATOR-TRANS-SHOW>Y')
    newf.append('<GENERATOR-LOGRAD>Y')
    newf.append('<GENERATOR-GAS-MODEL>Y')
    newf.append('<GENERATOR-CONT-MODEL>Y')
    newf.append('<GENERATOR-CONT-STELLAR>Y')
    newf.append('<GENERATOR-RADUNITS>'+unit)
    newf.append('<GENERATOR-RESOLUTIONKERNEL>N')
    newf.append('<GENERATOR-TRANS>02-01')

if (Telescope == 'JWST NIRSpec'):
    newf.append('<GENERATOR-INSTRUMENT>JWST_NIRSpec-2700: JWST/NIRSpec is the infrared spectrometer onboard the James Webb Space Telescope. The high-resolution configuration (RP 2700) considers the maximum resolving power for each of the available instrument gratings/filters combinations (G140H+F070LP, G140H+F100LP, G235H+F170LP, G395H+F290LP). The three gratings cover the 1.0 to 5.3 um spectral region with an average resolving power of 2700.')
    newf.append('<GENERATOR-RANGE1>1')
    newf.append('<GENERATOR-RANGE2>5.3')
    newf.append('<GENERATOR-RANGEUNIT>um')
    newf.append('<GENERATOR-RESOLUTION>2700')
    newf.append('<GENERATOR-RESOLUTIONUNIT>RP')
    newf.append('<GENERATOR-TELESCOPE>SINGLE')
    newf.append('<GENERATOR-DIAMTELE>5.64')
    newf.append('<GENERATOR-BEAM>1')
    newf.append('<GENERATOR-BEAM-UNIT>diffrac')
    newf.append('<GENERATOR-TELESCOPE1>1')
    newf.append('<GENERATOR-TELESCOPE2>2.0')
    newf.append('<GENERATOR-TELESCOPE3>1.0')
    newf.append('<GENERATOR-NOISE>CCD')
    newf.append('<GENERATOR-NOISE1>16.8')
    newf.append('<GENERATOR-NOISE2>0.005')
    newf.append('<GENERATOR-NOISEOTEMP>50')
    newf.append('<GENERATOR-NOISEOEFF>0.3')
    newf.append('<GENERATOR-NOISEOEMIS>0.10')
    newf.append('<GENERATOR-NOISETIME>'+str(exposure_time))
    newf.append('<GENERATOR-NOISEFRAMES>'+str(exposure_number))
    newf.append('<GENERATOR-NOISEPIXELS>8')
    newf.append('<GENERATOR-TRANS-APPLY>N')
    newf.append('<GENERATOR-TRANS-SHOW>N')
    newf.append('<GENERATOR-LOGRAD>Y')
    newf.append('<GENERATOR-GAS-MODEL>Y')
    newf.append('<GENERATOR-CONT-MODEL>Y')
    newf.append('<GENERATOR-CONT-STELLAR>Y')
    newf.append('<GENERATOR-RADUNITS>'+unit)
    newf.append('<GENERATOR-RESOLUTIONKERNEL>N')
    newf.append('<GENERATOR-TRANS>02-01') 
    
if (Telescope == 'JWST MIRI'):
    newf.append('<GENERATOR-INSTRUMENT>JWST_MIRI-LRS: JWST/MIRI is the Mid-Infrared Instrument onboard the James Webb Space Telescope. The low resolution spectroscopy (LRS) configuration samples the 5 to 12 um spectral region with a resolving power of 100 (at 7.5um), and observations can be performed with a 0.5 arcsec slit or via slitless spectroscopy. Fringing and other systematic sources of noise have been identified in this instrument, yet these effects are not included in the noise simulator. Read noise is for FAST readout (32 e-/pixel/read) and for slitless measurements.')
    newf.append('<GENERATOR-RANGE1>5.00')
    newf.append('<GENERATOR-RANGE2>12.00')
    newf.append('<GENERATOR-RANGEUNIT>um')
    newf.append('<GENERATOR-RESOLUTION>100')
    newf.append('<GENERATOR-RESOLUTIONUNIT>RP')
    newf.append('<GENERATOR-TELESCOPE>SINGLE')
    newf.append('<GENERATOR-DIAMTELE>5.64')
    newf.append('<GENERATOR-BEAM>1')
    newf.append('<GENERATOR-BEAM-UNIT>diffrac')
    newf.append('<GENERATOR-TELESCOPE1>1')
    newf.append('<GENERATOR-TELESCOPE2>2.0')
    newf.append('<GENERATOR-TELESCOPE3>1.0')
    newf.append('<GENERATOR-NOISE>CCD')
    newf.append('<GENERATOR-NOISE1>32')
    newf.append('<GENERATOR-NOISE2>0.2')
    newf.append('<GENERATOR-NOISEOTEMP>50')
    newf.append('<GENERATOR-NOISEOEFF>0.00@4.52,0.04@4.72,0.07@4.90,0.12@4.98,0.16@5.13,0.18@5.18,0.20@5.24,0.23@5.39,0.25@5.53,0.27@5.88,0.29@6.14,0.30@6.37,0.30@6.60,0.29@6.89,0.29@7.23,0.30@7.55,0.31@7.75,0.33@8.07,0.32@8.48,0.32@8.85,0.31@9.17,0.29@9.57,0.27@9.95,0.26@10.30,0.24@10.56,0.22@10.79,0.20@10.96,0.17@11.25,0.15@11.48,0.13@11.74,0.11@12.09,0.09@12.40,0.08@12.52')
    newf.append('<GENERATOR-NOISEOEMIS>0.10')
    newf.append('<GENERATOR-NOISETIME>'+str(exposure_time))
    newf.append('<GENERATOR-NOISEFRAMES>'+str(exposure_number))
    newf.append('<GENERATOR-NOISEPIXELS>0.76@5.01,1.03@5.65,1.44@6.57,1.87@7.54,2.17@8.24,2.49@8.95,2.76@9.55,3.08@10.30,3.44@11.03,3.72@11.69,4.03@12.35,4.30@13.02')
    newf.append('<GENERATOR-NOISEWELL>250000')
    newf.append('<GENERATOR-TRANS-APPLY>N')
    newf.append('<GENERATOR-TRANS-SHOW>N')
    newf.append('<GENERATOR-LOGRAD>N')
    newf.append('<GENERATOR-GAS-MODEL>Y')
    newf.append('<GENERATOR-CONT-MODEL>Y')
    newf.append('<GENERATOR-CONT-STELLAR>Y')
    newf.append('<GENERATOR-RADUNITS>'+unit)
    newf.append('<GENERATOR-RESOLUTIONKERNEL>N')
    newf.append('<GENERATOR-TRANS>02-01')
    
if (Telescope == 'Ideal'):
    newf.append('<GENERATOR-INSTRUMENT>user')
    newf.append('<GENERATOR-RANGE1>'+Ideal_wav_start)
    newf.append('<GENERATOR-RANGE2>'+Ideal_wav_end)
    newf.append('<GENERATOR-RANGEUNIT>um')
    newf.append('<GENERATOR-RESOLUTION>'+Ideal_R)
    newf.append('<GENERATOR-RESOLUTIONUNIT>RP')
    newf.append('<GENERATOR-TELESCOPE>SINGLE')
    newf.append('<GENERATOR-DIAMTELE>10')
    newf.append('<GENERATOR-BEAM>1')
    newf.append('<GENERATOR-BEAM-UNIT>diffrac')
    newf.append('<GENERATOR-TELESCOPE1>1')
    newf.append('<GENERATOR-TELESCOPE2>2.0')
    newf.append('<GENERATOR-TELESCOPE3>1.0')
    newf.append('<GENERATOR-NOISE>CCD')
    newf.append('<GENERATOR-NOISE1>20')
    newf.append('<GENERATOR-NOISE2>0.005')
    newf.append('<GENERATOR-NOISEOTEMP>288')
    newf.append('<GENERATOR-NOISEOEFF>0.4')
    newf.append('<GENERATOR-NOISEOEMIS>0.10')
    newf.append('<GENERATOR-NOISETIME>'+str(exposure_time))
    newf.append('<GENERATOR-NOISEFRAMES>'+str(exposure_number))
    newf.append('<GENERATOR-NOISEPIXELS>8')
    newf.append('<GENERATOR-NOISEWELL>250000')
    newf.append('<GENERATOR-TRANS-APPLY>N')
    newf.append('<GENERATOR-TRANS-SHOW>N')
    newf.append('<GENERATOR-LOGRAD>N')
    newf.append('<GENERATOR-GAS-MODEL>Y')
    newf.append('<GENERATOR-CONT-MODEL>Y')
    newf.append('<GENERATOR-CONT-STELLAR>Y')
    newf.append('<GENERATOR-RADUNITS>'+unit)
    newf.append('<GENERATOR-RESOLUTIONKERNEL>N')
    newf.append('<GENERATOR-TRANS>02-01')


# Save atmosphere parameters
newf.append('<ATMOSPHERE-DESCRIPTION>VULCAN')
newf.append('<ATMOSPHERE-STRUCTURE>Equilibrium')
newf.append('<ATMOSPHERE-PRESSURE>'+surface_P)
newf.append('<ATMOSPHERE-PUNIT>bar')
newf.append('<ATMOSPHERE-TEMPERATURE>280')
newf.append('<ATMOSPHERE-WEIGHT>'+str(mmw))
newf.append('<ATMOSPHERE-LAYERS>'+layers)
newf.append('<ATMOSPHERE-CONTINUUM>Rayleigh,Refraction,CIA_all,UV_all')
newf.append('<ATMOSPHERE-NGAS>'+str(NGAS))
newf.append('<ATMOSPHERE-GAS>'+GASES)
newf.append('<ATMOSPHERE-TYPE>'+HIT)
newf.append('<ATMOSPHERE-ABUN>'+ABUN)
newf.append('<ATMOSPHERE-UNIT>'+ATM_UNIT)
newf.append('<ATMOSPHERE-LAYERS-MOLECULES>'+GASES)
newf.append('<ATMOSPHERE-NAERO>2')
newf.append('<ATMOSPHERE-AEROS>Water,WaterIce')
newf.append('<ATMOSPHERE-ATYPE>AFCRL_WATER_HRI[0.20um-0.03m],AFCRL_ICE_HRI[0.20um-0.03m]')
newf.append('<ATMOSPHERE-AABUN>1,1')
newf.append('<ATMOSPHERE-AUNIT>scl,scl')
newf.append('<ATMOSPHERE-ASIZE>'+cloud_sizes)
newf.append('<ATMOSPHERE-ASUNI>um,um')
# Save surface parameters

with open(output_file,'w') as fw:
	for i in newf: fw.write(i+'\n')
    
    
# Writing data to file
with open(output_file, "a") as f:
    
    # Write each layer data
    for layer in range(int(layers)):
        layer_data = f"<ATMOSPHERE-LAYER-{layer + 1}>"
        layer_values = []
        
        # For each molecule, get the abundance in the current layer
        for molecule, abundances in molecules.items():
            layer_values.append(f"{abundances[layer]:.3E}")
        
        # Join layer values and write to file
        layer_data += ",".join(layer_values) + "\n"
        f.write(layer_data)

# Define the parameters as a multi-line string in the desired format
extras = """<ATMOSPHERE-TEMPERATURE>210
<ATMOSPHERE-TAU>0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07
<ATMOSPHERE-NMAX>1
<ATMOSPHERE-LMAX>2
<ATMOSPHERE-NAERO>0
<ATMOSPHERE-CONTINUUM>Rayleigh,Refraction,CIA_all,UV_all
<SURFACE-TEMPERATURE>288.20
<SURFACE-ALBEDO>0.06
<SURFACE-EMISSIVITY>0.98
<SURFACE-GAS-RATIO>1.0
<SURFACE-GAS-UNIT>ratio
<SURFACE-NSURF>0
<SURFACE-MODEL>Lambert
"""

# Open the file in append mode
filename = output_file # Replace with your actual file name
with open(filename, "a") as file:
    file.write(extras)

print(f"Data appended to {filename} successfully.")

print("Atmosphere data written to atmosphere_data.txt")

#%% Upload and download files to PSG

import os
api = ' https://psg.gsfc.nasa.gov//api.php >'
#command = 'curl -s -d app=globes --data-urlencode file@'
command = 'curl --data-urlencode file@'

#Calls PSG from the command line and outputs the file
print('Upload to PSG started')
os.system(command+filename+api+fileout)
print('Upload to PSG finished')

# This will leave you with a config file which you can upload manually
# And an output file

#%% Plot the spectra here

Spec = np.genfromtxt(fileout)

plt.figure(figsize = (10,5))
if (transit == True):
    plt.plot(Spec[:,0], Spec[:,5], lw = 2, color = '#1dccb8', label = name)
else:
    plt.plot(Spec[:,0], Spec[:,5], lw = 2, color = '#1dccb8', label = name)
plt.xlim(Spec[:,0].min(), Spec[:,0].max())
plt.ylim(0, Spec[:,5].max())
plt.xlabel('Wavelength [microns]', fontsize = 15, weight = 'bold')
plt.ylabel('Effective altitude [km]', fontsize = 15, weight = 'bold')
thick_axes(top = True)
plt.legend(loc = 0, fontsize = 15, frameon = False)
print('File plotted')

plt.savefig('PSG/spectra/'+overall_name+'.png', dpi = 200, bbox_inches = 'tight')
print('Figure saved')


