import requests
from typing import List, Tuple, Optional, Dict
import csv
import re
from xml.etree import ElementTree as ET

ACADEMIC_KEYWORDS = ["university", "college", "institute", "school", "hospital", "dept", "department", "centre", "center", "faculty"]
COMPANY_KEYWORDS = ["pharma", "biotech", "therapeutics", "inc", "ltd", "llc", "corporation", "gmbh", "co."]

# def fetch_pubmed_ids(query: str, retmax: int = 50, debug: bool = False) -> List[str]:
#     url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
#     params = {"db": "pubmed", "term": query, "retmax": retmax, "retmode": "json"}
#     response = requests.get(url, params=params)
#     response.raise_for_status()
#     ids = response.json().get("esearchresult", {}).get("idlist", [])
#     if debug:
#         print(f"Fetched PubMed IDs: {ids}")
#     return ids

def fetch_pubmed_ids(query: str, retmax: int = 50, debug: bool = False) -> List[str]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": query, "retmax": retmax, "retmode": "json"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        ids = response.json().get("esearchresult", {}).get("idlist", [])
        if debug:
            print(f"Fetched PubMed IDs: {ids}")
        return ids

    except requests.exceptions.Timeout:
        print("❌ PubMed ID fetch failed: Request timed out.")
    except requests.exceptions.HTTPError as e:
        print(f"❌ PubMed ID fetch failed: HTTP error - {e}")
    except requests.exceptions.RequestException as e:
        print(f"❌ PubMed ID fetch failed: Request error - {e}")
    except Exception as e:
        print(f"❌ PubMed ID fetch failed: Unexpected error - {e}")

    return []


def fetch_pubmed_details(pubmed_ids: List[str], debug: bool = False) -> List[Dict]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml"
    }

    if not pubmed_ids:
        return []

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.text)

    except requests.exceptions.Timeout:
        print("❌ PubMed details fetch failed: Request timed out.")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"❌ PubMed details fetch failed: HTTP error - {e}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"❌ PubMed details fetch failed: Request error - {e}")
        return []
    except ET.ParseError as e:
        print(f"❌ PubMed details fetch failed: XML parse error - {e}")
        return []
    except Exception as e:
        print(f"❌ PubMed details fetch failed: Unexpected error - {e}")
        return []

    response = requests.get(url, params=params)
    response.raise_for_status()
    root = ET.fromstring(response.text)
    articles = []

    for article in root.findall(".//PubmedArticle"):
        title = article.findtext(".//ArticleTitle", default="")
        pub_date = article.findtext(".//PubDate/Year", default="Unknown")
        pmid = article.findtext(".//PMID", default="")

        authors_info = article.findall(".//Author")
        non_academic_authors = []
        company_affiliations = []
        corresponding_email = None

        for author in authors_info:
            name = (author.findtext("LastName", "") + " " + author.findtext("ForeName", "")).strip()
            affiliation = author.findtext(".//AffiliationInfo/Affiliation", default="").lower()

            if any(keyword in affiliation for keyword in COMPANY_KEYWORDS):
                company_affiliations.append(affiliation)
                non_academic_authors.append(name)

                email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", affiliation)
                if not corresponding_email and email_match:
                    corresponding_email = email_match.group()

        if company_affiliations:
            articles.append({
                "PubmedID": pmid,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": "; ".join(non_academic_authors),
                "Company Affiliation(s)": "; ".join(company_affiliations),
                "Corresponding Author Email": corresponding_email or "N/A"
            })

    if debug:
        print(f"Extracted articles: {articles}")

    return articles

def write_to_csv(articles: List[Dict], filename: str):
    keys = ["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for article in articles:
            writer.writerow(article)
