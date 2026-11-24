# Huffman Coding Compression Tool

A simple Python command-line project that uses a Min-Heap and Huffman Tree to compress and decompress files without losing data.

## Requirements

- Python 3
- No extra libraries required

## Run

Compress a file:

```
python main.py compress input.txt output.huf
```

Decompress it:

```
python main.py decompress output.huf restored.txt
```

## Main concepts

1. Count how often each byte appears.
2. Put the frequencies into a Min-Heap.
3. Join the two smallest nodes until one Huffman tree remains.
4. Make binary codes by following left (0) and right (1).
5. Save the tree in the compressed file so it can be rebuilt later.
6. Decode the bits using the saved tree.

The compressed file contains a small header, the saved Huffman tree, and the encoded data.
