# Phase 2 — Gym Leaders + Elite Four & Champion
# Holds gym leader and elite four data per region and exposes helper functions
# for the team builder to incorporate gym and endgame coverage into scoring.
GYM_LEADERS = {
    'Kanto': [
        {'name': 'Brock',    'types': ['Rock']},
        {'name': 'Misty',    'types': ['Water']},
        {'name': 'Lt. Surge','types': ['Electric']},
        {'name': 'Erika',    'types': ['Grass']},
        {'name': 'Koga',     'types': ['Poison']},
        {'name': 'Sabrina',  'types': ['Psychic']},
        {'name': 'Blaine',   'types': ['Fire']},
        {'name': 'Giovanni', 'types': ['Ground']},
    ],
    'Johto': [
        {'name': 'Falkner',  'types': ['Flying']},
        {'name': 'Bugsy',    'types': ['Bug']},
        {'name': 'Whitney',  'types': ['Normal']},
        {'name': 'Morty',    'types': ['Ghost']},
        {'name': 'Chuck',    'types': ['Fighting']},
        {'name': 'Jasmine',  'types': ['Steel']},
        {'name': 'Pryce',    'types': ['Ice']},
        {'name': 'Clair',    'types': ['Dragon']},
    ],
    'Hoenn': [
        {'name': 'Roxanne',     'types': ['Rock']},
        {'name': 'Brawly',      'types': ['Fighting']},
        {'name': 'Wattson',     'types': ['Electric']},
        {'name': 'Flannery',    'types': ['Fire']},
        {'name': 'Norman',      'types': ['Normal']},
        {'name': 'Winona',      'types': ['Flying']},
        {'name': 'Tate & Liza', 'types': ['Psychic']},
        {'name': 'Wallace',     'types': ['Water']},
    ],
    'Sinnoh': [
        {'name': 'Roark',        'types': ['Rock']},
        {'name': 'Gardenia',     'types': ['Grass']},
        {'name': 'Maylene',      'types': ['Fighting']},
        {'name': 'Crasher Wake', 'types': ['Water']},
        {'name': 'Fantina',      'types': ['Ghost']},
        {'name': 'Byron',        'types': ['Steel']},
        {'name': 'Candice',      'types': ['Ice']},
        {'name': 'Volkner',      'types': ['Electric']},
    ],
    'Unova': [
        {'name': 'Cilan/Chili/Cress', 'types': ['Grass', 'Fire', 'Water']},
        {'name': 'Lenora',   'types': ['Normal']},
        {'name': 'Burgh',    'types': ['Bug']},
        {'name': 'Elesa',    'types': ['Electric']},
        {'name': 'Clay',     'types': ['Ground']},
        {'name': 'Skyla',    'types': ['Flying']},
        {'name': 'Brycen',   'types': ['Ice']},
        {'name': 'Drayden',  'types': ['Dragon']},
    ],
    'Kalos': [
        {'name': 'Viola',    'types': ['Bug']},
        {'name': 'Grant',    'types': ['Rock']},
        {'name': 'Korrina',  'types': ['Fighting']},
        {'name': 'Ramos',    'types': ['Grass']},
        {'name': 'Clemont',  'types': ['Electric']},
        {'name': 'Valerie',  'types': ['Fairy']},
        {'name': 'Olympia',  'types': ['Psychic']},
        {'name': 'Wulfric',  'types': ['Ice']},
    ],
    'Alola': [
        {'name': 'Ilima',    'types': ['Normal']},
        {'name': 'Lana',     'types': ['Water']},
        {'name': 'Kiawe',    'types': ['Fire']},
        {'name': 'Mallow',   'types': ['Grass']},
        {'name': 'Sophocles','types': ['Electric']},
        {'name': 'Acerola',  'types': ['Ghost']},
        {'name': 'Nanu',     'types': ['Dark']},
        {'name': 'Hapu',     'types': ['Ground']},
    ],
}

ELITE_FOUR = {
    'Kanto': [
        {'name': 'Lorelei',           'types': ['Ice']},
        {'name': 'Bruno',             'types': ['Fighting']},
        {'name': 'Agatha',            'types': ['Ghost']},
        {'name': 'Lance',             'types': ['Dragon']},
        {'name': 'Blue (Champion)',   'types': ['Normal', 'Fire', 'Water', 'Psychic', 'Flying']},
    ],
    'Johto': [
        {'name': 'Will',              'types': ['Psychic']},
        {'name': 'Koga',              'types': ['Poison']},
        {'name': 'Bruno',             'types': ['Fighting']},
        {'name': 'Karen',             'types': ['Dark']},
        {'name': 'Lance (Champion)',  'types': ['Dragon', 'Flying']},
    ],
    'Hoenn': [
        {'name': 'Sidney',            'types': ['Dark']},
        {'name': 'Phoebe',            'types': ['Ghost']},
        {'name': 'Glacia',            'types': ['Ice']},
        {'name': 'Drake',             'types': ['Dragon']},
        {'name': 'Steven (Champion)', 'types': ['Steel', 'Rock']},
    ],
    'Sinnoh': [
        {'name': 'Aaron',             'types': ['Bug']},
        {'name': 'Bertha',            'types': ['Ground']},
        {'name': 'Flint',             'types': ['Fire']},
        {'name': 'Lucian',            'types': ['Psychic']},
        {'name': 'Cynthia (Champion)','types': ['Ghost', 'Dragon', 'Fighting', 'Steel', 'Psychic']},
    ],
    'Unova': [
        {'name': 'Shauntal',          'types': ['Ghost']},
        {'name': 'Grimsley',          'types': ['Dark']},
        {'name': 'Caitlin',           'types': ['Psychic']},
        {'name': 'Marshal',           'types': ['Fighting']},
        {'name': 'Alder (Champion)',  'types': ['Bug', 'Fire', 'Normal', 'Fighting', 'Rock']},
    ],
    'Kalos': [
        {'name': 'Malva',             'types': ['Fire']},
        {'name': 'Siebold',           'types': ['Water']},
        {'name': 'Wikstrom',          'types': ['Steel']},
        {'name': 'Drasna',            'types': ['Dragon']},
        {'name': 'Diantha (Champion)','types': ['Normal', 'Psychic', 'Fighting', 'Fairy', 'Ghost']},
    ],
    'Alola': [
        {'name': 'Hala',              'types': ['Fighting']},
        {'name': 'Olivia',            'types': ['Rock']},
        {'name': 'Nanu',              'types': ['Dark']},
        {'name': 'Acerola',           'types': ['Ghost']},
        {'name': 'Kukui (Champion)',  'types': ['Normal', 'Fire', 'Water', 'Fighting', 'Rock']},
    ],
}


def get_gym_types(region):
    """Return a deduplicated list of all types used by gym leaders in the given region."""
    leaders = GYM_LEADERS.get(region, [])
    gym_types = []
    for leader in leaders:
        gym_types.extend(leader['types'])
    return list(set(gym_types))


def get_elite_four_types(region):
    """Return a deduplicated list of all types used by the Elite Four and Champion."""
    members = ELITE_FOUR.get(region, [])
    elite_types = []
    for member in members:
        elite_types.extend(member['types'])
    return list(set(elite_types))


def print_gym_leaders(region):
    """Print the gym leaders and their types for the chosen region."""
    leaders = GYM_LEADERS.get(region, [])
    print(f"\nGym Leaders in {region}:")
    for leader in leaders:
        types_str = ' / '.join(leader['types'])
        print(f"  {leader['name']:20s} [{types_str}]")


def print_elite_four(region):
    """Print the Elite Four and Champion and their types for the chosen region."""
    members = ELITE_FOUR.get(region, [])
    print(f"\nElite Four & Champion in {region}:")
    for member in members:
        types_str = ' / '.join(member['types'])
        print(f"  {member['name']:25s} [{types_str}]")