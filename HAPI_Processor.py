import numpy as np
from hapi import *

#=======================================================================
#PROGRAMMER:... C1C Jacob D Rickel USAF
#PROGRAM:...... HAPI_Processor.py
#VERSION:...... 1.0

def fetch_data(molecule_id, isotopologue_id, numin, numax, wavelength, temperature, pressure):
    """
    fetch_data - Fetches and calculates the absorption cross section for a given molecule and conditions.

    Parameters:
    molecule_id (int): HITRAN molecule ID
    isotopologue_id (int): HITRAN isotopologue ID
    numin (float): Lower bound of the wavenumber range
    numax (float): Upper bound of the wavenumber range
    wavelength (float): Wavelength at which to calculate the cross section
    temperature (float): Temperature in Kelvin
    pressure (float): Pressure in atm

    Returns:
    float: Absorption cross section in m^2/mol

    Example:
    absorption_cross_section = fetch_data(1, 1, 2.5, 296, 1)
    """

    # Print the parameters to ensure they are passed correctly (for debugging purposes)
    print(f"Parameters - molecule_id: {molecule_id}, isotopologue_id: {isotopologue_id}, numin: {numin}, numax: {numax}, wavelength: {wavelength}, temperature: {temperature}, pressure: {pressure}")

    # Initialize the database (creates/opens a database named 'data')
    db_begin('data')

    # Fetch the data for the specified molecule and wavenumber range
    fetch('MyTable', molecule_id, isotopologue_id, numin, numax)

    # Calculate the absorption coefficient using Lorentz profile
    nu, coef = absorptionCoefficient_Lorentz(
        SourceTables='MyTable',         # Table name where the data is stored
        Components=[(molecule_id, isotopologue_id)],  # List of tuples specifying the molecule and isotopologue
        Environment={'p': pressure, 'T': temperature}, # Dictionary specifying the environmental conditions
        OmegaRange=[numin, numax],      # Wavenumber range for the calculation
        OmegaStep=0.01,                 # Step size for the wavenumber grid
        HITRAN_units=True               # Specifies that the units are in HITRAN format
    )

    # Interpolate to find the absorption cross-section at the specified wavelength
    # np.interp performs linear interpolation to estimate the absorption cross-section
    absorption_cross_section = np.interp(wavelength, nu, coef)

    # Return the absorption cross-section as a float
    return float(absorption_cross_section)

    
        


