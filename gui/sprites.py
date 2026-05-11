import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


REGION_GAME = {
    'Kanto':  'firered',
    'Johto':  'heartgold',
    'Hoenn':  'emerald',
    'Sinnoh': 'platinum',
    'Unova':  'black-2',
    'Kalos':  'x',
    'Alola':  'sun',
}

# ── PokéAPI base URL ──────────────────────────────────────────────────────────
POKEAPI_BASE = "https://pokeapi.co/api/v2"
NAME_OVERRIDES = {
    # Special characters
    'Nidoran♀':             'nidoran-f',
    'Nidoran♂':             'nidoran-m',
    'Mr. Mime':              'mr-mime',
    'Farfetch\'d':           'farfetchd',
    'Farfetchd':             'farfetchd',
    'Ho-Oh':                 'ho-oh',
    'Mime Jr.':              'mime-jr',
    'Porygon-Z':             'porygon-z',
    'Flabébé':               'flabebe',
    'Type: Null':            'type-null',
    'Jangmo-o':              'jangmo-o',
    'Hakamo-o':              'hakamo-o',
    'Kommo-o':               'kommo-o',
    'Tapu Koko':             'tapu-koko',
    'Tapu Lele':             'tapu-lele',
    'Tapu Bulu':             'tapu-bulu',
    'Tapu Fini':             'tapu-fini',
    'Mr. Rime':              'mr-rime',
    'Sirfetch\'d':           'sirfetchd',
    'AegislashBlade Forme':  'aegislash',
    'AegislashShield Forme': 'aegislash',
    'GourgeistSmall Size':   'gourgeist-small',
    'GourgeistAverage Size': 'gourgeist-average',
    'GourgeistLarge Size':   'gourgeist-large',
    'GourgeistSuper Size':   'gourgeist-super',
    'Gourgeist':             'gourgeist-average',
    'WormadamPlant Cloak':   'wormadam',
    'WormadamSandy Cloak':   'wormadam-sandy',
    'WormadamTrash Cloak':   'wormadam-trash',
    'LycanrocMidday':        'lycanroc',
    'LycanrocMidnight':      'lycanroc-midnight',
    'LycanrocDusk':          'lycanroc-dusk',
    'OricorioBaile':         'oricorio',
    'OricorioPom-Pom':       'oricorio-pom-pom',
    'OricorioPau':           'oricorio-pau',
    'OricorioSensu':         'oricorio-sensu',
    'GastrodonEast':         'gastrodon',
    'GastrodonWest':         'gastrodon',
    'RotomHeat Rotom':       'rotom-heat',
    'RotomWash Rotom':       'rotom-wash',
    'RotomFrost Rotom':      'rotom-frost',
    'RotomFan Rotom':        'rotom-fan',
    'RotomMow Rotom':        'rotom-mow',
    'MeowsticMale':          'meowstic',
    'MeowsticFemale':        'meowstic-f',
    'WishiwashiSolo':        'wishiwashi',
    'WishiwashiSchool':      'wishiwashi-school',
    'MiniorMeteor':          'minior-red-meteor',
    'MiniorCore':            'minior',
    'Pumpkaboo':                  'pumpkaboo-average',
    'PumpkabooSmall Size':        'pumpkaboo-small',
    'PumpkabooAverage Size':      'pumpkaboo-average',
    'PumpkabooLarge Size':        'pumpkaboo-large',
    'PumpkabooSuper Size':        'pumpkaboo-super',
}


def _normalize_name(name):
    """
    Convert a Pokemon name to the format PokéAPI expects.
    Checks NAME_OVERRIDES first, then applies general normalization rules.
    """
    if name in NAME_OVERRIDES:
        return NAME_OVERRIDES[name]

    return (
        name.lower()
            .replace(' ', '-')
            .replace('.', '')
            .replace("'", '')
            .replace('♂', '-m')
            .replace('♀', '-f')
            .replace('é', 'e')
            .replace(':', '')
    )


def fetch_sprite(pokemon_name):
    """
    Fetch the game sprite for a Pokemon from PokéAPI.
    Returns a QPixmap of the sprite, or None if unavailable.
    """
    name = _normalize_name(pokemon_name)
    url = f"{POKEAPI_BASE}/pokemon/{name}"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return None

        data = response.json()

        # Use the front_default game sprite (pixelated classic look)
        sprite_url = data['sprites']['front_default']
        if not sprite_url:
            return None

        sprite_response = requests.get(sprite_url, timeout=5)
        if sprite_response.status_code != 200:
            return None

        pixmap = QPixmap()
        pixmap.loadFromData(sprite_response.content)

        # Scale up the sprite — game sprites are tiny (96x96)
        # Scale to 120x120 using nearest neighbour to keep the pixelated look
        pixmap = pixmap.scaled(
            120, 120,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.FastTransformation
        )

        return pixmap

    except requests.RequestException:
        return None


def fetch_location(base_form_name, region):
    """
    Fetch the catch location for a Pokemon's base form from PokéAPI.
    Uses the game version mapped to the chosen region.
    Returns a location string with a helpful message if not catchable in the wild.
    """
    game_version = REGION_GAME.get(region, '')
    name = _normalize_name(base_form_name)
    url = f"{POKEAPI_BASE}/pokemon/{name}/encounters"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return "Obtain via evolution"

        encounters = response.json()

        if not encounters:
            # No wild encounters at all — likely obtained by evolving or as a gift
            return "Obtain via evolution or as a gift"

        # Filter encounters to the specific game version
        locations = []
        for encounter in encounters:
            for version_detail in encounter['version_details']:
                if version_detail['version']['name'] == game_version:
                    location_name = encounter['location_area']['name']
                    # Clean up the location name
                    location_name = location_name.replace('-', ' ').title()
                    # Strip redundant suffixes for cleaner display
                    for suffix in [' Area', ' Zone']:
                        location_name = location_name.replace(suffix, '')
                    locations.append(location_name)

        if not locations:
            # Has wild encounters but not in this specific game
            return "Not available in the wild — obtain via trade or transfer"

        # Deduplicate and cap at 3 locations for display
        locations = list(dict.fromkeys(locations))
        return ', '.join(locations[:3])

    except requests.RequestException:
        return "Location unavailable"