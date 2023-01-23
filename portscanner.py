# all code is found on neuralline.com
import socket # imports the socket library
import threading # allows multi-threading
from queue import Queue # allows us to design a queue to run a multi-thread through

target = '127.0.0.1' # use default gateway of the ip address you want to scan
# could use localhost (127.0.0.1)
queue = Queue()
open_ports = []

# method that scans the port that is passed in and returns whether it is open or in use
def portscan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # checks to see if it is an internet socket, using tcp
        sock.connect((target, port))
        return True # shows that the port is open
    except ConnectionError:
        return False     
    except PermissionError:
        return False      

# method that fills the queue with open ports
def fill_queue(port_list):
    for port in port_list:
        queue.put(port) # queue operates on FIFO system

# worker method that the threads will be using to work through the queue until it is empty
def worker():
    while not queue.empty():
        port = queue.get()
        if(portscan(port)):
            print('Port {} is open'.format(port))
            open_ports.append(port)

port_list = range(1, 1024) # fills the list of ports that we want to check
fill_queue(port_list)

thread_list = []

for t in range(10): # will run with 10 threads
    thread = threading.Thread(target=worker) # refers to the worker target function
    thread_list.append(thread)

for thread in thread_list:
    thread.start()

for thread in thread_list:
    thread.join() # will wait for each thread to finish

print('Open ports are: ', open_ports)