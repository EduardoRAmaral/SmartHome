"""
    Routes to remove or add more rooms
"""
def routes(app, conn):
    
    """
        Route the quantity of rooms
        
        Returns
        -------
        {"message": number of rooms}}
            Message with the number of rooms
    """
    @app.route("/rooms/quant_rooms")
    def quant_rooms():
        quant = conn.get_quant_rooms()
        return {"message": quant[0]}, 200

    """
        Route to show all existing rooms
        
        Returns
        -------
        {"message": [<rooms>}}
            Message that shows a list with all existing rooms
    """
    @app.route("/rooms/show_all")
    def show_all():
        rooms = conn.get_all_rooms_info()
        message = []

        for r in rooms:
            message.append({
                "id": r[0],
                "name": r[1]
            })
        return {"message": message}, 200

    """
        Route to add a new division
        
        Returns
        -------
        {"message": <status>}
            Message that shows if the room was added or not
    """
    @app.route("/rooms/add/<name>")
    def add_division(name):
        mes = ""
        quant = conn.get_all_rooms_info()
        
        if quant == []:
            mes = "Division doesn\'t exist!"
        else:
            room = conn.get_specific_room(name)
            if room != []:
                conn.add_room(name)
                mes = "Division added"
            else:
                mes = "Division doesn\'t exist!"

        return {"message": mes}, 200

    """
        Route to delete a new division
        
        Returns
        -------
        {"message": <status>}
            Message that shows if the room was deleted or not
    """
    @app.route("/rooms/remove/<name>")
    def rem_division(name):
        mes = ""
        quant = conn.get_all_rooms_info()
        
        if quant == []:
            mes = "Division doesn\'t exist!"
        else:
            room = conn.get_specific_room(name)
            if room != []:
                conn.del_room(name)
                mes = "Division deleted"
            else:
                mes = "Division doesn\'t exist!"

        return {"message": mes}, 200