# __main__.py
import logging
import coloredlogs

from CETNext.cli import cli

logging.basicConfig(
    filename='latest.log',
    filemode='w',
    encoding='utf-8',
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(funcName)s: %(message)s"
)
coloredlogs.install(level="INFO", fmt="%(asctime)s - %(levelname)s - %(funcName)s: %(message)s")

def main():
    cli()

if __name__ == "__main__":
    main()