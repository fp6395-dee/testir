"""Testy logiki Board."""

import pytest

from src.board import Board, X, O, EMPTY, sub_of, local_of


def test_empty_board_has_all_moves():
    b = Board()
    moves = b.legal_moves(required_sub=None)
    assert len(moves) == 81


def test_apply_places_mark():
    b = Board()
    b.apply((0, 0), X)
    assert b.cells[0][0] == X


def test_apply_to_taken_cell_raises():
    b = Board()
    b.apply((0, 0), X)
    with pytest.raises(ValueError):
        b.apply((0, 0), O)


def test_required_sub_after_move():
    b = Board()
    # hodim v (0,0): lokalnye (0,0) -> sleduyuschee pod-pole (0,0)
    nxt = b.apply((0, 0), X)
    assert nxt == (0, 0)


def test_required_sub_redirect():
    b = Board()
    # hodim v (1,1): lokalnye (1,1) -> sleduyuschee pod-pole (1,1)
    nxt = b.apply((1, 1), X)
    assert nxt == (1, 1)


def test_sub_winner_detected():
    b = Board()
    # igraem v pod-pole (0,0): X zabiraet verhnyuyu stroku
    for c in range(3):
        b.apply((0, c), X)
        # sleduyuschiy hod O - kuda ugodno, no nam vazhno chtoby X hostil
        if c < 2:
            # delaem hod O v drugom pod-pole, chtoby ne meshat
            # no nuzhno soblyudat required_sub... uprostim: stavim O v (3,0)
            pass
    assert b.sub_winner[0][0] == X


def test_sub_of_and_local_of():
    assert sub_of((0, 0)) == (0, 0)
    assert sub_of((2, 2)) == (0, 0)
    assert sub_of((3, 4)) == (1, 1)
    assert sub_of((8, 8)) == (2, 2)

    assert local_of((0, 0)) == (0, 0)
    assert local_of((2, 2)) == (2, 2)
    assert local_of((3, 4)) == (0, 1)
    assert local_of((8, 8)) == (2, 2)


def test_overall_winner_via_full_sub_grid():
    b = Board()
    # poddelka: vruchnuyu zapolnyaem sub_winner
    b.sub_winner = [[X, X, X], [None, None, None], [None, None, None]]
    assert b.overall_winner() == X


def test_no_winner_yet():
    b = Board()
    assert b.overall_winner() is None
    assert not b.is_game_over()
