#!/usr/bin/python3

import sys
from Python_UART_Lib import UARTLib
from Python_UART_Lib import UART_Code

SERIAL_SPEED = 9600
VERIFICATION_CODE = {0x01}
CODE_TO_TEST = UART_Code.SET_LIGHTS_OFF

####### TEST1, Full test ############
#The aim of this test is to send increasing byte sizes from 1 to max = 16.
#Wants to prove the possibility to send various data lengths.


#getting two parameters: serial port
u = UARTLib(sys.argv[1],SERIAL_SPEED)

for i in range(0,16):
    (code, data, length) = u.send(CODE_TO_TEST, bytes(VERIFICATION_CODE))
    if code == UART_Code.ERROR or code == UART_Code.NACK:
        print("[!!] Test failed at iteration " + str(i))
        sys.exit(1)
    else:
        print("Iteration " + str(i) + ": OK")
    VERIFICATION_CODE.add(0x01)

print("Test OK")



