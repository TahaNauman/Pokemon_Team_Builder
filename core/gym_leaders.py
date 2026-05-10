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
        {'name': 'Roxanne',  'types': ['Rock']},
        {'name': 'Brawly',   'types': ['Fighting']},
        {'name': 'Wattson',  'types': ['Electric']},
        {'name': 'Flannery', 'types': ['Fire']},
        {'name': 'Norman',   'types': ['Normal']},
        {'name': 'Winona',   'types': ['Flying']},
        {'name': 'Tate & Liza', 'types': ['Psychic']},
        {'name': 'Wallace',  'types': ['Water']},
    ],
    'Sinnoh': [
        {'name': 'Roark',    'types': ['Rock']},
        {'name': 'Gardenia', 'types': ['Grass']},
        {'name': 'Maylene',  'types': ['Fighting']},
        {'name': 'Crasher Wake', 'types': ['Water']},
        {'name': 'Fantina',  'types': ['Ghost']},
        {'name': 'Byron',    'types': ['Steel']},
        {'name': 'Candice',  'types': ['Ice']},
        {'name': 'Volkner',  'types': ['Electric']},
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


def get_gym_types(region):
    """
    Return a deduplicated list of all types used by gym leaders in the given region.
    These are the types we want our team to be able to counter.
    """
    leaders = GYM_LEADERS.get(region, [])
    gym_types = []
    for leader in leaders:
        gym_types.extend(leader['types'])
    return list(set(gym_types))


def print_gym_leaders(region):
    """Print the gym leaders and their types for the chosen region."""
    leaders = GYM_LEADERS.get(region, [])
    print(f"\nGym Leaders in {region}:")
    for leader in leaders:
        types_str = ' / '.join(leader['types'])
        print(f"  {leader['name']:20s} [{types_str}]")