#-*- coding:utf-8 -*-
import socket
import requests
import json
import redis

import config
import rolecheck

from datetime import datetime

HOST = config.server['host']
PORT = config.server['port']
PREFIX = config.bot['prefix']

NICK = config.bot['botnick']
CHANNEL = config.bot['channel']
PASS = config.bot['oauth']

irc = socket.socket()
irc.connect((HOST, PORT))
irc.send(bytes(f'PASS oauth:{PASS}\r\n', 'utf-8'))
irc.send(bytes(f'NICK siro_32\r\n', 'utf-8'))
irc.send(bytes(f'JOIN #{CHANNEL}\r\n', 'utf-8'))

def sendmsg(message):
    irc.send(bytes(f'PRIVMSG #{CHANNEL} :{message}\r\n', 'utf-8'))
    with open(f'db/{CHANNEL}/botactions.txt', 'a', encoding = 'utf-8') as f:
        f.write(f'{datetime.utcnow()} | BOT MESSAGE: {message}\n')

while True:
    try:
        buffer = irc.recv(2048).decode('utf-8')

        if buffer == 'PING :tmi.twitch.tv\r\n':
            irc.send(bytes('PONG :tmi.twitch.tv\r\n', 'utf-8'))

        sw = buffer.find('PRIVMSG')
        
        if sw != -1:
            arr = buffer.split('\r\n')
            arr1 = arr[0].split('#')
            arr2 = arr1[1].split(':')
            arr3 = arr2[0].split(' ')

            susr = arr3[0]
            rmsg = arr2[1]

            print(f'{susr} said {rmsg}')

            rc = rolecheck.UserRole(susr)

            # Commands
            if rmsg == 'zzz':
                sendmsg('zzz')

            with open(f'db/{CHANNEL}/chatlog.txt', 'a', encoding = 'utf-8') as f:
                if rc.ishost():
                    f.write(f'{datetime.utcnow()} | STREAMER ({susr}): {rmsg}\n')
                elif rc.isstaff():
                    f.write(f'{datetime.utcnow()} | STAFF ({susr}): {rmsg}\n')
                elif rc.isglobalmod():
                    f.write(f'{datetime.utcnow()} | GLOBAL_MOD ({susr}): {rmsg}\n')
                elif rc.ismod():
                    f.write(f'{datetime.utcnow()} | MOD ({susr}): {rmsg}\n')
                elif rc.isadmin():
                    f.write(f'{datetime.utcnow()} | ADMIN ({susr}): {rmsg}\n')
                else:
                    f.write(f'{datetime.utcnow()} | {susr}: {rmsg}\n')

        else:
            print(buffer)

    except socket.error:
        print('Socket ERROR. Closing socket...')
    except socket.timeout:
        print('Socket TIMEOUT. Closing socket...')