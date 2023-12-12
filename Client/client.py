import socket


def encrypt1() -> str:
    with open(".key/n-a.txt", "r") as f:
        n1 = int(f.read())
        print(f'N1\t: {n1}')

    with open(".key/id-a.txt", "r") as f:
        id = f.read()
        print(f'ID-A\t: {id}')

    with open(".key/publicKey-b.txt", "r") as f:
        e = f.read().split('\n')
        n = int(e[1])
        e = int(e[0])

    m = n1 * 10 ** len(id) + int(id)  # combining n1 and id_a

    if m >= n:
        print('Error! m > n')
        exit()

    c = pow(m, e, n)  # performing encryption
    print(f'raw: {m}, enc: {c}')
    return str(c)


def decrypt1(c) -> None:
    with open(".key/privateKey-a.txt", "r") as f:
        d = f.read().split('\n')
        n = int(d[1])
        d = int(d[0])

    m = pow(int(c), d, n)
    print(f'N1\t: {str(m)[0]}')
    print(f'N2\t: {str(m)[1:]}')

    # ? check if N1 is the same
    with open(".key/n-a.txt", "r") as f:
        n1 = f.read().replace('\n', '')
        if n1 != str(m)[0]:
            print('N1 is not the same! Aborting')
            exit()

    # ? saving N2
    with open(".key/n-b.txt", "w") as f:
        print(str(m)[1:], file=f)
    print(f'raw: {c}, dec: {m}')


def encrypt2() -> str:
    with open(".key/n-b.txt", "r") as f:
        m = int(f.read())
        print(f'N2\t: {m}')

    with open(".key/publicKey-b.txt", "r") as f:
        e = f.read().split('\n')
        n = int(e[1])
        e = int(e[0])

    if m >= n:
        print('Error! m > n')
        exit()

    c = pow(m, e, n)  # performing encryption
    print(f'raw: {m}, enc: {c}')
    return str(c)


def decrypt2(c) -> str:
    with open(".key/privateKey-a.txt", "r") as f:
        d = f.read().split('\n')
        n = int(d[1])
        d = int(d[0])

    print(f'recieved\t: {c}')

    m = pow(int(c), d, n)
    print(f'decrypted\t: {m}')
    print()
    return str(m)


def store_symmetric_key(key) -> None:
    with open(".key/symmetric_key.txt", "w") as f:
        print(key, file=f)


def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = '127.0.0.1'
    server_port = 5555
    client.connect((server_ip, server_port))

    response = ''
    for i in range(0, 2):
        message = ''
        if i == 0:
            print('(1) Sending N1 || ID-A…')
            message = encrypt1()
            print()

        elif i == 1:
            print('(2) Reciving N1 || N2…')
            decrypt1(response)
            print()

            print('(3) Sending N2…')
            message = encrypt2()
            client.send(message.encode('utf-8'))
            print()

            print('(4) Reciving Session Key…')
            key = ''
            for _ in range(8):
                response = client.recv(1024).decode('utf-8')
                key += hex(int(decrypt2(response))).replace('0x', '')
            store_symmetric_key(key)
            print(f'Session Key\t: {key}')
            break
        else:
            break
        client.send(message.encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
    client.close()


if __name__ == "__main__":
    start_client()
