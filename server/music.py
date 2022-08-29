import mimetypes
import os
import threading
from flask import request
from flask import abort
from playsound import playsound
from werkzeug.utils import secure_filename

context = {"playing": False, "music": ""}

"""
    Music routing
"""
def routes(app):

    """
        Routing to upload a music file and store in the default upload folder (music/). It verifies
        if the provided file is an audio file and if there's no file with the same name has the one 
        given
        
        Returns
        -------
        {"error": "No file provided"}, 400
            No file provided by the user or wrong HTTP method used
        
        {"error": "Invalid file type"}, 400
            The file provided is not an audio file

        {"message": "File added"}, 200
            File uploaded successfully
    """
    @app.route("/music/upload", methods=["GET", "POST"])
    def music_upload():
        if request.method == "GET" or "file" not in request.files or request.files["file"].filename == "":
            return {"error": "No file provided"}, 400

        file = request.files["file"]
        filename = secure_filename(file.filename)
        filename = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filename)
        
        # Verify the file type and delete if not an audio file
        filetype = mimetypes.guess_type(filename)
        if not (filetype[0] != None and "audio/" in filetype[0]):
            os.remove(filename)
            return {"error": "Invalid file type"}, 400

        return {"message": "File added"}, 200

    """
        Routing with the song listing
        
        Returns
        -------
        {"count": len(res), "list": res}
            The number and names of musics on the 'music' folder
    """
    @app.route("/music/list")
    def music_list():
        res = []
        musics = os.listdir("music")

        for i in range(len(musics)):
            filetype = mimetypes.guess_type(musics[i])

            if filetype[0] != None and "audio/" in filetype[0]:
                res.append(musics[i])

        return {"count": len(res), "list": res}

    """
        Routing to play the music
        
        Returns
        -------
        abort(404)
            The music doesn't exist or the file isn't an audio file

        {"error": "No music name provided"}, 400
            A music name wasn't provided in the request

        {"message": f"Playing: {music}"}, 200
            Music started playing successfully, and the song name is shown in the response
    """
    @app.route("/music/play")
    def music_play():
        music = request.args.get("name")
        if (type(music) == None or music == ""):
            return {"error": "No music name provided"}, 400
        if (not os.path.exists(f"music/{music}")):
            abort(404)
        else:
            filetype = mimetypes.guess_type(f"music/{music}")

            if not "audio/" in filetype[0]:
                abort(404)
            else:
                def play():
                    if (not context["playing"]):
                        context["playing"] = True
                        context["music"] = music
                        playsound(f"music/{music}")

                playing = threading.Thread(target=play)
                playing.name = "Music"
                playing.start()

                return {"message": f"Playing: {music}"}, 200
    
    """
        Routing to retrieve the music status
        
        Returns
        -------
        {"message": "There's no track currently playing."}, 200
            There is no music playing at the moment 

        {"message": f"Currently playing: {context['music']}"}, 200
            The music that is currently playing
    """
    @app.route("/music/status")
    def music_status():
        if (not context["playing"]):
            return {"message": "There's no track currently playing."}, 200

        return {"message": f"Currently playing: {context['music']}"}, 200

    """
        Routing to stop the music

        Returns
        -------
        {"message": "Music stopped."}, 200
            The music has been stopped

        {"message": "There's no music playing."}, 200
            There wasn't any music playing
    """
    @app.route("/music/stop")
    def music_stop():
        if (context["playing"]):
            context["playing"] = False
            context["music"] = ""
            for i in threading._active.items():
                if i[1].name == "Music":
                    # KILL PROCESS HERE
                    thread = i[1]
                    break

            return {"message": "Music stopped."}, 200
        
        return {"message": "There's no music playing."}, 200
