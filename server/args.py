import argparse

"""
    The argument parser for the program.

    Returns
    -------
    parser.parse_args() : argparse.Namespace
"""
def parse():
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument("-H", "--host", type=str, default="127.0.0.1", help="Server host address (default: 127.0.0.1)")
    parser.add_argument("-P", "--port", type=int, default=8080, help="Server port (default: 8080)")
    parser.add_argument("-D", "--debug", action="store_true", default=False, help="Enable debug mode (Dangerous!)")

    return parser.parse_args()
