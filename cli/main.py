# import argparse
# from pubmed_fetcher.fetch import fetch_pubmed_ids, fetch_pubmed_details, write_to_csv

# def main():
#     parser = argparse.ArgumentParser(description="Fetch PubMed papers with non-academic affiliations.")
#     parser.add_argument("query", help="PubMed query string")
#     parser.add_argument("-f", "--file", help="Output filename to save CSV")
#     parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")
#     args = parser.parse_args()

#     ids = fetch_pubmed_ids(args.query, debug=args.debug)
#     articles = fetch_pubmed_details(ids, debug=args.debug)

#     if args.file:
#         write_to_csv(articles, args.file)
#         print(f"Results saved to {args.file}")
#     else:
#         for art in articles:
#             print(art)

# if __name__ == "__main__":
#     main()

import argparse
import sys
from pubmed_fetcher.fetch import fetch_pubmed_ids, fetch_pubmed_details, write_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with non-academic affiliations.")
    parser.add_argument("query", help="PubMed query string")
    parser.add_argument("-f", "--file", help="Output filename to save CSV")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    ids = fetch_pubmed_ids(args.query, debug=args.debug)
    if not ids:
        print("⚠️ No PubMed IDs found or failed to fetch data. Please refine your query or check your internet connection.")
        sys.exit(1)

    articles = fetch_pubmed_details(ids, debug=args.debug)
    if not articles:
        print("⚠️ No articles with non-academic affiliations found or failed to fetch article details.")
        sys.exit(1)

    if args.file:
        write_to_csv(articles, args.file)
        print(f"✅ Results saved to {args.file}")
    else:
        print("📄 Matching articles:")
        for art in articles:
            print(art)

if __name__ == "__main__":
    main()
