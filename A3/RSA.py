import random

def To_find_gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def extended_gcd_algo(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd_algo(b % a, a)
        return (g, x - (b // a) * y, y)

def mod_inverse(a, m):
    g, x, y = extended_gcd_algo(a, m)
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
        while To_find_gcd(e, phi) != 1:
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
        while To_find_gcd(e, phi) != 1:
            e += 1
        d = mod_inverse(e, phi)
        return ((e, n), (d, n))

if __name__=="__main__":

    public, private = generate_keypair()
    
