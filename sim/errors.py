"""Project-wide exception hierarchy.

Every error raised deliberately by this project subclasses VellumError, so a
caller can distinguish a Vellum failure from an unrelated one without catching
Exception. Genuine programmer errors (IndexError, AttributeError) are left
alone — the traceback is the useful part.

Depends on: nothing
Used by: every module
"""


class VellumError(Exception):
    """Base for every error raised deliberately by this project."""


class DimensionError(VellumError):
    """A quantity was used with the wrong physical dimensions.

    Raised when incompatible dimensions are combined, or when a value is
    unwrapped at a boundary expecting a different dimension. Never recoverable:
    a dimensional mismatch is a bug in the formula, not a runtime condition.
    """


class InvariantError(VellumError):
    """A physical invariant was violated — conservation, boundedness, ordering.

    Raised by simulation kernels checking their own state. Not used by the
    units layer, which computes nothing.
    """
