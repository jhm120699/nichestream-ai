import requests
import json
import subprocess
import time
import os

APP_ID = "N86T1R3OWZ"
API_KEY = "5140dac5e87f47346abbda1a34ee70c3"
INDEX_NAME = "products"

CATEGORIES = ["vertical-productivity", "vertical-marketing", "vertical-programming", "vertical-design", "vertical-finance"]

def run_db_query(sql):
    try:
        # We need to escape double quotes for the shell command
        # and handle the fact that team-db itself wants the SQL as a single quoted argument
        # Example: team-db "INSERT INTO products (name) VALUES ('My Product')"
        
        # Replace single quotes in values with two single quotes for SQL escaping
        # However, the whole command is wrapped in double quotes in the shell
        # So we need to be careful.
        
        cmd = ["team-db", sql]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error executing SQL: {sql}")
            print(f"Stderr: {result.stderr}")
            return None
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Exception running query: {e}")
        return None

def fetch_products(category):
    print(f"Fetching products for category: {category}")
    url = f"https://{APP_ID}-dsn.algolia.net/1/indexes/{INDEX_NAME}/query"
    headers = {
        "X-Algolia-Application-Id": APP_ID,
        "X-Algolia-API-Key": API_KEY
    }
    # Filter by tag
    payload = {
        "params": f"filters=_tags:{category}&hitsPerPage=20"
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get('hits', [])
    else:
        print(f"Failed to fetch from Algolia: {response.status_code}")
        return []

def escape_sql(text):
    if text is None:
        return ""
    return text.replace("'", "''")

def main():
    for category in CATEGORIES:
        hits = fetch_products(category)
        print(f"Found {len(hits)} products for {category}")
        
        for hit in hits:
            name = escape_sql(hit.get('name'))
            description = escape_sql(hit.get('description') or hit.get('tagline', ''))
            website_url = escape_sql(hit.get('websiteUrl', ''))
            
            # Check if product exists
            check_sql = f"SELECT id FROM products WHERE name = '{name}'"
            exists = run_db_query(check_sql)
            
            if exists and len(exists) > 0:
                print(f"Product '{name}' already exists, skipping.")
                continue
                
            # Insert product
            insert_product_sql = f"INSERT INTO products (name, category, description, affiliate_url) VALUES ('{name}', '{category}', '{description}', '{website_url}')"
            run_db_query(insert_product_sql)
            
            # Get the inserted ID
            get_id_sql = f"SELECT id FROM products WHERE name = '{name}' ORDER BY id DESC LIMIT 1"
            res = run_db_query(get_id_sql)
            if not res:
                continue
            product_id = res[0]['id']
            
            # Add features (using tags as features for now)
            tags = hit.get('_tags', [])
            for tag in tags:
                tag_esc = escape_sql(tag)
                insert_feature_sql = f"INSERT INTO product_features (product_id, feature_name, feature_value) VALUES ({product_id}, 'Tag', '{tag_esc}')"
                run_db_query(insert_feature_sql)
            
            # Since Indie Hackers doesn't have pros/cons, we'll add some generic ones or leave for AI
            # For the sake of the task, I'll add one generic pro based on revenue if available
            revenue = hit.get('revenue')
            if revenue and revenue > 0:
                pro = escape_sql(f"Proven revenue model (${revenue}/mo)")
                insert_pro_sql = f"INSERT INTO product_pros (product_id, pro_text) VALUES ({product_id}, '{pro}')"
                run_db_query(insert_pro_sql)

            print(f"Saved product: {name}")
            time.sleep(0.5) # Rate limiting self-imposed

if __name__ == "__main__":
    main()
