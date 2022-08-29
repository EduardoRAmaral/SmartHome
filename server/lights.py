from flask import request

from Python_UART_Lib import UART_Code

"""
    Sensors routing
"""
def routes(app, conn, uart):

    #####################################################
    #                                                   #
    #                    Luminosity                     #
    #                                                   #
    #####################################################
    """
        Routing with all the information regarding the luminosity

        Returns
        -------
        dict , 200
            Object with all the information regarding the luminosity levels
   """
    @app.route("/minilum")
    def minilum():
        lum = request.args.get('lum')
        msg = {}

        if (lum):
            (code, data, len) = uart.send(UART_Code.LUM,  int(lum).to_bytes(4, 'little'))
            
            if (code == UART_Code.ERROR):
                msg = {"message": "Couldn't edit minimum luminosity level."}
                return msg, 500

            elif (code == UART_Code.NACK):
                msg = {"message": "Invalid luminosity value provided."}
                return msg, 400
            else:
                conn.set_lum_lvl(lum)
                data_decoded = int.from_bytes(data,'little')
                msg = {"message": data_decoded}
        else:
            lum = conn.get_lum_lvl()
            msg = {"message": lum[0]}

        return msg, 200
    
    @app.route("/luminosity")
    def luminosity():
        (code, data, len) = uart.send(UART_Code.LUM,  None)

        if code == UART_Code.ERROR:
            msg = {"message": "Couldn't get luminosity level."}
            return msg, 500
        else:
            data_decoded = int.from_bytes(data, "little")
            return {"message": data_decoded}, 200


    #####################################################
    #                                                   #
    #                      Lights                       #
    #                                                   #
    #####################################################
    """
        Routing with all the information regarding the lights
        
        Route: /lights?room=<int>

        Returns
        -------
        dict , 200
            Object with all the information regarding the lights
   """
    @app.route("/lights")
    def lights():
        room = request.args.get('room')
        enabled = request.args.get('enabled')

        if (enabled):
            if (enabled == "on"):
                if (room):
                    if (int(room) >= 0 and int(room) <= 5):
                        (code, data, len) = uart.send(UART_Code.SET_LIGHTS_ON,  int(room).to_bytes(1, 'little'))
                        if code == UART_Code.ERROR:
                            if (room == 0):
                                return { "message": "Error while turning the lights on." }, 500
                            else:
                                return { "message": "Error while turning the light on." }, 500
                        else:
                            if (room == 0):
                                return { "message": "Lights turned on successfully." }, 200
                            else:
                                return { "message": "Light turned on successfully." }, 200
                    else:
                        return {"message": "Invalid room provided."}, 400
                else:
                    (code, data, len) = uart.send(UART_Code.SET_LIGHTS_ON,  int(0).to_bytes(1, 'little'))
                    if code == UART_Code.ERROR:
                        return { "message": "Error while turning the lights on." }, 500
                    else:
                        return { "message": "Lights turned on successfully." }, 200
            elif (enabled == "off"):
                if (room):
                    if (int(room) >= 0 and int(room) <= 5):
                        (code, data, len) = uart.send(UART_Code.SET_LIGHTS_OFF,  int(room).to_bytes(1, 'little'))
                        if code == UART_Code.ERROR:
                            if (room == 0):
                                return { "message": "Error while turning the lights off." }, 500
                            else:
                                return { "message": "Error while turning the light off." }, 500
                        else:
                            if (room == 0):
                                return { "message": "Lights turned off successfully." }, 200
                            else:
                                return { "message": "Light turned off successfully." }, 200
                    else:
                        return {"message": "Invalid room provided."}, 400
                else:
                    (code, data, len) = uart.send(UART_Code.SET_LIGHTS_OFF,  int(0).to_bytes(1, 'little'))
                    if code == UART_Code.ERROR:
                        return { "message": "Error while turning the lights off." }, 500
                    else:
                        return { "message": "Lights turned off successfully." }, 200
            else:
                return {"message": "Invalid option!"}, 406


        if (room):
            (code, data, len) = uart.send(UART_Code.GET_LIGHTS,  int(room).to_bytes(1, 'little'))
            
            if code == UART_Code.ERROR:
                return { "message": "Couldn't get lights info." }, 200
            else:
                data_decoded = int.from_bytes(data,'little')
                
                return { "message": data_decoded }, 200
        else:
            # send uart
            (code, data, len) = uart.send(UART_Code.GET_LIGHTS,  int(0).to_bytes(1, 'little'))
            
            if code == UART_Code.ERROR:
                return { "message": "Error to get the lights info" }, 200
            else:
                # just to make sure if the arduino returns data
                data_decoded = list(bytearray(data))
                
                return { "message": data_decoded }, 200

    """
        Route to turn on the lights in all rooms

        Route: /lights_on
        Payload: "room": <int>
        
        Returns
        -------
        {"message": <info>}
            Light status message
    """
    
    """
        Route to turn off the lights in all rooms

        Route: /lights_off
        Payload: "room": <int>

        Returns
        -------
        {"message": <info>}
            Light status message
    """