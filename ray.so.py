from base64 import b64encode
from enum import Enum
from os.path import basename
from sys import stdin


class ColorScheme(Enum):
    CANDY = "candy"
    MIDNIGHT = "midnight"
    SUNSET = "sunset"
    BREEZE = "breeze"


def codeslurp(path):
    if path == "-":
        return b64encode(stdin.buffer.read())
    with open(path, "rb") as istrm:
        return b64encode(istrm.read())


def main():
    from argparse import ArgumentParser
    from urllib.parse import urlencode
    from webbrowser import open_new

    parser = ArgumentParser()
    parser.add_argument(
        "-c",
        "--colors",
        default=ColorScheme.CANDY.value,
        type=lambda c: ColorScheme(c).value,
    )
    parser.add_argument("code")
    parser.add_argument("-l", "--language", default=None)
    parser.add_argument("-b", "--background", action="store_true", default=False)
    parser.add_argument("-p", "--padding", type=int, default=64)
    parser.add_argument("-t", "--title", default=None)
    parser.add_argument("-f", "--darkmode", action="store_false", default=True)
    args = parser.parse_args()
    if not args.title:
        args.title = basename(args.code)
    src = codeslurp(args.code)
    args.code = src
    query = urlencode(
        {
            k: v
            for k, v in args.__dict__.items()
            if k in {"code", "lang", "background", "padding", "title", "darkmode"} and v
        }
    )
    endpoint = f"https://www.ray.so/?{query}"
    open_new(endpoint)


if __name__ == "__main__":
    main()
