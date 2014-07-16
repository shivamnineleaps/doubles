from doubles.verification import verify_arguments

_any = object()


class Allowance(object):
    """An individual method allowance (stub)."""

    def __init__(self, target, method_name):
        """
        :param Target target: The object owning the method to stub.
        :param str method_name: The name of the method to stub.
        """

        self._target = target
        self._method_name = method_name
        self.args = _any
        self.kwargs = _any
        self._is_satisfied = True

        self.and_return(None)

    def and_raise(self, exception):
        """
        Causes the double to raise the provided exception when called.

        :param Exception exception: The exception to raise.
        """
        def proxy_exception():
            raise exception

        self._return_value = proxy_exception
        return self

    def and_return(self, *return_values):
        """
        Causes the double to return the provided values in order.  If multiple
        values are provided, they are returned one at a time in sequence as the double is called.
        If the double is called more times than there are return values, it should continue to
        return the last value in the list.


        :param object return_values: The values the double will return when called,
        """

        if not return_values:
            raise TypeError('and_return() expected at least 1 return value')

        return_values = list(return_values)
        final_value = return_values.pop()

        self._return_value = lambda: return_values.pop(0) if return_values else final_value
        return self

    def and_return_result_of(self, return_value):
        """
        Causes the double to return the result of calling the provided value.

        :param return_value: A callable that will be invoked to determine the double's return value.
        :type return_value: any callable object
        """

        self._return_value = return_value
        return self

    def is_satisfied(self):
        """
        Returns a boolean indicating whether or not the double has been satisfied. Stubs are
        always satisfied, but mocks are only satisifed if they've been called as was declared.

        :return: Whether or not the double is satisfied.
        :rtype: bool
        """
        return self._is_satisfied

    def with_args(self, *args, **kwargs):
        """
        Declares that the double can only be called with the provided arguments.

        :param args: Any positional arguments required for invocation.
        :param kwargs: Any keyword arguments required for invocation.
        """

        self.args = args
        self.kwargs = kwargs
        self._verify_arguments()
        return self

    def with_no_args(self):
        """Declares that the double can only be called with no arguments."""

        self.args = ()
        self.kwargs = {}
        self._verify_arguments()
        return self

    def satisfy_any_args_match(self):
        """
        Returns a boolean indicating whether or not the stub will accept arbitrary arguments.
        This will be true unless the user has specified otherwise using ``with_args`` or
        ``with_no_args``.

        :return: Whether or not the stub accepts arbitrary arguments.
        :rtype: bool
        """

        return self.args is _any and self.kwargs is _any

    def satisfy_exact_match(self, args, kwargs):
        """
        Returns a boolean indicating whether or not the stub will accept the provided arguments.

        :return: Whether or not the stub accepts the provided arguments.
        :rtype: bool
        """

        return self.args == args and self.kwargs == kwargs

    @property
    def return_value(self):
        """
        Extracts the real value to be returned from the wrapping callable.

        :return: The value the double should return when called.
        """

        return self._return_value()

    def _expected_argument_string(self):
        """
        Generates a string describing what arguments the double expected.

        :return: A string describing expected arguments.
        :rtype: str
        """

        if self.args is _any and self.kwargs is _any:
            return 'any args'
        else:
            return '(args={!r}, kwargs={!r})'.format(self.args, self.kwargs)

    def _verify_arguments(self):
        """
        Ensures that the arguments specified match the signature of the real method.

        :raise: ``VerifyingDoubleError`` if the arguments do not match.
        """

        verify_arguments(self._target, self._method_name, self.args, self.kwargs)