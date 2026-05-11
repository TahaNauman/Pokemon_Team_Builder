from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QPushButton, QTextEdit, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from core.loader import ALL_STARTERS, FINAL_EVOLUTIONS
from core.gym_leaders import (
    GYM_LEADERS, ELITE_FOUR,
    get_gym_types, get_elite_four_types
)
from core.team_builder import get_starter_weaknesses, build_team, select_mega
from gui.results_window import ResultsWindow


MEGA_REGIONS = {'Kalos', 'Alola'}


class InputWindow(QWidget):
    """Window 1 — region and starter selection."""

    def __init__(self, pk, pk_megas, evolution_families):
        super().__init__()
        self.pk = pk
        self.pk_megas = pk_megas
        self.evolution_families = evolution_families
        self.results_window = None

        self.setWindowTitle("Pokémon Team Builder")
        self.setMinimumSize(700, 600)
        self.setStyleSheet("background-color: #13131f;")

        self._build_ui()

    def _build_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # ── Left panel: inputs ────────────────────────────────────────────────
        left_panel = QVBoxLayout()
        left_panel.setSpacing(16)

        # Title
        title = QLabel("Pokémon Team Builder")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #ffffff;")
        left_panel.addWidget(title)

        subtitle = QLabel("Select your region and starter to get a recommended team.")
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("color: #aaaaaa; font-size: 12px;")
        left_panel.addWidget(subtitle)

        left_panel.addSpacing(10)

        # Region label + dropdown
        region_label = QLabel("Region")
        region_label.setStyleSheet("color: #cccccc; font-size: 13px; font-weight: bold;")
        left_panel.addWidget(region_label)

        self.region_combo = QComboBox()
        self.region_combo.addItems([
            'Kanto', 'Johto', 'Hoenn', 'Sinnoh',
            'Unova', 'Kalos', 'Alola'
        ])
        self.region_combo.setStyleSheet(self._combo_style())
        self.region_combo.currentTextChanged.connect(self._on_region_changed)
        left_panel.addWidget(self.region_combo)

        left_panel.addSpacing(8)

        # Starter label + dropdown
        starter_label = QLabel("Starter Pokémon")
        starter_label.setStyleSheet("color: #cccccc; font-size: 13px; font-weight: bold;")
        left_panel.addWidget(starter_label)

        self.starter_combo = QComboBox()
        self.starter_combo.setStyleSheet(self._combo_style())
        left_panel.addWidget(self.starter_combo)

        left_panel.addSpacing(16)

        # Build Team button
        self.build_btn = QPushButton("Build Team →")
        self.build_btn.setStyleSheet("""
            QPushButton {
                background-color: #e63946;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff4f5e;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #888;
            }
        """)
        self.build_btn.clicked.connect(self._on_build_clicked)
        left_panel.addWidget(self.build_btn)

        left_panel.addStretch()

        # ── Right panel: gym + elite four info ───────────────────────────────
        right_panel = QVBoxLayout()
        right_panel.setSpacing(8)

        info_title = QLabel("Trainers to Beat")
        info_title.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        info_title.setStyleSheet("color: #ffffff;")
        right_panel.addWidget(info_title)

        self.info_box = QTextEdit()
        self.info_box.setReadOnly(True)
        self.info_box.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e2e;
                color: #cccccc;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 10px;
                font-size: 11px;
            }
        """)
        right_panel.addWidget(self.info_box)

        # ── Combine panels ────────────────────────────────────────────────────
        main_layout.addLayout(left_panel, stretch=1)

        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.VLine)
        divider.setStyleSheet("color: #444;")
        main_layout.addWidget(divider)

        main_layout.addLayout(right_panel, stretch=1)

        # Trigger initial population
        self._on_region_changed(self.region_combo.currentText())

    def _on_region_changed(self, region):
        """Update starter dropdown and info panel when region changes."""
        # Update starters
        self.starter_combo.clear()
        self.starter_combo.addItems(ALL_STARTERS.get(region, []))

        # Update info panel
        lines = []

        lines.append("── Gym Leaders ──")
        for leader in GYM_LEADERS.get(region, []):
            types_str = ' / '.join(leader['types'])
            lines.append(f"  {leader['name']:20s} [{types_str}]")

        lines.append("")
        lines.append("── Elite Four & Champion ──")
        for member in ELITE_FOUR.get(region, []):
            types_str = ' / '.join(member['types'])
            lines.append(f"  {member['name']:25s} [{types_str}]")

        self.info_box.setText('\n'.join(lines))

    def _on_build_clicked(self):
        """Run the team builder and open the results window."""
        region = self.region_combo.currentText()
        starter = self.starter_combo.currentText()

        if not region or not starter:
            return

        self.build_btn.setEnabled(False)
        self.build_btn.setText("Building...")

        gen_map = {
            'Kanto': 1, 'Johto': 2, 'Hoenn': 3, 'Sinnoh': 4,
            'Unova': 5, 'Kalos': 6, 'Alola': 7
        }
        gen_no = gen_map[region]
        pk_region = self.pk[self.pk['Generation'] == gen_no]

        final_form = FINAL_EVOLUTIONS[starter]
        unchosen = [s for s in ALL_STARTERS[region] if s != starter]

        types, weaknesses = get_starter_weaknesses(self.pk, final_form)
        gym_types = get_gym_types(region)
        elite_four_types = get_elite_four_types(region)

        team = build_team(
            self.pk, pk_region, final_form, types, weaknesses,
            self.evolution_families, gym_types, unchosen, elite_four_types
        )

        if region in MEGA_REGIONS:
            mega_base, mega_row = select_mega(self.pk, self.pk_megas, team, weaknesses)
        else:
            mega_base, mega_row = None, None

        self.results_window = ResultsWindow(
            self.pk, team, mega_base, mega_row,
            region, self.evolution_families, self
        )
        self.hide()
        self.results_window.show()

    def _combo_style(self):
        return """
            QComboBox {
                background-color: #1e1e2e;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QComboBox:hover {
                border: 1px solid #6a6aaa;
            }
            QComboBox QAbstractItemView {
                background-color: #1e1e2e;
                color: #ffffff;
                selection-background-color: #4a4a8a;
            }
        """