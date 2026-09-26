"""Ultimate Tic-Tac-Toe GUI с улучшенным AI."""
import tkinter as tk
from dataclasses import dataclass, field
from typing import Optional, List, Tuple
import time

EMPTY = " "
X = "X"
O = "O"

COLOR_BG = "#1a1a2e"
COLOR_CELL = "#16213e"
COLOR_CELL_HOV = "#0f3460"
COLOR_TEXT = "#eaeaea"
COLOR_X = "#ff6b6b"
COLOR_O = "#4ecdc4"
COLOR_ACCENT = "#4ecdc4"
COLOR_LOSE = "#ff6b6b"
COLOR_DRAW = "#ffd93d"
WINNING_CELL_BG = "#533483"


@dataclass
class SubBoard:
    """Одно под-поле 3x3."""
    cells: list = field(default_factory=lambda: [EMPTY] * 9)
    
    def winner(self) -> Optional[str]:
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for line in lines:
            a, b, c = self.cells[line[0]], self.cells[line[1]], self.cells[line[2]]
            if a != EMPTY and a == b == c:
                return a
        return None
    
    def is_full(self) -> bool:
        return all(c != EMPTY for c in self.cells)
    
    def empty_indices(self) -> List[int]:
        return [i for i, c in enumerate(self.cells) if c == EMPTY]


@dataclass
class GameState:
    """Состояние игры Ultimate Tic-Tac-Toe."""
    sub_boards: list = field(default_factory=lambda: [SubBoard() for _ in range(9)])
    current: str = X
    next_subboard: Optional[int] = None
    won_subboards: list = field(default_factory=lambda: [None] * 9)
    
    @staticmethod
    def new(first_player: str = X):
        return GameState(current=first_player)
    
    def winner(self) -> Optional[str]:
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for line in lines:
            a, b, c = self.won_subboards[line[0]], self.won_subboards[line[1]], self.won_subboards[line[2]]
            if a is not None and a == b == c:
                return a
        return None
    
    def is_over(self) -> bool:
        return self.winner() is not None or self.is_full()
    
    def is_full(self) -> bool:
        return all(sb.is_full() for sb in self.sub_boards)
    
    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """Возвращает список всех возможных ходов (subboard_idx, cell_idx)."""
        moves = []
        if self.next_subboard is not None and not self.sub_boards[self.next_subboard].is_full():
            allowed_subboards = [self.next_subboard]
        else:
            allowed_subboards = [i for i in range(9) if not self.sub_boards[i].is_full()]
        
        for sb_idx in allowed_subboards:
            for cell_idx in self.sub_boards[sb_idx].empty_indices():
                moves.append((sb_idx, cell_idx))
        return moves
    
    def play(self, subboard_idx: int, cell_idx: int, player: str):
        """Сделать ход."""
        self.sub_boards[subboard_idx].cells[cell_idx] = player
        sub_winner = self.sub_boards[subboard_idx].winner()
        if sub_winner:
            self.won_subboards[subboard_idx] = sub_winner
        self.next_subboard = cell_idx
        self.current = O if player == X else X
    
    def copy(self):
        """Создать копию состояния."""
        new_state = GameState()
        new_state.current = self.current
        new_state.next_subboard = self.next_subboard
        new_state.won_subboards = self.won_subboards.copy()
        new_state.sub_boards = []
        for sb in self.sub_boards:
            new_sb = SubBoard()
            new_sb.cells = sb.cells.copy()
            new_state.sub_boards.append(new_sb)
        return new_state


def evaluate_board(state: GameState, bot: str) -> float:
    """Эвристическая оценка позиции."""
    human = O if bot == X else X
    score = 0
    winner = state.winner()
    if winner == bot:
        return 1000
    elif winner == human:
        return -1000
    
    for sb_idx in range(9):
        if state.won_subboards[sb_idx] == bot:
            score += 10
        elif state.won_subboards[sb_idx] == human:
            score -= 10
    
    lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    
    for sb_idx in range(9):
        if state.won_subboards[sb_idx] is not None:
            continue
        sb = state.sub_boards[sb_idx]
        for line in lines:
            cells = [sb.cells[i] for i in line]
            bot_count = cells.count(bot)
            human_count = cells.count(human)
            if bot_count > 0 and human_count == 0:
                score += bot_count * 2
            elif human_count > 0 and bot_count == 0:
                score -= human_count * 2
    
    for sb_idx in range(9):
        if state.sub_boards[sb_idx].cells[4] == bot:
            score += 3
        elif state.sub_boards[sb_idx].cells[4] == human:
            score -= 3
    return score


def minimax_alpha_beta(state: GameState, bot: str, human: str, 
                       depth: int, max_depth: int, 
                       alpha: float, beta: float) -> Tuple[float, Optional[Tuple[int, int]]]:
    """Minimax с альфа-бета отсечением."""
    if state.is_over() or depth >= max_depth:
        return evaluate_board(state, bot), None
    
    valid_moves = state.get_valid_moves()
    if not valid_moves:
        return evaluate_board(state, bot), None
    
    is_maximizing = (state.current == bot)
    best_move = None
    
    if is_maximizing:
        best_score = float('-inf')
        for move in valid_moves:
            new_state = state.copy()
            new_state.play(move[0], move[1], bot)
            score, _ = minimax_alpha_beta(new_state, bot, human, depth + 1, max_depth, alpha, beta)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return best_score, best_move
    else:
        best_score = float('inf')
        for move in valid_moves:
            new_state = state.copy()
            new_state.play(move[0], move[1], human)
            score, _ = minimax_alpha_beta(new_state, bot, human, depth + 1, max_depth, alpha, beta)
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_score, best_move


def bot_move_smart(state: GameState, bot: str, human: str) -> Tuple[int, int]:
    """Умный ход бота."""
    valid_moves = state.get_valid_moves()
    if not valid_moves:
        return None
    
    remaining_moves = sum(len(sb.empty_indices()) for sb in state.sub_boards)
    if remaining_moves <= 10:
        max_depth = 6
    elif remaining_moves <= 20:
        max_depth = 4
    else:
        max_depth = 3
    
    _, best_move = minimax_alpha_beta(state, bot, human, 0, max_depth, float('-inf'), float('inf'))
    if best_move is None:
        return valid_moves[0]
    return best_move


class UltimateTicTacToeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ultimate Tic-Tac-Toe")
        self.configure(bg=COLOR_BG)
        self.resizable(False, False)
        self.state = GameState.new(X)
        self.human = X
        self.bot = O
        self.mode = "bot"
        self.locked = False
        self.winning_subboards = set()
        self._build_ui()
        self._update_status()
    
    def _build_ui(self):
        main_frame = tk.Frame(self, bg=COLOR_BG)
        main_frame.pack(padx=20, pady=20)
        
        title_label = tk.Label(main_frame, text="Ultimate Tic-Tac-Toe", 
                              font=("Arial", 16, "bold"), fg=COLOR_TEXT, bg=COLOR_BG)
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        self.board_frame = tk.Frame(main_frame, bg=COLOR_BG)
        self.board_frame.grid(row=1, column=0, columnspan=3, pady=10)
        
        self.cell_buttons = {}
        
        for sb_row in range(3):
            for sb_col in range(3):
                sb_idx = sb_row * 3 + sb_col
                sb_frame = tk.Frame(self.board_frame, bg=COLOR_BG, highlightbackground="#333", 
                                   highlightthickness=2)
                sb_frame.grid(row=sb_row, column=sb_col, padx=5, pady=5)
                
                for cell_row in range(3):
                    for cell_col in range(3):
                        cell_idx = cell_row * 3 + cell_col
                        btn = tk.Button(sb_frame, text="", font=("Arial", 12, "bold"),
                                       width=3, height=1, bg=COLOR_CELL, fg=COLOR_TEXT,
                                       relief="flat", cursor="hand2")
                        btn.grid(row=cell_row, column=cell_col, padx=1, pady=1)
                        btn.bind("<Enter>", lambda e, idx=(sb_idx, cell_idx): self._hover(idx, True))
                        btn.bind("<Leave>", lambda e, idx=(sb_idx, cell_idx): self._hover(idx, False))
                        btn.config(command=lambda idx=(sb_idx, cell_idx): self.on_cell(idx))
                        self.cell_buttons[(sb_idx, cell_idx)] = btn
        
        self.status_var = tk.StringVar(value="Ваш ход.")
        self.status_label = tk.Label(main_frame, textvariable=self.status_var,
                                    font=("Arial", 12), fg=COLOR_TEXT, bg=COLOR_BG)
        self.status_label.grid(row=2, column=0, columnspan=3, pady=10)
        
        btn_frame = tk.Frame(main_frame, bg=COLOR_BG)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        self.new_game_btn = tk.Button(btn_frame, text="Новая игра", command=self.new_game,
                                     bg=COLOR_ACCENT, fg="white", font=("Arial", 10, "bold"),
                                     relief="flat", padx=15, pady=5)
        self.new_game_btn.pack(side=tk.LEFT, padx=5)
        
        self.mode_btn = tk.Button(btn_frame, text="Режим: против бота", command=self.toggle_mode,
                                 bg="#0f3460", fg="white", font=("Arial", 10),
                                 relief="flat", padx=15, pady=5)
        self.mode_btn.pack(side=tk.LEFT, padx=5)
        
        self.first_btn = tk.Button(btn_frame, text="Первый ход: я", command=self.toggle_first,
                                  bg="#0f3460", fg="white", font=("Arial", 10),
                                  relief="flat", padx=15, pady=5)
        self.first_btn.pack(side=tk.LEFT, padx=5)
    
    def _hover(self, idx, on: bool):
        if self.locked:
            return
        sb_idx, cell_idx = idx
        if self.state.sub_boards[sb_idx].cells[cell_idx] != EMPTY:
            return
        color = COLOR_CELL_HOV if on else COLOR_CELL
        self.cell_buttons[idx].config(bg=color)
    
    def _update_status(self):
        w = self.state.winner()
        if w:
            if self.mode == "bot":
                text = "Вы победили!" if w == self.human else "Бот победил."
                color = COLOR_ACCENT if w == self.human else COLOR_LOSE
            else:
                text = f"Победа: {w}"
                color = COLOR_ACCENT
            self.status_var.set(text)
            self.status_label.config(fg=color)
            return
        
        if self.state.is_full():
            self.status_var.set("Ничья.")
            self.status_label.config(fg=COLOR_DRAW)
            return
        
        if self.mode == "bot":
            text = "Ваш ход." if self.state.current == self.human else "Ход бота..."
        else:
            text = f"Ход: {self.state.current}"
        self.status_var.set(text)
        self.status_label.config(fg=COLOR_TEXT)
    
    def _paint_cell(self, sb_idx: int, cell_idx: int):
        ch = self.state.sub_boards[sb_idx].cells[cell_idx]
        color = COLOR_X if ch == X else COLOR_O if ch == O else COLOR_TEXT
        self.cell_buttons[(sb_idx, cell_idx)].config(text=ch, fg=color)
    
    def _mark_winning_subboards(self):
        winner = self.state.winner()
        if not winner:
            return
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for line in lines:
            if all(self.state.won_subboards[i] == winner for i in line):
                self.winning_subboards.update(line)
                for sb_idx in line:
                    for cell_row in range(3):
                        for cell_col in range(3):
                            cell_idx = cell_row * 3 + cell_col
                            self.cell_buttons[(sb_idx, cell_idx)].config(bg=WINNING_CELL_BG)
                break
    
    def new_game(self):
        self.state = GameState.new(X)
        self.winning_subboards = set()
        for sb_idx in range(9):
            for cell_idx in range(9):
                btn = self.cell_buttons[(sb_idx, cell_idx)]
                btn.config(text="", bg=COLOR_CELL, fg=COLOR_TEXT)
        self.locked = False
        self._update_status()
        if self.mode == "bot" and self.state.current == self.bot:
            self._schedule_bot()
    
    def toggle_mode(self):
        if self.mode == "bot":
            self.mode = "human"
            self.mode_btn.config(text="Режим: два игрока")
        else:
            self.mode = "bot"
            self.mode_btn.config(text="Режим: против бота")
        self.new_game()
    
    def toggle_first(self):
        if self.mode == "bot":
            self.human, self.bot = self.bot, self.human
            label = "Первый ход: я" if self.human == X else "Первый ход: бот"
            self.first_btn.config(text=label)
        self.new_game()
    
    def on_cell(self, idx):
        if self.locked:
            return
        if self.state.is_over():
            return
        sb_idx, cell_idx = idx
        if self.state.sub_boards[sb_idx].cells[cell_idx] != EMPTY:
            return
        valid_moves = self.state.get_valid_moves()
        if (sb_idx, cell_idx) not in valid_moves:
            return
        player = self.state.current
        self.state.play(sb_idx, cell_idx, player)
        self._paint_cell(sb_idx, cell_idx)
        if self.state.is_over():
            self._mark_winning_subboards()
            self._update_status()
            return
        self._update_status()
        if self.mode == "bot" and self.state.current == self.bot:
            self._schedule_bot()
    
    def _schedule_bot(self):
        self.locked = True
        self.after(100, self._bot_turn)
    
    def _bot_turn(self):
        if self.state.is_over():
            self.locked = False
            return
        move = bot_move_smart(self.state, self.bot, self.human)
        if move:
            sb_idx, cell_idx = move
            self.state.play(sb_idx, cell_idx, self.bot)
            self._paint_cell(sb_idx, cell_idx)
            if self.state.is_over():
                self._mark_winning_subboards()
                self._update_status()
                self.locked = False
                return
        self.locked = False
        self._update_status()


if __name__ == "__main__":
    app = UltimateTicTacToeApp()
    app.mainloop()
