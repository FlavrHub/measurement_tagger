import os
import sys
import json
import argparse

from tagger import Tagger
from converter import Converter
from extracter import Extracter

from utils import get_class, hyponyms


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--measurement_type", default="d", choices=["d", "t", "m"],
                        help="Type of measurement to tag (default = distance)")
    parser.add_argument("-t", "--text", help="Name of text file to tag")
    parser.add_argument("--return_unconverted", action="store_true",
                        help="Return measurements that have not been normalised")

    args = parser.parse_args()
    params = json.load(open("params.json", "r"))

    name = args.text
    text_dir = os.path.join(os.getcwd(), "text")
    path = os.path.join(text_dir, name)

    try:
        m = params[args.measurement_type]
    except KeyError:
        print("Invalid measurement type!")
        sys.exit()

    container = get_class("measurement.measures", m["container"])
    formatter = get_class("formatter", m["formatter"])
    converter = Converter(container, args.return_unconverted)

    tags = hyponyms(m["synset"])
    tagger = Tagger(tags, m["right_mods"])

    extracter = Extracter(path, tagger, formatter, converter)
    extracter.extract()
    print(extracter)


if __name__ == "__main__":
    main()
