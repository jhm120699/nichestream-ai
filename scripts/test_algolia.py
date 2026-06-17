import requests

app_id = "N86T1R3OWZ"
api_key = "5140dac5e87f47346abbda1a34ee70c3"

indices = ["products", "posts", "projects", "users"]

for index in indices:
    url = f"https://{app_id}-dsn.algolia.net/1/indexes/{index}/query"
    headers = {
        "X-Algolia-Application-Id": app_id,
        "X-Algolia-API-Key": api_key
    }
    payload = {"params": "query=&hitsPerPage=5"}
    response = requests.post(url, headers=headers, json=payload)
    print(f"Index: {index}, Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Hits: {len(data.get('hits', []))}")
        if data.get('hits'):
            print(f"Sample hit keys: {data['hits'][0].keys()}")
