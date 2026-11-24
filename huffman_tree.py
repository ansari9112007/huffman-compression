"""Huffman tree: build with a min-heap, generate codes, (de)serialize."""
import heapq
from collections import Counter


class Node:
    def __init__(self, freq=0, byte=None, left=None, right=None):
        self.freq = freq
        self.byte = byte
        self.left = left
        self.right = right

    def is_leaf(self):
        return self.left is None and self.right is None


def build_tree(data):
    freq = Counter(data)
    heap = [(f, i, Node(f, byte=b)) for i, (b, f) in enumerate(sorted(freq.items()))]
    heapq.heapify(heap)
    counter = len(heap)
    while len(heap) > 1:
        f1, _, a = heapq.heappop(heap)
        f2, _, b = heapq.heappop(heap)
        heapq.heappush(heap, (f1 + f2, counter, Node(f1 + f2, left=a, right=b)))
        counter += 1
    return heap[0][2]


def build_codes(root):
    if root.is_leaf():  # only one distinct byte in file
        return {root.byte: "0"}
    codes = {}
    stack = [(root, "")]
    while stack:
        node, prefix = stack.pop()
        if node.is_leaf():
            codes[node.byte] = prefix
        else:
            stack.append((node.right, prefix + "1"))
            stack.append((node.left, prefix + "0"))
    return codes


def write_tree(node, writer):
    if node.is_leaf():
        writer.bit(1)
        writer.byte(node.byte)
    else:
        writer.bit(0)
        write_tree(node.left, writer)
        write_tree(node.right, writer)


def read_tree(reader):
    if reader.bit():
        return Node(byte=reader.byte())
    left = read_tree(reader)
    right = read_tree(reader)
    return Node(left=left, right=right)