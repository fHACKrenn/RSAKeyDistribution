import socket
import threading
import random
import time

# ? key for DES


def generate_session_key() -> str:
    arr = '123456789abcdf'
    key = ''
    for _ in range(16):
        key += arr[random.randint(0, len(arr) - 1)]
    return key


def decrypt1(c) -> None:
    with open(".key/privateKey-b.txt", "r") as f:
        d = f.read().split('\n')
        n = int(d[1])
        d = int(d[0])

    m = pow(int(c), d, n)
    print(f'N1\t: {str(m)[0]}')
    print(f'ID-A\t: {str(m)[1:]}')

    with open(".key/n-a.txt", "w") as f:
        print(str(m)[0], file=f)

    with open(".key/id-a.txt", "w") as f:
        print(str(m)[1:], file=f)
    print(f'raw: {c}, dec: {m}')


def encrypt1() -> str:
    with open(".key/n-a.txt", "r") as f:
        n1 = int(f.read())
        print(f'N1\t: {n1}')

    with open(".key/n-b.txt", "r") as f:
        n2 = f.read()
        print(f'N2\t: {n2}')

    with open(".key/publicKey-a.txt", "r") as f:
        e = f.read().split('\n')
        n = int(e[1])
        e = int(e[0])

    m = n1 * 10 ** len(n2) + int(n2)
    c = pow(m, e, n)
    print(f'raw: {m}, enc: {c}')
    return str(c)


def decrypt2(c) -> None:
    with open(".key/privateKey-b.txt", "r") as f:
        d = f.read().split('\n')
        n = int(d[1])
        d = int(d[0])

    m = pow(int(c), d, n)
    print(f'N2\t: {m}')

    # ? check if N2 is the same
    with open(".key/n-b.txt", "r") as f:
        n1 = f.read().replace('\n', '')
        if n1 != str(m)[0]:
            print('N2 is not the same! Aborting')
            exit()
    print(f'raw: {m}, dec: {c}')


def encrypt2(key) -> str:
    m = int(key, 16)
    with open(".key/publicKey-a.txt", "r") as f:
        e = f.read().split('\n')
        n = int(e[1])
        e = int(e[0])

    c = pow(m, e, n)
    print(f'sending\t\t: {m}')
    print(f'encrypted\t: {c}')
    print()
    return str(c)


def store_symmetric_key(key) -> None:
    with open(".key/symmetric_key.txt", "w") as f:
        print(key, file=f)


def handle_client(client_socket):
    for i in range(2):
        message = ''
        data = client_socket.recv(1024).decode('utf-8')

        if i == 0:
            print('(1) Reciving N1 || ID-A…')
            decrypt1(data)
            print()

            print('(2) Sending N1 || N2…')
            message = encrypt1()
            client_socket.send(message.encode('utf-8'))
            print()

        elif i == 1:
            print('(3) Reciving N2…')
            decrypt2(data)
            print()

            key = generate_session_key()
            store_symmetric_key(key)
            print('(4) Sending Session Key…')
            print(f'Session Key\t: {key}')
            print()
            # ? because it can only encrypt m < n, needs to do repeatedly
            for j in range(0, 16, 2):
                subkey = key[j:j+2]
                message = encrypt2(subkey)
                time.sleep(0.5)
                client_socket.send(message.encode('utf-8'))

    client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Enable SO_REUSEADDR
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(('0.0.0.0', 5555))  # Use an available port number
    server.listen(5)
    print("Server listening for connections...")

    # ? my own code
    client, addr = server.accept()
    print(f"Accepted connection from {addr}")
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()


if __name__ == "__main__":
    start_server()
