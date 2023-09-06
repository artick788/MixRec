import uuid
import yt_dlp
import ffmpeg
import shutil


def download_youtube(url: str, file_path: str):
    rand = str(uuid.uuid4())

    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': 'output' + rand + '.%(ext)s',
        'addmetadata': True,
        'extractaudio': True,
        'prefer-ffmpeg': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }
    tries: int = 4
    while tries > 0:
        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([url])
                temp_name: str = 'output' + rand
                stream = ffmpeg.input(temp_name + '.webm')
                stream = ffmpeg.output(stream, temp_name + "." + 'mp3')

        except Exception as e:
            print("Download failed: " + str(e) + " \nTries: " + str(tries))

        except:
            print("Download failed: no further details, \nTries: " + str(tries))
        tries -= 1

    # rename
    shutil.move(temp_name + ".mp3", file_path)
