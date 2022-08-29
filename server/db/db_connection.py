import os.path
import sqlite3


class DBConnection:

    # Open a new connection to a db
    def get_db_connection(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, 'database.db')
        conn = None

        try:
            conn = sqlite3.connect(db_path)
        except Exception as e:
            print(e)
        
        conn.row_factory = sqlite3.Row
        return conn
    
    ##########################################################
    ####################### LUMINOSITY #######################
    ##########################################################
    """
        Get luminosity value stored on db
    """
    def get_lum_lvl(self):
        conn = self.get_db_connection()
        query = 'SELECT nvl_luminosidade FROM configs'
        res = conn.execute(query).fetchone()        
        conn.close()
        return res
    
    """
        Get luminosity value stored on db
    """
    def set_lum_lvl(self, value):
        conn = self.get_db_connection()
        query = """
            UPDATE configs
            SET nvl_luminosidade = (?)
            WHERE id = 1
        """
        cur = conn.cursor()
        cur.execute(query, (value,))
        conn.commit()
        conn.close()

    ######################################################################
    ####################### AUTOSYSTEMS OPERATIONS #######################
    ######################################################################
    """
        Get Autosystem status
    """
    def get_autosystem_status(self):
        conn = self.get_db_connection()
        
        query = 'SELECT autosystem FROM configs'
        res = conn.execute(query).fetchone()
        conn.close()

        return res[0]
    
    """
        Change Autosystem status
    """
    def set_autosystem_status(self, status=0):
        conn = self.get_db_connection()

        query = '''
            UPDATE configs
            SET autosystem = (?)
            WHERE id = 1
        '''
        cur = conn.cursor()
        cur.execute(query, (status,))
        conn.commit()
        conn.close()

    ###############################################################
    ####################### ROOM OPERATIONS #######################
    ###############################################################
    """
        Service to count the rooms
    """
    def get_specific_room(self, room):
        conn = self.get_db_connection()
        query = 'SELECT * FROM rooms WHERE room_name = ?'
        res = conn.execute(query, (room)).fetchall()

        conn.close()
        return res
    
    """
        Service to count the rooms
    """
    def get_quant_rooms(self):
        conn = self.get_db_connection()
        query = 'SELECT COUNT(*) FROM rooms'
        res = conn.execute(query).fetchone()

        conn.close()
        return res
    
    """
        Service to count the rooms
    """
    def get_all_rooms_info(self):
        conn = self.get_db_connection()
        query = 'SELECT * FROM rooms'
        res = conn.execute(query).fetchall()

        conn.close()
        return res

    """
        Service to register a room
    """    
    def add_room(self, name=None):
        conn = self.get_db_connection()

        sql = '''
            INSERT INTO rooms (room_name)
            VALUES (?)
        '''
        cur = conn.cursor()
        cur.execute(sql, (name))
        conn.commit()

    """
        Service to remove a room
    """
    def del_room(self, room_name):
        conn = self.get_db_connection()
        query = '''
            DELETE FROM tasks
            WHERE room_name = ?
        '''
        conn.execute(query, (room_name,))
        conn.close()

        return 'Room deleted'