import requests
import json
base_url = "https://api.musixmatch.com/ws/1.1/"
api_key = "&apikey=9843f22c0731122bbc217d7f65785544"

# example call: base_url + lyrics_matcher + format_url + artist_search_parameter + artist_variable + track_search_parameter + track_variable + api_key
# example json print: print(json.dumps(api_call, sort_keys=True, indent=2))
artist_name = "Drake"
track_name = "Feel no ways"
lyrics_matcher = "matcher.lyrics.get"
format_url = "?format=json&callback=callback"
artist_search_parameter = "&q_artist="
track_search_parameter = "&q_track="

api_call = base_url + lyrics_matcher + format_url + artist_search_parameter + artist_name + track_search_parameter + track_name + api_key
request = requests.get(api_call)
data = request.json()
data = data['message']['body']
print(data['lyrics']['lyrics_body'])
