import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np


"""------------------------------------------------------------------------------------------------------------------------"""

CLIENT_ID = "a60cb37839d14166b191940d1ce59a8d"
CLIENT_SECRET = "f6f63e52e3f24de588529ca336b7a099"

client_credentials_manager = SpotifyClientCredentials(client_id='a60cb37839d14166b191940d1ce59a8d', client_secret='f6f63e52e3f24de588529ca336b7a099')
sp =spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_playlist_name(playlist_id):
	 return sp.playlist(playlist_id)['name']

def get_song_features(playlist_id):
	playlist = sp.user_playlist_tracks("spotify", playlist_id)
	playlist_tracks = [item['track'] for item in playlist['items']]
	audio_features_all_songs = [(track['name'], sp.audio_features(track['uri'])[0]) for track in playlist_tracks]

	filtered_audio_features = []
	for song in audio_features_all_songs:
		try:
			filtered_song_features = (song[0], {name: song[1][name] for name in song[1] if type(song[1][name]) == float or type(song[1][name]) == int})
			filtered_audio_features.append(filtered_song_features)
		except:
			print("song doesn't exist")

	return filtered_audio_features

def avg_playlist_vals(playlist_id):
	playlist_tracks = get_song_features(playlist_id)

	total_values = {}
	for track in playlist_tracks:
		audio_features = track[1]
		for audio_feature in audio_features:
			if audio_feature in total_values:
				total_values[audio_feature].append(audio_features[audio_feature])
			else:
				total_values[audio_feature] = [audio_features[audio_feature]]

	avg_values = {name: get_avg(total_values[name]) for name in total_values}

	return avg_values

def get_avg(lst):
	return sum(lst)/len(lst)

def audio_features_to_vector(audio_features):
	vector = []
	ignored_keys = ['key', 'loudness', 'tempo', 'duration_ms', 'time_signature']
	for key in audio_features:
		if key not in ignored_keys:
			vector.append(audio_features[key])

	return vector

def inner_product(v1, v2):
	sum = 0
	for i in range(len(v1)):
		sum += v1[i] * v2[i]

	return sum

def norm_squared(v1):
	return inner_product(v1, v1)

def compare_vectors(v1, v2):
	return norm_squared(v1) + norm_squared(v2) - 2*inner_product(v1, v2)

def min_error(lst):
	return min(lst)

def all_category_ids():
	ids = []
	categories = sp.categories(limit = 50)['categories']['items']
	for category in categories:
		ids.append(category['id'])

	return ids

def category_playlist_ids():
	playlist_ids = {}
	for category_id in all_category_ids():
		try:
			playlists_in_category = playlist_id = sp.category_playlists(category_id=category_id, country=None, limit=1, offset=0)['playlists']['items']
			if len(playlists_in_category) > 0:
				first_playlist = playlists_in_category[0]
				if 'id' in first_playlist:
					playlist_id = sp.category_playlists(category_id=category_id, country=None, limit=1, offset=0)['playlists']['items'][0]['id']
					playlist_ids[category_id] = playlist_id
		except:
			print("playlist with category id doesn't exist")
	return playlist_ids

def most_similar_song_in_playlist(playlist_id, avg_song_vector):
	
	tracks_in_playlist = get_song_features(playlist_id)

	min_difference, min_track = None, None

	for track in tracks_in_playlist:
		track_audio_vector = audio_features_to_vector(track[1])
		err = compare_vectors(track_audio_vector, avg_song_vector)
		if min_difference == None or err < min_difference:
			min_difference, min_track = err, track
			print(track_audio_vector, min_difference)
	return (min_track, min_difference)

def most_similar_song_over_categories(category_ids, avg_song_vector):
	category_playlists = category_playlist_ids()
	min_difference, min_track = None, None

	for category_id in category_ids:
		closest_in_playlist = most_similar_song_in_playlist(category_playlists[category_id], avg_song_vector)
		if min_difference == None or closest_in_playlist[1] < min_difference:
			min_track = closest_in_playlist[0]
			min_difference = closest_in_playlist[1]

	return closest_in_playlist[0]


