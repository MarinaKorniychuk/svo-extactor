import inspect
from typing import Callable


def get_class_from_method(meth: Callable) -> type:
    """Guess the defining class of the method.
    This implementation differentiates between bound methods and “unbound methods“ (functions)
    since in Python 3 there is no reliable way to extract the enclosing class from an “unbound method".

    (The concept of “unbound methods” has been removed from the language. When referencing a method
    as a class attribute, you now get a plain function object.)

    - for a bound method, it simply traverses the MRO.
    - for an “unbound method“, it relies on parsing its qualified name, which is available only from Python 3.3
      and is quite reckless and unrecommended.

    For more details please refer: https://stackoverflow.com/a/25959545
    """
    if inspect.ismethod(meth):
        for cls in inspect.getmro(meth.__self__.__class__):
            if cls.__dict__.get(meth.__name__) is meth:
                return cls
        meth = meth.__func__  # fallback to __qualname__ parsing
    if inspect.isfunction(meth):
        cls = getattr(
            inspect.getmodule(meth),
            meth.__qualname__.split(".<locals>", 1)[0].rsplit(".", 1)[0],
        )
        if isinstance(cls, type):
            return cls
    return getattr(meth, "__objclass__", None)  # handle special descriptor objects
