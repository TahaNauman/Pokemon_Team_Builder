type_chart = {
    'Normal':   {
        'strong_against': [],
        'weak_against':   ['Fighting'],
        'immune_to':      ['Ghost']
    },
    'Fire':     {
        'strong_against': ['Grass', 'Ice', 'Bug', 'Steel'],
        'weak_against':   ['Water', 'Ground', 'Rock'],
        'immune_to':      []
    },
    'Water':    {
        'strong_against': ['Fire', 'Ground', 'Rock'],
        'weak_against':   ['Electric', 'Grass'],
        'immune_to':      []
    },
    'Electric': {
        'strong_against': ['Water', 'Flying'],
        'weak_against':   ['Ground'],
        'immune_to':      []
    },
    'Grass':    {
        'strong_against': ['Water', 'Ground', 'Rock'],
        'weak_against':   ['Fire', 'Ice', 'Poison', 'Flying', 'Bug'],
        'immune_to':      []
    },
    'Ice':      {
        'strong_against': ['Grass', 'Ground', 'Flying', 'Dragon'],
        'weak_against':   ['Fire', 'Fighting', 'Rock', 'Steel'],
        'immune_to':      []
    },
    'Fighting': {
        'strong_against': ['Normal', 'Ice', 'Rock', 'Dark', 'Steel'],
        'weak_against':   ['Flying', 'Psychic', 'Fairy'],
        'immune_to':      []
    },
    'Poison':   {
        'strong_against': ['Grass', 'Fairy'],
        'weak_against':   ['Ground', 'Psychic'],
        'immune_to':      []
    },
    'Ground':   {
        'strong_against': ['Fire', 'Electric', 'Poison', 'Rock', 'Steel'],
        'weak_against':   ['Water', 'Grass', 'Ice'],
        'immune_to':      ['Electric']
    },
    'Flying':   {
        'strong_against': ['Grass', 'Fighting', 'Bug'],
        'weak_against':   ['Electric', 'Ice', 'Rock'],
        'immune_to':      ['Ground']
    },
    'Psychic':  {
        'strong_against': ['Fighting', 'Poison'],
        'weak_against':   ['Bug', 'Ghost', 'Dark'],
        'immune_to':      []
    },
    'Bug':      {
        'strong_against': ['Grass', 'Psychic', 'Dark'],
        'weak_against':   ['Fire', 'Flying', 'Rock'],
        'immune_to':      []
    },
    'Rock':     {
        'strong_against': ['Fire', 'Ice', 'Flying', 'Bug'],
        'weak_against':   ['Water', 'Grass', 'Fighting', 'Ground', 'Steel'],
        'immune_to':      []
    },
    'Ghost':    {
        'strong_against': ['Psychic', 'Ghost'],
        'weak_against':   ['Ghost', 'Dark'],
        'immune_to':      ['Normal', 'Fighting']
    },
    'Dragon':   {
        'strong_against': ['Dragon'],
        'weak_against':   ['Ice', 'Dragon', 'Fairy'],
        'immune_to':      []
    },
    'Dark':     {
        'strong_against': ['Psychic', 'Ghost'],
        'weak_against':   ['Fighting', 'Bug', 'Fairy'],
        'immune_to':      ['Psychic']
    },
    'Steel':    {
        'strong_against': ['Ice', 'Rock', 'Fairy'],
        'weak_against':   ['Fire', 'Fighting', 'Ground'],
        'immune_to':      ['Poison']
    },
    'Fairy':    {
        'strong_against': ['Fighting', 'Dragon', 'Dark'],
        'weak_against':   ['Poison', 'Steel'],
        'immune_to':      ['Dragon']
    },
    'None':     {
        'strong_against': [],
        'weak_against':   [],
        'immune_to':      []
    },
}