import socket, string, re, requests, json
 
# Set all the variables necessary to connect to Twitch IRC
HOST = "irc.twitch.tv"
NICK = "xxx" #nickname for BOT
PORT = 6667
PASS = "xxx" #oauth key for Twitch
readbuffer = ""
MODT = False
 

# Connecting to Twitch IRC by passing credentials and joining a certain channel
s = socket.socket()
s.connect((HOST, PORT))
s.send(str.encode("PASS " + PASS + "\r\n"))
s.send(str.encode("NICK " + NICK + "\r\n"))
s.send(str.encode("JOIN #CHANNELNAME \r\n")) # replace xxx with channelname

IRC_RE = re.compile(r"(:(?P<nick>[^ !@]+)(\!(?P<user>[^ @]+))?(\@(?P<host>[^ ]+))? )?(?P<command>[^ ]+) (?P<params1>([^:]*))(?P<params2>(:.*)?)")
URL_RE = re.compile(r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*", re.MULTILINE|re.UNICODE)

# Method for sending a message

def send_message(message):
    s.send(str.encode("PRIVMSG #CHANNELNAME :" + message + "\r\n"))

def translate(m):
  m = IRC_RE.match(m.strip())
  if not m:
    return None
  m = m.groupdict()
  m["params"] = m.pop("params1").split()
  if m["params2"]:    m["params"] += [m["params2"][1:]]
  m.pop("params2")
  return m

fd = s.makefile()
while True:
  line = fd.readline().rstrip("\r\n")
  commands = translate(line)
  #print(commands)

  if commands['command'] == 'PRIVMSG':
    user = commands['params'][0]
    msg = commands['params'][1]
    url = URL_RE.match(msg)
    if url:
      print(user)
      print(msg)
      send_message('You have sent a url ' + msg)
    else:
      print(user)
      print(msg)
      send_message('You have sent a message' + user)