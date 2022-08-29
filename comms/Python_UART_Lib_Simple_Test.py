#!/usr/bin/python3

import sys
from Python_UART_Lib import UARTLib
from Python_UART_Lib import UART_Code

SERIAL_SPEED = 9600
VERIFICATION_CODE = 0x30403040
CODE_TO_TEST = UART_Code.SET_LIGHTS_OFF

####### TEST1, SIMPLE TEST ############
#The aim of this test is to send an int using any code and get it in return shifted withan xor.
#Just to ensure basic performance.

#getting two parameters: serial port
u = UARTLib(sys.argv[1],SERIAL_SPEED)
(code, data, length) = u.send(CODE_TO_TEST, int(VERIFICATION_CODE).to_bytes(4, 'little'))
if code == UART_Code.ERROR:
    data_decoded = -1
else:
    data_decoded = int.from_bytes(data,'little')  ^ 0x80808080

if data_decoded == VERIFICATION_CODE:
    print("Test OK")
else:
    print("[!!] Test KO")


