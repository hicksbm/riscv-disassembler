# helper.py
# defines useful functions

hex_to_bin = {
    '0' : '0000',
    '1' : '0001',
    '2' : '0010',
    '3' : '0011',
    '4' : '0100',
    '5' : '0101',
    '6' : '0110',
    '7' : '0111',
    '8' : '1000',
    '9' : '1001',
    'a' : '1010',
    'b' : '1011',
    'c' : '1100',
    'd' : '1101',
    'e' : '1110',
    'f' : '1111',
    'A' : '1010',
    'B' : '1011',
    'C' : '1100',
    'D' : '1101',
    'E' : '1110',
    'F' : '1111',
}

def to_binary_string(string : str):
    tokens = string.split("'")
    num_bits = int(tokens[0])
    radix = tokens[1][0]
    values = tokens[1][1::]
    binary_output = ''
    if (radix == 'b'):
        binary_output = values
    if (radix == 'h'):
        for hex_char in values:
            binary_output += hex_to_bin[hex_char]
    # truncate binary_output to num_bits
    binary_output = binary_output[::-1]
    binary_output = binary_output[:num_bits]
    binary_output = binary_output[::-1]
    return binary_output