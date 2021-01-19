#!/usr/bin/env python3
import socket
import time
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def handle_request(conn, addr):
  #recieve data, wait a bit, then send it back
  full_data = conn.recv(BUFFER_SIZE)
  print(full_data)
  conn.sendall(full_data)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            
            #allow for multiple connection with a Process daemon
            p = Process(target=handle_request, args=(conn, addr))
            p.daemon = True
            p.start()
            print("Started process ", p)

if __name__ == "__main__":
    main()
