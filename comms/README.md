# Communication codes
This are the codes used for communication between arduino and raspberry pi. The full documentation about the installation, usage and functionalities is found [here](https://github.com/fssecur3/smart-home/wiki/Communications-between-Raspberry-Pi-and-Arduino).

## Files in this directory

**Arduino_UART_Lib:** Source code of the library for Arduino.
**Python_UART_Lib.py:** Source code of the library for Python.
**Arduino_Lib_UART_Full:** Folder containing an Arduino Project to test the UART Library. The aim of this test is to send increasing byte sizes from 1 to max = 16. Wants to prove the possibility to send various data lengths. Can be used as an example of the library usage.
**Python_UART_Lib_Full_Test.py:** Folder containing a Python file used as a sender of the above explained test. Can be used as an example of the library usage.
**Arduino_Lib_UART_Test:** Simple test to ensure data comunication. Files for Arduino.
**Python_UART_Lib_Simple_Test.py:** Simple test to ensure data comunication. File for raspberry.

