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

# 𝑥×9=(((𝑥×2)×2)×2)+𝑥
# 𝑥×11=((((𝑥×2)×2)+𝑥)×2)+𝑥
# 𝑥×13=((((𝑥×2)+𝑥)×2)×2)+𝑥
# 𝑥×14=((((𝑥×2)+𝑥)×2)+𝑥)×2
def galois_mult(num, mult):
    """
    Performs multiplication of two numbers  in GF(2^8), here the mult can only be 2 and 3. range of num is [0,255].
    """
    res = 0xff & (num << 1)
    if mult == 2:
        if num < 128: return res
        else: return res ^ 0x1b
    if mult == 3:
        return num ^ galois_mult(num, 2)

        