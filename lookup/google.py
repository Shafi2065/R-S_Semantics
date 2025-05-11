import json
import urllib.parse
import urllib.request

def google_lookup(term):
  
    api_key='AIzaSyCkz5APwGK2fvnHXp_XAU6oYc90e8C9cC8'
  
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'

    # Construct query parameters
    params = {
        'query': term,
        'limit': 1,  # Return only the first matching entity
        'indent': True,
        'key': api_key,
    }

    # Construct the complete URL
    url = service_url + '?' + urllib.parse.urlencode(params)

    try:
        # Send the request and load the response
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())

        # Extract the first result
        if data['itemListElement']:
            result = data['itemListElement'][0]['result']
            uri = result.get('@id', None)
            label = result.get('name', None)
            return uri, label

    except Exception as e:
        print(f"Error during Google lookup for '{term}': {e}")

    return None, None

