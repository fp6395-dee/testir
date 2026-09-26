"""
board.py - logika igrovogo polya Ultimate Tic-Tac-Toe.

Pole 9x9 razbito na 9 pod-poley 3x3. Kazhdyy hod:
  - opredelyaet, v kakom pod-pole igrok obyazan igrat (po kletke vnutri pod-polya)
  - esli pod-pole uzhe vyigrano ili zapolneno, igrok mozhet hodit v lyuboe svobodnoe
  - posle hoda proveryaetsya, ne vyigrano li pod-pole, i ne zakonchilas li igra

Klass Board - chistaya logika, bez I/O.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

EMPTY = "."
X = "X"
O = "O"

BOARD_SIZE = 9       # obschiy razmer 9x9
SUB_SIZE = 3         # razmer pod-polya 3x3
SUB_COUNT = 3        # 3x3 pod-poley


Position = Tuple[int, int]        # (row, col) na bolshom pole, 0..8
SubIndex = Tuple[int, int]        # (sr, sc) indeks pod-polya, 0..2


def sub_of(pos: Position) -> SubIndex:
    """Kakomu pod-polyu prinadlezhit kletka."""
    r, c = pos
    return (r // SUB_SIZE, c // SUB_SIZE)


def pos_in_sub(sub: SubIndex, local: Tuple[int, int]) -> Position:
    """(pod-pole, lokalnye koord 0..2) -> koordinaty na bolshom pole."""
    sr, sc = sub
    lr, lc = local
    return (sr * SUB_SIZE + lr, sc * SUB_SIZE + lc)


def local_of(pos: Position) -> Tuple[int, int]:
    """Lokalnye koordinaty vnutri pod-polya (0..2, 0..2)."""
    r, c = pos
    return (r % SUB_SIZE, c % SUB_SIZE)


@dataclass
class Board:
    """
    Sostoyanie igrovyh kletok i pod-poley.

    cells[r][c] - 'X', 'O' ili '.'
    sub_winner[ sr ][ sc ] - 'X', 'O' ili None (pod-pole ne zakoncheno)
    """

    cells: List[List[str]] = field(
        default_factory=lambda: [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    )
    sub_winner: List[List[Optional[str]]] = field(
        default_factory=lambda: [[None] * SUB_COUNT for _ in range(SUB_COUNT)]
    )

    # ---------------------------------------------------------- helpers
    def in_bounds(self, pos: Position) -> bool:
        r, c = pos
        return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE

    def is_empty(self, pos: Position) -> bool:
        return self.in_bounds(pos) and self.cells[pos[0]][pos[1]] == EMPTY

    def sub_is_playable(self, sub: SubIndex) -> bool:
        """Pod-pole mozhno igrat, esli ono ne vyigrano i v nem est svobodnye kletki."""
        sr, sc = sub
        if self.sub_winner[sr][sc] is not None:
            return False
        for r in range(sr * SUB_SIZE, sr * SUB_SIZE + SUB_SIZE):
            for c in range(sc * SUB_SIZE, sc * SUB_SIZE + SUB_SIZE):
                if self.cells[r][c] == EMPTY:
                    return True
        return False

    def free_cells_in_sub(self, sub: SubIndex) -> List[Position]:
        sr, sc = sub
        result = []
        for r in range(sr * SUB_SIZE, sr * SUB_SIZE + SUB_SIZE):
            for c in range(sc * SUB_SIZE, sc * SUB_SIZE + SUB_SIZE):
                if self.cells[r][c] == EMPTY:
                    result.append((r, c))
        return result

    def any_free_cell(self) -> Optional[Position]:
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.cells[r][c] == EMPTY:
                    return (r, c)
        return None

    # ---------------------------------------------------------- moves
    def legal_moves(self, required_sub: Optional[SubIndex]) -> List[Position]:
        """
        Spisok dopustimyh hodov dlya tekuschego igroka.

        required_sub - pod-pole, v kotoroe obyazan igrat (mozhet byt None,
        togda lyuboe svobodnoe pod-pole).
        """
        # esli required_sub zadan i igraem v nego - tolko ego svobodnye kletki
        if required_sub is not None and self.sub_is_playable(required_sub):
            return self.free_cells_in_sub(required_sub)

        # inache - lyubye svobodnye kletki v lyubyh igrovyh pod-polyah
        moves: List[Position] = []
        for sr in range(SUB_COUNT):
            for sc in range(SUB_COUNT):
                if self.sub_is_playable((sr, sc)):
                    moves.extend(self.free_cells_in_sub((sr, sc)))
        return moves

    def apply(self, pos: Position, player: str) -> Optional[SubIndex]:
        """
        Postavit' znak igroka v pos. Vozvrashchaet pod-pole,
        v kotoroe obyazan hodit sleduyuschiy igrok (ili None).
        """
        if not self.is_empty(pos):
            raise ValueError(f"Kletka {pos} zanyata ili vne polya.")
        r, c = pos
        self.cells[r][c] = player

        sub = sub_of(pos)
        self._update_sub_winner(sub)

        local_r, local_c = local_of(pos)
        next_sub = (local_r, local_c)
        # esli sleduyuschee pod-pole nedostupno - svobodnyy vybor
        if not self.sub_is_playable(next_sub):
            return None
        return next_sub

    def _update_sub_winner(self, sub: SubIndex) -> None:
        sr, sc = sub
        if self.sub_winner[sr][sc] is not None:
            return
        winner = self._check_3x3_sub(sr, sc)
        if winner is not None:
            self.sub_winner[sr][sc] = winner

    def _check_3x3_sub(self, sr: int, sc: int) -> Optional[str]:
        # lokalnaya setka 3x3
        g = [
            [self.cells[sr * SUB_SIZE + i][sc * SUB_SIZE + j]
             for j in range(SUB_SIZE)]
            for i in range(SUB_SIZE)
        ]
        return _winner_of_3x3(g)

    # ---------------------------------------------------------- win check
    def overall_winner(self) -> Optional[str]:
        g = self.sub_winner
        # prevratim None v EMPTY
        grid = [
            [g[i][j] if g[i][j] is not None else EMPTY for j in range(SUB_COUNT)]
            for i in range(SUB_COUNT)
        ]
        return _winner_of_3x3(grid)

    def is_full(self) -> bool:
        return self.any_free_cell() is None

    def is_game_over(self) -> bool:
        return self.overall_winner() is not None or self.is_full()


def _winner_of_3x3(grid: List[List[str]]) -> Optional[str]:
    """Univeralnaya proverka pobeditelya na setke 3x3 (X, O ili None)."""
    lines = []
    for i in range(3):
        lines.append([grid[i][0], grid[i][1], grid[i][2]])
        lines.append([grid[0][i], grid[1][i], grid[2][i]])
    lines.append([grid[0][0], grid[1][1], grid[2][2]])
    lines.append([grid[0][2], grid[1][1], grid[2][0]])

    for a, b, c in lines:
        if a != EMPTY and a == b == c:
            return a
    return None
