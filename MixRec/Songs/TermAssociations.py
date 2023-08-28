from .models import Song

associations: dict = {
    'popularity': [
        'popular',
        'hit',
        'top',
        'chart',
        'trending'
    ],
    'energy': [
        'hype',
        'energetic',
        'party',
        'dance',
        'intense',
        'vibrant'
    ],
    'danceability': [
        'dance',
        'groove',
        'rhythm',
        'beat',
        'bop',
        'vibe'
    ],
    'happiness': [
        'happy',
        'joy',
        'cheerful',
        'upbeat',
        'positive',
        'optimistic'
    ],
    'acousticness': [
        'acoustic',
        'unplugged',
    ],
    'instrumentalness': [
        'instrumental',
        'melody',
        'harmony',
        'tune',
    ],
    'liveness': [
        'live',
        'dynamic',
        'energy',
        'vibrant',
    ],
    'speechiness': [
        'vocal',
        'dialog',
        'rap',
        'talk',
        'speech',
    ],
}


def get_assocations(song: Song) -> list:
    assos = []
    if song.popularity > 65:
       assos.extend(associations['popularity'])
    if song.energy > 0.65:
        assos.extend(associations['energy'])
    if song.danceability > 0.65:
        assos.extend(associations['danceability'])
    if song.happiness > 0.65:
        assos.extend(associations['happiness'])
    if song.acousticness > 0.65:
        assos.extend(associations['acousticness'])
    if song.instrumentalness > 0.65:
        assos.extend(associations['instrumentalness'])
    if song.liveness > 0.65:
        assos.extend(associations['liveness'])
    if song.speechiness > 0.65:
        assos.extend(associations['speechiness'])
    return assos





