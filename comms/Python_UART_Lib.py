#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Joaquim Ferrer Sagarra

from enum import IntEnum
from serial import Serial
import signal

MAX_COUNT = 3  # Max 3 retries


class UART_Code(IntEnum):

    ACK = 0
    NACK = 1
    LUM = 2
    TMP = 3
    SET_LIGHTS_ON = 4
    SET_LIGHTS_OFF = 5
    GET_LIGHTS = 6
    SET_AUTOMODE = 7
    GET_AUTOMODE = 8
    OCCUPIED = 9
    ERROR = 10


class UARTLib:

    def __init__(self, port, speed):
        self.s = Serial(port, speed, timeout = 0.5)

    def __inside_send(self, in_code, in_data):

        data = []
        code = UART_Code.ERROR
        length = -1
        byte_count = 0
        data_len = 0

        if in_data is not None:
            data_len = len(in_data)

        header = chr(in_code | data_len << 4)
        try:
            if in_data is not None:
                to_write = header.encode() + in_data
            else:
                to_write = header.encode()
            self.s.write(to_write)
            byte = self.s.read(1)
            code = int.from_bytes(byte, 'little') & 0x0F  # Lower bits
            length = (int.from_bytes(byte, 'little') & 0xF0) >> 4  # Upper bits
            while byte_count < length:
                data.append(int.from_bytes(self.s.read(1),'little'))
                byte_count = byte_count + 1
            signal.alarm(0)
        except Exception as e:
            signal.alarm(0)
            print(e)
            return UART_Code.ERROR, None, -1
            self.s.read(1000);   #Empty buffer --> Sometimes receiving double response.

        return code, data, length

    def send(self, code, data):

        count = 0
        out_code = UART_Code.ERROR
        out_data = None
        out_length = -1

        if data != None and type(data) != bytes:
            raise Exception("code parameter must be type bytes on None")

        (out_code, out_data, out_length) = self.__inside_send(code, data)
        while out_code == UART_Code.ERROR and count < MAX_COUNT:
            #print("Retry")
            (out_code, out_data, out_length) = self.__inside_send(code, data)
            count = count + 1
        self.s.reset_input_buffer();
        return out_code, out_data, out_length


