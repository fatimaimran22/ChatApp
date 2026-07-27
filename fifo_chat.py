import os
from threading import Thread
import sys
from config import FIFO_AB, FIFO_BA

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

        fifo_map = {
            "A": (FIFO_BA, FIFO_AB),
            "B": (FIFO_AB, FIFO_BA),
        }

        self.read_fifo, self.write_fifo = fifo_map[self.role]

    def receive_messages(self):
        while True:
            message = self.reader.readline()

            if not message:
                print("Other User Disconnected.")
                break

            print(message, end="")
            print("->", end="", flush=True)
                

    def open_fifo(self):
            if self.role == 'A':
                self.writer = open(self.write_fifo, "w")
                self.reader = open(self.read_fifo, "r")
            else:
                self.reader = open(self.read_fifo, "r")
                self.writer = open(self.write_fifo, "w")

    def send_messages(self): 
        try:
            while True:
                message = input("->")
                self.writer.write(f"{role}: {message}\n")
                self.writer.flush()
        except KeyboardInterrupt:
            print(f"\n Exiting Process: {self.role}")
            self.cleanup()
            return
        
    def cleanup(self):
        if self.writer:
            self.writer.close()

    def start_receiver(self):
        receiver_thread = Thread(target=self.receive_messages, daemon= True)
        receiver_thread.start()
    

    def run(self):
        print(f"-------User: {self.role}---------")
        self.create_fifos()
        self.open_fifo()
        self.start_receiver()
        self.send_messages()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fifo_chat.py A|B")
        sys.exit(1)

    role = sys.argv[1].upper()
    if role not in ("A", "B"):
        print("Role must be A or B")
        sys.exit(1)

    FifoChat(role).run()

