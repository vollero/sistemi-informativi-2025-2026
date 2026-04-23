#!/usr/bin/env python3
"""
Punto di ingresso del laboratorio palestra REPL.
"""

import sys

from app_db import PalestraDatabase
from app_repl import PalestraREPL


def main():
    reset = "--reset" in sys.argv
    db = PalestraDatabase()
    db.initialize(reset=reset)

    app = PalestraREPL(db)
    app.esegui()


if __name__ == "__main__":
    main()
