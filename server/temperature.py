from Python_UART_Lib import UART_Code
import struct

def routes(app, uart):
    """
        Route to get the temperature of a room in the house
        
        Returns
        -------
        {"message": <temp>}
            Message with the room's temperature
    """
    @app.route("/temperature")
    def temperature():
        (code, data, len) = uart.send(UART_Code.TMP,  None)
        
        if code == UART_Code.ERROR:
            return { "message": "Could not read the temperature." }, 500
        else:
            temp = struct.unpack('f', bytes(data))
            return { "message": f"{temp[0]}" }, 200
