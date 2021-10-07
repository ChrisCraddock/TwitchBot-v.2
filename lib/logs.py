import logging
import socket
from emoji import demojize

sock = socket.socket()
sock.connect(('irc.chat.twitch.tv', 6667))
resp = sock.recv(2048).decode('utf-8')



logging.basicConfig(level = logging.DEBUG,
                    format = '%(asctime)s-%(message)s',
                    datefmt = '%Y-%m-%d_%H:%M:%S',
                    handlers=[logging.FileHandler('chat.log', encoding='utf-8')])


logging.info(demojize(resp))