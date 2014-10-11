#!/usr/bin/python
# -*- coding: utf-8 -*-

# Based off of ajfs woryea bot

import sys
import socket
import string
import json
import random
import csv
import hashlib
import cmds
from m8ball import *

try:
    with open('eat.json', 'rb') as fp:
        stuff_i_ate = json.load(fp)
except:
    stuff_i_ate = {}

## Default Settings
CHAD_NICK=""
CHAD_IGNORE=False
CHAD_SILENCE=""

HOST="anarchy.esper.net"
PORT=6667
NICK="arcdick"
IDENT="arctic"
REALNAME="arctic"
CHAN="#gg2test"
KEY = "420"


# if len(sys.argv[0])>0:
    # exec(open(sys.argv[1]).read())

NICKSERV_IDENT=None

OWNER=""
OWNER_VERIFY="~arctsdsddic@75-140-75-64.dhcp.mtpk.ca.charter.com"

LOGINMD5 = '1a50c4f531d1f061b8689c69daac7583'

## Variables
joined=False
ops = []
tell = {}
admins = []
ignore = []

# f = open('ignore.csv', 'r+')
# try:
    # ignore = list(csv.reader(f))
# finally:
    # f.close()
    # del f

readbuffer=""

m8ball = []
m8ball.append("Don't count on it")
m8ball.append('My reply is no')
m8ball.append('It is certain')
m8ball.append('Outlook not so good')
m8ball.append('Most likely')
m8ball.append('Concentrate and ask again')
m8ball.append('Yes definitely')
m8ball.append('Without a doubt')
m8ball.append('It is decidedly so')
m8ball.append('My sources say no')
m8ball.append('Signs point to yes')
m8ball.append('Reply hazy try again')
m8ball.append('Better not tell you now')
m8ball.append('Very doubtful')
m8ball.append('Cannot predict now')
m8ball.append('You may rely on it')
m8ball.append('Ask again later')
m8ball.append('As I see it, yes')
m8ball.append('Yes')
m8ball.append('Outlook good')


def send(msg):
    line = "%s\r\n" % msg
    try:
        s.send(line)
        print line
    except UnicodeEncodeError:
        print "UNICODE ENCODE ERROR: %s"%line
def send_silent(msg):
    line = "%s\r\n" % msg
    try:
        s.send(line)
    except UnicodeEncodeError:
        print "UNICODE ENCODE ERROR: %s"%line
def sendprivmsg(user,msg):
    send("PRIVMSG %s :%s" % (user,msg))
def sendtochan(msg):
    sendprivmsg(CHAN,msg)
def sendcommand(command,user,msg):
    send(command+"%s :%s" % (user,msg))
def sendmode(user,mode,msg=''):
    send("MODE "+user+" "+mode+" "+msg)

s=socket.socket( )
s.connect((HOST, PORT))
send("NICK %s\r\n" % NICK)
send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))

while 1:
    readbuffer=readbuffer+s.recv(1024)
    temp=string.split(readbuffer, "\n")
    readbuffer=temp.pop()
    
    for line in temp:
        line=string.rstrip(line)
        print line
        line=string.split(line)

        if line[0]=="PING":
            send("PONG %s" % line[1])
            if joined != True:
                send_silent("JOIN %s" % (CHAN + ' ' + KEY))
                joined==True
        if line[1]=="JOIN":
            userbits = string.split(line[0].lstrip(':'),'!')
            user = userbits[0]
            userip = userbits[1]
            #sendtochan(userip)
            if (str(user) in tell):
                send("PRIVMSG %s :%s" % (CHAN,user + ", " + tell[str(user)]))
                del tell[str(user)]
        elif line[1]=="INVITE" and line[3].lstrip(':')==CHAN:
            send("JOIN %s" % (CHAN))
        elif line[1]=="MODE": ## MODE
            if line[2]==NICK and line[3].count('+i')>0 and not NICKSERV_IDENT: ## +i - Identified
                if joined==False:
                    send("JOIN %s" % (CHAN))
                    joined==True
            if line[2]==CHAN and line[3].count('+o')>0: ## User opped
                if not (line[4] in ops):
                    ops.append(line[4])
            elif line[2]==CHAN and line[3].count('-o')>0: ## User deopped
                if line[4] in ops:
                    ops.remove(line[4])
            if line[2]==CHAN and line[3].count('+v')>0: ## User voiced
                if not (line[4] in voice):
                    voice.append(line[4])
            elif line[2]==CHAN and line[3].count('-v')>0: ## User devoiced
                if line[4] in voice:
                    voice.remove(line[4])
        elif line[1]=="353": ## Names list
            if line[4]==CHAN and line[2]==NICK:
                for i in line[5:]:
                    i = i.lstrip(':')
                    if i[0]=='@':
                        ops.append(i.lstrip('@'))
        elif line[1]=="PRIVMSG":
            userbits = string.split(line[0].lstrip(':'),'!')
            user = userbits[0]
            chan = line[2]
            msg = line[3:]
            msg[0] = msg[0].lstrip(':')
            msgtext = ' '.join(msg)
            if (str(user) in tell):
                send("PRIVMSG %s :%s" % (CHAN,user + ", " + tell[str(user)]))
                del tell[str(user)]
            if msgtext[0] == '!':
                
                _cmd = msg[0][1:]
                cmd = _cmd.lower()
                if cmd == 'say':
                    sendtochan(' '.join(msg[1:]))
                elif cmd == 'tell':
                    tell[str(''.join(msg[1]))] = str(user + ' wanted to tell you: '+ ' '.join(msg[2:]))
                    sendtochan("I'll tell him the next time I see him")
                elif cmd == 'm8ball':
                    try:
                        i = random.randint(0,len(m8ball) - 1)
                        sendtochan(m8ball[i])
                    except:
                        sendtochan(i)
                elif cmd == 'login':
                    if (hashlib.md5(''.join(msg[1])).hexdigest() == LOGINMD5):
                        admins.append(userbits[1])
                        sendprivmsg(user, "Successfully logged in")
                    else:
                        sendprivmsg(user, "No")
                if (userbits[1] == OWNER_VERIFY or userbits[1] in admins):
                    if cmd == 'kick':
                        sendcommand("KICK ",CHAN,' '.join(msg[1:]))
                    elif cmd == 'op':
                        sendmode(CHAN,"+o"," ".join(msg[1:]))
                    elif cmd == 'voice':
                        sendmode(CHAN,"+v"," ".join(msg[1:]))
                    elif cmd == 'nick':
                        send("NICK %s"%' '.join(msg[1:]))
                    elif cmd == 'exec':
                        try:
                            sendtochan(eval(' '.join(msg[1:])))
                            pass
                        except:
                            sendtochan('Error: ' + str(sys.exc_info()[0]))
                            pass
