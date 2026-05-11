import pandas as pd

ALL_STARTERS = {
    'Kanto':  ['Bulbasaur', 'Charmander', 'Squirtle'],
    'Johto':  ['Chikorita', 'Cyndaquil', 'Totodile'],
    'Hoenn':  ['Treecko', 'Torchic', 'Mudkip'],
    'Sinnoh': ['Turtwig', 'Chimchar', 'Piplup'],
    'Unova':  ['Snivy', 'Tepig', 'Oshawott'],
    'Kalos':  ['Chespin', 'Fennekin', 'Froakie'],
    'Alola':  ['Rowlet', 'Litten', 'Popplio']
}

FINAL_EVOLUTIONS = {
        'Bulbasaur': 'Venusaur',   'Charmander': 'Charizard',  'Squirtle': 'Blastoise',
        'Chikorita': 'Meganium',   'Cyndaquil': 'Typhlosion',  'Totodile': 'Feraligatr',
        'Treecko':   'Sceptile',   'Torchic': 'Blaziken',      'Mudkip': 'Swampert',
        'Turtwig':   'Torterra',   'Chimchar': 'Infernape',    'Piplup': 'Empoleon',
        'Snivy':     'Serperior',  'Tepig': 'Emboar',          'Oshawott': 'Samurott',
        'Chespin':   'Chesnaught', 'Fennekin': 'Delphox',      'Froakie': 'Greninja',
        'Rowlet':    'Decidueye',  'Litten': 'Incineroar',     'Popplio': 'Primarina'
    }

def load_data(pokemon_path="data/Pokemon.csv", evo_path="data/evolution_families.csv"):
    """Load and clean the Pokemon dataset and evolution families CSV."""
    pk = pd.read_csv(pokemon_path)
    pk['Type 2'] = pk['Type 2'].fillna('None')
    is_mega = pk['Name'].str.contains('Mega', case=False)
    pk_megas = pk[is_mega].copy()
    pk = pk[~is_mega].copy()
    evo_df = pd.read_csv(evo_path)
    evolution_families = dict(zip(evo_df['Name'], evo_df['Family']))
    return pk, pk_megas, evolution_families

def select_region():
    """Prompt the user to select a region and return the region name and generation number."""
    region_to_gen = {
        'Kanto': 1, 'Johto': 2, 'Hoenn': 3, 'Sinnoh': 4,
        'Unova': 5, 'Kalos': 6, 'Alola': 7
    }
    while True:
        region = input("Enter the region you are playing: ").title()
        gen_no = region_to_gen.get(region)
        if gen_no is None:
            print(f"Invalid region. Choose from: {', '.join(region_to_gen.keys())}")
        else:
            return region, gen_no

def select_starter(region):
    """Prompt the user to select a starter Pokemon for the given region.
    Returns the chosen starter, its final evolution, and the unchosen starters."""

    print(f"\nAvailable starters in {region}:")
    for s in ALL_STARTERS[region]:
        print(f"  - {s}")
    while True:
        starter = input("\nChoose your starter: ").title()
        if starter not in ALL_STARTERS[region]:
            print(f"Invalid starter. Choose from: {', '.join(ALL_STARTERS[region])}")
        else:
            final_form = FINAL_EVOLUTIONS[starter]
            unchosen = [s for s in ALL_STARTERS[region] if s != starter]
            print(f"\nYou chose {starter} → Final evolution: {final_form}")
            return starter, final_form, unchosen