"""Try the calculator from the terminal:  python -m landscaper.cli --lang es sod=1200 mulch=6"""
import argparse

from .calculator import build_quote, load_pricing
from .explain import explain_quote


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="en", choices=["en", "es"])
    ap.add_argument("items", nargs="+", help="service=quantity, e.g. sod=1200")
    a = ap.parse_args(argv)
    pricing = load_pricing()
    items = [(k, v) for k, v in (i.split("=", 1) for i in a.items)]
    print(explain_quote(build_quote(items, pricing), pricing, a.lang))


if __name__ == "__main__":
    main()
