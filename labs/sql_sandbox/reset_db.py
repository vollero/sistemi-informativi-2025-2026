"""
Ricrea il database SQLite di base della sandbox SQL.
"""

from sql_utils import crea_database_base, parser_argomenti_sandbox


def main():
    parser = parser_argomenti_sandbox(
        "Ricrea il database SQLite della sandbox",
        include_project=True,
    )
    args = parser.parse_args()

    try:
        db_path = crea_database_base(args.project)
    except FileNotFoundError as exc:
        print(exc)
        raise SystemExit(1) from exc

    print(f"Database ricreato in: {db_path}")


if __name__ == "__main__":
    main()
