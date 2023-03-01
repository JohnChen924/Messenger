import socket
import json
import time

class DirectMessage(dict):
  
  def __init__(self):
    """
    declare variables
    """
    self.recipient = None
    self.message = None
    self.timestamp = None

  def organ(self, a, b, c):
    """
    returns a list containing a dictionary of lists of messages and lists
    time of messages by users
    """
    _list = []
    for i in range(len(a)):
      self.recipient = a[i]
      self.message = b[i]
      self.timestamp = c[i]
      d = {'message': self.message, 'from': self.recipient, 'timestamp':self.timestamp}
      _list.append(d)
    return _list
   
class Oops(Exception):
  """
  custom exception class
  """
  pass
  
class DirectMessenger:
  
  def __init__(self, dsuserver=None, username=None, password=None):
    """
    declaring variables and setting the variables with information recieved
    when the class is called. Will automatically join to the given server of
    the user's choice and to the port 3021. self.token will be filled
    """
    self.token = None
    self.dsu = dsuserver
    self.username = username
    self.password = password
    self.old = None
    self.new = None
    self.join()
  
  def join(self):
    """
    joins to user input server and port 3021. Will add the token recieved from
    srv_msg to self.token
    """
    a = True
    join = {"join":{"username":self.username,"password":self.password}}
    join = json.dumps(join)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
          client.connect((self.dsu, 3021))      
        except socket.gaierror:
          print("UNKNOWN SERVER")
          a = False #if a becomes false then the code below will not work
        if a:
          send = client.makefile('w')
          recv = client.makefile('r')
          send.write(join + '\r\n')
          send.flush()
          srv_msg = recv.readline()
          srv_msg = json.loads(srv_msg)
          try:
            self.token = srv_msg['response']['token'] #add value from token dictionary value to self.token
          except KeyError:
            raise Oops("USERNAME AND PASSWORD DO NOT MATCH") #stop program and show the error
          
        
  def send(self, message:str, recipient:str) -> bool:
    """
    connect to the server and port, and send message to the recipient from the parameter
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((self.dsu, 3021))

        send = client.makefile('w')
        recv = client.makefile('r')
        
        while True:
          print(self.username, "has connected to ", recipient, "\n")
          msg = {"token":self.token, "directmessage": {"entry": message,"recipient": recipient, "timestamp": str(time.time())}}
          msg = json.dumps(msg)
          send.write(msg + '\r\n')
          send.flush()
          print("Message sent")
          break

		
  def retrieve_new(self) -> list:
    """
    retrieve new messages from the server
    """
    return self.retriever("new")
     
  def retrieve_all(self) -> list:
    """
    retrieve all messages from the server
    """
    return self.retriever("all")
  
  def retriever(self,_type):
    """
    helps with retrieving messages and adding to lists
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
          client.connect((self.dsu, 3021))      
        except socket.gaierror:
          print("UNKNOWN SERVER")

        send = client.makefile('w')
        recv = client.makefile('r')
        
        join = {"token":self.token, "directmessage": _type}
        join = json.dumps(join)
        send.write(join + '\r\n')
        send.flush()
        msg = recv.readline()
    msg = json.loads(msg)
    try:
      srv_msg = msg['response']['messages'] #add value from token dictionary value to self.token
    except KeyError:
      raise Oops("NO USERNAME/PASSWORD INPUT") #stop program and show the error
    a = srv_msg
    for i in range(len(a)):
      a[i]['timestamp'] = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(a[i]['timestamp']))))
    #changes the format of the time to the time we are used to seeing
    q = []
    for i in range(len(a)):
      q.append(a[i]['from'])
             
    mylist = list(dict.fromkeys(q))
    _input = []
    _time = []
    for i in range(len(mylist)):
      x = []
      z = []
      for j in range(len(a)):
          if a[j]['from'] == mylist[i]:
              x.append(a[j]['message'])
              z.append(a[j]['timestamp'])
      _input.append(x)
      _time.append(z)
    a = DirectMessage()
    return a.organ(mylist,_input,_time)
