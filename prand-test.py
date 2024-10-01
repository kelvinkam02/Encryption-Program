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

def genpsuedo(seed, numOfBytes):
    lcg = genlc(seed)
    psuedobytes = []
    for _ in range(numOfBytes):
        ksbyte = next(lcg)
        psuedobytes.append(ksbyte)
    return psuedobytes

def main():
    parser = argparse.ArgumentParser(description="Generate pseudorandom bytes from a seed or password")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", "--password", type=str, help="Password for generating seed")
    group.add_argument("-s", "--seed", type=int, help="Seed value for the linear congruential generator")
    parser.add_argument("-n", "--numOfBytes", type=int, default=1, help="Number of pseudorandom bytes to generate")
    args = parser.parse_args()
    if args.password:
        seed = genseed(args.password)
    else:
        seed = args.seed
    psuedobytes = genpsuedo(seed, args.numOfBytes)
    if args.password:
        print(f'using seed={seed}')
    for byte in psuedobytes:
        print(byte)

if __name__ == "__main__":
    main()
