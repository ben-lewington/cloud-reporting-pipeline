import sys

from pipeline.sources.sql import get_eng

if __name__ == "__main__":
    eng = get_eng()

    print("Hello, World!")
