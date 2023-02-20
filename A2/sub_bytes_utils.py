import tables
def substitute_bytes(state):
    """
    Substitutes each byte in the input matrix using the AES S-Box.
    Args: matrix: A 4x4 matrix of bytes to be substituted.
    Returns: matrix: A 4x4 matrix with each byte substituted using the AES S-Box.
    """
    new_state = state.copy()
    for i in range(4):
        for j in range(4):
            r = state[i][j] // 0x10
            c = state[i][j] % 0x10    
            new_state[i][j] = tables.s_box[r][c]
    return new_state

def inverse_substitute_bytes(state):
    """
    Substitutes each byte in the input matrix using the AES In-S-Box.
    Args: matrix: A 4x4 matrix of bytes to be substituted.
    Returns: matrix: A 4x4 matrix with each byte substituted using the AES In-S-Box.
    """
    new_state = state.copy()
    for i in range(4):
        for j in range(4):
            r = state[i][j] // 0x10
            c = state[i][j] % 0x10    
            new_state[i][j] = tables.inv_s_box[r][c] 
    return new_state