import unittest
import filecmp
import subprocess

import sys
sys.path.append(sys.path[0] + "/build")

from huffman import *


class TestList(unittest.TestCase):

    def test_cnt_freq(self):
        freqlist = cnt_freq("../src/file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0] 
        self.assertListEqual(freqlist[97:104], anslist)

    def test_create_huff_tree(self):
        freqlist = cnt_freq("../src/file2.txt")
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree.freq, 32)
        self.assertEqual(hufftree.char, 97)
        left = hufftree.left
        self.assertEqual(left.freq, 16)
        self.assertEqual(left.char, 97)
        right = hufftree.right
        self.assertEqual(right.freq, 16)
        self.assertEqual(right.char, 100)

    def test_create_header(self):
        freqlist = cnt_freq("../src/file2.txt")
        self.assertEqual(create_header(freqlist), "97 2 98 4 99 8 100 16 102 2")

    def test_create_code(self):
        freqlist = cnt_freq("../src/file2.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        self.assertEqual(codes[ord('d')], '1')
        self.assertEqual(codes[ord('a')], '0000')
        self.assertEqual(codes[ord('f')], '0001')

    def test_01_textfile(self):
        huffman_encode("../src/file1.txt", "test_outputs/file1_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file

        self.assertEqual(filecmp.cmp("test_outputs/file1_out.txt", "../src/file1_soln.txt"), True)

    def test_02_textfile(self):
        huffman_encode("../src/file2.txt", "test_outputs/file2_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file

        self.assertEqual(filecmp.cmp("test_outputs/file2_out.txt", "../src/file2_soln.txt"), True)

    def test_03_textfile(self):
        huffman_encode("../src/declaration.txt", "test_outputs/declaration_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file

        self.assertEqual(filecmp.cmp("test_outputs/declaration_out.txt", "../src/declaration_soln.txt"), True)

    def test_04_textfile(self):
        huffman_encode("../src/multiline.txt", "test_outputs/multiline_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file

        self.assertEqual(filecmp.cmp("test_outputs/multiline_out.txt","../src/multiline_soln.txt"), True)

    def compare_huffman_freqs(self):
        encoded_freqs = cnt_freq("../src/declaration.txt")
        f = open("../src/declaration.txt", "r")

        for i, val in enumerate(f):
            if i == 0:
                decoded_freqs = parse_header(val)

        f.close()

        self.assertEqual(encoded_freqs, decoded_freqs)

    def test_huffman_decode_output(self):
        huffman_decode("../src/file1_soln.txt", "test_outputs/file1_decode.txt")

        self.assertEqual(filecmp.cmp("test_outputs/file1_decode.txt","../src/file1.txt"), True)


    def test_huffman_decode_output2(self):
        huffman_decode("../src/declaration_soln.txt", "test_outputs/declaration_decode.txt")

        self.assertEqual(filecmp.cmp("test_outputs/declaration_decode.txt","../src/declaration.txt"), True)

    def test_huffman_decode_output3(self):
        huffman_decode("../src/multiline_soln.txt", "test_outputs/multiline_decode.txt")

        self.assertEqual(filecmp.cmp("test_outputs/multiline_decode.txt","../src/multiline.txt"), True)


if __name__ == '__main__':
   unittest.main()
