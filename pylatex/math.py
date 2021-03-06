# -*- coding: utf-8 -*-
"""
This module implements the classes that deal with math.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .base_classes import Command, Container, Environment
from .package import Package
from .utils import dumps_list


class MathEquation(Environment):
    """The base class of math equation environments.

    Other math equation environments extend the base class.
    """

    packages = [Package('amsmath')]
    escape = False
    content_separator = "\\\\\n"

    def __init__(self, numbering=True, escape=None, *args, **kwargs):
        """
        Parameters
        ----------
        numbering : bool
            Whether to number equations
        escape : bool
            if True, will escape strings
        """
        self.numbering = numbering
        self.escape = escape
        if not numbering:
            self._star_latex_name = True
        super(MathEquation, self).__init__(*args, **kwargs)

    def add_row(self, row):
        """Add a row into the equations.

        Similar to add_row in Table.
        """
        self.append(
            dumps_list([elm for elm in row], token=' & ', escape=False))


class Align(MathEquation):
    """A class to wrap LaTeX's align environment.

    align is the base of the math equation environments in LaTeX.
    """

    pass


class Split(MathEquation):
    """A class to wrap LaTeX's split environment."""

    pass


class Gather(MathEquation):
    """A class to wrap LaTeX's gather environment."""

    pass


class Equation(MathEquation):
    """A class to wrap LaTeX's equation environment."""

    pass


class Alignat(Align):
    """Class that represents a aligned equation environment."""

    #: Alignat environment cause compile errors when they do not contain items.
    #: This is why it is omitted fully if they are empty.
    omit_if_empty = True

    def __init__(self, aligns=2, numbering=True, escape=None):
        """
        Parameters
        ----------
        aligns : int
            number of alignments
        numbering : bool
            Whether to number equations
        escape : bool
            if True, will escape strings
        """
        self.aligns = aligns
        super().__init__(
            numbering=numbering, escape=escape,
            start_arguments=[str(int(aligns))])


class Math(Container):
    """A class representing a math environment."""

    packages = [Package('amsmath')]
    content_separator = ' '

    def __init__(self, *, inline=False, data=None, escape=None):
        """
        Args
        ----
        data: list
            Content of the math container.
        inline: bool
            If the math should be displayed inline or not.
        escape : bool
            if True, will escape strings
        """

        self.inline = inline
        self.escape = escape
        super().__init__(data=data)

    def dumps(self):
        """Return a LaTeX formatted string representing the object.

        Returns
        -------
        str

        """
        if self.inline:
            return '$' + self.dumps_content() + '$'
        return '\\[%\n' + self.dumps_content() + '%\n\\]'


class VectorName(Command):
    """A class representing a named vector."""

    _repr_attributes_mapping = {
        'name': 'arguments',
    }

    def __init__(self, name):
        """
        Args
        ----
        name: str
            Name of the vector
        """

        super().__init__('mathbf', arguments=name)


class Matrix(Environment):
    """A class representing a matrix."""

    packages = [Package('amsmath')]

    _repr_attributes_mapping = {
        'alignment': 'arguments',
    }

    def __init__(self, matrix, *, mtype='p', alignment=None):
        r"""
        Args
        ----
        matrix: `numpy.ndarray` instance
            The matrix to display
        mtype: str
            What kind of brackets are used around the matrix. The different
            options and their corresponding brackets are:
            p = ( ), b = [ ], B = { }, v = \| \|, V = \|\| \|\|
        alignment: str
            How to align the content of the cells in the matrix. This is ``c``
            by default.

        References
        ----------
        * https://en.wikibooks.org/wiki/LaTeX/Mathematics#Matrices_and_arrays
        """

        import numpy  # noqa, Sanity check if numpy is installed

        if isinstance(matrix, (list, tuple)):
            matrix = numpy.array(matrix)
        self.matrix = matrix

        self.latex_name = mtype + 'matrix'
        self._mtype = mtype
        if alignment is not None:
            self.latex_name += '*'

        super().__init__(arguments=alignment)

    def dumps_content(self):
        """Return a string representing the matrix in LaTeX syntax.

        Returns
        -------
        str
        """

        import numpy as np

        string = ''
        shape = self.matrix.shape

        for (y, x), value in np.ndenumerate(self.matrix):
            if x:
                string += '&'
            string += str(value)

            if x == shape[1] - 1 and y != shape[0] - 1:
                string += r'\\' + '%\n'

        super().dumps_content()

        return string


class Determinant(Matrix):
    """Determinant < Matrix."""

    def __init__(self, matrix, *args, **kwargs):
        """
        Args
        ---
        matrix: numpy.ndarray
            square matrix
        """
        super(Determinant, self).__init__(matrix, mtype='v', *args, **kwargs)
        assert self.matrix.ndim == 2 and \
            self.matrix.shape[1] == self.matrix.shape[0]


class Vector(Matrix):
    """Vector < Matrix.

    Vector is a 1dim Matrix. If it receives a matrix,
    then the matrix will be reshaped.
    """

    def __init__(self, vec, mtype='p', *args, **kwargs):
        r"""
        Args
        ----
        vec: `numpy.ndarray` instance
        mtype: str
            'p' | 'b' ('p' by default)
        """
        super(Vector, self).__init__(matrix=vec, mtype=mtype, *args, **kwargs)
        if self.matrix.ndim == 2:
            m, n = self.matrix.shape
            if m > 1 and n > 1:
                self.matrix = self.matrix.reshape(1, m * n)
        else:
            self.matrix = self.matrix.reshape(1, self.matrix.shape[0])


class ColumnVector(Vector):
    """Column Vector, subclass of Vector."""

    def __init__(self, *args, **kwargs):
        """See Vector"""
        super(ColumnVector, self).__init__(*args, **kwargs)
        self.matrix = self.matrix.T


# Functions for ease.
def dollar(x, *args, **kwargs):
    """Shorthand for inline math form: $math expression$.

    Example
    ---
    >>> dollar('c_B')
    $c_B$
    """
    return Math(data=x, inline=True, escape=False, *args, **kwargs)


def ddollar(x, *args, **kwargs):
    r"""Shorthand for math form: \[math expression\] == $$math expression$$.

    Example
    ---
    >>> ddollar('c_B')
    \[c_B\]
    """
    return Math(data=x, inline=False, escape=False, *args, **kwargs)
