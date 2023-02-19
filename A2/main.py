import secrets
import tables

NO_OF_ROUNDS = 10
BLOCK_SIZE = 128

# gives a 16 byte hex string (total 32 characters)
def get_random_bytes(bytes):
    return secrets.token_hex(bytes)
    
 # takes in a 16 byte hex string and returns a state matrix
def get_state(str):
    state = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            state[j][i] = int(str[8*i+2*j : 8*i + 2*(j+1)], 16)
    return state

# prints the state, in a matrix form 
def print_state(state, display = ""):
    print(display)
    for i in range(4):
        print("\n\n")
        for j in range(4):
            print(str(state[i][j]), end= "\t" )   
    print("\n\n")


def substitute_bytes(state):
    new_state = state.copy()
    for i in range(4):
        for j in range(4):
            r = state[i][j] // 0x10
            c = state[i][j] % 0x10    
            new_state[i][j] = tables.s_box[r][c]
    return new_state

def inverse_substitute_bytes(state):
    new_state = state.copy()
    for i in range(4):
        for j in range(4):
            r = state[i][j] // 0x10
            c = state[i][j] % 0x10    
            new_state[i][j] = tables.inv_s_box[r][c] 
    return new_state

# ShiftRows transformation consists of shifting the rows of the state array by count bytes.
def shift_rows(orignal_state):
    state = orignal_state.copy()
    state[1][0], state[1][1], state[1][2], state[1][3] = state[1][1], state[1][2], state[1][3], state[1][0]
    state[2][0], state[2][1], state[2][2], state[2][3] = state[2][2], state[2][3], state[2][0], state[2][1]
    state[3][0], state[3][1], state[3][2], state[3][3] = state[3][3], state[3][0], state[3][1], state[3][2]
    return state

def inv_shift_rows(orignal_state):
    state = orignal_state.copy()
    state[1][0], state[1][1], state[1][2], state[1][3] = state[1][3], state[1][0], state[1][1], state[1][2]
    state[2][0], state[2][1], state[2][2], state[2][3] = state[2][2], state[2][3], state[2][0], state[2][1]
    state[3][0], state[3][1], state[3][2], state[3][3] = state[3][1], state[3][2], state[3][3], state[3][0]
    return state

def add_round_key(state, key):
    new_state = state.copy()
    for r in range(4):
        for c in range(4):
            new_state[r][c] = state[r][c] ^ key[r][c]
    return new_state


def mix_columns(state):
    #TODO
    return
def inverse_mix_columns(state):
    #TODO
    return
def key_expansion(master_key):
    #TODO
    return

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

def encrypt_128(plain_text, master_key):
    s = get_state (plain_text)
    keys = key_expansion(master_key)
    s = add_round_key(s, keys[0])

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
    final_state = s.copy()
    cipher = get_string_from_state(final_state)
    return cipher

def decrypt_128(cipher_text, master_key):
    s = get_state (cipher_text)
    keys = key_expansion(master_key)

    s = add_round_key(s, keys[NO_OF_ROUNDS])
    for i in range (1, NO_OF_ROUNDS+1):
        if i == NO_OF_ROUNDS:
            s = inv_shift_rows(s)
            s = inverse_substitute_bytes(s)
            s = add_round_key(s, keys[NO_OF_ROUNDS-i])           
            s = inverse_mix_columns(s)
           
        else:
            s = inv_shift_rows(s)
            s = inverse_substitute_bytes(s)
            s = add_round_key(s, keys[NO_OF_ROUNDS-i])   
    final_state = s.copy()
    decrypted_string = get_string_from_state(final_state)
    return decrypted_string

plain_text = get_random_bytes(16)
master_key = get_random_bytes(16)
state = get_state (plain_text)
key_check = get_state (master_key)
print(plain_text, master_key, "\n", state, type(state[0][0]))
print_state(state)
state = substitute_bytes(state)
print_state(state, "subbytes done")
state = shift_rows(state)
print_state(state, "shift rows done")
state = add_round_key(state, key_check)
print_state(state, "add round key done")
print(get_string_from_state(state))