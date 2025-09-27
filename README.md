# SNP Info Extractor

A simple Python script that extracts basic SNP (rsID) information from NCBI SNP pages and saves it to an Excel file.  
It retrieves chromosome, GRCh37 / GRCh38 positions, alleles, and gene consequence.

---

## Features

- Input: a comma-separated list of rs IDs (e.g. `rs429358, rs7412`)
- Output: Excel file with columns:
  `rsID`, `Chromosome`, `GRCh37 Position`, `GRCh38 Position`, `Alleles`, `Gene Consequence`
- Ideal for small-scale SNP lookups.

---

## Requirements

- Python 3.8+
- Python packages:

```bash
pip install requests beautifulsoup4 pandas openpyxl lxml
````

---

## Output Columns

* `rsID` — SNP identifier
* `Chromosome` — Chromosome number (if available)
* `GRCh37 Position` — Numeric position on GRCh37
* `GRCh38 Position` — Numeric position on GRCh38
* `Alleles` — Allele string
* `Gene Consequence` — Consequence or `None` if missing

---

## How it Works

1. Fetches NCBI SNP webpage for each rsID: `https://www.ncbi.nlm.nih.gov/snp/{rsid}`.
2. Uses BeautifulSoup to parse HTML and extract:

   * `Position`, `Alleles`, `Gene : Consequence`
   * Placement table (`genomics_placements_table`) for GRCh37/GRCh38 coordinates
3. Combines all results in a pandas `DataFrame` and writes to Excel.

---

## Important Notes

* The script scrapes NCBI public pages. For large-scale queries, use NCBI Entrez/e-utilities.
* Some fields may be missing for certain SNPs; these will appear blank in Excel.
* Internet connection is required.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Contact / Author

Created by Rahul Madhav
