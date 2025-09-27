import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Function to get SNP details
def get_snp_details(rs_id):
    url = f"https://www.ncbi.nlm.nih.gov/snp/{rs_id}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Initialize the dictionary to store SNP details
    snp_details = {
        "rsID": rs_id,
        "Chromosome": "",
        "GRCh37 Position": "",
        "GRCh38 Position": "",
        "Alleles": "",
        "Gene Consequence": ""
    }

    # Extracting Position, Alleles, and Gene Consequence
    try:
        position = soup.find('dt', string='Position').find_next_sibling('dd').find('span').text.strip()
        alleles = soup.find('dt', string='Alleles').find_next_sibling('dd').text.strip()
        gene_consequence_dd = soup.find('dt', string='Gene : Consequence').find_next_sibling('dd')
        
        # Check for 'None' case
        gene_consequence_div = gene_consequence_dd.find('div', class_='gray')
        if gene_consequence_div:
            gene_consequence = "None"
        else:
            gene_consequence = gene_consequence_dd.find('span').text.strip()

        snp_details["Chromosome"] = position.split(':')[0]
        snp_details["GRCh38 Position"] = position.split(':')[1].split()[0]  # Extracting only the numerical part
        snp_details["Alleles"] = alleles
        snp_details["Gene Consequence"] = gene_consequence
    except AttributeError:
        # Handle missing data cases
        pass

    # Extracting GRCh37 and GRCh38 positions from the table
    table = soup.find('table', id='genomics_placements_table')
    if table:
        for row in table.find('tbody').find_all('tr'):
            cols = row.find_all('td')
            if len(cols) == 2:
                ref_build = cols[0].text.strip()
                position_info = cols[1].text.strip()
                # Only consider main chromosome entries, ignore alt locus entries
                if "GRCh37" in ref_build and "alt locus" not in ref_build:
                    snp_details["GRCh37 Position"] = position_info.split('g.')[1].split('>')[0].rstrip('ACGT')  # Extracting only the numerical part
                elif "GRCh38" in ref_build and "alt locus" not in ref_build:
                    snp_details["GRCh38 Position"] = position_info.split('g.')[1].split('>')[0].rstrip('ACGT')  # Extracting only the numerical part

    return snp_details

# Main function
def main():
    print("Welcome to SNP info extractor")
    rs_input = input("Please enter the list of rs IDs separated by commas: ")
    output_file = input("Please enter the desired output file name (with .xlsx extension): ")
    print("Fetching SNP details...")

    # Ensure the output file has the correct extension
    if not output_file.endswith('.xlsx'):
        output_file += '.xlsx'

    # Split the input into a list of rs IDs
    rs_ids = [rs.strip() for rs in rs_input.split(',')]

    # Fetch details for all rs IDs
    snp_data = []
    for rs_id in rs_ids:
        snp_data.append(get_snp_details(rs_id))

    # Create a DataFrame and save to Excel
    df = pd.DataFrame(snp_data)
    df.to_excel(output_file, index=False)

    print(f"{output_file} successfully saved")

if __name__ == "__main__":
    main()
