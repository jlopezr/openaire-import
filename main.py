import requests
import argparse
from pymongo import MongoClient
import itertools

def get_paged_organizations(db, per_page=10, total_pages=None):
    url = "https://api.openaire.eu/graph/v1/organizations"
    page_size = per_page
    cursor = "*"  # Initial cursor for the first page

    if total_pages is None or total_pages <= 0:
        it = itertools.count(1)
    else:
        it = range(1, total_pages + 1)

    for page in it:
        params = {
            "pageSize": page_size,
            "cursor": cursor
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Error in the request: {response.status_code}")
            print(response.text)
            break

        data = response.json()

        print(f"\n--- Page {page} ---")
        for org in data.get("results", []):
            print(f"id: {org.get('id')}, Name: {org.get('legalName')}")
            db.organizations.insert_one(org)

        # Get the next cursor
        cursor = data.get("header", {}).get("nextCursor")
        if not cursor:
            print("No more pages.")
            break

def get_paged_projects(db, per_page=10, total_pages=None):
    url = "https://api.openaire.eu/graph/v1/projects"
    page_size = per_page
    cursor = "*"  # initial cursor for the first page

    if total_pages is None or total_pages <= 0:
        it = itertools.count(1)
    else:
        it = range(1, total_pages + 1)

    for page in it:
        params = {
            "pageSize": page_size,
            "cursor": cursor
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Error in the request: {response.status_code}")
            print(response.text)
            break

        data = response.json()

        print(f"\n--- Page {page} ---")
        for org in data.get("results", []):
            print(f"id: {org.get('id')}, Title: {org.get('title')}")
            db.projects.insert_one(org)

        # Get the next cursor
        cursor = data.get("header", {}).get("nextCursor")
        if not cursor:
            print("No more pages.")
            break
    
def main():
    parser = argparse.ArgumentParser(description="Process OpenAire elements by page.")
    parser.add_argument('collection', choices=['organizations', 'projects'],
                        help='Which collection to import: organizations or projects')
    parser.add_argument('--per-page', type=int, default=100, help='Number of elements per page')
    parser.add_argument('--total-pages', type=int, default=None, help='Total number of pages to process (if not specified, process all)')
    parser.add_argument('--drop', action='store_true', help='Empty the collection before starting')
    args = parser.parse_args()

    # Open MongoDB connection
    with MongoClient("mongodb://localhost:27017/") as client:
        db = client["openaire"]
        
        # Drop the selected collection if requested
        if args.drop:
            print(f"Dropping the '{args.collection}' collection...")
            getattr(db, args.collection).drop()

        if args.collection == 'organizations':
            print("Getting paged organizations...")
            get_paged_organizations(db, args.per_page, args.total_pages)
            total = db.organizations.count_documents({})
            print(f"\nTotal organizations saved: {total}")
        elif args.collection == 'projects':
            print("Getting paged projects...")
            get_paged_projects(db, args.per_page, args.total_pages)
            total = db.projects.count_documents({})
            print(f"\nTotal projects saved: {total}")

if __name__ == "__main__":
    main()
