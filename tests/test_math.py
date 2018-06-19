#!/usr/bin/python


"""Test to validate dollar and Vector."""

from pylatex.math import Vector, dollar


def test_dollar():
    assert dollar('c_B').dumps() == r'$c_B$', \
        "Unexpected result of dollar"


def test_vector():
    assert Vector([1, 2]).dumps() == r'''\begin{pmatrix}%
1&2%
\end{pmatrix}'''
