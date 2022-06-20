import socket
from mp3stego import Steganography

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server


def receive_file():
    mp3file_content = b''
    while True:
        data = sock.recv(1024)
        mp3file_content += data
        print(len(mp3file_content))
        if not data:
            break

    return mp3file_content


script = "ls -l\n echo hello world"
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))

    with open('test.mp3', 'rb') as mp3file:
        s = Steganography(quiet=False)
        # hide the script in the test_out.mp3 file (which is the test.mp3 file with the hidden script)
        s.hide_message('test.mp3', 'test_out.mp3', script)

    with open('test_out.mp3', 'rb') as mp3file_out:
        sock.send(mp3file_out.read())  # send the mp3 file with the hidden script to the server
