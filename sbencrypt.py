#!/usr/bin/python3
import argparse
import hashlib
MODULUS = 256
MULTIPLIER = 1103515245
INCREMENT = 12345
def genlc(seed):
    while True:
        seed = (MULTIPLIER * seed + INCREMENT) % MODULUS
        yield seed
def genseed(password):
    hash_object = hashlib.md5(password.encode())
    return int.from_bytes(hash_object.digest(), byteorder='big')

def genpseudo(seed, num_bytes):
    lcg = genlc(seed)
    pseudorandom_bytes = []
    for _ in range(num_bytes):
        keystream_byte = next(lcg)
        pseudorandom_bytes.append(keystream_byte)
    return pseudorandom_bytes

def shuffle(block, key):
    for i in range(len(key)):
        first = key[i] & 0xf 
        second = (key[i] >> 4) & 0xf  
        block[first], block[second] = block[second], block[first]  
def addpadding(data):
    pad_length = 16 - (len(data) % 16)
    padding = bytes([pad_length] * pad_length)  
    return data + padding  
def main():
    parser = argparse.ArgumentParser(description="Encrypt data using block cipher with cipher block chaining and padding")
    parser.add_argument("password", type=str, help="Password for generating seed")
    parser.add_argument("plaintext", type=str, help="Path to the plaintext file")
    parser.add_argument("ciphertext", type=str, help="Path to the ciphertext file")
    args = parser.parse_args()
    seed = genseed(args.password)
    with open(args.plaintext, 'rb') as f:
        plaintext = f.read()
    padded_plaintext = addpadding(plaintext)
    keystream = genpseudo(seed, len(padded_plaintext))
    prev_block = keystream[:16]
    ciphertext_blocks = []
    for i in range(0, len(padded_plaintext), 16):
        temp_block = bytearray(padded_plaintext[i:i+16])
        for j in range(16):
            temp_block[j] ^= prev_block[j]
        shuffle(temp_block, keystream[i:i+16])
        ciphertext_block = bytearray(16)
        for j in range(16):
            ciphertext_block[j] = temp_block[j] ^ keystream[i+j]
        prev_block = ciphertext_block
        ciphertext_blocks.append(ciphertext_block)
    with open(args.ciphertext, 'wb') as f:
        for block in ciphertext_blocks:
            f.write(block)
if __name__ == "__main__":
    main()
