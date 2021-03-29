# Imports
import sys
from typing import *


# Main
def main(argc: int, argv: List[str]):
    from flask import Flask
    application = Flask(__name__)
    application.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
