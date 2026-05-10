from core.loader import load_data, select_region, select_starter
from core.team_builder import get_starter_weaknesses, build_team, select_mega, print_team
from core.gym_leaders import get_gym_types, print_gym_leaders


def main():
    pk, pk_megas, evolution_families = load_data(
        pokemon_path="data/Pokemon.csv",
        evo_path="data/evolution_families.csv"
    )

    region, gen_no = select_region()
    pk_region = pk[pk['Generation'] == gen_no]

    if pk_region.empty:
        print("No Pokemon found for this region.")
        return

    print_gym_leaders(region)
    gym_types = get_gym_types(region)
    print(f"Gym types to cover: {gym_types}")

    starter, final_form, unchosen_starters = select_starter(region)

    types, weaknesses = get_starter_weaknesses(pk, final_form)
    print(f"\nStarter types:       {types}")
    print(f"Weaknesses to cover: {weaknesses}")

    team = build_team(pk, pk_region, final_form, types, weaknesses, evolution_families, gym_types, unchosen_starters)

    mega_base, mega_row = select_mega(pk, pk_megas, team, weaknesses)

    print_team(pk, team, mega_base, mega_row)


if __name__ == "__main__":
    main()