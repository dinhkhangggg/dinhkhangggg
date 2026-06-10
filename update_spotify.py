import os
import requests
import base64

CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
REFRESH_TOKEN = os.environ.get('SPOTIFY_REFRESH_TOKEN')

def get_access_token():
    if not CLIENT_ID or not CLIENT_SECRET or not REFRESH_TOKEN:
        print("Missing secrets")
        return None
        
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    
    response = requests.post(
        'https://accounts.spotify.com/api/token',
        headers={'Authorization': f'Basic {b64_auth_str}'},
        data={'grant_type': 'refresh_token', 'refresh_token': REFRESH_TOKEN}
    )
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print("Failed to get token:", response.text)
        return None

def get_now_playing(access_token):
    response = requests.get(
        'https://api.spotify.com/v1/me/player/currently-playing',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    if response.status_code == 204 or response.status_code != 200:
        return None
    return response.json()

def update_readme(song_info):
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
        
    start_tag = '<!-- SPOTIFY-NOW-PLAYING-START -->'
    end_tag = '<!-- SPOTIFY-NOW-PLAYING-END -->'
    
    if start_tag not in content or end_tag not in content:
        print("Could not find tags in README")
        return
        
    before = content.split(start_tag)[0]
    after = content.split(end_tag)[1]
    
    if song_info is None or not song_info.get('item'):
        spotify_html = f"<p align='center'><img src='https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Headphone.png' width='25' /> <i>Hiện tại mình đang không nghe nhạc gì cả 😴</i></p>"
    else:
        song_name = song_info['item']['name']
        artist_name = ", ".join([artist['name'] for artist in song_info['item']['artists']])
        album_img = song_info['item']['album']['images'][1]['url'] if len(song_info['item']['album']['images']) > 1 else song_info['item']['album']['images'][0]['url']
        song_url = song_info['item']['external_urls']['spotify']
        
        spotify_html = f"""
<p align="center">
  <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Headphone.png" width="30" /> <b>Đang nghe trên Spotify:</b><br/><br/>
  <a href="{song_url}" target="_blank">
    <img src="{album_img}" width="100" style="border-radius: 10px;" />
  </a>
  <br/>
  <a href="{song_url}"><b>{song_name}</b></a><br/>
  <i>{artist_name}</i>
</p>
"""
        
    new_content = f"{before}{start_tag}\n{spotify_html}\n{end_tag}{after}"
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("README updated successfully")

if __name__ == '__main__':
    token = get_access_token()
    if token:
        song = get_now_playing(token)
        update_readme(song)
