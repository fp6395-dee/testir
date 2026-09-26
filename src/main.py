"""
main.py - konsolnyy interfeys Ultimate Tic-Tac-Toe.

Zapusk:
    python -m src.main

Upravlenie:
    Koordinaty kletki vvodim kak 'r c' (0..8), naprimer: 4 4
    'q' - vyhod, 'r' - perezapustit partiyu.
"""

from __future__ import annotations

import sys

from .board import Board, SUB_SIZE, SUB_COUNT, EMPTY, X, O
from .game import Game


def render(board: Board) -> str:
    """
    Pechataet 9x9 s ramkami mezhdu pod-polyami i nomerami strok/stolbcov.
    """
    lines = []
    header = "    " + " ".join(str(c) for c in range(9))
    lines.append(header)
    for r in range(9):
        if r % SUB_SIZE == 0 and r != 0:
            lines.append("   " + "-" * (2 * 9 + SUB_COUNT))
        row_cells = []
        for c in range(9):
            if c % SUB_SIZE == 0 and c != 0:
                row_cells.append("|")
            row_cells.append(board.cells[r][c])
        lines.append(f"{r:2d}  " + " ".join(row_cells))
    # pod-polevyy itog
    lines.append("")
    lines.append("Pobediteli pod-poley:")
    for sr in range(SUB_COUNT):
        row = []
        for sc in range(SUB_COUNT):
            w = board.sub_winner[sr][sc] or "."
            row.append(w)
        lines.append("   " + " ".join(row))
    return "\n".join(lines)


def ask_move(game: Game) -> str:
    req = game.required_sub
    if req is None:
        prompt = f"({game.current}) svobodnyy vybor, koordinaty r c: "
    else:
        prompt = f"({game.current}) pod-pole {req}, koordinaty r c: "
    return input(prompt).strip()


def parse_move(text: str):
    parts = text.replace(",", " ").split()
    if len(parts) != 2:
        return None
    try:
        r, c = int(parts[0]), int(parts[1])
    except ValueError:
        return None
    return (r, c)


def main() -> int:
    game = Game()
    print("Ultimate Tic-Tac-Toe")
    print("Koordinaty: 'r c' (0..8). 'q' - vyhod, 'r' - restart.")
    print()

    while True:
        print(render(game.board))
        print()
        if game.is_over():
            w = game.winner()
            if w:
                print(f"Pobeda: {w}")
            else:
                print("Nichia.")
            print()
            ans = input("Enter - novaya partiya, q - vyhod: ").strip().lower()
            if ans == "q":
                return 0
            game.reset()
            continue

        raw = ask_move(game)
        if raw.lower() == "q":
            return 0
        if raw.lower() == "r":
            game.reset()
            continue
        pos = parse_move(raw)
        if pos is None:
            print("Neponyatno. Vvedi dva chisla 0..8 cherez probel.")
            continue
        try:
            game.play(pos)
        except ValueError as e:
            print(f"Oshibka: {e}")
        print()


if __name__ == "__main__":
    sys.exit(main())
