from flask import request

from Python_UART_Lib import UART_Code

class AutoSystem():
    """
        A class used to create an instance of the home automatic system
    """
    def __init__(self):
        self.instance = {}

    """
        The routing from the automatic system's web API

        Attributes
        ----------
        app : flask.app.Flask
            The flask app, running the API
    """
    def routes(self, app, conn, uart):
        """
            '/autosystem' route, presenting the status and letting the end
            user change if the automatic system is enabled or not by using
            the 'enabled' GET parameter with the values 'on' or 'off'.

            Returns
            -------
            instance : dict , 200
                The current status with no new changes
            
            instance : dict , 201
                The current status with the new changes (enable or disable
                automatic system) provided by the user
            
            instance : dict , 406
                The current status with a warning (because of an invalid
                option provided by the user, by using 'enabled' GET
                parameter)
        """
        @app.route("/autosystem", methods=['GET'])
        def autosystem():
            autosystem_status = conn.get_autosystem_status()
            code = 200
            self.instance.pop("info", None)
            
            """
            if autosystem_status == 1:
                self.instance["message"] = "Current status: On"
                self.instance["status"] = 1
                self.instance["changed"] = False
            else:
                self.instance["message"] = "Current status: Off"
                self.instance["status"] = 0
                self.instance["changed"] = False

            """

            enabled = request.args.get("enabled")
        
            if (enabled):
                if enabled == "on":
                    if autosystem_status:
                        self.instance["info"] = "Automatic system is already enabled!"
                        self.instance["changed"] = False
                    else:
                        # Store autosystem current status
                        conn.set_autosystem_status(1)

                        # Uart
                        (code, data, len) = uart.send(UART_Code.SET_AUTOMODE,  int(1).to_bytes(4, 'little'))
                        
                        if code == UART_Code.ERROR:
                            self.instance["warning"] = "Error changing Automode"
                            code = 406
                        else:
                            autosystem_status = 1
                            self.instance["info"] = "Automatic system enabled successfully!"
                            self.instance["message"] = "Current status: On"
                            self.instance["status"] = autosystem_status
                            self.instance["changed"] = True
                            code = 201
                elif enabled == "off":
                    if not autosystem_status:
                        self.instance["info"] = "Automatic system is already disabled!"
                        self.instance["changed"] = False
                    else:
                        # Store autosystem current status
                        conn.set_autosystem_status(0)

                        # Uart
                        (code, data, len) = uart.send(UART_Code.SET_AUTOMODE,  int(0).to_bytes(1, 'little'))
                        
                        if code == UART_Code.ERROR:
                            self.instance["warning"] = "Error changing Automode"
                            code = 406
                        else:
                            autosystem_status = 0
                            self.instance["info"] = "Automatic system disabled successfully!"
                            self.instance["message"] = "Current status: Off"
                            self.instance["status"] = autosystem_status
                            self.instance["changed"] = True
                            code = 201
                else:
                    self.instance["warning"] = "Invalid option!"
                    code = 406
            else:
                return {"message": autosystem_status}, 200

            return self.instance, code


        """
        !! ANTES DAS ALTERAÇÕES !!

        def autosystem():
            self.instance.pop("info", None)
            code = 200

            enabled = request.args.get("enabled")

            if self.__AUTOSYSTEM_STATUS == 1:
                self.instance["message"] = "Current status: On"
                self.instance["status"] = 1
                self.instance["changed"] = False
            else:
                self.instance["message"] = "Current status: Off"
                self.instance["status"] = 0
                self.instance["changed"] = False
            
            if (enabled):
                if enabled == "on":
                    if self.__AUTOSYSTEM_STATUS:
                        self.instance["info"] = "Automatic system is already enabled!"
                    else:
                        self.instance["info"] = "Automatic system enabled successfully!"
                        self.instance["message"] = "Current status: On"
                        self.instance["status"] = 1
                        self.instance["changed"] = True
                        self.__AUTOSYSTEM_STATUS = 1
                        code = 201
                elif enabled == "off":
                    if not self.__AUTOSYSTEM_STATUS:
                        self.instance["info"] = "Automatic system is already disabled!"
                    else:
                        self.instance["info"] = "Automatic system disabled successfully!"
                        self.instance["message"] = "Current status: Off"
                        self.instance["status"] = 0
                        self.instance["changed"] = True
                        self.__AUTOSYSTEM_STATUS = 0
                        code = 201
                else:
                    self.instance["warning"] = "Invalid option!"
                    code = 406

            return self.instance, code"""
