#!/usr/bin/env python3
import socket, sys
import time
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def get_remote_ip(host):
  print(f'Getting IP for {host}')
  try:
    remote_ip = socket.gethostbyname( host )
  except socket.gaierror:
    print('Hostname could not be resolved. Exiting')
    sys.exit()
  print(f'Ip address of {host} is {remote_ip}')
  return remote_ip

def handle_request(conn, addr, end):
  #recieve data, wait a bit, then send it back
  send_full_data = conn.recv(BUFFER_SIZE)
  print(f"Sending recieved data {send_full_data} to google")
  end.sendall(send_full_data)

  end.shutdown(socket.SHUT_WR)

  data = end.recv(BUFFER_SIZE)
  print(f"Sending recieved data {data} to client")

  conn.send(data)

def main():
  host = "www.google.com"
  port = 80

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Starting proxy server")
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    #bind socket to address
    s.bind((HOST, PORT))
    #set to listening mode
    s.listen(1)
    
    #continuously listen for connections
    while True:
        conn, addr = s.accept()
        print("Connected by", addr)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as end:
          print("Connecting to Google")
          remote_ip = get_remote_ip(host)

          end.connect((remote_ip, port))
          
          #allow for multiple connection with a Process daemon
          p = Process(target=handle_request, args=(conn, addr, end))
          p.daemon = True
          p.start()
          print("Started process ", p)
          
        conn.close()

if __name__ == "__main__":
    main()
