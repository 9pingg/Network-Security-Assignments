import tables

def HexandXor(hex1, hex2):
    '''
    Convert to binary and xor it and  cut the prefix value return hex value.
    '''
    binvalue1 = bin(int(str(hex1), 16))
    binvalue2 = bin(int(str(hex2), 16))
    
    xord = int(binvalue1, 2) ^ int(binvalue2, 2)

    hexed = hex(xord)[2:]

    if len(hexed) != 8:
        hexed = '0' + hexed

    return hexed

def RotationOfWord(word):
    '''
    Takes from 1 to the end, adds on from the start to 1
    '''
    result = word[1:] + word[:1]
    return result

def SubstitutionOfWord(word):
    '''
       In this, Subsitituion of words take place, first loop throug the current word, then check first char, then second char
       if its a letter(a-f) get corresponding decimal  #otherwise just take the value and add 1, get indexbase 
       on row and col (16x16 grid) and get the value from sbox without prefix and at last check length to ensure 
       leading 0s are not forgotton, then form tuple and return subsitute word.
    '''
    sWord = ()
    for i in range(4):
        if word[i][0].isdigit() == False:
            row = ord(word[i][0]) - 86
        else:
            row = int(word[i][0])+1

        if word[i][1].isdigit() == False:
            col = ord(word[i][1]) - 86
        else:
            col = int(word[i][1])+1        
        piecevalue = hex(tables.s_box[row-1][col-1])
        piecevalue = piecevalue[2:]
        if len(piecevalue) != 2:
            piecevalue = '0' + piecevalue
        sWord = (*sWord, piecevalue)

    return ''.join(sWord)
    
def keyExpansion(key):
    '''
    Create a word array w, and to hold 44 tuples,First fill out 4 words based on the key, then fill out the rest based on previews words, rotword, 
    subword and rcon values and if multiple of 4 use rot, sub, rcon etc and at last xor the hex values.
    '''
    w = [()]*44

    for i in range(4):
        w[i] = (key[4*i], key[4*i+1], key[4*i+2], key[4*i+3])

    for i in range(4, 44):
        temp = w[i-1]
        word = w[i-4]

        if i % 4 == 0:
            rotateWord = RotationOfWord(temp)
            subword = SubstitutionOfWord(rotateWord)
            index = int(i/4)
            rconstant = tables.r_const_table[index]
            temp = HexandXor(subword, hex(rconstant)[2:]) 
            
        word = ''.join(word)
        temp = ''.join(temp)

        xorvalue = HexandXor(word, temp)
        w[i] = (xorvalue[:2], xorvalue[2:4], xorvalue[4:6], xorvalue[6:8])
    res = []
    st =""
    count =0
    for i in range(len(w)):
        st+=w[i][0] + w[i][1] + w[i][2] + w[i][3]
        count+=1
        if(count == 4):
            res.append(st)
            count =0
            st=""
    return res

        
        
def start(bytes):
    '''
    #Generating random key of 16 Bytes, and then Expansion of the Keys from key [0,43] and
    generate 11 ley strings in the resultes array.
    '''
    key=[]
    for i in range(0,len(bytes)-1):
        if(i%2==0):
            key.append(bytes[i:i+2])
    res = keyExpansion(key)
    print("Master key: " + "".join(key))
    return res


