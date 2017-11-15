from queue import Queue,Empty
from threading import Thread
from time import sleep

class Receiver(Thread):
   def __init__(self, queue):
       Thread.__init__(self)
       self.queue = queue

   def run(self):
      i=0
      while True:
           # a fake receiver; it just puts a message into the queue every .5 sec
           self.queue.put("hello" + str(i))
           i=(i+1)%100
           sleep(0.5)

def main():
   # Create a queue to communicate with the worker threads
   queue = Queue()
   # Create one daemon to receive messages (currently a fake receiver)
   receiver = Receiver(queue)
   # Setting daemon to True will let the main thread exit even though the workers are blocking
   receiver.daemon = True
   receiver.start()

   print('p - prints received messages\ns <msg> - sends message\nq - quits\n')
   cmd = input('& ')
   while (cmd[0] != 'q'):
      if (cmd[0] == 'p'):
         try:
            while (True):
               msg = queue.get(False,None)
               print(msg)
         except Empty:
            print('---')
      cmd = input('& ')

   print('Bye...')

main()
