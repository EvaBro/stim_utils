from typing import Optional
from psychopy import parallel


class ButtonBox():
    port: Optional[parallel.ParallelPort] = None 
    ctrl_port: Optional[parallel.ParallelPort] = None 

    def __init__(self, address:int):
        self.port = parallel.ParallelPort(address=address)
        self.ctrl_port = parallel.ParallelPort(address+2)

        # initialize the port
        if self.ctrl_port.readPin(7) == 0:
            self.ctrl_port.setPin(7, 1)  # set direction bit in control register to input mode

    def getAllButtons(self):
        data = self.port.port.Inp32(self.port.base+1)
        return [0,(data >> 3) & 1,(data >> 4) & 1,0,0,0,0,0]
        