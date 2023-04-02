import random

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def mod_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError('Modular inverse does not exist')
    else:
        return x % m

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def generate_keypair(choice):
    if choice ==0:
        p = random.randint(100, 1000)
        while not is_prime(p):
            p += 1
        q = random.randint(1000, 10000)
        while not is_prime(q):
            q += 1
        n = p * q
        phi = (p-1) * (q-1)
        e = random.randint(2, phi-1)
        while gcd(e, phi) != 1:
            e += 1
        d = mod_inverse(e, phi)
        return ((e, n), (d, n))
    else:
        print("Enter Prime numbers p and q")
        p = int(input())
        q = int(input())
        n = p * q
        phi = (p-1) * (q-1)
        e = random.randint(2, phi-1)
        while gcd(e, phi) != 1:
            e += 1
        d = mod_inverse(e, phi)
        return ((e, n), (d, n))

def encrypt(public_key, plaintext):
    e, n = public_key
    ciphertext = [(ord(char) ** e) % n for char in plaintext]
    return ciphertext

def decrypt(private_key, ciphertext):
    d, n = private_key
    plaintext = [chr((char ** d) % n) for char in ciphertext]
    return ''.join(plaintext)

if __name__=="__main__":

    public, private = generate_keypair()
    print(public)
    print(private)
    message = 'Hello, world!'
    encrypted_message = encrypt(public, message)
    decrypted_message = decrypt(private, encrypted_message)

    