# continuation

*A module for handling continuations in Python*

The `continuation` module is another attempt for providing a clean way of embedding continuation-passing-style (CPS) expressions in a Python script. While not the single purpose of this module, tail-recursion can easely be acheived with it.

The module internally uses standard and pythonic features (mostly lambda calculus and exceptions) and doesn't attempt to "inspect" the stack or the functions for modifying them. For this reason, it should integrate smoothly with any version of Python. Furthermore, nested systems of continuations are correctly handled.

### Installation

Just type:

    pip install continuation

or (for a system-wide installation):

    sudo pip install continuation

Since the module is rather small, the single file `__init__.py` can also be quickly renamed as `continuation.py` and directly put in the directory of a given project for _ad hoc_ purposes.

### Usage

Import the module with:

    from continuation import with_CC, with_continuation

Here is a tail-recursive version of the factorial function:

    @with_continuation
    def k_factorial(k):
        def _inner(n, f):
            return f if n < 2 else (k << k_factorial)(n-1, n*f)
        return _inner
    factorial = lambda n: (with_CC >> k_factorial)(n, 1)
    
    print(factorial(7))
    
The following example shows that recursion doesn't use the stack any longer:
    
    def without_continuation(n, a):
        return without_continuation(n-1, a) if n > 0 else a
    
    @with_continuation
    def k_stress(k):
        def _inner(n, a):
            return (k << k_stress)(n-1, a) if n > 0 else a
        return _inner
    stress = lambda n, a: (with_CC >> k_stress)(n, a)
    
    try:
        print(without_continuation(5000, 42))
    except RuntimeError as e:
        print(e.message)
    print(stress(5000, 42))
    
The following example shows how to pass the continuation from a function to another one:
    
    @with_continuation
    def k_identity(k):
        def _inner(x):
            return x
        return _inner
    
    @with_continuation
    def k_factorial(k):
        def _inner(n, f):
            return (k << k_identity)(f) if n < 2 else (k << k_factorial)(n-1, n*f)
        return _inner
    
    factorial = lambda n: (with_CC >> k_factorial)(n, 1)
    
    print(factorial(7))
