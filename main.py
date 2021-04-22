# Imports
import sys
from declarations import *

from routes import *


# Main
def main(argc: int, argv: List[str]):
    from application import run
    run()


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
