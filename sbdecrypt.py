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
    hashobj = hashlib.md5(password.encode())
    return int.from_bytes(hashobj.digest(), byteorder='big')

def genpsuedo(seed, num_bytes):
    lcg = genlc(seed)
    psuedobytes = []
    for _ in range(num_bytes):
        ksbytes = next(lcg)
        psuedobytes.append(ksbytes)
    return psuedobytes

def shuffle(block, key):
    for i in range(len(key)):
        first = key[i] & 0xf  
        second = (key[i] >> 4) & 0xf  
        block[first], block[second] = block[second], block[first]  

def paddingremove(data):
    lengthOfPad = data[-1]  
    if lengthOfPad == 0 or lengthOfPad > 16:
        raise ValueError("Invalid")
    return data[:-lengthOfPad]  

def main():
    parser = argparse.ArgumentParser(description="Decrypt data encrypted with block cipher with cipher block chaining and padding")
    parser.add_argument("password", type=str, help="Password for generating seed")
    parser.add_argument("ciphertext", type=str, help="Path to the ciphertext file")
    parser.add_argument("plaintext", type=str, help="Path to the plaintext file")
    args = parser.parse_args()
    seed = genseed(args.password)

    with open(args.ciphertext, 'rb') as f:
        ciphertext = f.read()

    keystream = genpsuedo(seed, len(ciphertext))
    prev_block = keystream[:16]
    plaintext_blocks = []
    for i in range(0, len(ciphertext), 16):
        shuffled_block = bytearray(16)
        for j in range(16):
            shuffled_block[j] = ciphertext[i+j] ^ keystream[i+j]
    
        shuffle(shuffled_block, keystream[i:i+16])
        plaintext_block = bytearray(16)
        for j in range(16):
            plaintext_block[j] = shuffled_block[j] ^ prev_block[j]
        
        prev_block = ciphertext[i:i+16]
        plaintext_blocks.append(plaintext_block)
    

    plaintext = b''.join(plaintext_blocks)
    plaintext = paddingremove(plaintext)
    with open(args.plaintext, 'wb') as f:
        f.write(plaintext)

if __name__ == "__main__":
    main()
