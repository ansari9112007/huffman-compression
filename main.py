
"""Command-line entry point.

python main.py compress   input.txt  output.huf
python main.py decompress output.huf restored.txt
"""
import argparse
import os
import sys

from codes import compress, decompress


def main():
    p = argparse.ArgumentParser(description="Huffman coding compression tool")
    p.add_argument("mode", choices=["compress", "decompress"])
    p.add_argument("input")
    p.add_argument("output")
    args = p.parse_args()

    if not os.path.isfile(args.input):
        sys.exit(f"Error: input file '{args.input}' not found.")

    if args.mode == "compress":
        compress(args.input, args.output)
    else:
        decompress(args.input, args.output)


if __name__ == "__main__":
    main()
