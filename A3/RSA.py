import random

def to_find_gcd(a, b):
    while b != 0:
        temp = b
        b = a % b
        a = temp
    return a


def extended_gcd_algo(a1, a2):
    if a1 == 0:
        return (a2, 0, 1)
    
    g, x, y = extended_gcd_algo(a2 % a1, a1)
    new_x = y - (a2 // a1) * x
    new_y = x
    return (g, new_x, new_y)

def mod_inverse_func(a, mod):
    g, x, y = extended_gcd_algo(a, mod)
    if g != 1:
        return None
    else:
        return x % mod


def checkPrime(n):
    if n <= 1: return False
    # Check if the number is divisible by any integer from 2 to sqrt(num)
    sqrt_num = int(n** 0.5) + 1
    for x in range(2, sqrt_num):
        if n % x == 0:
            return False
    return True

def generate_keypair(choice):
    # to generate keypair ((e, n), (d, n))
    if choice ==0:
        p = random.randint(100, 1000)
        while not checkPrime(p):
            p += 1
        q = random.randint(1000, 10000)
        while not checkPrime(q):
            q += 1
        n = p * q
        phi = (p-1) * (q-1)
        e = random.randint(2, phi-1)
        while to_find_gcd(e, phi) != 1:
            e += 1
        d = mod_inverse_func(e, phi)
        return ((e, n), (d, n))
    else:
        print("Enter Prime numbers p and q")
        p = int(input())
        q = int(input())
        n = p * q
        phi = (p-1) * (q-1)
        e = random.randint(2, phi-1)
        while to_find_gcd(e, phi) != 1:
            e += 1
        d = mod_inverse_func(e, phi)
        return ((e, n), (d, n))

if __name__=="__main__":

    public, private = generate_keypair()
    
