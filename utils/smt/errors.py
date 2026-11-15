"""Keep candidate mistakes distinct from checker and process failures."""


class SolverExecutionError(RuntimeError):
    """The generated checker could not run or returned an invalid protocol result."""


class SolverTimeoutError(TimeoutError):
    """The checker exceeded its wall-clock limit."""


class InvalidInvariantError(ValueError):
    """The candidate could not be constructed as a Boolean Z3 expression."""
