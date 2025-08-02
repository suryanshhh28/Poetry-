# 🔬 PubMed Paper Fetcher CLI

A Python command-line tool to search PubMed for research papers and **identify papers with at least one author affiliated with a non-academic organization** (like pharmaceutical or biotech companies). Results can be exported as a CSV for further analysis.

---

## 🚀 Features

- 🔍 Search PubMed using any query term
- 🧪 Detect non-academic affiliations (e.g., *Inc.*, *LLC*, *Pharma*, *Biotech*, etc.)
- 📧 Extract corresponding author emails if available
- 📄 Export results to a well-formatted CSV file
- 🐍 Built with clean, modular Python using `Poetry`
- 💥 Graceful error handling for empty queries and API failures

---

## 🛠️ Installation
```
git clone https://github.com/your-username/pubmed-paper-fetcher.git
cd pubmed-paper-fetcher
poetry install
```

## 🧪 Usage

poetry run get-papers-list "your-query"

Optional flags:

-f, --file : Save results to a CSV file
-d, --debug : Enable debug logs

poetry run get-papers-list "cancer immunotherapy" -f results.csv --debug

📦 Output Sample (CSV)
PubmedID	Title	Publication Date	Non-academic Author(s)	Company Affiliation(s)	Corresponding Author Email
12345678	Immunotherapy Advances	2023	John Doe	ABC Biotech Ltd.	john.doe@abcbiotech.com

## ❗ Error Handling

❌ No internet → clear message and graceful exit
❌ Invalid or empty query → warns user
❌ No non-academic affiliations → informs user, doesn't crash

## 🧠 How It Works

Uses ESearch API to find PubMed IDs based on your query
Uses EFetch API to fetch article details in XML
Parses author affiliations and filters for non-academic ones
Outputs to CLI or CSV

## 🧰 Project Structure

bash
Copy
Edit
pubmed-paper-fetcher/
│
├── pubmed_fetcher/
│   ├── __init__.py
│   └── fetch.py         # Core logic to fetch and filter articles
│
├── cli.py               # CLI interface using argparse
├── pyproject.toml       # Poetry config
└── README.md
