#!/usr/bin/python


"""Test to validate that Environments uphold contract of base classes."""

from pylatex.math import diff, dollar


def test_diff():
    assert diff('x', 'y').dumps() == r'\frac{\mathrm{d}x}{\mathrm{d}y}', \
        "Unexpected result of diff"


def test_dollar():
    assert dollar('c_B') == r'$c_B$', \
        "Unexpected result of dollar"
