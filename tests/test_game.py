"""Testy igrovogo cikla Game."""

import pytest

from src.board import X, O
from src.game import Game


def test_start_state():
    g = Game()
    assert g.current == X
    assert g.required_sub is None
    assert len(g.legal_moves()) == 81
    assert not g.is_over()


def test_turn_alternation():
    g = Game()
    g.play((0, 0))
    assert g.current == O
    g.play((0, 1))
    assert g.current == X


def test_move_outside_required_sub_raises():
    g = Game()
    g.play((0, 0))         # required_sub becomes (0, 0)
    assert g.required_sub == (0, 0)
    with pytest.raises(ValueError):
        g.play((5, 5))     # vne pod-polya (0, 0)


def test_reset_clears_state():
    g = Game()
    g.play((0, 0))
    g.play((0, 1))
    g.reset()
    assert g.current == X
    assert g.required_sub is None
    assert g.history == []
    assert not g.is_over()
