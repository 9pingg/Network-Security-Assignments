# looking at the constant matrix we need gmult function to multiply values to 2 and 3.

mix_column_constant_matrix = [
        [0x02, 0x03, 0x01, 0x01],
        [0x01, 0x02, 0x03, 0x01],
        [0x01, 0x01, 0x02, 0x03],
        [0x03, 0x01, 0x01, 0x02]
]

# looking at this constant matrix we need gmult function to multiply values to 9, b, d, and e.
inv_mix_column_constant_matrix = [
        [0x0e, 0x0b, 0x0d, 0x09],
        [0x09, 0x0e, 0x0b, 0x0d],
        [0x0d, 0x09, 0x0e, 0x0b],
        [0x0b, 0x0d, 0x09, 0x0e]
    ]

def mix_columns(state):
    """ 
    Performs the MixColumns step in AES on the input matrix.
    Args: matrix: A 4x4 matrix to be transformed.
    Returns: matrix: A new 4x4 state  resulting from the MixColumns transformation.
    """
    new_state = [[0 for _ in range(4)] for _ in range(4)]
    for c in range(4):
        word_c = [state[i][c] for i in range(4)]
        s0 = galois_mult(word_c[0], 2) ^ galois_mult(word_c[1], 3) ^ word_c[2] ^ word_c[3]
        s1 = word_c[0] ^ galois_mult(word_c[1], 2) ^ galois_mult(word_c[2], 3) ^ word_c[3]
        s2 = word_c[0] ^ word_c[1] ^ galois_mult(word_c[2], 2) ^ galois_mult(word_c[3], 3)
        s3 = galois_mult(word_c[0], 3) ^ word_c[1] ^ word_c[2] ^ galois_mult(word_c[3], 2)
        new_word_c = [s0, s1, s2, s3]
        for i in range(4):
            new_state[i][c] = new_word_c[i]
    return new_state

def inverse_mix_columns(state):

    new_state = [[0 for _ in range(4)] for _ in range(4)]
    for c in range(4):
        word_c = [state[i][c] for i in range(4)]
        s0 = galois_mult(word_c[0], 0xe) ^ galois_mult(word_c[1], 0xb) ^ galois_mult(word_c[2], 0xd) ^ galois_mult(word_c[3], 0x9)
        s1 = galois_mult(word_c[0], 0x9) ^ galois_mult(word_c[1], 0xe) ^ galois_mult(word_c[2], 0xb) ^ galois_mult(word_c[3], 0xd)
        s2 = galois_mult(word_c[0], 0xd) ^ galois_mult(word_c[1], 0x9) ^ galois_mult(word_c[2], 0xe) ^ galois_mult(word_c[3], 0xb)
        s3 = galois_mult(word_c[0], 0xb) ^ galois_mult(word_c[1], 0xd) ^ galois_mult(word_c[2], 0x9) ^ galois_mult(word_c[3], 0xe)
        new_word_c = [s0, s1, s2, s3]
        for i in range(4):
            new_state[i][c] = new_word_c[i]
    return new_state



# 𝑥×9=(((𝑥×2)×2)×2)+𝑥
# 𝑥×11=((((𝑥×2)×2)+𝑥)×2)+𝑥
# 𝑥×13=((((𝑥×2)+𝑥)×2)×2)+𝑥
# 𝑥×14=((((𝑥×2)+𝑥)×2)+𝑥)×2

def galois_mult(num, mult=2):
    """
    Performs multiplication of two numbers  in GF(2^8), here the mult can only be 2, 3, 9, 11, 13, and 14. range of num is [0,255].
    """
    res = 0xff & (num << 1)
    if mult == 1: 
        return num
    if mult == 2:
        if num < 128: return res
        else: return res ^ 0x1b
    if mult == 3:
        return num ^ galois_mult(num, 2)
    if mult == 9:
        return num ^ galois_mult(galois_mult(galois_mult(num)))
    if mult == 11:
        return num ^ galois_mult(galois_mult(galois_mult(num))) ^ galois_mult(num)  
    if mult == 13:
        return num ^ galois_mult(galois_mult(galois_mult(num))) ^ galois_mult(galois_mult(num))
    if mult == 14:
        return galois_mult(galois_mult(galois_mult(num))) ^ galois_mult(galois_mult(num)) ^ galois_mult(num)
    else: raise Exception("The mult can only be 2, 3, 9, 11, 13, and 14")


