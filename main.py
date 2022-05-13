from credentials import sp
import pandas as pd
import urllib.request

def show_tracks(results, uriArray): #get the song id
    for i, item in enumerate(results['items']):
        track = item['track']
        uriArray.append(track['id'])

def track_id(username, playlist_id): #show song from playlist that we pick before
    trackID = []
    results = sp.user_playlist(username, playlist_id)
    tracks = results['tracks']
    show_tracks(tracks, trackID)
    while tracks['next']:
        tracks = sp.next(tracks)
        show_tracks(tracks, trackID)
    return trackID

def getTrackFeatures(id): #get the song atributes of the song
    meta = sp.track(id)
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    artwork = meta['album']['images'][0]['url']
    track = [name, album, artist, artwork]
    return track

def main_func(playlist_creator, playlist_uri, filename):
    ids = track_id(playlist_creator, playlist_uri)
    tracks = []
    for i in range(len(ids)):
        track = getTrackFeatures(ids[i])
        tracks.append(track)
        df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'artwork'])
        df.to_csv(filename+".csv", sep = ',', index=False)
    return df

#fill main_func with playlist creator and playlist uri
df = main_func('thalibarrifqi', '7ER372B5dxUQ28JcyoZkWV', 'playlist') 
df = pd.read_csv('playlist.csv')

for i, item in enumerate(df['name']):
    url = df['artwork'][i] #url of the song album artwork
    file_name = str(i)
    urllib.request.urlretrieve(url, 'images/'+file_name+'.png') #downloading artwork to images folder