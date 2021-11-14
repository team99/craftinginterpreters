import logging
import sys

from dataclasses import dataclass

# we use this to ensure we don't try to execute that
# has a known error
# it also lets us exit with a non-zero exit code
# if had_error, sys.exit(65)
had_error = False

logging.basicConfig(
    format="%(asctime)s %(levelgname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def throw_error(line: int, message: str):
    report_error(line, message)


def report_error(line: int, message: str):
    logging.error(f"{line}: {message}")

    had_error = True


@dataclass
class Token:
    ...


@dataclass
class Scanner:

    source: str

    def scan_tokens(self) -> list[Token]:
        return []


def run(lines: str):
    scanner = Scanner(lines)
    tokens = scanner.scan_tokens(lines)
    [print(t) for t in tokens]


def main(filename: str):
    logging.info(f"file name {filename}")
    with open(filename) as file:
        text = file.read()

    run(text)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 -m yelin-python.lox [script]")

    main(sys.argv[1])

    # TODO to add run prompt
