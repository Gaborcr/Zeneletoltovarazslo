import os
import yt_dlp
from mutagen.flac import FLAC

def download_audio(url, output_path="downloads"):
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Set yt-dlp options to download directly as FLAC
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'flac',
        }],
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'quiet': True
    }

    # Download the audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace('.webm', '.flac').replace('.m4a', '.flac')
    
    return filename, info


def extract_metadata(info):
    # Extract artist, album, and release date from the metadata
    artist = info.get('artist', 'Unknown Artist')
    album = info.get('album', 'Unknown Album')
    release_date = str(info.get('release_date', 'Unknown Date'))
    
    return artist, album, release_date


def embed_metadata(flac_file, artist, album, release_date, title):
    # Embed metadata into FLAC file
    audio = FLAC(flac_file)
    audio['artist'] = artist
    audio['album'] = album
    audio['date'] = release_date
    audio['title'] = title
    audio.save()


if __name__ == "__main__":
    url = input("Enter YouTube URL: ")
    flac_file, info = download_audio(url)

    artist, album, release_date = extract_metadata(info)
    title = info.get('title', 'Unknown Title')
    
    embed_metadata(flac_file, artist, album, release_date, title)
    
    print(f"Download complete: {flac_file}")
    print(f"Artist: {artist}\nAlbum: {album}\nRelease Date: {release_date}")
