from const import *
import socket
import binascii


def hex_to_ascii(hex_string):
    try:
        # Convert hexadecimal to bytes
        hex_bytes = binascii.unhexlify(hex_string)

        # Decode bytes to ASCII
        ascii_string = hex_bytes.decode('ascii')

        return ascii_string
    except binascii.Error as e:
        print(f"Error: {e}")
        return None


def ascii_to_hex(ascii_string):
    try:
        # Encode ASCII to bytes
        ascii_bytes = ascii_string.encode('ascii')

        # Convert bytes to hexadecimal
        hex_string = binascii.hexlify(ascii_bytes).decode('ascii')

        return hex_string
    except UnicodeEncodeError as e:
        print(f"Error: {e}")
        return None

# Python3 code for the above approach

# Hexadecimal to binary conversion


def hex_to_bin(s):
    s = s.upper()
    mp = {'0': "0000",
          '1': "0001",
          '2': "0010",
          '3': "0011",
          '4': "0100",
          '5': "0101",
          '6': "0110",
          '7': "0111",
          '8': "1000",
          '9': "1001",
          'A': "1010",
          'B': "1011",
          'C': "1100",
          'D': "1101",
          'E': "1110",
          'F': "1111"}
    bin = ""
    for i in range(len(s)):
        bin = bin + mp[s[i]]
    return bin


# Binary to hexadecimal conversion


def bin2hex(s):
    mp = {"0000": '0',
          "0001": '1',
          "0010": '2',
          "0011": '3',
          "0100": '4',
          "0101": '5',
          "0110": '6',
          "0111": '7',
          "1000": '8',
          "1001": '9',
          "1010": 'A',
          "1011": 'B',
          "1100": 'C',
          "1101": 'D',
          "1110": 'E',
          "1111": 'F'}
    hex = ""
    for i in range(0, len(s), 4):
        ch = ""
        ch = ch + s[i]
        ch = ch + s[i + 1]
        ch = ch + s[i + 2]
        ch = ch + s[i + 3]
        hex = hex + mp[ch]

    return hex

# Binary to decimal conversion


def bin2dec(binary):

    binary1 = binary
    decimal, i, n = 0, 0, 0
    while (binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return decimal

# Decimal to binary conversion


def dec2bin(num):
    res = bin(num).replace("0b", "")
    if (len(res) % 4 != 0):
        div = len(res) / 4
        div = int(div)
        counter = (4 * (div + 1)) - len(res)
        for i in range(0, counter):
            res = '0' + res
    return res

# Permute function to rearrange the bits


def permute(k, arr, n):
    # print(len(k), k)
    permutation = ""
    for i in range(0, n):
        index = arr[i] - 1
        # print(f"i: {i}, arr[i]: {arr[i]}, index: {index}")
        permutation = permutation + k[index]
    return permutation

# shifting the bits towards left by nth shifts


def shift_left(k, nth_shifts):
    s = ""
    for i in range(nth_shifts):
        for j in range(1, len(k)):
            s = s + k[j]
        s = s + k[0]
        k = s
        s = ""
    return k

# calculating xow of two strings of binary number a and b


def xor(a, b):
    ans = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            ans = ans + "0"
        else:
            ans = ans + "1"
    return ans


def encrypt(pt, rkb, rk):
    pt = hex_to_bin(pt)

    # Initial Permutation
    pt = permute(pt, initial_perm, 64)
    print("After initial permutation", bin2hex(pt))

    # Splitting
    left = pt[0:32]
    right = pt[32:64]
    for i in range(0, 16):
        # Expansion D-box: Expanding the 32 bits data into 48 bits
        right_expanded = permute(right, exp_d, 48)

        # XOR RoundKey[i] and right_expanded
        xor_x = xor(right_expanded, rkb[i])

        # S-boxex: substituting the value from s-box table by calculating row and column
        sbox_str = ""
        for j in range(0, 8):
            row = bin2dec(int(xor_x[j * 6] + xor_x[j * 6 + 5]))
            col = bin2dec(
                int(xor_x[j * 6 + 1] + xor_x[j * 6 + 2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))
            val = sbox[j][row][col]
            sbox_str = sbox_str + dec2bin(val)

        # Straight D-box: After substituting rearranging the bits
        sbox_str = permute(sbox_str, per, 32)

        # XOR left and sbox_str
        result = xor(left, sbox_str)
        left = result

        # Swapper
        if (i != 15):
            left, right = right, left
        print("Round ", i + 1, " ", bin2hex(left),
              " ", bin2hex(right), " ", rk[i])

    # Combination
    combine = left + right

    # Final permutation: final rearranging of bits to get cipher text
    cipher_text = permute(combine, final_perm, 64)
    return cipher_text


# This code is contributed by Aditya Jain

def start_client():
    # Set the server IP address and port
    server_ip = '127.0.0.1'
    server_port = 5555

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((server_ip, server_port))
    print(f"Connected to {server_ip}:{server_port}")

    with open(".key/symmetric_key.txt", "r") as f:
        key = f.read().replace('\n', '')
        key = hex_to_bin(key)
        key = permute(key, keyp, 56)

        # Splitting
        left = key[0:28]  # rkb for RoundKeys in binary
        right = key[28:56]  # rk for RoundKeys in hexadecimal

        rkb = []
        rk = []
        for i in range(0, 16):
            # Shifting the bits by nth shifts by checking from shift table
            left = shift_left(left, shift_table[i])
            right = shift_left(right, shift_table[i])

            # Combination of left and right string
            combine_str = left + right

            # Compression of key from 56 to 48 bits
            round_key = permute(combine_str, key_comp, 48)

            rkb.append(round_key)
            rk.append(bin2hex(round_key))
        rkb_rev = rkb[::-1]
        rk_rev = rk[::-1]

    while True:
        # Get user input for the message to send
        plain_text = input("Enter a message (8 chars): ")
        # print(len(plain_text), plain_text)
        cipher_text = bin2hex(encrypt(ascii_to_hex(plain_text), rkb, rk))
        print(f'raw: {plain_text}\nenc: {cipher_text}')

        if plain_text.lower() == 'exit':
            break

        # Send the message to the server
        client_socket.send(cipher_text.encode('utf-8'))

        # Receive and print the server's response
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Server response: {response}")
        plain_text = hex_to_ascii(bin2hex(encrypt(response, rkb_rev, rk_rev)))
        print(f'raw: {response}\ndec: {plain_text}')

    # Close the connection when done
    client_socket.close()


if __name__ == "__main__":
    start_client()
    # text = 'sususapi'
    # hexx = ascii_to_hex(text)
    # print(len(hexx), hexx)
    # print(len(hex_to_bin(hexx)), hex_to_bin(hexx))
