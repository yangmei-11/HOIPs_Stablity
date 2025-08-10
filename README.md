# HOIPs_Stablity
read_cif_data.py
This script batch-processes crystallographic structure files in CIF or POSCAR format located in the cif_merge directory.

It parses each structure using pymatgen to obtain the crystal structure object.

It extracts additional metadata from comment lines in the files (lines starting with # in the format # key: value).

The structure is serialized into a dictionary, and the chemical formula is recorded.

All parsed data, including metadata and structure information, are stored in kim_raw_data.csv for subsequent analysis.

extract_material_features.py
This script generates a comprehensive feature set from the structures and composition data saved in kim_raw_data.csv.

Restores the crystal structure from its dictionary representation and computes basic structural features (density, volume, space group number, lattice parameters, etc.) using pymatgen.

Extracts composition-based features, including molar mass, element counts, average electronegativity, total electrons, and atomic coordinates.

Uses the featurebox library to compute weighted averages and maximum values of 21 elemental properties (e.g., atomic radius, atomic mass, electronegativity, oxidation states, melting point, density) from both the overall composition and site-specific (A/B/X) positions.

Combines all structural, compositional, and site-specific descriptors into a single feature table containing 288 features, which is saved as data_all.csv for downstream machine learning tasks.
