#!/usr/bin/python3
import sys
MODULUS = 256
MULTIPLIER = 1103515245
INCREMENT = 12345

def genlc(seed):
    while True:
        seed = (MULTIPLIER * seed + INCREMENT) % MODULUS
        yield seed

def genseed(password):
    hash_value = hash(password)
    return hash_value % MODULUS

def genks(seed, length):
    lcg = genlc(seed)
    return [next(lcg) for _ in range(length)]

def cipherapply(data, keystream):
    return bytes(a ^ b for a, b in zip(data, keystream))

def readfile(filename):
    with open(filename, 'rb') as f:
        return f.read()

def writefile(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)

def main():
    if len(sys.argv) != 4:
        print("Usage: {} password input_file output_file".format(sys.argv[0]))
        sys.exit(1)
    password = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    seed = genseed(password)
    plaintext = readfile(input_file)
    keystream = genks(seed, len(plaintext))
    ciphertext = cipherapply(plaintext, keystream)
    writefile(ciphertext, output_file)
    print("Encryption/decryption complete.")
if __name__ == "__main__":
    main()
