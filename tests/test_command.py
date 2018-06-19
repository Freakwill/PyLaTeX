#!/usr/bin/python


"""Test to validate that Environments uphold contract of base classes."""

from pylatex.base_classes import slash, newcommand


def test_command():
    assert slash.frac('x', 'y').dumps() == r'\frac{x}{y}', \
        "Unexpected result of slash.frac"


def test_newcommand():
    res = newcommand('mycmd', '#1+#2', default='lala').dumps()
    assert res == r'\newcommand{\mycmd}[2][lala]{#1+#2}', \
        "Unexpected result of newcommand"
