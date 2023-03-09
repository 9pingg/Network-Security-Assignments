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
    print("output of the 1st encryption round: ", enc_round1)
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
            s = add_round_key(s, keys[NO_OF_ROUNDS-i])           
            s = inverse_mix_columns(s)
        else:
            s = inv_shift_rows(s)
            s = inverse_substitute_bytes(s)
            s = add_round_key(s, keys[NO_OF_ROUNDS-i])   
        if i == 1:
            d1 = s.copy()
            dec_round1 = get_string_from_state(d1)
        if i == 9:
            d9 = s.copy()
            dec_round9 = get_string_from_state(d9)
        print(i, get_string_from_state(s))
    print("output of the 1st decryption round: ", dec_round1)
    print("output of the 9th decryption round: ", dec_round9)
    final_state = s.copy()
    decrypted_string = get_string_from_state(final_state)
    return decrypted_string


def main(): 
    plain_text = get_random_bytes(16)
    print("plain_text ", plain_text)
    master_key = get_random_bytes(16)
    state = get_state (plain_text)
    key_check = get_state (master_key)
    e = encrypt_128(plain_text, master_key)
    d = decrypt_128(e, master_key)
    print(plain_text,e,d)
    print(plain_text == d)  

    # check 

if __name__ == '__main__':  
    main()
# print(plain_text, master_key, "\n", state, type(state[0][0]))
# print_state(state)
# state = substitute_bytes(state)
# print_state(state, "subbytes done")
# state = shift_rows(state)
# print_state(state, "shift rows done")
# state = add_round_key(state, key_check)
# print_state(state, "add round key done")
# print(get_string_from_state(state))