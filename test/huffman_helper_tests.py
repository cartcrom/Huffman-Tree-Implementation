import unittest
import subprocess

import sys
sys.path.append(sys.path[0] + "/build")

from huffman import *


class TestList2(unittest.TestCase):
    def test_rec_get_code(self):
        testlist = cnt_freq("../src/file2.txt")
        testtree = create_huff_tree(testlist)
        codes = rec_get_code(testtree, "")
        self.assertEqual(codes, [(97, '0000'), (102, '0001'), (98, '001'), (99, '01'), (100, '1')])

if __name__ == '__main__':
   unittest.main()
