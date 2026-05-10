# Pokemon Team Builder

Build an optimal 6-Pokemon team for any Pokemon region playthrough. Given a region and a starter, the tool picks the 5 best complementary Pokemon based on type coverage, gym matchups, and intelligent scoring.

## Features

- **7 Regions** — Kanto through Alola (Gen 1–7)
- **Starter-Aware** — Blocks evolution families of all starter Pokemon so your team stays diverse
- **Weakness Coverage** — Scores candidates by how well they cover the starter's weaknesses (immunities +5, resistances +3)
- **Gym Optimization** — Prioritizes Pokemon that resist or are immune to the region's gym types
- **Evolution Family Blocking** — No two Pokemon from the same evolution line on your team
- **Mega Evolution Suggestion** — Recommends the best Mega candidate based on BST gain and type coverage improvement
- **Varied Results** — Randomly picks from top-3 scorers each iteration, so reruns produce different sound teams
- **No Legendaries, Trade Evolutions, or Duplicate Forms** — Only practical, obtainable picks

## How It Works

```
User picks region + starter
        │
        ▼
Load Pokemon dataset (Gen 1-7) & evolution families
        │
        ▼
Filter: no legendaries, no trade evos, no form dupes
        │
        ▼
Score each candidate by:
  • +5 per immunity to starter weakness
  • +3 per resistance to starter weakness
  • +1/+2 per gym type resistance/immunity
  • -1 per redundant type on existing team
  • -2 per shared weakness with existing team
  • BST/600 as tiebreaker
        │
        ▼
Pick top-3 scorers → random selection → repeat for team of 6
        │
        ▼
Recommend best Mega Evolution from the team
        │
        ▼
Print final team with types, BST, and Mega arrow
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the team builder
python main.py
```


## Project Structure

```
├── main.py                 # Entry point — CLI orchestrator
├── core/
│   ├── gym_leaders.py      # Gym leader data for all 7 regions
│   ├── loader.py           # CSV loading, region/starter selection prompts
│   ├── team_builder.py     # Team building algorithm, scoring, Mega selection
│   └── type_chart.py       # Complete 18-type matchup chart
├── data/
│   ├── Pokemon.csv         # 801 Pokemon (Gen 1-7) with stats, types, flags
│   └── evolution_families.csv  # Evolution family mappings
├── requirements.txt
└── LICENSE
```

