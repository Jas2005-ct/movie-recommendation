import requests

def test_search_api():
    base_url = "http://127.0.0.1:8000/api/search-suggestions/"
    query = "action"
    response = requests.get(f"{base_url}?query={query}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Search API Success! Found {len(data['results'])} results for '{query}'.")
        for item in data['results']:
            print(f"- {item['title']} ({item['year']})")
    else:
        print(f"Search API Failed with status code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_search_api()
