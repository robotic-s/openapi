import requests
import json

# Replace with your server's URL
SERVER_URL = "https://openapi.sandeshai.in"

def make_request(endpoint, params=None, method='GET', headers=None):
    url = SERVER_URL + endpoint
    if headers is None:
        headers = {}
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, params=params, timeout=10)
        else:
            print(f"Unsupported HTTP method: {method}")
            return None

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        try:
            return response.json()
        except ValueError:
            print(f"HTTP error occurred: {e}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error occurred: {e}")
        return None

def get_api_key():
    api_key = input("Enter your API key: ")
    return api_key

def search(api_key):
    query = input("Enter search query: ")
    filter_type = input("Enter filter (optional, e.g., songs, videos, albums): ")
    params = {'query': query}
    if filter_type:
        params['filter'] = filter_type
    headers = {'X-API-Key': api_key}
    response = make_request('/search', params=params, headers=headers)
    if response:
        print(json.dumps(response, indent=2))
    else:
        print("Failed to retrieve search results.")

def get_song_details(api_key):
    video_id = input("Enter video ID: ")
    headers = {'X-API-Key': api_key}
    response = make_request(f'/song/{video_id}', headers=headers)
    if response:
        print(json.dumps(response, indent=2))
    else:
        print("Failed to retrieve song details.")

def get_song_id(api_key):
    song_name = input("Enter song name: ")
    params = {'song': song_name}
    headers = {'X-API-Key': api_key}
    response = make_request('/song_id', params=params, headers=headers)
    if response:
        print(f"Song ID: {response.get('song_id')}")
    else:
        print("Failed to retrieve song ID.")

def get_artist_details(api_key):
    artist_id = input("Enter artist ID: ")
    headers = {'X-API-Key': api_key}
    response = make_request(f'/artist/{artist_id}', headers=headers)
    if response:
        print(json.dumps(response, indent=2))
    else:
        print("Failed to retrieve artist details.")

def get_artist_id(api_key):
    artist_name = input("Enter artist name: ")
    params = {'artist': artist_name}
    headers = {'X-API-Key': api_key}
    response = make_request('/artist_id', params=params, headers=headers)
    if response:
        print(f"Artist ID: {response.get('artist_id')}")
    else:
        print("Failed to retrieve artist ID.")

def get_album_details(api_key):
    album_id = input("Enter album ID: ")
    headers = {'X-API-Key': api_key}
    response = make_request(f'/album/{album_id}', headers=headers)
    if response:
        print(json.dumps(response, indent=2))
    else:
        print("Failed to retrieve album details.")

def get_album_id(api_key):
    album_name = input("Enter album name: ")
    params = {'album': album_name}
    headers = {'X-API-Key': api_key}
    response = make_request('/album_id', params=params, headers=headers)
    if response:
        print(f"Album ID: {response.get('album_id')}")
    else:
        print("Failed to retrieve album ID.")

def get_playlist_details(api_key):
    playlist_id = input("Enter playlist ID: ")
    headers = {'X-API-Key': api_key}
    response = make_request(f'/playlist/{playlist_id}', headers=headers)
    if response:
        print(json.dumps(response, indent=2))
    else:
        print("Failed to retrieve playlist details.")

def get_playlist_id(api_key):
    playlist_name = input("Enter playlist name: ")
    params = {'playlist': playlist_name}
    headers = {'X-API-Key': api_key}
    response = make_request('/playlist_id', params=params, headers=headers)
    if response:
        print(f"Playlist ID: {response.get('playlist_id')}")
    else:
        print("Failed to retrieve playlist ID.")

def get_charts(api_key):
    country = input("Enter country code (default 'US'): ") or 'US'
    params = {'country': country}
    headers = {'X-API-Key': api_key}
    response = make_request('/charts', params=params, headers=headers)
    if response:
        print(json.dumps(response, indent=2))
    else:
        print("Failed to retrieve charts.")



def explore_trending(api_key):
    headers = {'X-API-Key': api_key}
    response = make_request('/explore/trending', headers=headers)
    if response:
        print(json.dumps(response, indent=2))
    else:
        print("Failed to retrieve trending music.")

def get_recommendations(api_key):
    video_id = input("Enter video ID: ")
    headers = {'X-API-Key': api_key}
    response = make_request(f'/recommendations/{video_id}', headers=headers)
    if response:
        print(json.dumps(response, indent=2))
    else:
        print("Failed to retrieve recommendations.")

def get_lyrics(api_key):
    video_id = input("Enter video ID: ")
    headers = {'X-API-Key': api_key}
    response = make_request(f'/lyrics/{video_id}', headers=headers)
    if response:
        if response.get('status') == 'success':
            print(f"Lyrics:\n{response.get('lyrics')}")
        else:
            print(response.get('message'))
    else:
        print("Failed to retrieve lyrics.")

def get_search_suggestions(api_key):
    query = input("Enter partial query: ")
    params = {'query': query}
    headers = {'X-API-Key': api_key}
    response = make_request('/search_suggestions', params=params, headers=headers)
    if response:
        print("Suggestions:")
        for suggestion in response:
            print(f"- {suggestion}")
    else:
        print("Failed to retrieve search suggestions.")

def main():
    print("Welcome to the Data Client Interface")
    api_key = get_api_key()
    while True:
        print("\nMenu:")
        print("1. Search YouTube Music")
        print("2. Get Song Details")
        print("3. Get Song ID")
        print("4. Get Artist Details")
        print("5. Get Artist ID")
        print("6. Get Album Details")
        print("7. Get Album ID")
        print("8. Get Playlist Details")
        print("9. Get Playlist ID")
        print("10. Get Charts")
        print("11. Explore Trending")
        print("12. Get Recommendations")
        print("13. Get Lyrics")
        print("14. Get Search Suggestions")
        print("15. Exit")
        choice = input("Select an option: ")
        if choice == '1':
            search(api_key)
        elif choice == '2':
            get_song_details(api_key)
        elif choice == '3':
            get_song_id(api_key)
        elif choice == '4':
            get_artist_details(api_key)
        elif choice == '5':
            get_artist_id(api_key)
        elif choice == '6':
            get_album_details(api_key)
        elif choice == '7':
            get_album_id(api_key)
        elif choice == '8':
            get_playlist_details(api_key)
        elif choice == '9':
            get_playlist_id(api_key)
        elif choice == '10':
            get_charts(api_key)
        elif choice == '11':
            explore_trending(api_key)
        elif choice == '12':
            get_recommendations(api_key)
        elif choice == '13':
            get_lyrics(api_key)
        elif choice == '14':
            get_search_suggestions(api_key)
        elif choice == '15':
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == '__main__':
    main()
