import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from core.loader import load_data
from gui.input_window import InputWindow


def run():
    """Launch the Pokemon Team Builder application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Pokémon Team Builder")
    app.setStyle("Fusion")

    # Load data once at startup — shared across both windows
    pk, pk_megas, evolution_families = load_data(
        pokemon_path="data/Pokemon.csv",
        evo_path="data/evolution_families.csv"
    )

    window = InputWindow(pk, pk_megas, evolution_families)
    window.show()

    sys.exit(app.exec())