import random
import itertools
import hashlib
import os
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
# function to format the print statement
def printt(msg, val):
    p = "\n\n"
    for i in range(100):
        p+="#"
    p+="\n"
    print(msg + " " + str(val) + p)

# returns random string of given length.
def generate_random_string(len):
    character_set = "ABC"
    s = ''.join(random.choices(character_set,k = len))
    return s

# function returns the hash of a given string
def hash(user_text, toPrint):
    hash_256 = hashlib.sha256(user_text.encode('utf-8')).hexdigest()
    hashstring = ""
    
    # MATCHING A = 0 - 5, B = 6 - 10, C = 11 - 16

    for b in hash_256:
        dec = int(b, 16)
        if dec <= 5 : hashstring += 'A'
        elif dec <= 10 : hashstring += 'B'
        else : hashstring += 'C'
    if toPrint: 
        printt("hash: ", hashstring)
    #printt("length: ", len(hashstring))
    return hashstring
        
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
    decrypted_user_text = decrypted_text[0:n-64]
    decrypted_hash = decrypted_text[-64:]  
    print("hashing the decrypted_user_text to check if it matches the decrypted_hash")
    if decrypted_hash == hash(decrypted_user_text, 0): printt("Its a match, after hashing the user_text: ", hash(decrypted_user_text, 0))
    else : print("Wrong Hash")

# function to perform brute force to find key 
def brute_force(ciphertext, plaintext):
    p = ['AA', 'AB', 'AC', 'BB', 'BA', 'BC', 'CC', 'CA', 'CB']
    e_p =  ['AA', 'AB', 'AC', 'BB', 'BA', 'BC', 'CC', 'CA', 'CB']
    dics = []
    for perm in itertools.permutations(p, len(e_p)):
        dics.append(dict(zip(perm, e_p)))
    print("total possible keys: ", len(dics))
    keysChecked = 0
    for d in dics:
        if plaintext == decrypt(ciphertext, d): 
            print("Key Found: ", d)
            printt("total keys checked: " , keysChecked)
            break
        keysChecked += 1
    return "Not Found"    
    
if __name__ == "__main__":   
    # user_text = get_plain_text()
    # user_text = generate_random_string(5)
    
    print ("Choices:\n1) generate a random string as user_text\n2) input provided by user: ")
    choice = input().strip()
    user_text = ""
    if choice == "1":
        print("random string to be generated, enter length of the string:")
        len = int(input().strip())
        if len % 2 == 0:
            user_text = generate_random_string(len)
        else:
            print("length should be even, restart......")
            quit()
    elif choice == "2":
        user_text = get_plain_text()
    else:
        print("Invalid choice")
        quit()
    printt("user_text:", user_text)
    plain_text = user_text + hash(user_text,1)
    printt("plain_text:", plain_text)
    key = get_key()
    printt("key:", key)

    print(type(key), type(user_text))
    cipher_text = encrypt(plain_text, key)
    printt("cipher_text:", cipher_text)
    decrypted_text = decrypt(cipher_text, key)
    printt("decrypted_text:", decrypted_text)
    checkMatch(decrypted_text)
    brute_force(cipher_text, plain_text)