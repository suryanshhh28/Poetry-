# PubMed Paper Fetcher

This tool fetches research papers from PubMed that include at least one author affiliated with a pharmaceutical or biotech company.

## Installation

```bash
git clone https://github.com/yourusername/pubmed-paper-fetcher.git
cd pubmed-paper-fetcher
poetry install

## To test 

poetry run get-papers-list "EXAMPLE NAME" -f results.csv
EXAMPLE NAME -> cloud bursts, earthquakes, etc (WHATEVER YOU LIKE)

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Output filename to save CSV
  -d, --debug           Enable debug logging
