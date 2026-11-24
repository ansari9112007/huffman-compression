
"""compress() and decompress() functions."""
import struct
import sys

from bitio import BitReader, BitWriter
from huffman_tree import build_codes, build_tree, read_tree, write_tree

MAGIC = b"HUF1"


def compress(in_path, out_path):
    with open(in_path, "rb") as f:
        data = f.read()

    header = MAGIC + struct.pack(">Q", len(data))
    payload = b""
    if data:
        root = build_tree(data)
        codes = build_codes(root)
        w = BitWriter()
        write_tree(root, w)
        for b in data:
            w.bits(codes[b])
        payload = w.finish()

    with open(out_path, "wb") as f:
        f.write(header + payload)

    in_size, out_size = len(data), len(header) + len(payload)
    print(f"Original:   {in_size} bytes")
    print(f"Compressed: {out_size} bytes")
    if in_size:
        print(f"Ratio:      {out_size / in_size:.2%} of original")
    if out_size >= in_size:
        print("Note: output is not smaller (file too small for Huffman to help).")


def decompress(in_path, out_path):
    with open(in_path, "rb") as f:
        blob = f.read()
    if blob[:4] != MAGIC:
        sys.exit("Error: not a valid Huffman-compressed file.")
    (n,) = struct.unpack(">Q", blob[4:12])

    out = bytearray()
    if n:
        r = BitReader(blob, start=12)
        root = read_tree(r)
        if root.is_leaf():
            out = bytearray([root.byte]) * n
        else:
            for _ in range(n):
                node = root
                while not node.is_leaf():
                    node = node.right if r.bit() else node.left
                out.append(node.byte)

    with open(out_path, "wb") as f:
        f.write(out)
    print(f"Decompressed {len(out)} bytes -> {out_path}")
# Displaying codec.py.