import requests
import json
import os
import taglib


def upload(file_name, genre):
    url = "http://localhost:8000/apiv1/song/"

    # get song attributes
    f = taglib.File(file_name)
    body: dict = {
        "artist": f.tags.get("ARTIST", [""])[0],
        "title": f.tags.get("TITLE", [""])[0],
        "album": f.tags.get("ALBUM", [""])[0],
        "genre": genre,
        "description": "Uploaded from Uploader.py",
        "option": "upload"
    }
    files = {
        'file': open(file_name, 'rb')
    }

    # upload file
    response = requests.post(url, data=body, files=files)
    data = response.json()
    if data["success"]:
        print(f"Uploaded {file_name}")
    else:
        print(f"Failed to upload {file_name}: {data['message']}")


def upload_directory(directory, genre):
    for file_name in os.listdir(directory):
        if file_name.endswith(".mp3"):
            upload(directory + "/" + file_name, genre)



