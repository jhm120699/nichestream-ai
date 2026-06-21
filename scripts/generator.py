import os
import json
import subprocess
import argparse
from slugify import slugify
from openai import OpenAI

# Initialize OpenAI client (requires OPENAI_API_KEY env var)
client = None
if os.getenv("OPENAI_API_KEY"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_db_query(sql):
    cmd = ["team-db", sql]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running SQL: {result.stderr}")
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None

def get_product_data(product_id):
    product = run_db_query(f"SELECT * FROM products WHERE id = {product_id}")
    if not product:
        return None
    product = product[0]
    
    features = run_db_query(f"SELECT feature_name, feature_value FROM product_features WHERE product_id = {product_id}")
    pros = run_db_query(f"SELECT pro_text FROM product_pros WHERE product_id = {product_id}")
    cons = run_db_query(f"SELECT con_text FROM product_cons WHERE product_id = {product_id}")
    
    return {
        "info": product,
        "features": features or [],
        "pros": pros or [],
        "cons": cons or []
    }

def load_template(template_name):
    path = os.path.join(os.path.dirname(__file__), "templates", f"{template_name}.md")
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return None

def generate_review(product_data, template_type="review"):
    info = product_data["info"]
    features_str = "\n".join([f"- {f['feature_name']}: {f['feature_value']}" for f in product_data["features"]])
    pros_str = "\n".join([f"- {p['pro_text']}" for p in product_data["pros"]])
    cons_str = "\n".join([f"- {c['con_text']}" for c in product_data["cons"]])
    
    template = load_template(template_type)
    
    prompt = f"""
    You are an expert SEO content writer and product reviewer.
    Generate a highly engaging, structured, and SEO-optimized content for the following product:
    
    Product Name: {info['name']}
    Category: {info['category']}
    Description: {info['description']}
    
    Features:
    {features_str}
    
    Known Pros:
    {pros_str}
    
    Known Cons:
    {cons_str}
    
    Template to follow:
    {template if template else "Use a standard review structure."}
    
    requirements:
    1. Output in valid JSON format with the following keys:
       - title: A catchy, SEO-friendly title.
       - content: The full content in Markdown format, following the template structure.
       - rating: A numeric rating from 1 to 5 (float).
       - seo_title: A meta SEO title (max 60 chars).
       - seo_description: A meta SEO description (max 160 chars).
       - json_ld: A JSON-LD string representing the product review schema.
    2. The content should be at least 600 words.
    3. Use a professional yet conversational tone.
    """
    
    # Check for dry run
    if not os.getenv("OPENAI_API_KEY"):
        print("MOCK: OPENAI_API_KEY not found. Returning mock data.")
        return {
            "title": f"Complete Review of {info['name']}",
            "content": f"# Review of {info['name']}\n\nThis is a mock review for {info['name']} in the {info['category']} category.",
            "rating": 4.5,
            "seo_title": f"{info['name']} Review - Is it worth it?",
            "seo_description": f"Read our deep dive into {info['name']}. We cover features, pros, and cons of this {info['category']} tool.",
            "json_ld": "{\"@context\": \"https://schema.org/\", \"@type\": \"Product\"}"
        }
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Using a strong model for quality content
            messages=[
                {"role": "system", "content": "You are a professional SEO reviewer."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return None

def save_review(product_id, review_data):
    name = run_db_query(f"SELECT name FROM products WHERE id = {product_id}")[0]['name']
    slug = slugify(name)
    
    # Save to database
    title = review_data['title'].replace("'", "''")
    content = review_data['content'].replace("'", "''")
    seo_title = review_data['seo_title'].replace("'", "''")
    seo_description = review_data['seo_description'].replace("'", "''")
    json_ld = review_data.get('json_ld', '').replace("'", "''")
    rating = review_data['rating']
    
    sql = f"""
    INSERT INTO reviews (product_id, title, content, rating, status, slug, seo_title, seo_description, json_ld)
    VALUES ({product_id}, '{title}', '{content}', {rating}, 'published', '{slug}', '{seo_title}', '{seo_description}', '{json_ld}')
    """
    run_db_query(sql)

    # Save to file system for Astro
    pages_dir = os.path.join(os.path.dirname(__file__), "..", "src", "pages", "reviews")
    os.makedirs(pages_dir, exist_ok=True)
    
    file_path = os.path.join(pages_dir, f"{slug}.md")
    
    # Escape quotes and format as Markdown with Frontmatter for Astro
    clean_title = review_data['title'].replace('"', '\\"')
    clean_description = review_data['seo_description'].replace('"', '\\"')
    clean_seo_title = review_data['seo_title'].replace('"', '\\"')
    json_ld_indented = "\n".join(["  " + line for line in review_data.get('json_ld', '').split("\n")])
    
    md_content = f"""---
    layout: ../../layouts/Layout.astro
    title: "{clean_title}"
    description: "{clean_description}"
    seo_title: "{clean_seo_title}"
    productName: "{name}"
    rating: {review_data['rating']}
    json_ld: |
    {json_ld_indented}
    ---

{review_data['content']}
"""
    with open(file_path, "w") as f:
        f.write(md_content)
    
    return True

def generate_comparison(product_data1, product_data2, template_type="comparison"):
    info1 = product_data1["info"]
    info2 = product_data2["info"]
    
    template = load_template(template_type)
    
    prompt = f"""
    You are an expert SEO content writer and product reviewer.
    Generate a highly engaging, structured, and SEO-optimized comparison review between these two products:
    
    Product 1: {info1['name']}
    Category: {info1['category']}
    Description: {info1['description']}
    
    Product 2: {info2['name']}
    Category: {info2['category']}
    Description: {info2['description']}
    
    Template to follow:
    {template if template else "Compare both products, their features, pros/cons, and decide which is better for different use cases."}
    
    Requirements:
    1. Output in valid JSON format with the following keys:
       - title: A catchy, SEO-friendly title (e.g., {info1['name']} vs {info2['name']}).
       - content: The full comparison in Markdown format.
       - rating: A combined or representative rating (float).
       - seo_title: A meta SEO title.
       - seo_description: A meta SEO description.
       - json_ld: A JSON-LD string representing the comparison/product schema.
    2. The content should be at least 800 words.
    """
    
    if not os.getenv("OPENAI_API_KEY"):
        print("MOCK: OPENAI_API_KEY not found. Returning mock comparison.")
        return {
            "title": f"{info1['name']} vs {info2['name']}: Which is Better?",
            "content": f"# {info1['name']} vs {info2['name']}\n\nComparing {info1['name']} and {info2['name']} in the {info1['category']} space.",
            "rating": 4.0,
            "seo_title": f"{info1['name']} vs {info2['name']} Comparison",
            "seo_description": f"Deciding between {info1['name']} and {info2['name']}? Read our full comparison.",
            "json_ld": "{\"@context\": \"https://schema.org/\", \"@type\": \"Product\"}"
        }

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional SEO reviewer."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Generate AI reviews for products.")
    parser.add_argument("--id", type=int, help="ID of the product to generate a review for.")
    parser.add_argument("--vs", type=int, help="ID of the second product for comparison.")
    parser.add_argument("--all", action="store_true", help="Generate reviews for all products that don't have one.")
    parser.add_argument("--type", type=str, default="review", help="Template type to use (review, alternatives, comparison).")
    args = parser.parse_args()
    
    if args.id and args.vs:
        print(f"Generating comparison between {args.id} and {args.vs}")
        data1 = get_product_data(args.id)
        data2 = get_product_data(args.vs)
        if not data1 or not data2:
            print("One or both products not found.")
            return
        
        review = generate_comparison(data1, data2, template_type=args.type)
        if review:
            # For comparison, we might need a special slug or entry in the database.
            # For now, let's just associate it with the first product.
            save_review(args.id, review) 
            print(f"Generated comparison for {data1['info']['name']} and {data2['info']['name']}")
        return

    if args.id:
        product_ids = [args.id]
    elif args.all:
        products = run_db_query("SELECT id FROM products WHERE id NOT IN (SELECT product_id FROM reviews)")
        product_ids = [p['id'] for p in products]
    else:
        print("Please specify --id or --all")
        return

    for pid in product_ids:
        print(f"Processing product ID: {pid}")
        data = get_product_data(pid)
        if not data:
            print(f"Product {pid} not found.")
            continue
            
        review = generate_review(data, template_type=args.type)
        if review:
            save_review(pid, review)
            print(f"Generated and saved review for {data['info']['name']}")
        else:
            print(f"Failed to generate review for {data['info']['name']}")

if __name__ == "__main__":
    main()
