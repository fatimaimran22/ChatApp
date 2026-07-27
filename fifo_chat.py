import os
from threading import Thread
import sys
from config import FIFO_AB, FIFO_BA
import time

class FifoChat:
    def __init__(self, role):
        self.role = role.upper()
        self.read_fifo = None
        self.write_fifo = None
        self.reader = None
        self.writer = None


    def create_fifos(self):
        if not os.path.exists(FIFO_AB):
            os.mkfifo(FIFO_AB)

        if not os.path.exists(FIFO_BA):
            os.mkfifo(FIFO_BA)

        if self.role == 'A':
            self.read_fifo = FIFO_BA
            self.write_fifo = FIFO_AB
        elif self.role == 'B':
            self.read_fifo = FIFO_AB
            self.write_fifo = FIFO_BA
        else:
            raise ValueError("Role must be A or B")

    def open_fifos(self):
        if self.role == 'A':
            self.writer = open(self.write_fifo, "w")
            self.reader = open(self.read_fifo, "r")
        else:
            self.reader = open(self.read_fifo, "r")
            self.writer = open(self.write_fifo, "w")

    def receive_messages(self):
        try:
            while True:
                message = self.reader.readline()

                if not message:
                    print("Other User Disconnected.")
                    break

                print(message, end="")
                print("->", end="", flush=True)
                
        except Exception as e:
            print(e)

    def send_messages(self):
        try:
            while True:
                message = input("->")
                self.writer.write(f"{role}: {message}\n")
                self.writer.flush()
        except KeyboardInterrupt:
            print(f"\n Exiting Process: {self.role}")
            self.cleanup()
            sys.exit(0)


    def cleanup(self):
        if self.reader:
            self.reader.close()
        if self.writer:
            self.writer.close()

    def start_receiver(self):
        receiver_thread = Thread(target=self.receive_messages, daemon= True)
        receiver_thread.start()
    

    def run(self):
        try:
            self.create_fifos()
            self.open_fifos()
            self.start_receiver()
            self.send_messages()

        except KeyboardInterrupt:
            print(f"\n Exiting Process: {self.role}")
            self.cleanup()
            sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fifo_chat.py A|B")
        sys.exit(1)

    role = sys.argv[1].upper()
    if role not in ("A", "B"):
        print("Role must be A or B")
        sys.exit(1)

    FifoChat(role).run()

