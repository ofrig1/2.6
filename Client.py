"""
author - Ofri Guz
date   - 19/11/23
client server
"""

import socket
import logging

MAX_PACKET = 1024
IP = '127.0.0.1'
PORT = 8820


def protocol_client_send(message):
    """
    send message with protocol
    :param message:
    :return:
    """
    message_len = len(message)
    final_message = str(message_len) + '$' + message
    return final_message


def protocol_client_receive(my_socket):
    """
    receives message with protocol
    :param my_socket:
    :return:
    """
    cur_char = ''
    message_len = ''
    while cur_char != '$':
        cur_char = my_socket.recv(1).decode()
        if cur_char != '$':
            message_len += cur_char
    return my_socket.recv(int(message_len)).decode()


def main():
    """
    Sends messages to server and get responses
    :return:
    """
    logging.basicConfig(filename="client.log", level=logging.DEBUG)
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.connect((IP, PORT))
        while True:
            msg = input("Enter message: ")
            logging.debug("User input: " + msg)
            my_socket.send(protocol_client_send(msg).encode())
            response = protocol_client_receive(my_socket)
            print(response)
            if msg == "EXIT":
                break
    except socket.error as err:
        print('received socket error ' + str(err))
    finally:
        logging.debug("Closing Client Socket")
        my_socket.close()


if __name__ == "__main__":
    main()
