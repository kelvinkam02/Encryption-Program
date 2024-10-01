#!/usr/bin/python3

import argparse
import sys

def columnar_transposition(message, key):
    colnum = len(key)
    rownum = (len(message) + colnum - 1) // colnum
    table = [''] * rownum
    for i, char in enumerate(message):
        table[i % rownum] += char
    
    ciphertext = ''.join(table[key.index(str(i))] for i in range(1, colnum + 1))
    return ciphertext

def main():
    parser = argparse.ArgumentParser(description="Part 1: Columnar Transposition Encrypt")
    parser.add_argument("-b", "--blocksize", type=int, default=16, help="Table Size")
    parser.add_argument("-k", "--key", required=True, help="Encryption key")
    parser.add_argument("plaintextfile", nargs="?", type=argparse.FileType("rb"), default=sys.stdin.buffer, help="Input file")
    args = parser.parse_args()
    input_data = args.plaintextfile.read().decode('utf-8')
    ciphertext = columnar_transposition(input_data, args.key)
    sys.stdout.buffer.write(ciphertext.encode('utf-8'))
if __name__ == "__main__":
    main()