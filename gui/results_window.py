from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QPushButton, QScrollArea
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap

from core.team_builder import evaluate_team
from gui.sprites import fetch_sprite, fetch_location


# ── Background worker for API calls ──────────────────────────────────────────
# Fetches sprites and locations off the main thread so the GUI doesn't freeze

class FetchWorker(QThread):
    """Worker thread that fetches sprite and location for one Pokemon."""
    result_ready = pyqtSignal(int, QPixmap, str)   # (card_index, pixmap, location)

    def __init__(self, index, pokemon_name, base_form_name, region):
        super().__init__()
        self.index = index
        self.pokemon_name = pokemon_name
        self.base_form_name = base_form_name
        self.region = region

    def run(self):
        pixmap = fetch_sprite(self.pokemon_name)
        location = fetch_location(self.base_form_name, self.region)
        self.result_ready.emit(self.index, pixmap or QPixmap(), location)


# ── Pokemon card widget ───────────────────────────────────────────────────────

class PokemonCard(QFrame):
    """A single card displaying one Pokemon's sprite, name, types, BST and location."""

    TYPE_COLORS = {
        'Fire':     '#F08030', 'Water':    '#6890F0', 'Grass':    '#78C850',
        'Electric': '#F8D030', 'Ice':      '#98D8D8', 'Fighting': '#C03028',
        'Poison':   '#A040A0', 'Ground':   '#E0C068', 'Flying':   '#A890F0',
        'Psychic':  '#F85888', 'Bug':      '#A8B820', 'Rock':     '#B8A038',
        'Ghost':    '#705898', 'Dragon':   '#7038F8', 'Dark':     '#705848',
        'Steel':    '#B8B8D0', 'Fairy':    '#EE99AC', 'Normal':   '#A8A878',
    }

    def __init__(self, name, type1, type2, bst, is_mega_candidate=False, mega_row=None):
        super().__init__()
        self.name = name
        self.is_mega_candidate = is_mega_candidate
        self.mega_row = mega_row

        self._build_ui(name, type1, type2, bst)

    def _build_ui(self, name, type1, type2, bst):
        self.setMinimumSize(200, 320)
        self.setMaximumWidth(220)
        self.setFrameShape(QFrame.Shape.Box)

        if self.is_mega_candidate:
            self.setStyleSheet("""
                QFrame {
                    border: 3px solid #FFD700;
                    border-radius: 10px;
                    background-color: #1e1e2e;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    border: 1px solid #444;
                    border-radius: 10px;
                    background-color: #1e1e2e;
                }
            """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(6)
        layout.setContentsMargins(10, 10, 10, 10)

        # Sprite placeholder — gets filled by worker thread
        self.sprite_label = QLabel("Loading...")
        self.sprite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sprite_label.setFixedSize(120, 120)
        self.sprite_label.setStyleSheet("color: #888; font-size: 11px; border: none;")
        layout.addWidget(self.sprite_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Pokemon name
        name_label = QLabel(name)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        name_label.setStyleSheet("color: #ffffff; border: none;")
        layout.addWidget(name_label)

        # Base type badges
        layout.addLayout(self._type_badges(type1, type2))

        # Base BST
        bst_label = QLabel(f"BST: {bst}")
        bst_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bst_label.setStyleSheet("color: #aaaaaa; font-size: 10px; border: none;")
        layout.addWidget(bst_label)

        # ── Mega section ─────────────────────────────────────────────────────
        if self.is_mega_candidate and self.mega_row is not None:
            # Divider
            divider = QLabel("──────────────")
            divider.setAlignment(Qt.AlignmentFlag.AlignCenter)
            divider.setStyleSheet("color: #FFD700; font-size: 8px; border: none;")
            layout.addWidget(divider)

            # Mega name
            mega_display = self.mega_row['Name'].replace(name, '', 1).strip()
            mega_name_label = QLabel(f"★ {mega_display}")
            mega_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            mega_name_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            mega_name_label.setStyleSheet("color: #FFD700; border: none;")
            layout.addWidget(mega_name_label)

            # Only show Mega type badges if the type actually changes
            base_types = {type1, type2 or 'None'}
            mega_t1 = self.mega_row['Type 1']
            mega_t2 = self.mega_row['Type 2'] if self.mega_row['Type 2'] != 'None' else None
            mega_types = {mega_t1, mega_t2 or 'None'}

            if mega_types != base_types:
                type_change_label = QLabel("Type changes to:")
                type_change_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                type_change_label.setStyleSheet("color: #aaaaaa; font-size: 9px; border: none;")
                layout.addWidget(type_change_label)
                layout.addLayout(self._type_badges(mega_t1, mega_t2))

            # BST with gain shown
            bst_gain = self.mega_row['Total'] - bst
            mega_bst_label = QLabel(f"BST: {self.mega_row['Total']}  (+{bst_gain})")
            mega_bst_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            mega_bst_label.setStyleSheet("color: #FFD700; font-size: 10px; border: none;")
            layout.addWidget(mega_bst_label)

        # Location placeholder — gets filled by worker thread
        self.location_label = QLabel("Fetching location...")
        self.location_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.location_label.setWordWrap(True)
        self.location_label.setStyleSheet("color: #88cc88; font-size: 9px; border: none;")
        layout.addWidget(self.location_label)

    def _type_badges(self, type1, type2):
        """Build a horizontal layout of type badges."""
        type_layout = QHBoxLayout()
        type_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        type_layout.setSpacing(4)

        for t in [type1, type2]:
            if t and t != 'None':
                badge = QLabel(t)
                badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
                color = self.TYPE_COLORS.get(t, '#888888')
                badge.setStyleSheet(f"""
                    background-color: {color};
                    color: white;
                    border-radius: 4px;
                    padding: 2px 6px;
                    font-size: 10px;
                    font-weight: bold;
                    border: none;
                """)
                type_layout.addWidget(badge)

        return type_layout

    def set_sprite(self, pixmap):
        """Set the sprite image once fetched."""
        if pixmap and not pixmap.isNull():
            self.sprite_label.setPixmap(pixmap)
            self.sprite_label.setText('')
        else:
            self.sprite_label.setText("No sprite")

    def set_location(self, location):
        """Set the catch location once fetched."""
        self.location_label.setText(f"📍 {location}")


# ── Results window ────────────────────────────────────────────────────────────

class ResultsWindow(QWidget):
    """Window 2 — displays the recommended team in a 2x3 grid."""

    def __init__(self, pk, team, mega_base, mega_row, region, evolution_families, input_window):
        super().__init__()
        self.pk = pk
        self.team = team
        self.mega_base = mega_base
        self.mega_row = mega_row
        self.region = region
        self.evolution_families = evolution_families
        self.input_window = input_window
        self.workers = []
        self.cards = []
        self.evaluation = evaluate_team(pk, team)

        self.setWindowTitle("Your Recommended Team")
        self.setMinimumSize(520, 800)
        self.setStyleSheet("background-color: #13131f;")

        self._build_ui()
        self._start_fetching()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        # Title
        title = QLabel("Your Recommended Team")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #ffffff;")
        main_layout.addWidget(title)

        # Region label
        region_label = QLabel(f"Region: {self.region}")
        region_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        region_label.setStyleSheet("color: #aaaaaa; font-size: 12px;")
        main_layout.addWidget(region_label)

        # ── Evaluation score panel ────────────────────────────────────────────
        score_frame = QFrame()
        score_frame.setStyleSheet("""
            QFrame {
                background-color: #1e1e2e;
                border: 1px solid #444;
                border-radius: 8px;
            }
        """)
        score_layout = QVBoxLayout(score_frame)
        score_layout.setContentsMargins(16, 10, 16, 10)
        score_layout.setSpacing(6)

        # Combined score
        e = self.evaluation
        combined_label = QLabel(f"Team Score: {e['combined']}/100")
        combined_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        combined_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        combined_label.setStyleSheet("color: #ffffff; border: none;")
        score_layout.addWidget(combined_label)

        # Breakdown row
        breakdown = QHBoxLayout()
        breakdown.setSpacing(20)

        for label, value in [
            (f"Type Coverage", f"{e['types_covered']}/{e['total_types']}  ({e['coverage_score']}%)"),
            (f"Weakness Resistance", f"{e['weakness_resistance']}%  ({e['types_weak_to']} weak)"),
            (f"Avg BST", f"{e['avg_bst']}"),
        ]:
            item_layout = QVBoxLayout()
            item_layout.setSpacing(2)

            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("color: #aaaaaa; font-size: 10px; border: none;")

            val = QLabel(value)
            val.setAlignment(Qt.AlignmentFlag.AlignCenter)
            val.setStyleSheet("color: #88cc88; font-size: 11px; font-weight: bold; border: none;")

            item_layout.addWidget(lbl)
            item_layout.addWidget(val)
            breakdown.addLayout(item_layout)

        score_layout.addLayout(breakdown)
        main_layout.addWidget(score_frame)

        # 2x3 grid of cards wrapped in a scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #13131f;
            }
            QScrollBar:vertical {
                background: #1e1e2e;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #4a4a8a;
                border-radius: 4px;
            }
        """)

        grid_container = QWidget()
        grid_container.setStyleSheet("background-color: #13131f;")
        grid = QGridLayout(grid_container)
        grid.setSpacing(16)
        grid.setContentsMargins(16, 16, 16, 16)
        grid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for i, name in enumerate(self.team):
            row_data = self.pk[self.pk['Name'] == name].iloc[0]
            type1 = row_data['Type 1']
            type2 = row_data['Type 2'] if row_data['Type 2'] != 'None' else None
            bst = row_data['Total']
            is_mega = (name == self.mega_base)

            card = PokemonCard(
                name, type1, type2, bst,
                is_mega_candidate=is_mega,
                mega_row=self.mega_row if is_mega else None
            )
            self.cards.append(card)

            row = i // 2
            col = i % 2
            grid.addWidget(card, row, col, alignment=Qt.AlignmentFlag.AlignCenter)

        scroll.setWidget(grid_container)
        main_layout.addWidget(scroll)

        # Back button
        back_btn = QPushButton("Build Another Team")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a4a8a;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #6a6aaa;
            }
        """)
        back_btn.clicked.connect(self._go_back)
        main_layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def _go_back(self):
        """Hide results window and bring input window back to focus."""
        self.close()
        self.input_window.build_btn.setEnabled(True)
        self.input_window.build_btn.setText("Build Team →")
        self.input_window.show()
        self.input_window.raise_()
        self.input_window.activateWindow()

    def _start_fetching(self):
        """Spawn a worker thread per Pokemon to fetch sprites and locations."""
        for i, name in enumerate(self.team):
            # Get base form for location lookup
            base_form = self.evolution_families.get(name, name)

            worker = FetchWorker(i, name, base_form, self.region)
            worker.result_ready.connect(self._on_fetch_done)
            self.workers.append(worker)
            worker.start()

    def _on_fetch_done(self, index, pixmap, location):
        """Called when a worker thread finishes — updates the card."""
        if index < len(self.cards):
            self.cards[index].set_sprite(pixmap)
            self.cards[index].set_location(location)