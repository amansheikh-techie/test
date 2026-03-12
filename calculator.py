"""Simple calculator module providing basic operations and a command-line interface."""

import sys


def add(a, b):
    """Return the sum of two numbers."""
    return a + b


def subtract(a, b):
    """Return the difference of two numbers (a - b)."""
    return a - b


def multiply(a, b):
    """Return the product of two numbers."""
    return a * b


def divide(a, b):
    """Return the quotient of two numbers. Raises ZeroDivisionError on division by zero."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


def _parse_args(args=None):
    import argparse

    parser = argparse.ArgumentParser(description="Basic calculator")
    parser.add_argument("operation", choices=["add", "sub", "mul", "div"],
                        help="operation to perform")
    parser.add_argument("x", type=float, help="first operand")
    parser.add_argument("y", type=float, help="second operand")
    return parser.parse_args(args)


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    opts = _parse_args(argv)
    ops = {
        "add": add,
        "sub": subtract,
        "mul": multiply,
        "div": divide,
    }
    func = ops[opts.operation]
    try:
        result = func(opts.x, opts.y)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    else:
        print(result)
        return result


if __name__ == "__main__":
    main()
