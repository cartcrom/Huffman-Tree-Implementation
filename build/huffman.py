class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char   # stored as an integer - the ASCII character code value
        self.freq = freq   # the frequency associated with the node
        self.left = None   # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right

    def set_left(self, node):
        self.left = node

    def set_right(self, node):
        self.right = node


def comes_before(a, b):
    """Returns True if tree rooted at node a comes before tree rooted at node b, False otherwise"""
    if a.freq < b.freq or a.freq == b.freq and a.char < b.char:     # Precedence: Frequency (or character if f1 == f2)
        return True
    else:
        return False


def combine(a, b):
    """Creates and returns a new Huffman node with children a and b, with the "lesser node" on the left
    The new node's frequency value will be the sum of the a and b frequencies
    The new node's char value will be the lesser of the a and b char ASCII values"""

    min_val = min(a.char, b.char)           # Find the smaller character
    combo = a.freq + b.freq                 # Combine their frequencies

    new_node = HuffmanNode(min_val, combo)  # Create a new node with these values

    new_node.set_left(a)                    # Set the inputs as children
    new_node.set_right(b)

    return new_node                         # Return the new node


def cnt_freq(filename):
    """Opens a text file with a given file name (passed as a string) and counts the 
    frequency of occurrences of all the characters within that file"""

    f = open(filename, "r")             # Opens source file
    ret_array = [0] * 256               # Creates an array for frequency counts to be stored for each ASCII Values 0-256

    for i in f:                         # Cycles through each line in source file
        for i2 in i:                        # Cycles through each letter in each line
            ret_array[ord(i2)] += 1             # For this letter, add to its frequency count in the array

    f.close()                           # Done viewing source file; close it

    return ret_array                    # Return the finished array of frequency counts


def create_huff_tree(char_freq):
    """Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree"""

    leaves = []                                             # Will hold leaf nodes that will be connected

    for idx, val in enumerate(char_freq):                   # Add each frequency count as a new HuffmanNode
        if val != 0:
            leaves.append(HuffmanNode(idx,val))

    while len(leaves) > 1:                                  # Until there is only one fully completed Huffman Tree:
        leaves = sorted(leaves, key=lambda huffmannode: huffmannode.char)   # Sort by char value
        leaves = sorted(leaves, key=lambda huffmannode: huffmannode.freq)   # And then by frequency

        new_node = combine(leaves.pop(0), leaves.pop(0))    # Create a new node with the two lowest frequency leaves

        leaves.append(new_node)                             # Add this new node to leaves

    return leaves.pop()                                     # The last item in leaves is the finished tree


def create_code(input_tree):
    """Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation 
    as the index into the array, with the resulting Huffman code for that character stored at that location"""

    ret_array = [None] * 256                        # Create storage for binary huffman codes for ASCII values 0-256

    if input_tree is not None:
        codes = rec_get_code(input_tree, "")        # Use recursive helper method to create codes
        for i in codes:                             # For each code created,
            ret_array[i[0]] = i[1]                      # Store it based on the ASCII value it leads to

    return ret_array                                # Return codes


def rec_get_code(current, code):
    """Recursively percolates down a Huffman Tree and stores binary codes if the current node has no children"""
    codes = []
    if current.left is None and current.right is None:  # If current is a leaf node,
        codes.append(tuple((current.char, code)))           # Return a tuple consisting of current's char and final code

    if current.left is not None:                        # If the current node has a left child, percolate left/down
        codes += rec_get_code(current.left, code+"0")       # "0" indicates moving left down a Huffman Tree

    if current.right is not None:                       # If the current node has a right child, percolate right/down
        codes += rec_get_code(current.right, code + "1")    # "1" indicates moving left down a Huffman Tree

    return codes                                        # Return all codes of current node and any nodes beneath it


def create_header(freqs):
    """Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” """

    ret_string = ""
    for idx, val in enumerate(freqs):                       # For each character frequency,
        if val > 0:                                             # If this character is used at all
            ret_string += " " + str(idx) + " " + str(val)           # Add its ASCII value and frequency to header

    return ret_string[1:]                                   # Return header, without first space at beginning


def huffman_encode(in_file, out_file):
    """Takes inout file name and output file name as parameters
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Take not of special cases - empty file and file with only one unique character"""
    freq = cnt_freq(in_file)                        # Obtain character frequency counts
    header = create_header(freq)                    # Create header string with these counts

    code = ""
    codes = create_code(create_huff_tree(freq))     # Create Huffman codes

    in_ = open(in_file, "r")                        # Open the original file

    for i in in_:                                   # For each line in f,
        for i2 in i:                                    # and each letter in each line,
            code += codes[ord(i2)]                          # use the ASCII value as index to get this letters Huff Code

    in_.close()                                     # Close the file

    out = open(out_file, "w")                       # Open the output file

    out.write(header + '\n')                        # Write the header on the first line, end line
    out.write(code)                                 # Write the huffman codes on the second line

    out.close()                                     # Close the file

    return out                                      # Return output


def parse_header(header_string):
    """Transforms a string header into an array of frequencies"""
    return_array = [0] * 256                                # Create an array of frequency counts, 0 by default

    header_vals = list(map(int, header_string.split()))     # Store each header value seperately, casted as an int

    for i in range(0, len(header_vals), 2):                 # For every other item in header_vals,
        return_array[header_vals[i]] = header_vals[i + 1]        # Using i as index, store the next value: the freq cnt

    return return_array                                     # Return frequencies


def huffman_decode(encoded_file, decode_file):
    """Inputs a huffman-encoded file and decodes it"""
    f = open(encoded_file, "r")                     # Open the encoded file to read it

    write_string = ""                               # Create string to add decoded letters to

    for line, val in enumerate(f):                  # For each line of the encoded file,

        if line == 0:                                   # Looking at the header line,
            tree = create_huff_tree(parse_header(val))      # create a Huffman Tree with the frequencies in the header
            current = tree                                  # Start decoding from top of tree

        elif line == 1:                                 # Looking at the Huffman Code line,
            for i in range(len(val)):                       # for each 1 or 0:

                if val[i] == "0":                               # If i is 0,
                    current = current.left                          # percolate left/down in the tree
                elif val[i] == "1":                             # If i is 1,
                    current = current.right                         # percolate right/down in the tree

                if current.left is None and current.right is None:  # If current has no children, it's the end of a code
                    write_string += chr(current.char)                   # write its character
                    current = tree                                      # and return to top of tree

    f.close()                                       # Close the input file

    d = open(decode_file, "w")                      # Open the output file
    d.write(write_string)                           # Write the write_string onto it
    d.close()                                       # Close the output file

    return d                                        # Return the output file