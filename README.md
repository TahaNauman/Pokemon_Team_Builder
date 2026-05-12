# Pokemon Team Builder

A PyQt6 desktop application that builds an optimal 6-Pokemon team for any region playthrough through Gen 1–7. Given a region and starter, it selects the 5 best complementary Pokemon using intelligent type-coverage scoring, then displays the team with live sprites, catch locations, and a quality score.

## Features

- **7 Regions** — Kanto through Kalos (Gen 1–6) with per-region game version mapping
- **Starter-Aware** — Blocks evolution families of all starter Pokemon for a diverse team
- **Weakness Coverage** — Scores candidates by immunities (+5) and resistances (+3) to the starter's weaknesses
- **Gym + Elite Four Optimization** — Prioritizes Pokemon that shore up defense against every Gym Leader, Elite Four member, and Champion
- **Evolution Family Blocking** — No two Pokemon from the same evolutionary line
- **Form Variant Handling** — Maps alternate forms (Rotom, Aegislash, Lycanroc, etc.) to their base to prevent duplicates
- **Mega Evolution Suggestion** — Recommends the best Mega candidate (Kalos/Alola only) based on BST gain and type coverage improvement
- **Trade Evolution Exclusion** — Skips 30 trade-dependent Pokemon for practical teams
- **No Legendaries** — Only obtainable, mainstream picks
- **Polished PyQt6 GUI** — Dark-themed desktop app with region/starter selection and team results
- **Pokemon Card UI** — 200x320 cards showing sprite, type badges (color-coded), BST, Mega info, and catch location
- **Live Sprite Fetching** — Async PokéAPI sprite and encounter-location lookups via QThread (no freezing)
- **Team Quality Evaluation** — Post-build score out of 100 (40% coverage + 40% resistance + 20% BST)
- **Varied Results** — Picks randomly from the top 2 scorers each iteration, so reruns produce different but sound teams
- **"Build Another Team"** — Returns to the selection screen without restarting

## How It Works

```
User picks region + starter
        │
        ▼
Load Pokemon dataset (Gen 1–7) & evolution families
        │
        ▼
Filter: no legendaries, no trade evos, no form dupes, block starter families
        │
        ▼
Score each candidate by:
  • +5 per immunity to starter weakness
  • +3 per resistance to starter weakness
  • +1/+2 per gym type resistance/immunity
  • +2/+3 per Elite Four type resistance/immunity
  • -1 per redundant type on existing team
  • -2 per shared weakness with existing team
  • BST/600 as tiebreaker
        │
        ▼
Pick top-2 scorers → random selection → repeat for team of 6
        │
        ▼
Recommend best Mega Evolution (Kalos/Alola only)
        │
        ▼
Evaluate team: coverage + resistance + BST → score out of 100
        │
        ▼
Display cards with live sprites, type badges, locations
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Requirements

- Python 3.13+
- pandas — CSV data loading
- requests — PokéAPI HTTP calls
- Pillow — image processing
- PyQt6 — desktop GUI framework

## Data Source

Pokemon data and encounter locations are fetched live from [PokéAPI](https://pokeapi.co/) (no API key required). Local CSV files provide the core dataset (`Pokemon.csv`) and evolution family mappings (`evolution_families.csv`).

## Project Structure

```
├── main.py                 # Entry point — launches the PyQt6 GUI
├── core/                   # Backend logic
│   ├── gym_leaders.py      # Gym Leader + Elite Four data (7 regions)
│   ├── loader.py           # CSV loading, starter data
│   ├── team_builder.py     # Scoring, team building, Mega selection, evaluation
│   └── type_chart.py       # Complete 18-type matchup chart
├── gui/                    # PyQt6 frontend
│   ├── app.py              # QApplication setup and data loading
│   ├── input_window.py     # Region/starter selection window
│   ├── results_window.py   # Team results with Pokemon cards
│   └── sprites.py          # PokéAPI sprite + encounter-location fetching
├── data/
│   ├── Pokemon.csv         # 801 Pokemon (Gen 1–6) with stats, types, flags
│   └── evolution_families.csv  # 727 evolution family mappings
├── requirements.txt
└── LICENSE
```
