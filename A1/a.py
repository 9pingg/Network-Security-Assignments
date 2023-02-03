import random
import itertools
# TODO implement hash


# function to perform brute force to find key 
def brute_force(ciphertext, plaintext):
    p = ['AA', 'AB', 'AC', 'BB', 'BA', 'BC', 'CC', 'CA', 'CB']
    e_p =  ['AA', 'AB', 'AC', 'BB', 'BA', 'BC', 'CC', 'CA', 'CB']
    dics = []
    for perm in itertools.permutations(p, len(e_p)):
        dics.append(dict(zip(perm, e_p)))
    print("total: ", len(dics))
    keysChecked = 0
    for d in dics:
        if plaintext == decrypt(ciphertext, d): 
            print("Found, total keys checked " , keysChecked, d)
            break
        keysChecked += 1
    return "Not Found"    
    
# function to check whether the entered string is valid or not.
def check(p_text, character_set):
    # only takes in strings with even length
    if len(p_text) % 2 != 0: return False
    # string should only have characters defined in the character set
    return all(c in character_set for c in p_text)

#function to get plain_text as an user input.
def get_plain_text():
    while True :
        print("Enter the plain text\nPlain text should only contain {A,B,C} and the length should be even: ")
        character_set = "ABC"
        p_text = input().strip()
        if check(p_text, character_set):
            return p_text
        else :
            continue

# function returns a random key
def get_key():
    p = ['AA', 'AB', 'AC', 'BB', 'BA', 'BC', 'CC', 'CA', 'CB']
    e_p =  ['AA', 'AB', 'AC', 'BB', 'BA', 'BC', 'CC', 'CA', 'CB']
    # none of the key value should match check
    random.shuffle(e_p)
    # distribute 
    key = {}
    for idx, p_ in enumerate(p):
        key[p_] = e_p[idx: idx+1][0]
    return key

# function takes in key and the plain text as parameters, and returns the cipher text
def encrypt(plain_text, key):
    c_text = ""
    for i in range(0, len(plain_text), 2):
        c_text += key[plain_text[i: i+2]]
    return c_text

# function takes in key and the plain text as parameters, and returns the cipher text
def decrypt(cipher_text, key):
    key = dict((values,key) for key,values in key.items())
    decrypted_text = ""
    for i in range(0, len(cipher_text), 2):
        decrypted_text += key[cipher_text[i: i+2]]
    return decrypted_text

# to check if the hash of decrypted_user_text matches the hash.
def checkMatch(decrypted_text):
    n = len(plain_text)
    decrypted_user_text = decrypted_text[0:n//2]
    decrypted_hash = decrypted_text[n//2:]  
    if decrypted_hash == hash(decrypted_user_text): print("Its a match")
    else : print("Wrong Hash")

if __name__ == "__main__":   
    user_text = get_plain_text()
    plain_text = user_text + hash(user_text)
    print(plain_text)
    key = get_key()
    print(key)
    cipher_text = encrypt(plain_text, key)
    print(cipher_text)
    decrypted_text = decrypt(cipher_text, key)
    print(decrypted_text)
    checkMatch(decrypted_text)
    brute_force(cipher_text, plain_text)