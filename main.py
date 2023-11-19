"""
author - Ofri Guz
date   - 19/11/23
socket server
"""
import socket
from datetime import datetime
import random
import logging

IP = '127.0.0.1'
PORT = 8820
QUEUE_SIZE = 1
MAX_PACKET = 1024
PERSON_NAME = "Ofri"
TIME = 'TIME'
RAND = 'RAND'
NAME = 'NAME'
EXIT = 'EXIT'


def protocol_send(message):
    # send message with protocol
    message_len = len(message)
    final_message = str(message_len) + '$' + str(message)
    print("final msg "+final_message)
    return final_message


def protocol_receive(my_socket):
    # receives message with protocol
    cur_char = ''
    message_len = ''
    while cur_char != '$':
        cur_char = my_socket.recv(1).decode()
        # print("char "+cur_char)
        if cur_char != '$':
            message_len += cur_char
    return my_socket.recv(int(message_len)).decode()


def time():
    # Function: TIME
    # Input:
    # Output: Current Time (on client server)
    current_time = datetime.now().strftime("%H:%M:%S")
    return current_time


def name():
    # Function: NAME
    # Input:
    # Output: "My name is" + Name (on client server)
    name_message = "My name is " + PERSON_NAME
    return name_message


def rand():
    # Function: RAND
    # Input:
    # Output: Random Number between 1-10
    random_num = random.randint(1, 10)
    return random_num


def exit_client(client_socket):
    # Function: EXIT
    # Input: Client Socket
    # Output: Send "Socket Connection Closed" to client server
    client_socket.send("Socket Connection Closed".encode())


def random_word(client_socket):
    # Function: not one of the available ones
    # Input: Client Socket
    # Output: Send "Not one of the available functions" to client server
    print("Client sent random word")
    client_socket.send(protocol_send("Not one of the available functions").encode())


def handle_msg(client_socket):
    # Function: Handles message that client sends
    # Input: Client socket
    # Output: Sends client what they requested
    try:
        while True:
            request = protocol_receive(client_socket)
            # print("Client sent " + request)
            if request == TIME:
                client_socket.send(protocol_send(time()).encode())
            elif request == NAME:
                client_socket.send(protocol_send(name()).encode())
            elif request == RAND:
                client_socket.send(protocol_send(str(rand())).encode())
            elif request == EXIT:
                exit_client(client_socket)
                break
            else:
                random_word(client_socket)
            logging.debug("Server received " + request)
            print('server received ' + request)
    except socket.error as err:
        print('received socket error on client socket' + str(err))
    finally:
        client_socket.close()
        logging.debug("Client Socket Disconnected")


def main():
    logging.basicConfig(filename="server.log", level=logging.DEBUG)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        while True:
            client_socket, client_address = server_socket.accept()
            handle_msg(client_socket)
    finally:
        server_socket.close()


if __name__ == "__main__":
    assert 0 < rand() <= 10, "Random number not between 1 & 10"
    assert time() == datetime.now().strftime("%H:%M:%S"), "Time not correct"
    assert name() == "My name is " + PERSON_NAME
    main()
