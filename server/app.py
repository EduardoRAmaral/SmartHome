import serial.tools.list_ports
from flask import Flask
import autosystem as autosystem
import index as index
import lights as lights
import music as music
import rooms as rooms
import temperature as temperature
import args
from db.db_connection import DBConnection
from Python_UART_Lib import UARTLib
    
"""
    The main function, the first code to be executed when the program is run.
"""
def main():
    argv = args.parse()
    app = Flask("Smart Home")

    # UART Connection
    ports = list(serial.tools.list_ports.comports())

    uart = None
    try:
        p = str(ports[len(ports) - 1]).split(' - ')[0]
        print("Connected to port " + p)
        uart = UARTLib(p, 9600)
    except:
        print("Couldn't connect to Arduino.")
        exit(1)

    # DBConnection
    conn = DBConnection()

    # Routes
    autosystem.AutoSystem().routes(app, conn, uart)
    lights.routes(app, conn, uart)
    music.routes(app)
    temperature.routes(app, uart)
    index.routes(app)
    rooms.routes(app, conn)

    app.config["UPLOAD_FOLDER"] = "music"
    app.run(host=argv.host, port=argv.port, debug=argv.debug)

if __name__ == "__main__":
    main()