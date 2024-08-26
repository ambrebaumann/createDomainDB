# Usage: python createCATHtsv.py cath-domain-description-file-v4_3_0.txt output_folder

import re
import logging
import sys
import os

input_file = sys.argv[1]
output_path = sys.argv[2]

def clean_content(content):
    """ Clean the content of text by removing problematic URLs or double slashes. """
    # Remove problematic URL patterns or fix any issues related to double slashes
    content = re.sub(r'http://[\S]+', '', content)  # Remove URLs starting with http://
    content = re.sub(r'https://[\S]+', '', content) # Remove URLs starting with https://
    content = re.sub(r'Http://[\S]+', '', content)   # Remove URLs starting with Http:://
    content = re.sub(r'Https://[\S]+', '', content)  # Remove URLs starting with Https:://
    return content


def parse_cath_domain_file(file_path):
    # Regex patterns for extracting the required fields
    domain_pattern = re.compile(r"DOMAIN\s+(\w+)")
    srange_pattern = re.compile(r"SRANGE\s+START=([-\w]+)\s+STOP=([-\w]+)")
    
    # Initialize lists to store the parsed data
    domains = []
    domains_1_4 = []
    domains_5 = []
    srange_starts = []
    srange_stops = []
    
    # Read the file content
    with open(file_path, 'r') as file:
        file_content = file.read()
        cleaned_content = clean_content(file_content)
    
    # Split the content into blocks for each domain
    blocks = cleaned_content.split("//")
    
    # Initialize a counter for skipped blocks
    skipped_blocks = 0
    
    for block in blocks:

        domain_match = domain_pattern.search(block)
        srange_match = srange_pattern.search(block)
        
        if domain_match and srange_match:
            domain = domain_match.group(1)
            start = srange_match.group(1)
            stop = srange_match.group(2)
            
            domains.append(domain)
            domains_1_4.append(domain[:4])
            domains_5.append(domain[4])
            srange_starts.append(start)
            srange_stops.append(stop)

        else:
            # Log skipped blocks
            skipped_blocks += 1
            logging.warning(f"Skipping block due to missing domain or SRANGE:\n{block}\n{'-'*50}")
    
    # Log the number of skipped blocks
    logging.info(f"Total blocks skipped: {skipped_blocks}")
    
    return domains, domains_1_4, domains_5, srange_starts, srange_stops


def create_tsv(domains, domains_1_4, domains_5, srange_starts, srange_stops, output_file):
    with open(output_file, 'w') as f:
        for i in range(len(domains)):
            f.write(f"{domains[i]}\t{domains_1_4[i]}\t{domains_5[i]}\t{srange_starts[i]}\t{srange_stops[i]}\n")

    # Log the successful creation of the TSV file
    logging.info(f"TSV file created successfully: {output_file}")


def generate_output_filename(input_file):
    # Extract the base name of the file (e.g., "cath-domain-description-file-v4_3_0.txt")
    base_name = os.path.basename(input_file)
    
    # Use regex to extract the version part from the filename
    match = re.search(r'v[\d_]+', base_name)
    
    if match:
        version = match.group(0)
        output_file_name = f"cath-domain-{version}.tsv"
    else:
        # If version is not found, fallback to a generic name
        output_file_name = "cath-domain-output.tsv"
    
    # Return the generated output filename
    return output_file_name


def main() :
    # Set up logging configuration
    logging.basicConfig(filename=os.path.join(output_path, "cath_domain_parser.log"), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Parse the input file
    domains, domains_1_4, domains_5, srange_starts, srange_stops = parse_cath_domain_file(input_file)

    # Generate the output file name
    output_file_name = generate_output_filename(input_file)
    output_file_path = os.path.join(output_path, output_file_name)
    create_tsv(domains, domains_1_4, domains_5, srange_starts, srange_stops, output_file_path)


if __name__ == "__main__":
    main()

