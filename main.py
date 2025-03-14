import os
import yt_dlp
from pydub import AudioSegment
from mutagen.flac import FLAC

def download_audio(url, output_path="downloads"):
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Set yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'quiet': True
    }

    # Download the audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
    
    return filename, info


def convert_to_flac(mp3_file):
    # Convert MP3 to FLAC
    audio = AudioSegment.from_mp3(mp3_file)
    flac_file = mp3_file.replace(".mp3", ".flac")
    audio.export(flac_file, format="flac")

    # Optionally delete the original MP3
    os.remove(mp3_file)
    return flac_file


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
    mp3_file, info = download_audio(url)
    flac_file = convert_to_flac(mp3_file)

    artist, album, release_date = extract_metadata(info)
    title = info.get('title', 'Unknown Title')
    
    embed_metadata(flac_file, artist, album, release_date, title)
    
    print(f"Download complete: {flac_file}")
    print(f"Artist: {artist}\nAlbum: {album}\nRelease Date: {release_date}")