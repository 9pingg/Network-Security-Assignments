import secrets
import tables

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

def inverse_shift_rows(orignal_state):
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

plain_text = get_random_bytes(16)
master_key = get_state(get_random_bytes(16))
state = get_state (plain_text)
print(plain_text, master_key, "\n", state, type(state[0][0]))
print_state(state)
# print(tables.S_box)
# t = 0xca * 0x0a
# print(str(t), type(tables.S_box[0][0]))
state = substitute_bytes(state)
print_state(state, "subbytes done")
state = shift_rows(state)
print_state(state, "shift rows done")
print_state(master_key, "master key")

state = add_round_key(state, master_key)
print_state(state, "add round key done")
