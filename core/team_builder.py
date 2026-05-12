import random
from core.type_chart import type_chart as TYPE_CHART

TRADE_EVOLUTIONS = {
    # Kanto
    'Alakazam', 'Machamp', 'Golem', 'Gengar',
    # Johto
    'Politoed', 'Slowking', 'Steelix', 'Scizor', 'Kingdra',
    'Porygon2',
    # Hoenn
    'Huntail', 'Gorebyss',
    # Sinnoh
    'Rhyperior', 'Electivire', 'Magmortar', 'Togekiss',
    'Yanmega', 'Leafeon', 'Glaceon', 'Gliscor',
    'Mamoswine', 'PorygonZ', 'Gallade', 'Probopass',
    'Dusknoir', 'Froslass',
    # Unova
    'Gigalith', 'Conkeldurr', 'Escavalier', 'Accelgor',
    # Kalos
    'Aromatisse', 'Slurpuff',
}

FORM_VARIANTS = {
    'AegislashBlade Forme':   'Aegislash',
    'AegislashShield Forme':  'Aegislash',
    'GourgeistSmall Size':    'Gourgeist',
    'GourgeistAverage Size':  'Gourgeist',
    'GourgeistLarge Size':    'Gourgeist',
    'GourgeistSuper Size':    'Gourgeist',
    'WormadamPlant Cloak':    'Wormadam',
    'WormadamSandy Cloak':    'Wormadam',
    'WormadamTrash Cloak':    'Wormadam',
    'LycanrocMidday':   'Lycanroc',
    'LycanrocMidnight': 'Lycanroc',
    'LycanrocDusk':     'Lycanroc',
    'OricorioBaile':    'Oricorio',
    'OricorioPom-Pom':  'Oricorio',
    'OricorioPau':      'Oricorio',
    'OricorioSensu':    'Oricorio',
    'GastrodonEast':    'Gastrodon',
    'GastrodonWest':    'Gastrodon',
    'RotomHeat Rotom':        'Rotom',
    'RotomWash Rotom':        'Rotom',
    'RotomFrost Rotom':       'Rotom',
    'RotomFan Rotom':         'Rotom',
    'RotomMow Rotom':         'Rotom',
    'MeowsticMale':     'Meowstic',
    'MeowsticFemale':   'Meowstic',
    'WishiwashiSolo':   'Wishiwashi',
    'WishiwashiSchool': 'Wishiwashi',
    'MiniorMeteor':     'Minior',
    'MiniorCore':       'Minior',
    'PumpkabooSmall Size': 'Pumpkaboo',
    'PumpkabooAverage Size': 'Pumpkaboo',  
    'PumpkabooLarge Size': 'Pumpkaboo',
    'PumpkabooSuper Size': 'Pumpkaboo',
}


def get_family(name, evolution_families):
    """Return the evolution family root for a given Pokemon name."""
    base = FORM_VARIANTS.get(name, name)
    return evolution_families.get(base, base)


def get_starter_weaknesses(pk, final_form):
    """Return the types and weaknesses of the starter's final evolution."""
    starter_row = pk[pk['Name'] == final_form].iloc[0]

    types = [starter_row['Type 1']]
    if starter_row['Type 2'] != 'None':
        types.append(starter_row['Type 2'])

    weaknesses = []
    for t in types:
        chart = TYPE_CHART.get(t, {'strong_against': [], 'weak_against': [], 'immune_to': []})
        weaknesses.extend(chart['weak_against'])

    weaknesses = list(set(weaknesses))
    return types, weaknesses


def score_candidate(row, covered_weaknesses, team_types, gym_types=None, elite_four_types=None, current_team_weaknesses=None):
    """
    Score a candidate Pokemon for team fit.

    Weakness coverage (primary):
    +5  for each team weakness this Pokemon is immune to
    +3  for each team weakness this Pokemon is strong against
    -2  for each of its own weaknesses that overlap with starter's weaknesses
    -4  for each of its own weaknesses that overlap with current team weaknesses
    -1  scaled penalty for type overlap with current team

    Gym coverage (secondary):
    +1  for each gym leader type this Pokemon is strong against
    +2  for each gym leader type this Pokemon is immune to

    Elite Four + Champion coverage:
    +2  for each Elite Four type this Pokemon is strong against
    +3  for each Elite Four type this Pokemon is immune to

    +BST/600 as a tiebreaker
    """
    if gym_types is None:
        gym_types = []
    if elite_four_types is None:
        elite_four_types = []
    if current_team_weaknesses is None:
        current_team_weaknesses = set()

    c_types = [row['Type 1']]
    if row['Type 2'] != 'None':
        c_types.append(row['Type 2'])

    score = 0
    candidate_weaknesses = []

    for c_type in c_types:
        chart = TYPE_CHART.get(c_type, {'strong_against': [], 'weak_against': [], 'immune_to': []})

        for w in covered_weaknesses:
            if w in chart['strong_against']:
                score += 3
            elif w in chart['immune_to']:
                score += 5

        for g in gym_types:
            if g in chart['strong_against']:
                score += 1
            elif g in chart['immune_to']:
                score += 2

        for e in elite_four_types:
            if e in chart['strong_against']:
                score += 2
            elif e in chart['immune_to']:
                score += 3

        candidate_weaknesses.extend(chart['weak_against'])

        type_count = team_types.count(c_type)
        if type_count > 0:
            score -= 1 * type_count

    for w in candidate_weaknesses:
        if w in covered_weaknesses:
            score -= 2   
        if w in current_team_weaknesses:
            score -= 4   

    total_stats = row.get('Total', 0)
    score += total_stats / 600

    return score
def build_team(pk, pk_region, final_form, types, weaknesses, evolution_families, gym_types=None, unchosen_starters=None, elite_four_types=None):
    """
    Build a team of 6 Pokemon based on type coverage, gym leader coverage,
    and Elite Four + Champion coverage.

    Excludes:
    - Legendaries
    - Unchosen starter lines
    - Trade-only evolutions
    - Duplicate form variants (e.g. both Aegislash-Blade and Aegislash-Shield)

    Randomly picks from the top 3 scoring candidates each iteration
    so reruns produce varied teams while still being type-sound.

    Returns the final team as a list of Pokemon names.
    """
    if gym_types is None:
        gym_types = []
    if unchosen_starters is None:
        unchosen_starters = []
    if elite_four_types is None:
        elite_four_types = []

    blocked_families = {get_family(final_form, evolution_families)}
    for s in unchosen_starters:
        blocked_families.add(get_family(s, evolution_families))

    seen_families = set(blocked_families)
    valid_indices = []

    for idx, row in pk_region.iterrows():
        name = row['Name']
        family = get_family(name, evolution_families)

        if row['Legendary']:
            continue
        if family in blocked_families:
            continue
        if name in TRADE_EVOLUTIONS:
            continue
        if family in seen_families:
            continue

        seen_families.add(family)
        valid_indices.append(idx)

    candidates = pk_region.loc[valid_indices].copy()

    team = [final_form]
    team_types = types.copy()
    used_families = {get_family(final_form, evolution_families)}
    covered_weaknesses = set(weaknesses)

    MIN_BST = 400

    while len(team) < 6:
        current_team_weaknesses = set()
        current_team_immunities = set()
        for t in team_types:
            chart = TYPE_CHART.get(t, {'strong_against': [], 'weak_against': [], 'immune_to': []})
            current_team_weaknesses.update(chart['weak_against'])
            current_team_immunities.update(chart['immune_to'])
        current_team_weaknesses -= current_team_immunities

        scored = []

        for idx, row in candidates.iterrows():
            name = row['Name']

            if get_family(name, evolution_families) in used_families:
                continue

            if row.get('Total', 0) < MIN_BST:
                continue

            s = score_candidate(row, covered_weaknesses, team_types, gym_types, elite_four_types, current_team_weaknesses)
            scored.append((s, name))

        if not scored:
            for idx, row in candidates.iterrows():
                name = row['Name']
                if get_family(name, evolution_families) in used_families:
                    continue
                s = score_candidate(row, covered_weaknesses, team_types, gym_types, elite_four_types, current_team_weaknesses)
                scored.append((s, name))

        if not scored:
            print("Not enough eligible Pokemon to fill the team.")
            break

        scored.sort(key=lambda x: x[0], reverse=True)
        top_n = scored[:2]
        _, best_pokemon = random.choice(top_n)

        team.append(best_pokemon)
        used_families.add(get_family(best_pokemon, evolution_families))

        new_row = pk[pk['Name'] == best_pokemon].iloc[0]
        new_types = [new_row['Type 1']]
        if new_row['Type 2'] != 'None':
            new_types.append(new_row['Type 2'])
            team_types.extend(new_types)

        for t in new_types:
            chart = TYPE_CHART.get(t, {'strong_against': [], 'weak_against': [], 'immune_to': []})
            covered_weaknesses -= set(chart['strong_against'])
            covered_weaknesses -= set(chart['immune_to'])

        candidates = candidates[candidates['Name'] != best_pokemon]

    return team

def select_mega(pk, pk_megas, team, team_weaknesses):
    """
    Select the best Mega Evolution for the team.

    Scoring per eligible Mega:
    - BST gain normalised to 0-5 range across all candidates
    - Type coverage improvement: +3 per team weakness the Mega's
      new types cover that the base form didn't, +5 per immunity gained

    Returns (base_name, mega_row) or (None, None) if no Megas available.
    """
    eligible = []

    for name in team:
        pattern = f"^Mega {name}"
        matches = pk_megas[pk_megas['Name'].str.contains(pattern, case=False, regex=True)]
        if matches.empty:
            continue

        base_row = pk[pk['Name'] == name].iloc[0]
        base_bst = base_row['Total']
        base_types = {base_row['Type 1'], base_row['Type 2']} - {'None'}

        for _, mega_row in matches.iterrows():
            mega_bst = mega_row['Total']
            bst_gain = mega_bst - base_bst

            mega_types = {mega_row['Type 1'], mega_row['Type 2']} - {'None'}
            new_types = mega_types - base_types

            coverage_gain = 0
            for t in new_types:
                chart = TYPE_CHART.get(t, {'strong_against': [], 'weak_against': [], 'immune_to': []})
                for w in team_weaknesses:
                    if w in chart['strong_against']:
                        coverage_gain += 3
                    elif w in chart['immune_to']:
                        coverage_gain += 5

            eligible.append((name, mega_row, bst_gain, coverage_gain))

    if not eligible:
        return None, None

    max_bst_gain = max(e[2] for e in eligible) or 1
    scored = []
    for base_name, mega_row, bst_gain, coverage_gain in eligible:
        bst_score = (bst_gain / max_bst_gain) * 5
        total_score = bst_score + coverage_gain
        scored.append((total_score, base_name, mega_row))

    scored.sort(key=lambda x: x[0], reverse=True)
    _, best_base, best_mega = scored[0]

    return best_base, best_mega


def evaluate_team(pk, team):
    """
    Evaluate the quality of a recommended team across three dimensions:

    1. Type Coverage  — how many of the 18 types the team can hit
                        super-effectively or is immune to (0-100)
    2. Weakness Resistance — how many of the 18 types the team is NOT
                             collectively weak to (0-100)
    3. Average BST    — mean base stat total normalised to 0-100

    Combined score weighted: coverage 40%, weakness 40%, BST 20%

    Returns a dict with each component and the combined total.
    """
    ALL_TYPES = [t for t in TYPE_CHART.keys() if t != 'None']
    TOTAL_TYPES = len(ALL_TYPES)  # should be 18

    team_types = []
    for name in team:
        row = pk[pk['Name'] == name].iloc[0]
        team_types.append(row['Type 1'])
        if row['Type 2'] != 'None':
            team_types.append(row['Type 2'])

    covered_types = set()
    for t in team_types:
        chart = TYPE_CHART.get(t, {'strong_against': [], 'weak_against': [], 'immune_to': []})
        covered_types.update(chart['strong_against'])
        covered_types.update(chart['immune_to'])

    covered_types = covered_types & set(ALL_TYPES)
    coverage_score = (len(covered_types) / TOTAL_TYPES) * 100

    team_weaknesses = set()
    team_immunities = set()

    for t in team_types:
        chart = TYPE_CHART.get(t, {'strong_against': [], 'weak_against': [], 'immune_to': []})
        team_weaknesses.update(chart['weak_against'])
        team_immunities.update(chart['immune_to'])

    team_weaknesses -= team_immunities
    team_weaknesses = team_weaknesses & set(ALL_TYPES)
    weakness_resistance = ((TOTAL_TYPES - len(team_weaknesses)) / TOTAL_TYPES) * 100

    bst_values = [pk[pk['Name'] == name].iloc[0]['Total'] for name in team]
    avg_bst = sum(bst_values) / len(bst_values)
    bst_score = (avg_bst / 600) * 100

    combined = (coverage_score * 0.4) + (weakness_resistance * 0.4) + (bst_score * 0.2)

    return {
        'combined':            round(combined, 1),
        'coverage_score':      round(coverage_score, 1),
        'weakness_resistance': round(weakness_resistance, 1),
        'avg_bst':             round(avg_bst, 1),
        'bst_score':           round(bst_score, 1),
        'types_covered':       len(covered_types),
        'types_weak_to':       len(team_weaknesses),
        'total_types':         TOTAL_TYPES,
    }

def print_team(pk, team, mega_base=None, mega_row=None):

    """Pretty print the final team, highlighting the Mega Evolution."""
    print("\n===== Your Suggested Team =====")
    for i, name in enumerate(team, 1):
        row = pk[pk['Name'] == name].iloc[0]
        t2 = f" / {row['Type 2']}" if row['Type 2'] != 'None' else ''
        base_str = f"  {i}. {name:15s}  [{row['Type 1']}{t2}]  BST: {row['Total']}"

        if mega_base and name == mega_base:
            mega_t2 = f" / {mega_row['Type 2']}" if mega_row['Type 2'] != 'None' else ''
            mega_str = (
                f"  → MEGA: {mega_row['Name']:20s}"
                f"  [{mega_row['Type 1']}{mega_t2}]"
                f"  BST: {mega_row['Total']}"
            )
            print(base_str)
            print(mega_str)
        else:
            print(base_str)