import secrets
from mix_columns_utils import mix_columns, inverse_mix_columns
from shift_rows_utils import shift_rows, inv_shift_rows
from sub_bytes_utils import substitute_bytes, inverse_substitute_bytes
from key_expansion import start

NO_OF_ROUNDS = 10
BLOCK_SIZE = 128


def get_random_bytes(bytes):
    '''
    Generates a random 16 byte hex string (total 32 characters)
    Args: bytes (int): The number of bytes of the hexadecimal string.
    Returns: str: A hexademical string of 16 bytes.
    '''
    return secrets.token_hex(bytes)
    
def get_state(str):
    '''
    Takes in a 16 byte hex string and returns a 4x4 state matrix.
    '''
    state = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            state[j][i] = int(str[8*i+2*j : 8*i + 2*(j+1)], 16)
    return state

def print_state(state, display = ""):
    '''
    Prints the input state matrix in a nicely formatted way.
    '''
    print(display)
    for i in range(4):
        print("\n\n")
        for j in range(4):
            print(str(state[i][j]), end= "\t" )   
    print("\n\n")

def get_string_from_state(state):
    """
    Converts a state matrix of decimal values to a hexadecimal representation and joins them into a single string.
    Args:   state matrix 
    Returns: str: A string containing the concatenated hexadecimal representation of the input values.
    """
    final_state = [0 for _ in range(16)]
    for r in range(4):
        for c in range(4):
            final_state[r + 4 * c] = state[r][c]
    res = ''.join([hex(x)[2:].zfill(2) for x in final_state])
    return res

def add_round_key(state, key_string):
    key = get_state(key_string)
    new_state = state.copy()
    for r in range(4):
        for c in range(4):
            new_state[r][c] = state[r][c] ^ key[r][c]
    return new_state

def getKeyForRoundN(cnt):
    return cnt

def encrypt_128(plain_text, master_key):
    s = get_state (plain_text)
    keys = start(master_key)
    s = add_round_key(s, keys[0])
    print("0", get_string_from_state(s))
    enc_round1 = ""
    enc_round9 = ""
    for i in range (1, NO_OF_ROUNDS+1):
        if i == NO_OF_ROUNDS:
            s = substitute_bytes(s)
            s = shift_rows(s)
            s = add_round_key(s, keys[i])
        else:
            s = substitute_bytes(s)
            s = shift_rows(s)
            s = mix_columns(s)
            s = add_round_key(s, keys[i])

        if i == 1:
            e1 = s.copy()
            enc_round1 = get_string_from_state(e1)
        if i == 9:
            e9 = s.copy()
            enc_round9 = get_string_from_state(e9)
        print(i, get_string_from_state(s))
    print("\noutput of the 1st encryption round: ", enc_round1)
    print("output of the 9th encryption round: ", enc_round9)
    final_state = s.copy()
    cipher = get_string_from_state(final_state)
    return cipher

def decrypt_128(cipher_text, master_key):
    s = get_state (cipher_text)
    keys = start(master_key)
    s = add_round_key(s, keys[NO_OF_ROUNDS])
    print("0", get_string_from_state(s))
    dec_round1 = ""
    dec_round9 = ""
    for i in range (1, NO_OF_ROUNDS+1):
        if i != NO_OF_ROUNDS:
            s = inv_shift_rows(s)
            s = inverse_substitute_bytes(s)
            if i == 1:
                d1 = s.copy()
                dec_round1 = get_string_from_state(d1)
            if i == 9:
                d9 = s.copy()
                dec_round9 = get_string_from_state(d9)
            s = add_round_key(s, keys[NO_OF_ROUNDS-i])           
            s = inverse_mix_columns(s)
        else:
            s = inv_shift_rows(s)
            s = inverse_substitute_bytes(s)
            s = add_round_key(s, keys[NO_OF_ROUNDS-i])   
        
        print(i, get_string_from_state(s))
    print("\noutput of the 1st decryption round: ", dec_round1)
    print("output of the 9th decryption round: ", dec_round9)
    final_state = s.copy()
    decrypted_string = get_string_from_state(final_state)
    return decrypted_string

def get_input(place):
    while True:
        print("Enter a hexadecimal string of length 32 for", place, ": ")
        inp = input()
        if len(inp) != 32:
            print("Error: Hex string must be exactly 32 characters long.")
        elif not all(c in '0123456789abcdef' for c in inp):
            print("Error: Hex string must only contain hexadecimal characters (0-9, a-f).")
        else:
            return inp

def main(): 
    choice = int(input("Enter 0 for user input \nEnter 1 for randomly generated plain_text and master_key: "))
    plain_text = ""
    master_key = ""
    if choice == 1:
        plain_text = get_random_bytes(16)
        print("\nplain_text", plain_text)
        master_key = get_random_bytes(16)
        print("master key", master_key, "\n")
    elif choice == 0:
        plain_text = get_input("plain_text")
        print("\nplain_text:", plain_text)
        master_key = get_input("master_key")
        print("master key:", master_key, "\n")
    else: 
        print("Wrong choice: ", choice)
        return 1
    
    print("==== ENCRYPTION BEGINS ==== \n")
    cipher_text = encrypt_128(plain_text, master_key)
    print("\n==== DECRYPTION BEGINS ==== \n")
    decrypted_text = decrypt_128(cipher_text, master_key)

    print("\nplain_text: ", plain_text)
    print("cipher_text: ", cipher_text)
    print("decrypted_text: ", decrypted_text)
    print(plain_text == decrypted_text)  


if __name__ == '__main__':  
    main()

# plain_text = "dd06309f04da87df644726e304234012"
# master_key = "ddee540d70661c716d12c764c450ecee"