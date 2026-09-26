#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tic-Tac-Toe 3x3 s GUI na tkinter i botom (minimax)."""

import tkinter as tk
from tkinter import font as tkfont
from dataclasses import dataclass
from typing import List, Optional, Tuple


EMPTY = ""
X = "X"
O = "O"

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]


@dataclass
class GameState:
    cells: List[str]
    current: str

    @classmethod
    def new(cls, first: str = X) -> "GameState":
        return cls(cells=[EMPTY] * 9, current=first)

    def empty_indices(self) -> List[int]:
        return [i for i, v in enumerate(self.cells) if v == EMPTY]

    def winner(self) -> Optional[str]:
        for a, b, c in WIN_LINES:
            if self.cells[a] and self.cells[a] == self.cells[b] == self.cells[c]:
                return self.cells[a]
        return None

    def winning_line(self) -> Optional[Tuple[int, int, int]]:
        for a, b, c in WIN_LINES:
            if self.cells[a] and self.cells[a] == self.cells[b] == self.cells[c]:
                return (a, b, c)
        return None

    def is_full(self) -> bool:
        return EMPTY not in self.cells

    def is_over(self) -> bool:
        return self.winner() is not None or self.is_full()

    def play(self, idx: int, player: str) -> None:
        if self.cells[idx] != EMPTY:
            raise ValueError(f"Cell {idx} is occupied")
        self.cells[idx] = player
        self.current = O if player == X else X

def minimax(state: GameState, bot: str, human: str, depth: int = 0):
    w = state.winner()
    if w == bot:
        return (10 - depth, None)
    if w == human:
        return (depth - 10, None)
    if state.is_full():
        return (0, None)

    next_player = state.current
    is_max = (next_player == bot)
    best_move = None

    if is_max:
        best_score = -10**9
        for i in state.empty_indices():
            state.cells[i] = next_player
            state.current = human if next_player == bot else bot
            score, _ = minimax(state, bot, human, depth + 1)
            state.cells[i] = EMPTY
            state.current = next_player
            if score > best_score:
                best_score = score
                best_move = i
        return best_score, best_move
    else:
        best_score = 10**9
        for i in state.empty_indices():
            state.cells[i] = next_player
            state.current = bot if next_player == human else human
            score, _ = minimax(state, bot, human, depth + 1)
            state.cells[i] = EMPTY
            state.current = next_player
            if score < best_score:
                best_score = score
                best_move = i
        return best_score, best_move


def bot_move(state: GameState, bot: str, human: str) -> int:
    _, move = minimax(state, bot, human, 0)
    if move is None:
        return state.empty_indices()[0]
    return move


COLOR_BG       = "#1e1e2e"
COLOR_CELL     = "#2a2a3e"
COLOR_CELL_HOV = "#3a3a55"
COLOR_X        = "#7fdbff"
COLOR_O        = "#ff8f8f"
COLOR_TEXT     = "#e0e0f0"
COLOR_ACCENT   = "#a6e3a1"
COLOR_DRAW     = "#f9e2af"
COLOR_LOSE     = "#f38ba8"
WINNING_CELL_BG = "#4a6b5a"


class TicTacToeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic-Tac-Toe")
        self.configure(bg=COLOR_BG)
        self.resizable(False, False)

        self.state = GameState.new(X)
        self.human = X
        self.bot = O
        self.mode = "bot"
        self.locked = False
        self.winning_cells = set()

        self.f_cell   = tkfont.Font(family="Segoe UI", size=44, weight="bold")
        self.f_status = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        self.f_button = tkfont.Font(family="Segoe UI", size=11)

        self._build_ui()
        self._update_status()

    def _build_ui(self):
        top = tk.Frame(self, bg=COLOR_BG)
        top.pack(fill="x", padx=16, pady=(14, 6))
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(
            top, textvariable=self.status_var,
            bg=COLOR_BG, fg=COLOR_TEXT, font=self.f_status,
        )
        self.status_label.pack()

        board_wrap = tk.Frame(self, bg=COLOR_BG)
        board_wrap.pack(padx=16, pady=10)

        self.buttons = []
        for i in range(9):
            r, c = divmod(i, 3)
            b = tk.Button(
                board_wrap, text="", width=3, height=1,
                font=self.f_cell,
                bg=COLOR_CELL, fg=COLOR_TEXT,
                activebackground=COLOR_CELL_HOV,
                activeforeground=COLOR_TEXT,
                relief="flat", bd=0, highlightthickness=0,
                command=lambda idx=i: self.on_cell(idx),
            )
            b.grid(row=r, column=c, padx=3, pady=3, ipadx=10, ipady=10)
            b.bind("<Enter>", lambda e, idx=i: self._hover(idx, True))
            b.bind("<Leave>", lambda e, idx=i: self._hover(idx, False))
            self.buttons.append(b)

        bottom = tk.Frame(self, bg=COLOR_BG)
        bottom.pack(fill="x", padx=16, pady=(6, 16))

        self.new_btn = tk.Button(
            bottom, text="Novaya igra", font=self.f_button,
            bg=COLOR_ACCENT, fg="#1e1e2e",
            activebackground="#8ed08a", activeforeground="#1e1e2e",
            relief="flat", bd=0, padx=14, pady=6,
            command=self.new_game,
        )
        self.new_btn.pack(side="left")

        self.mode_btn = tk.Button(
            bottom, text="Rezhim: protiv bota", font=self.f_button,
            bg=COLOR_CELL, fg=COLOR_TEXT,
            activebackground=COLOR_CELL_HOV, activeforeground=COLOR_TEXT,
            relief="flat", bd=0, padx=14, pady=6,
            command=self.toggle_mode,
        )
        self.mode_btn.pack(side="left", padx=(8, 0))

        self.first_btn = tk.Button(
            bottom, text="Pervyy hod: ya", font=self.f_button,
            bg=COLOR_CELL, fg=COLOR_TEXT,
            activebackground=COLOR_CELL_HOV, activeforeground=COLOR_TEXT,
            relief="flat", bd=0, padx=14, pady=6,
            command=self.toggle_first,
        )
        self.first_btn.pack(side="left", padx=(8, 0))

    def _hover(self, idx: int, on: bool):
        if self.locked:
            return
        if self.state.cells[idx] != EMPTY:
            return
        if idx in self.winning_cells:
            return
        self.buttons[idx].config(bg=COLOR_CELL_HOV if on else COLOR_CELL)

    def _update_status(self):
        w = self.state.winner()
        if w:
            if self.mode == "bot":
                text = "Vy pobedili!" if w == self.human else "Bot pobedil."
                color = COLOR_ACCENT if w == self.human else COLOR_LOSE
            else:
                text = f"Pobeda: {w}"
                color = COLOR_ACCENT
            self.status_var.set(text)
            self.status_label.config(fg=color)
            return
        if self.state.is_full():
            self.status_var.set("Nichya.")
            self.status_label.config(fg=COLOR_DRAW)
            return

        if self.mode == "bot":
            text = "Vash hod." if self.state.current == self.human else "Hod bota..."
        else:
            text = f"Hod: {self.state.current}"
        self.status_var.set(text)
        self.status_label.config(fg=COLOR_TEXT)

    def _paint(self, idx: int):
        ch = self.state.cells[idx]
        color = COLOR_X if ch == X else COLOR_O if ch == O else COLOR_TEXT
        self.buttons[idx].config(text=ch, fg=color)

    def _mark_winning(self):
        line = self.state.winning_line()
        if not line:
            return
        self.winning_cells = set(line)
        for i in line:
            self.buttons[i].config(bg=WINNING_CELL_BG)

    def _set_board_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        for b in self.buttons:
            b.config(state=state)

    def new_game(self):
        self.state = GameState.new(X)
        self.winning_cells = set()
        for i, b in enumerate(self.buttons):
            b.config(text="", bg=COLOR_CELL, fg=COLOR_TEXT, state="normal")
        self.locked = False
        self._update_status()
        if self.mode == "bot" and self.state.current == self.bot:
            self._schedule_bot()

    def toggle_mode(self):
        if self.mode == "bot":
            self.mode = "human"
            self.mode_btn.config(text="Rezhim: dva igroka")
        else:
            self.mode = "bot"
            self.mode_btn.config(text="Rezhim: protiv bota")
        self.new_game()

    def toggle_first(self):
        if self.mode == "bot":
            self.human, self.bot = self.bot, self.human
            label = "Pervyy hod: ya" if self.human == X else "Pervyy hod: bot"
            self.first_btn.config(text=label)
        self.new_game()

    def on_cell(self, idx: int):
        if self.locked:
            return
        if self.state.is_over():
            return
        if self.state.cells[idx] != EMPTY:
            return

        player = self.state.current
        self.state.play(idx, player)
        self._paint(idx)

        if self.state.is_over():
            self._mark_winning()
            self._update_status()
            return

        self._update_status()

        if self.mode == "bot" and self.state.current == self.bot:
            self._schedule_bot()

    def _schedule_bot(self):
        self.locked = True
        self._set_board_enabled(False)
        self.after(220, self._bot_turn)

    def _bot_turn(self):
        if self.state.is_over():
            self.locked = False
            self._set_board_enabled(True)
            return
        move = bot_move(self.state, self.bot, self.human)
        self.state.play(move, self.bot)
        self._paint(move)

        if self.state.is_over():
            self._mark_winning()
            self._update_status()
            self.locked = False
            self._set_board_enabled(True)
            return

        self.locked = False
        self._set_board_enabled(True)
        self._update_status()


def main():
    app = TicTacToeApp()
    app.mainloop()


if __name__ == "__main__":
    main()
