#V1 Author: Jacob Rickel 6/18/2024
# Multi-Wavelength-Species-Identification
A combined Matlab/Python library to identify species in a mixture given measured absorptions at discreet wavelengths by comparing the measurements to values from multiple databases

# Databases included in current version:
1) HiTRAN (https://www.hitran.org/)
2) Pinkowski (https://www.sciencedirect.com/science/article/pii/S0022407318307374)

# Databases I'm hoping to include someday:
1) HiTEMP
2) GEISA
3) NIST Chemical Webbook (https://webbook.nist.gov/chemistry/name-ser/)
4) PNNL
5) Stanford/Literature review

## Overview
This project integrates several MATLAB scripts to interact with the HITRAN database using the HAPI (HITRAN Application Programming Interface) for retrieving molecular spectroscopy data mainly absorbance cross section. The main components include data retrieval, processing, and output generation. This document outlines the prerequisites, setup, functionality of the code blocks, and detailed usage instructions.
---

## Prerequisites

### Software Requirements
1. **Python**: Ensure Python 3.x is installed. You can download it from [python.org](https://www.python.org/).
2. **MATLAB**: Ensure MATLAB is installed and configured to run Python scripts.
   **Note**: MATLAB is compatible only with certain versions of Python. Refer to the table below for compatible Python versions with different MATLAB releases.

### MATLAB and Python Compatibility

| MATLAB Release | Compatible Python Versions |
|----------------|-----------------------------|
| R2024a         | 3.9, 3.10, 3.11             |
| R2023b         | 3.9, 3.10, 3.11             |
| R2023a         | 3.8, 3.9, 3.10              |
| R2022b         | 2.7, 3.8, 3.9, 3.10         |
| R2022a         | 2.7, 3.8, 3.9               |
| R2021b         | 2.7, 3.7, 3.8, 3.9          |
| R2021a         | 2.7, 3.7, 3.8               |
| R2020b         | 2.7, 3.6, 3.7, 3.8          |
| R2020a         | 2.7, 3.6, 3.7               |
| R2019b         | 2.7, 3.6, 3.7               |
| R2019a         | 2.7, 3.5, 3.6, 3.7          |
| R2018b         | 2.7, 3.5, 3.6               |
| R2018a         | 2.7, 3.5, 3.6               |
| R2017b         | 2.7, 3.4, 3.5, 3.6          |
| R2017a         | 2.7, 3.4, 3.5               |
| R2016b         | 2.7, 3.3, 3.4, 3.5          |
| R2016a         | 2.7, 3.3, 3.4               |
| R2015b         | 2.7, 3.3, 3.4               |
| R2015a         | 2.7, 3.3, 3.4               |
| R2014b         | 2.7                         |

3. **Necessary Libraries**: Install the hitran api and numpy Python libraries using pip in the command prompt for windows:
    pip install hitran-api numpy
4. **Internet Access**: Required to access the HITRAN database via the HAPI API.

### Useful Links
- HAPI Manual: https://hitran.org/static/hapi/hapi_manual.pdf
- HAPI Documentation: https://hitran.org/hapi/
- Pinkowski paper that includes scattered high-temperature spectra, and discusses a framework for determining species mole fractions (x) in an unknown mixture using a user-defined set of possible molecules (n) based on measured absorbances (b) at several discreet wavelengths (m): (https://www.sciencedirect.com/science/article/pii/S0022407318307374)
---

## Setup Instructions
1. **Install Required Packages** (pip install hitran-api numpy)
2. **Download HITRAN Data Files** (optional. You can download them from the HITRAN website or configure the code to access the data through the HAPI API) 
3. **MATLAB Configuration**
    Ensure MATLAB is configured to use the correct Python interpreter. For example, MATLAB R2021b supports Python versions up to 3.8. You can set this in 
    MATLAB's preferences:

## Physical Principles and Underlying Math:
The code blocks discussed below follow a method discussed in Pinkowski et al. for determining species mole fractions (x) in an unknown mixture using a user-defined set of possible molecules (n) based on measured absorbances (b) at several discreet wavelengths (m). The underlying physical principle that makes this possible is Beer's Law. For a single species at a single wavelength:

\alpha=n*\sigma*L 

where:
\alpha = absorbance [-] at a specific wavelength (\lambda) measured using laser absorbance \alpha=(-ln(I/Io))
n      = number density [mol/m^3]
\sigma = absorbtion cross-section [m^2/mol] - This is temperature, pressure, and wavelength-specific.
L      = path length [m]

So in words:
absorbance = number density * absorbtion cross section * Path Length

But if there are several species in a mixture, multiple species may absorb at the same wavelength. If several species in the mixture absorb strongly at that wavelength the determination of composition becomes basically impossible. When multiple species are considered, absorbance contributions at that wavelength sum linearly:

\alpha_\lambda=\sum(\sigma_i*n_i*L)

That is, total absorbance equals the sum of the individual absorbances.

If you want to determine the composition of a multi-species mixture, you need to measure absorbance at at least as many wavelengths as you have species. Then, you can build a Beer-Lambert system in the form:

Kx=b

where K is an M x N matrix of absorbtion cross-sections a combinations of M wavelengths and N species.  x is the composition you're trying to find, and b is the absorbance at the M wavelengths you have measured.  As long as M>=N, the matrix can be solved. In many high-temperature applications, absorption cross-sections must be measured from scratch. Absorbtion cross-sections of specific molecules at the temperatures, pressures, and wavelengths of interest may be found in one of several available databases. The purpose of the code blocks described below is to draw from the HiTRAN database, use that data to complete the K-matrix and use it to solve for x from a given b matrix. 

## Code Blocks Overview
The code structure is such that the highest level code draws from those listed below.



### File: `HAPI_Processor.py`
This script initializes the HITRAN API and fetches the relevant absorption cross-section data. It includes functions for querying HITRAN data based on user-defined parameters. This function is independent.
-hapi.py must be in same folder as HAPI_Processor.py.

**Key Functions:**

- initialize_hapi(): Sets up the HITRAN API connection.
- get_absorption_cross_section(): Queries the HITRAN database for absorption cross-section data.

### File: `absorptionCrossSectionPinkowski.mlx`

This script calculates the absorption cross-section using the methodology outlined by Pinkowski et al. The paper is included in the useful links. This function is independent.

### File: `check_molecule_presence.mlx`

This script checks the presence of specific molecules in the HITRAN data appended with Pinkowski's models for molecules not in HITRAN and outputs relevant information. This function is independent.

### File: `getAbsorptionCrossSection.mlx`

This MATLAB Live Script processes the HITRAN data using the Python script. It is configured to call the `HAPI_Processor.py` functions to retrieve and process the data. This function requires: `HAPI_Processor.py`,`absorptionCrossSectionPinkowski.mlx`, and `check_molecule_presence.mlx`.

   **Instructions for Configuration:**

- Change Data Paths: Update the path in the script to point to the correct location of `HAPI_Processor.py`.
- Example of current implementation on the local machine: 

            % Ensure the Python environment is set up
            pyenv('Version', 'C:/Users/C25Jacob.Rickel/AppData/Local/Programs/Python/Python311/pythonw.exe'); 
            % Adjust the path to your Python installation

            % Full path to the Python script
            scriptPath = 'C:/Users/C25Jacob.Rickel/Downloads/HAPI_Processor.py'; 
            % Adjust the path to where you saved the Python script

            % Ensure the current directory is not the numpy source directory
            cd('C:/Users/C25Jacob.Rickel/Downloads'); % Change to a suitable directory

### File: `Cross_Matrix.mlx`
generates mxn K-matrix (m wavelengths x n molecules where cells are absorbption cross-sections)
This script generates a matrix of cross-sections for different molecules and conditions, utilizing the HITRAN data retrieved through HAPI. This function requires: `HAPI_Processor.py`,`absorptionCrossSectionPinkowski.mlx`, `check_molecule_presence.mlx`, and `getAbsorptionCrossSection.mlx`.



---

## Detailed Usage Instructions

### Setting Up the Environment

1. **Python Environment**

    Ensure Python and all dependencies are installed and the environment is activated. Install necessary packages
    using pip:

    pip install hitran-api numpy

2. **MATLAB Configuration**

    Configure MATLAB to use the correct Python environment. For example:

    pyenv('Version', 'path/to/python')

### Running the Scripts

1. **Run MATLAB Scripts**

    Open the MATLAB Live Scripts (`*.mlx`) in MATLAB and run them. The scripts are configured to call the
    appropriate functions from `HAPI_Processor.py` automatically.

2. **Modify Paths as Needed**

    If necessary, modify the paths in the `getAbsorptionCrossSection.mlx` to point to the correct locations of `HAPI_Processor.py`
    and other data files.

### Input Instructions for Each File

#### `absorptionCrossSectionPinkowski.mlx`

**Purpose**: Calculates the absorption cross-section for a given species ID, wavelength, and temperature.

**Input**:

- speciesID: Numeric ID of the species for which the absorption cross-section is to be calculated (integer). Supported species IDs:
  - 6: CH4 (Methane)
  - 38: C2H4 (Ethylene)
  - 56: C3H6 (Propylene)
  - 57: iC4H8 (Isobutene)
  - 58: 1C4H8 (1-Butene)
  - 59: C6H6 (Benzene)
  - 60: C7H8 (Toluene)
- wavelength: Wavelength (in micrometers) at which the absorption cross-section is to be calculated (scalar).
- T: Temperature in Kelvin (scalar).

**Example Call**:

speciesID = 6;

wavelength = 3.1758;

T = 1000;

sigma = absorptionCrossSectionPinkowski(speciesID, wavelength, T);

#### `check_molecule_presence.mlx`

**Purpose**: Checks the presence of specific molecules in the downloaded HITRAN data.

**Input**:

- search_id: The ID of the molecule to search for (integer).

**Example Call**:

search_id = 1

is_present = check_molecule_presence(search_id);

#### `getAbsorptionCrossSection.mlx`

**Purpose**: Calculates the absorption cross-section for a given molecule.

**Input**:

- molecule_id: HITRAN molecule ID (integer)
  
- isotopologue_id: HITRAN isotopologue ID (integer)
  
- wavelength: Wavelength (in micrometers) at which to calculate the cross-section (scalar)
  
- temperature: Temperature in Kelvin (scalar)
  
- pressure: Pressure in atm (scalar)

**Example Call**:
molecule_id = 1;

isotopologue_id = 1;

wavelength = 2.5;

temperature = 296;

pressure = 1;

absorption_cross_section = getAbsorptionCrossSection(molecule_id, isotopologue_id, wavelength, temperature, pressure);

#### `Cross_Matrix.mlx`

**Purpose**: Computes the absorption cross-section matrix for given molecules and wavelengths.

**Input**:

- molecule_id: Array of HITRAN molecule IDs (vector)
  
- isotopologue_id: Scalar or vector of HITRAN isotopologue IDs
  
- wavelength: Array of wavelengths (in micrometers) at which to calculate the cross-section (vector)
  
- temperature: Temperature in Kelvin (scalar)
  
- pressure: Pressure in atm (scalar)

**Example Call**:

molecule_ids = [1, 2];

isotopologue_ids = [1, 2];

wavelengths = [2.5, 3.0, 3.5];

temperature = 296;

pressure = 1;

K = Cross_Matrix(molecule_ids, isotopologue_ids, wavelengths, temperature, pressure

---

### Explanation of Code Integration

The Python script `HAPI_Processor.py` is responsible for interacting with the HITRAN API to fetch absorption cross-section data. The MATLAB scripts process this data to perform various analyses and generate output.

- **Data Retrieval**: `HAPI_Processor.py` fetches data from HITRAN based on user-defined parameters it is called by `getAbsorptionCrossSection.mlx`.
- **Data Processing**: MATLAB scripts `absorptionCrossSectionPinkowski.mlx` and `getAbsorptionCrossSection.mlx` take user inputs to generate single cross section values. They process the retrieved data to calculate absorption cross-sections.  `check_molecule_presence.mlx` determines if the molecule is at all in the set of data. Finally `Cross_Matrix.mlx` creates a matrix of absorbance cross section given vectors of molecule IDs and wavelengths for a given temperature and pressure.
- **Output Generation**: The scripts generate output in the form of matrices and visualizations, which can be used for further analysis.

### Input and Output Formatting

1. **Input Parameters**

    Ensure that the input parameters for data retrieval and processing are correctly specified in the MATLAB scripts. For example:

    molecule_ids = [1, 2];
   
    isotopologue_ids = [1, 2];
   
    wavelengths = [2.5, 3.0, 3.5];
   
    temperature = 296;
   
    pressure = 1;
   
    K = Cross_Matrix(molecule_ids, isotopologue_ids, wavelengths, temperature, pressure);

3. **Output Formatting**

    The output from the scripts will typically include data tables and visualizations. Ensure that the output is saved or displayed as needed. For example, in MATLAB:

    result = Cross_Matrix(molecule_ids, isotopologue_ids, wavelengths, temperature, pressure);
   
    disp(result);


