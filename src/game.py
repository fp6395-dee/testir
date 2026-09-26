"""
game.py - igrovoy cikl Ultimate Tic-Tac-Toe bez I/O.

Klass Game upravlyaet ocherednostyu, validaciey hodov i sostoyaniem.
Interfeys (console/GUI) rabotaet cherez metody Game.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .board import Board, X, O, Position, SubIndex


@dataclass
class Game:
    board: Board = field(default_factory=Board)
    current: str = X                 # chey hod
    required_sub: Optional[SubIndex] = None
    history: List[Position] = field(default_factory=list)

    def legal_moves(self) -> List[Position]:
        return self.board.legal_moves(self.required_sub)

    def is_over(self) -> bool:
        return self.board.is_game_over()

    def winner(self) -> Optional[str]:
        return self.board.overall_winner()

    def play(self, pos: Position) -> None:
        """Sdelat hod. Brosaet ValueError, esli hod nedopustim."""
        if self.is_over():
            raise ValueError("Igra uzhe zakonchena.")
        if pos not in self.legal_moves():
            raise ValueError(f"Nedopustimyy hod: {pos}.")
        self.required_sub = self.board.apply(pos, self.current)
        self.history.append(pos)
        self.current = O if self.current == X else X

    def reset(self) -> None:
        self.board = Board()
        self.current = X
        self.required_sub = None
        self.history.clear()
