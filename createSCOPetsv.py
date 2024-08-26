# Usage: python createSCOPetsv.py dir.cla.scope.2.08-stable.txt output_folder

import csv
import sys
import os
import re

scope_file = sys.argv[1]
output_path = sys.argv[2]



def parse_chains(description):
    chains_info = description.split(',')
    chains = []
    for info in chains_info:
        chain, range_part = info.split(':')
        if '-' in range_part:
            start, stop = range_part.split('-', 1)
        else:
            start, stop = ('/', '/')
        chains.append((chain, start, stop))
    return chains


def process_scope_file(scope_file, output_file):
    """Process the SCOPe file and write filtered chain data to the output TSV."""
    
    # Define the criteria for exclusion
    excluded_sccs = {'l.1.1.1'} #Because artifacts 

    excluded_pdbs = {'s046'} #Because doesn't exist

    excluded_scopeids = {'d6qiod_', 'd6udjl1', 'd6yd2a2', 'd6yd3a2', 'd3msza1', 'd6quha1', 'd6quhc1',
                    'd6quja1', 'd6qujd1', 'd6quia1', 'd6quid1', 'd5ft8b1', 'd5ft8d1', 'd5ft8f_',
                    'd5ft8h1', 'd5ft8j_', 'd5ft8l_', 'd5ft8n_', 'd4ue3l_', 'd4ue3m_', 'd4ue3s_', 'd4ue3t_'}
    # Chains or residues doesn't exist
    
    with open(scope_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')

        for row in reader:
            # Ensure the row has the correct number of columns
            if len(row) != 6:
                continue

            sid, pdb_id, description, sccs, sunid, ancestor_nodes = row

            # Exclude rows based on predefined criteria
            if sccs in excluded_sccs or sid in excluded_scopeids or pdb_id in excluded_pdbs:
                continue

            # Check if there are multiple different chains
            chains = [info.split(':')[0] for info in description.split(',')]
            if len(set(chains)) > 1:
                continue

            # Parse the description to extract chain information
            chains_info = parse_chains(description)

            # Write each chain's information to the output file
            for chain, start, stop in chains_info:
                writer.writerow([sid, pdb_id, chain, start, stop])
def generate_output_filename(input_file):
    #Generate the output filename based on the input filename
    base_name = os.path.basename(input_file)
    
    # Extract the version part (e.g., "2.08-stable") using regex
    match = re.search(r'scope\.(.+)\.txt', base_name)
    if match:
        version = match.group(1)
        output_file_name = f"scope-domain-{version}.tsv"
    else:
        # Fallback in case the version is not found
        output_file_name = "scope-domain-output.tsv"
    
    # Return the generated output filename
    return output_file_name

def main():
    output_file_name = generate_output_filename(scope_file)
    output_file_path = os.path.join(output_path, output_file_name)

    process_scope_file(scope_file, output_file_path)

    print(f"TSV file created successfully: {output_file_name}")


if __name__ == '__main__':
    main()