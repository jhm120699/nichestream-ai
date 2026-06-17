import requests

app_id = "N86T1R3OWZ"
api_key = "5140dac5e87f47346abbda1a34ee70c3"
index = "products"

url = f"https://{app_id}-dsn.algolia.net/1/indexes/{index}/query"
headers = {
    "X-Algolia-Application-Id": app_id,
    "X-Algolia-API-Key": api_key
}
payload = {"params": "query=&hitsPerPage=1000"}
response = requests.post(url, headers=headers, json=payload)
if response.status_code == 200:
    hits = response.json().get('hits', [])
    tags = set()
    for hit in hits:
        for tag in hit.get('_tags', []):
            if tag.startswith('vertical-'):
                tags.add(tag)
    
    for tag in sorted(list(tags)):
        print(tag)
