"""Run with: python test_huffman.py"""
import os
import tempfile
import unittest

from codes import compress, decompress


class TestHuffman(unittest.TestCase):
    def roundtrip(self, data):
        d = tempfile.mkdtemp()
        a, b, c = (os.path.join(d, x) for x in ("a.txt", "a.huf", "c.txt"))
        with open(a, "wb") as f:
            f.write(data)
        compress(a, b)
        decompress(b, c)
        with open(c, "rb") as f:
            self.assertEqual(f.read(), data)
        return os.path.getsize(b)

    def test_normal_text(self):
        data = b"hello huffman world " * 200
        self.assertLess(self.roundtrip(data), len(data))

    def test_single_char(self):
        self.roundtrip(b"aaaaaaaa")

    def test_empty(self):
        self.roundtrip(b"")

    def test_unicode(self):
        self.roundtrip("नमस्ते दुनिया ".encode("utf-8") * 50)


if __name__ == "__main__":
    unittest.main()