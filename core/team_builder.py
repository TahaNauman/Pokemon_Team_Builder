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
    'Aegislash-Blade':   'Aegislash',
    'Aegislash-Shield':  'Aegislash',
    'Wormadam-Plant':    'Wormadam',
    'Wormadam-Sandy':    'Wormadam',
    'Wormadam-Trash':    'Wormadam',
    'Lycanroc-Midday':   'Lycanroc',
    'Lycanroc-Midnight': 'Lycanroc',
    'Lycanroc-Dusk':     'Lycanroc',
    'Oricorio-Baile':    'Oricorio',
    'Oricorio-Pom-Pom':  'Oricorio',
    'Oricorio-Pau':      'Oricorio',
    'Oricorio-Sensu':    'Oricorio',
    'Gastrodon-East':    'Gastrodon',
    'Gastrodon-West':    'Gastrodon',
    'Rotom-Heat':        'Rotom',
    'Rotom-Wash':        'Rotom',
    'Rotom-Frost':       'Rotom',
    'Rotom-Fan':         'Rotom',
    'Rotom-Mow':         'Rotom',
    'Meowstic-Male':     'Meowstic',
    'Meowstic-Female':   'Meowstic',
    'Wishiwashi-Solo':   'Wishiwashi',
    'Wishiwashi-School': 'Wishiwashi',
    'Minior-Meteor':     'Minior',
    'Minior-Core':       'Minior',
}


def get_family(name, evolution_families):
    """Return the evolution family root for a given Pokemon name."""
    # First resolve any form variant to its base name
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


def score_candidate(row, covered_weaknesses, team_types, gym_types=None):
    """
    Score a candidate Pokemon for team fit.

    Weakness coverage (primary):
    +5  for each team weakness this Pokemon is immune to
    +3  for each team weakness this Pokemon is strong against
    -2  for each of its own weaknesses that overlap with team's existing weaknesses
    -1  for each type already on the team (discourages redundancy)

    Gym coverage (secondary — reduced weight to prevent gym types
    dominating and producing the same team every run):
    +1  for each gym leader type this Pokemon is strong against
    +2  for each gym leader type this Pokemon is immune to

    +BST/600 as a tiebreaker
    """
    if gym_types is None:
        gym_types = []

    c_types = [row['Type 1']]
    if row['Type 2'] != 'None':
        c_types.append(row['Type 2'])

    score = 0
    candidate_weaknesses = []

    for c_type in c_types:
        chart = TYPE_CHART.get(c_type, {'strong_against': [], 'weak_against': [], 'immune_to': []})

        # ── Weakness coverage (primary driver) ───────────────────────────────
        for w in covered_weaknesses:
            if w in chart['strong_against']:
                score += 3
            elif w in chart['immune_to']:
                score += 5

        # ── Gym coverage (secondary, reduced to +1/+2) ───────────────────────
        for g in gym_types:
            if g in chart['strong_against']:
                score += 1
            elif g in chart['immune_to']:
                score += 2

        candidate_weaknesses.extend(chart['weak_against'])

        # Penalty scales with how many of this type are already on the team
        # -1 for first duplicate, -2 for second, -3 for third, etc.
        type_count = team_types.count(c_type)
        if type_count > 0:
            score -= 1 * type_count

    for w in candidate_weaknesses:
        if w in covered_weaknesses:
            score -= 2

    # Tiebreaker: prefer higher base stat total
    total_stats = row.get('Total', 0)
    score += total_stats / 600

    return score


def build_team(pk, pk_region, final_form, types, weaknesses, evolution_families, gym_types=None, unchosen_starters=None):
    """
    Build a team of 6 Pokemon based on type coverage and gym leader coverage.

    Excludes:
    - Legendaries
    - Unchosen starter lines
    - Trade-only evolutions
    - Duplicate form variants (e.g. both Aegislash-Blade and Aegislash-Shield)

    Issue 2 fix: randomly picks from the top 3 scoring candidates each
    iteration so reruns produce varied teams while still being type-sound.

    Returns the final team as a list of Pokemon names.
    """
    if gym_types is None:
        gym_types = []
    if unchosen_starters is None:
        unchosen_starters = []

    # Build the set of families to block — chosen starter + unchosen starters
    blocked_families = {get_family(final_form, evolution_families)}
    for s in unchosen_starters:
        blocked_families.add(get_family(s, evolution_families))

    # Filter candidates upfront:
    # - No legendaries
    # - No blocked starter families
    # - No trade evolutions
    # - No duplicate form variants (keep only the first occurrence per form group)
    seen_forms = set()
    valid_indices = []

    for idx, row in pk_region.iterrows():
        name = row['Name']
        form_key = FORM_VARIANTS.get(name, name)   # collapse forms to base name

        if row['Legendary']:
            continue
        if get_family(name, evolution_families) in blocked_families:
            continue
        if name in TRADE_EVOLUTIONS:
            continue
        if form_key in seen_forms:
            continue

        seen_forms.add(form_key)
        valid_indices.append(idx)

    candidates = pk_region.loc[valid_indices].copy()

    team = [final_form]
    team_types = types.copy()
    used_families = {get_family(final_form, evolution_families)}
    covered_weaknesses = set(weaknesses)

    while len(team) < 6:
        scored = []

        for idx, row in candidates.iterrows():
            name = row['Name']

            if get_family(name, evolution_families) in used_families:
                continue

            s = score_candidate(row, covered_weaknesses, team_types, gym_types)
            scored.append((s, name))

        if not scored:
            print("Not enough eligible Pokemon to fill the team.")
            break

        # Sort by score descending and randomly pick from the top 3
        # This preserves type-coverage quality while adding variety across reruns
        scored.sort(key=lambda x: x[0], reverse=True)
        top_n = scored[:3]
        _, best_pokemon = random.choice(top_n)

        # Add to team
        team.append(best_pokemon)
        used_families.add(get_family(best_pokemon, evolution_families))

        new_row = pk[pk['Name'] == best_pokemon].iloc[0]
        new_types = [new_row['Type 1']]
        if new_row['Type 2'] != 'None':
            new_types.append(new_row['Type 2'])
        team_types.extend(new_types)

        # Update covered weaknesses
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
    - BST gain normalised to a 0-1 range across all candidates  (+0 to +5)
    - Type coverage improvement: +3 per team weakness the Mega's
      new types cover that the base form didn't, +5 per immunity gained

    Returns (base_name, mega_row) or (None, None) if no Megas available.
    """

    # Build a lookup: base Pokemon name → its Mega row(s)
    # Dataset has names like "Mega Venusaur", "Mega Charizard X", etc.
    # We match by checking if the base name appears in the Mega name.
    eligible = []   # list of (base_name, mega_row, bst_gain, coverage_gain)

    for name in team:
        # Find all Megas whose name contains this Pokemon's name
        matches = pk_megas[pk_megas['Name'].str.contains(name, case=False)]
        if matches.empty:
            continue

        base_row = pk[pk['Name'] == name].iloc[0]
        base_bst = base_row['Total']
        base_types = {base_row['Type 1'], base_row['Type 2']} - {'None'}

        for _, mega_row in matches.iterrows():
            mega_bst = mega_row['Total']
            bst_gain = mega_bst - base_bst

            # Calculate type coverage improvement
            mega_types = {mega_row['Type 1'], mega_row['Type 2']} - {'None'}
            new_types = mega_types - base_types   # types gained by Mega evolving

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

    # Normalise BST gain across all candidates to 0-5 range
    max_bst_gain = max(e[2] for e in eligible) or 1
    scored = []
    for base_name, mega_row, bst_gain, coverage_gain in eligible:
        bst_score = (bst_gain / max_bst_gain) * 5
        total_score = bst_score + coverage_gain
        scored.append((total_score, base_name, mega_row))

    scored.sort(key=lambda x: x[0], reverse=True)
    _, best_base, best_mega = scored[0]

    return best_base, best_mega


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