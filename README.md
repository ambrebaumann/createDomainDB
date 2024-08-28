# SCOPe/CATH domain creation pipeline

This pipeline processes SCOPe and CATH domain files, extracts relevant string and residue information, downloads associated PDB files, and generates PDB files by domain.

## Features

1. **Domain File Processing**:
   - Extracts information from SCOPe or CATH domain files.
   - Creates TSV files containing details of domains, chains, and residues.

2. **Automated PDB File Downloading**:
   - Identifies the necessary PDB files.
   - Parallel downloading of PDB files from the PDB database.

3. **PDB File Generation by Domain**:
   - Extracts specific chains and residues for each domain.
   - Creates PDB files for each identified domain.

## Prerequisites

- Python 3.8 or higher
- Standard Python modules (`re`, `logging`, `sys`, `os`, `csv`, `multiprocessing`)
- `aria2c` download tool for downloading PDB files

## Installation

Clone the repository and navigate to the project folder:

```bash
git clone https://your-repo.git
cd your-repo
```

## Usage

The main script to run the entire pipeline is allPipeline.sh. It manages all steps, from initial domain file processing to generating PDB files by domain.

### Basic Command

```bash
bash allPipeline.sh <domainFile> <SCOPEorCATH> <outputDir> <nbCPUs>
```

### Arguments

- `<domainFile>`: Path to the SCOPe or CATH domain file to be processed.
- `<SCOPEorCATH>`: Specify "SCOPE" to process a SCOPe file or "CATH" to process a CATH file.
- `<outputDir>`: Output directory where all generated files will be stored.
- `<nbCPUs>`: Number of CPU cores to use for parallel processing (recommended: 4 or more).

### Usage Example

See runTest.sh and the test folder.
