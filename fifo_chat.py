import os
from threading import Thread
from config import FIFO_AB, FIFO_BA


# Process  Read FIFO  Write FIFO 
# A         fifo_ba    fifo_ab   
# B         fifo_ab    fifo_ba   


class FifoChat:
    def __init__(self, role):
        self.role = role.upper()


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

    def run(self):
        self.create_fifos()
        print("Reading from:", self.read_fifo)
        print("Writing to:", self.write_fifo)


if __name__ == "__main__":
    role = input(" Enter Role (A/B): ")
    FifoChat(role).run()

