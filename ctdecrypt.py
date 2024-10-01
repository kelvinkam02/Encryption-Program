#!/usr/bin/python3

import argparse
import sys

def columnar_transposition(ciphertext, key):
    col = len(key)
    row = (len(ciphertext) + col - 1) // col
    table = [''] * row
    lengthofcol = [len(ciphertext) // col + int(i < len(ciphertext) % col) for i in range(col)]
    start = 0
    for i, length in enumerate(lengthofcol):
        end = start + length
        table[i % row] += ciphertext[start:end]
        start = end

    plaintext = ''.join(table[key.index(str(i))] for i in range(1, col + 1))
    return plaintext

def ctdecrypt(blocksize, key, ciphertext):
    ciphertext_data = ciphertext.read().decode('utf-8')
    ciphertext.close()
    plaintext = columnar_transposition(ciphertext_data, key)
    sys.stdout.buffer.write(plaintext.encode('utf-8'))

def main():
    parser = argparse.ArgumentParser(description="Part 1: Columnar Transposition Decrypt ")
    parser.add_argument("-b", "--blocksize", type=int, default=16, help="Table Size")
    parser.add_argument("-k", "--key", required=True, help="Decryption key")
    parser.add_argument("ciphertextfile", nargs="?", type=argparse.FileType("r"), default=sys.stdin, help="Input file")
    args = parser.parse_args()
    
    ctdecrypt(args.blocksize, args.key, args.ciphertextfile)

if __name__ == "__main__":
    main()
