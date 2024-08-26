import os
import sys
import multiprocessing
import logging

domaineFile=sys.argv[1]
pdbFolder=sys.argv[2]
domainFolder=sys.argv[3]
outputFolder=sys.argv[4]
num_cpus = int(sys.argv[5])  # Number of CPUs to use

# Set up logging
log_file = os.path.join(outputFolder, 'unprocessed_domains.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

def custom_residue_compare(res_num, start_pos, end_pos):
    """
    Compare the residue number (res_num) with the start and end positions to determine if it falls within the range.
    Handles alphanumeric residue numbers (e.g., '100A') by separating numeric and alphabetic parts.
    """

    res_num = str(res_num)
    start_pos = str(start_pos)
    end_pos = str(end_pos)

    try:
        # Extract numeric parts of residue numbers
        res_num_int = int(res_num.rstrip('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
        start_pos_int = int(start_pos.rstrip('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
        end_pos_int = int(end_pos.rstrip('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    except ValueError:
        return False
    
    # Extract alphabetic suffixes from residue numbers
    res_suffix = res_num.lstrip('0123456789')
    start_suffix = start_pos.lstrip('0123456789')
    end_suffix = end_pos.lstrip('0123456789')

    # Check if the residue number is outside the start-end range
    if res_num_int > end_pos_int or res_num_int < start_pos_int:
        return False
    
    # Check if the residue number matches start or end positions, considering the suffixes
    if res_num_int == start_pos_int and res_suffix < start_suffix:
        return False
    if res_num_int == end_pos_int and res_suffix > end_suffix:
        return False
    
    # Return True if all checks pass
    return True

def process_line(line, pdbFolder, domainFolder):
    """
    Process a single line from the input file: extract chain and residue information, 
    and write matching PDB records to an output file.
    """
    if line.strip() == "":
        return  # Skip empty lines

    domainID, pdbID, chain, start_pos, end_pos = line.strip().split("\t")

    # Construct the full paths for the PDB input file and output file
    pdb_file_path = os.path.join(pdbFolder, f'{pdbID}.pdb')
    domain_file_path = os.path.join(domainFolder, f'{domainID}.pdb')

    # Check if the PDB file exists
    if os.path.exists(pdb_file_path):
        with open(pdb_file_path, 'r') as pdb:
            # Read each line of the PDB file
            for pdb_line in pdb:
                if pdb_line.startswith('ATOM'):
                    ch = pdb_line[21]  # Extract chain identifier from the PDB line
                    res_num = pdb_line[22:26].strip()  # Extract residue number

                    # If start_pos is '/', process the entire chain
                    if start_pos == '/':
                        if ch == chain:
                            # Append the PDB line to the output file for the chain
                            with open(domain_file_path, 'a') as chain_file:
                                chain_file.write(pdb_line)
                    else:
                        # Compare residue number with start and end positions, and match the chain
                        if custom_residue_compare(res_num, start_pos, end_pos) and ch == chain:
                            # Append the PDB line to the output file for the specific residue range
                            with open(domain_file_path, 'a') as chain_file:
                                chain_file.write(pdb_line)
    else:
        # Log a message if the PDB file does not exist
        logging.info(f'{line.strip()} - {pdb_file_path} does not exist!')

def main():
    # Read the input file and collect all lines
    with open(domaineFile, 'r') as infile:
        lines = infile.readlines()

    # Use multiprocessing.Pool to parallelize the processing of lines
    with multiprocessing.Pool(processes=num_cpus) as pool:
        # Map the process_line function to each line in the input file
        pool.starmap(process_line, [(line, pdbFolder, domainFolder) for line in lines])

if __name__ == "__main__":
    main()