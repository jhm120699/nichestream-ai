import requests

app_id = "N86T1R3OWZ"
api_key = "5140dac5e87f47346abbda1a34ee70c3"
index = "products"

url = f"https://{app_id}-dsn.algolia.net/1/indexes/{index}/query"
headers = {
    "X-Algolia-Application-Id": app_id,
    "X-Algolia-API-Key": api_key
}
payload = {"params": "query=&hitsPerPage=100"}
response = requests.post(url, headers=headers, json=payload)
if response.status_code == 200:
    hits = response.json().get('hits', [])
    tags = {}
    for hit in hits:
        for tag in hit.get('_tags', []):
            tags[tag] = tags.get(tag, 0) + 1
    
    sorted_tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)
    for tag, count in sorted_tags[:20]:
        print(f"{tag}: {count}")
