# -*- coding: utf-8 -*-
"""
This module implements a class that implements a latex command.

This can be used directly or it can be inherrited to make an easier interface
to it.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .latex_object import LatexObject


class Command(LatexObject):

    """A class that represents a LaTeX command."""

    def __init__(self, command, arguments=None, options=None,
                 extra_arguments=None, packages=None):
        r""".

        Args
        ----
        command: str
            Name of the command
        arguments: None, str, list or `~.Arguments`
            The main arguments of the command.
        options: None, str, list or `~.Options`
            Options of the command. These are placed in front of the arguments.
        extra_arguments: None, str, list or `~.Arguments`
            Extra arguments for the command. When these are supplied the
            options will be placed before them instead of before the normal
            arguments. This allows for a way of having one or more arguments
            before the options.
        packages: list of `~.Package` instances
            A list of the packages that this command requires

        Examples
        --------
        >>> Command('documentclass',
        >>>         options=Options('12pt', 'a4paper', 'twoside'),
        >>>         arguments='article').dumps()
        '\\documentclass[12pt,a4paper,twoside]{article}'
        >>> Command('com')
        '\\com'
        >>> Command('com', 'first')
        '\\com{first}'
        >>> Command('com', 'first', 'option')
        '\\com[option]{first}'
        >>> Command('com', 'first', 'option', 'second')
        '\\com{first}[option]{second}'

        """

        self.command = command

        self._set_parameters(arguments, 'arguments')
        self._set_parameters(options, 'options')
        if extra_arguments is None:
            self.extra_arguments = None
        else:
            self._set_parameters(extra_arguments, 'extra_arguments')

        super().__init__(packages)

    def _set_parameters(self, parameters, argument_type):
        parameter_cls = Options if argument_type == 'options' else Arguments

        if parameters is None:
            parameters = parameter_cls()
        elif not isinstance(parameters, parameter_cls):
            parameters = parameter_cls(parameters)

        setattr(self, argument_type, parameters)

    def __key(self):
        """Return a hashable key, representing the command.

        Returns
        -------
        tuple
        """

        return self.command, self.arguments, self.options, self.extra_arguments

    def __eq__(self, other):
        """Compare two commands.

        Args
        ----
        other: `~.Command` instance
            The command to compare this command to


        Returns
        -------
        bool:
            If the two instances are equal
        """

        if isinstance(other, Command):
            return self.__key() == other.__key()

        return False

    def __hash__(self):
        """Calculate the hash of a command.

        Returns
        -------
        int:
            The hash of the command
        """

        return hash(self.__key())

    def dumps(self):
        """Represent the command as a string in LaTeX syntax.

        Returns
        -------
        str
            The LaTeX formatted command
        """

        options = self.options.dumps()
        arguments = self.arguments.dumps()

        if self.extra_arguments is None:
            return r'\{command}{options}{arguments}'\
                .format(command=self.command, options=options,
                        arguments=arguments)

        extra_arguments = self.extra_arguments.dumps()

        return r'\{command}{arguments}{options}{extra_arguments}'\
            .format(command=self.command, arguments=arguments, options=options,
                    extra_arguments=extra_arguments)


class Parameters(LatexObject):

    """The base class used by `~Options` and `~Arguments`.

    This class should probably never be used on its own and inhereting from it
    is only useful if a class like `~Options` or `~Arguments` is needed again.
    """

    def __init__(self, *args, **kwargs):
        r""".

        Args
        ----
        \*args:
            Positional parameters
        \*\*kwargs:
            Keyword parameters
        """

        if len(args) == 1 and hasattr(args[0], '__iter__') and\
                not isinstance(args[0], str):
            args = args[0]

        self._positional_args = list(args)
        self._key_value_args = dict(kwargs)

        super().__init__(packages=None)

    def __key(self):
        """Generate a unique hashable key representing the parameter object.

        Returns
        -------
        tuple
        """

        return tuple(self._list_args_kwargs())

    def __eq__(self, other):
        """Compare two parameters.

        Returns
        -------
        bool
        """

        return type(self) == type(other) and self.__key() == other.__key()

    def __hash__(self):
        """Generate a hash of the parameters.

        Returns
        -------
        int
        """

        return hash(self.__key())

    def _format_contents(self, prefix, separater, suffix):
        """Format the parameters.

        The formatting is dono using the three arguments suplied to this
        function.

        Arguments
        ---------
        prefix: str
        separater: str
        suffix: str

        Returns
        -------
        str
        """

        params = self._list_args_kwargs()

        if len(params) <= 0:
            return ''

        string = prefix + separater.join(map(str, params)) + suffix

        return string

    def _list_args_kwargs(self):
        """Make a list of strings representing al parameters.

        Returns
        -------
        list
        """

        params = []
        params.extend(self._positional_args)
        params.extend(['{k}={v}'.format(k=k, v=v) for k, v in
                       self._key_value_args.items()])

        return params


class Options(Parameters):

    """A class implementing LaTex options for a command.

    It supports normal positional parameters, as well as key-value pairs.
    Options are the part of a command located between the square brackets
    (``[]``). The positional parameters will be outputted in order and will
    appear before the key-value-pairs. The key value-pairs won't be outputted
    in the order in which they were entered


    Examples
    --------
    >>> args = Options('a', 'b', 'c').dumps()
    '[a,b,c]'
    >>> Options('clip', width=50, height='25em', trim='1 2 3 4').dumps()
    '[clip,trim=1 2 3 4,width=50,height=25em]'

    """

    def dumps(self):
        """Represent the parameters as a string in LaTeX syntax.

        This is to be appended to a command.

        Returns
        -------
        str
        """

        return self._format_contents('[', ',', ']')


class Arguments(Parameters):

    """A class implementing LaTex arguments for a command.

    It supports normal positional parameters, as well as key-value pairs.
    Arguments are the part of a command located between the curly braces
    (``{}``). The positional parameters will be outputted in order and will
    appear before the key-value-pairs. The key value-pairs won't be outputted
    in the order in which they were entered


    Examples
    --------
    >>> args = Arguments('a', 'b', 'c').dumps()
    '{a}{b}{c}'
    >>> args = Arguments('clip', width=50, height='25em').dumps()
    >>> args.dumps()
    '{clip}{width=50}{height=25em}'

    """

    def dumps(self):
        """Represent the parameters as a string in LaTeX syntax.

        This is to be appended to a command.

        Returns
        -------
        str
        """

        return self._format_contents('{', '}{', '}')