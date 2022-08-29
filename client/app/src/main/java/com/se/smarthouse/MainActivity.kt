package com.se.smarthouse

import android.annotation.SuppressLint
import android.content.Context
import android.os.Bundle
import android.text.InputType.TYPE_CLASS_NUMBER
import android.util.Log
import android.widget.*
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import com.google.gson.Gson
import okhttp3.Callback
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.Response
import java.io.IOException


var baseURL = "http://172.17.28.244:8080"

val gson = Gson()

class MainActivity : AppCompatActivity() {
    @SuppressLint("SetTextI18n", "WrongViewCast", "UseSwitchCompatOrMaterialCode")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val pref = getPreferences(Context.MODE_PRIVATE)
        val tempId = pref.getString("IP", "")

        if (tempId != null) {
            //baseURL = tempId
        }

        Log.v("TEST", "Program Start")

        //Change IP to connect to
        val changeIP  = findViewById<Button>(R.id.homeIcon)
        changeIP.setOnClickListener{
            changeIP()

        }

        //Change Minimum Luminosity
        val changeLumi  = findViewById<Button>(R.id.changeLumi)

        getMiniLumi()

        changeLumi.setOnClickListener{
            changeMiniLumi()

        }

        // Refresh Luminosity
        val refreshLumi = findViewById<Button>(R.id.refreshLumi)
        updateLumi()
        refreshLumi.setOnClickListener{
            updateLumi()
        }


        // Refresh Temperature
        val refreshTemp = findViewById<Button>(R.id.refreshTemp)
        //updateTemp()
        refreshTemp.setOnClickListener{
            updateTemp()
        }

        //Music Buttons
        val playButton = findViewById<ToggleButton>(R.id.play)
        val backButton = findViewById<Button>(R.id.back)
        val nextButton = findViewById<Button>(R.id.next)

        getMusicStatus()

        playButton.setOnCheckedChangeListener{ _, isChecked ->
            if (isChecked) {
                playMusic()
            } else {
                stopMusic()
            }
        }

        backButton.setOnClickListener{
            beforeMusic()
        }
        nextButton.setOnClickListener{
            nextMusic()
        }

        //General Controls
        val generalAutoSwitch = findViewById<Switch>(R.id.autoSwitchGeneral)
        generalAutoSwitch.isChecked = true
        getAutoRequest()

        generalAutoSwitch?.setOnCheckedChangeListener { _, isChecked ->
            setAuto(isChecked)
            printAutomatic(isChecked)
        }


        val generalSwitch = findViewById<Switch>(R.id.switchGeneral)
        //checkAll()

        generalSwitch?.setOnCheckedChangeListener { _, isChecked ->
            changeLights(1, isChecked)
            changeLights(2, isChecked)
            changeLights(3, isChecked)
            changeLights(4, isChecked)
            changeLights(5, isChecked)
            printLights(isChecked, "All Lights")
        }

        //Living Room
        val livingRoomLights = findViewById<Switch>(R.id.SwitchLivingRoom)
        //checkLights(1)


        livingRoomLights?.setOnCheckedChangeListener { _, isChecked ->
            changeLights(1, isChecked)
            printLights(isChecked, "Living Room Lights")
        }

        //Room 1
        val room1Switch = findViewById<Switch>(R.id.SwitchRoom1)
        //checkLights(2)

        room1Switch?.setOnCheckedChangeListener { _, isChecked ->
            changeLights(2, isChecked)
            printLights(isChecked, "Room 1 Lights")
        }

        //Room 2
        val room2Switch = findViewById<Switch>(R.id.SwitchRoom2)
        //checkLights(3)

        room2Switch?.setOnCheckedChangeListener { _, isChecked ->
            changeLights(3, isChecked)
            printLights(isChecked, "Room 2 Lights")
        }

        //Bathroom
        val bathroomSwitch = findViewById<Switch>(R.id.SwitchBathroom)
        //checkLights(4)

        bathroomSwitch?.setOnCheckedChangeListener { _, isChecked ->
            changeLights(4, isChecked)
            printLights(isChecked, "Bathroom Lights")
        }

        //Kitchen
        val kitchenSwitch = findViewById<Switch>(R.id.SwitchKitchen)
        checkLights(5)

        kitchenSwitch?.setOnCheckedChangeListener { _, isChecked ->
            changeLights(5, isChecked)
            printLights(isChecked, "Kitchen Lights")
        }
    }

    /**
     * Changes Connection to Raspberry
     */
    private fun changeIP(){
        val builder = AlertDialog.Builder(this)
        val inflater = layoutInflater
        builder.setTitle("Enter the IP address and Port for the Raspberry")

        val dialogLayout = inflater.inflate(R.layout.alert_dialog_ip, null)
        val editText  = dialogLayout.findViewById<EditText>(R.id.editText)
        builder.setView(dialogLayout)
        builder.setPositiveButton("OK") { _, _ ->

            baseURL = editText.text.toString()
            val pref = getPreferences(Context.MODE_PRIVATE)
            val edit = pref.edit()

            edit.clear()
            edit.commit()

            edit.putString("IP", baseURL)

            edit.commit()
        }
        builder.show()
    }

    /**
     * Checks if there is music playing
     */
    private fun getMusicStatus(){
        var url = "/music/status"

        val getURL ="$baseURL$url"

        val request = Request.Builder().url(getURL).build()
        val client = OkHttpClient()

        client.newCall(request).enqueue(object: Callback{
            override fun onResponse(call: okhttp3.Call, response: Response) {
                var body = response.body?.string().toString()
                body.trimIndent()

                println(body)

                var mUser = gson.fromJson(body, TempResponse::class.java)
                if(mUser.message == "Currently playing: music.mp3"){
                    val playButton = findViewById<ToggleButton>(R.id.play)

                    playButton.isChecked = true;

                }
                else{
                    val playButton = findViewById<ToggleButton>(R.id.play)
                    playButton.isChecked = false;
                }
            }
            override fun onFailure(call: okhttp3.Call, e: IOException) {
                println(call)
                println(e)
                println("FAIL")
            }
        })
    }

    /**
     * Starts the music
     */
    private fun playMusic(){
        var url = "/music/play"
        var name = "music.mp3"
        val getURL ="$baseURL$url?name=$name"

        val request = Request.Builder().url(getURL).build()
        val client = OkHttpClient()

        client.newCall(request).enqueue(object: Callback{
            override fun onResponse(call: okhttp3.Call, response: Response) {
                var body = response.body?.string().toString()
                body.trimIndent()

                println(body)

                //var mUser = gson.fromJson(body, TempResponse::class.java)
            }
            override fun onFailure(call: okhttp3.Call, e: IOException) {
                println(call)
                println(e)
                println("FAIL")
            }
        })
    }

    /**
     * Stops the music
     */
    private fun stopMusic(){
        var url = "/music/stop"

        val getURL ="$baseURL$url"

        val request = Request.Builder().url(getURL).build()
        val client = OkHttpClient()

        client.newCall(request).enqueue(object: Callback{
            override fun onResponse(call: okhttp3.Call, response: Response) {
                var body = response.body?.string().toString()
                body.trimIndent()

                println(body)

                //var mUser = gson.fromJson(body, TempResponse::class.java)
            }
            override fun onFailure(call: okhttp3.Call, e: IOException) {
                println(call)
                println(e)
                println("FAIL")
            }
        })
    }

    /**
     * advances to the next song
     */
    private fun nextMusic(){
    }

    /**
     * go to the previous song
     */
    private fun beforeMusic(){
    }

    /**
     * check the lights state in one room
     * @param room ID of the room
     */
    private fun checkLights(room:Int){
        var url = "/lights"

        val getURL ="$baseURL$url?room=$room"

        val request = Request.Builder().url(getURL).build()
        val client = OkHttpClient()

        client.newCall(request).enqueue(object: Callback{
            override fun onResponse(call: okhttp3.Call, response: Response) {
                var body = response.body?.string().toString()
                body.trimIndent()

                println(body)

                //var mUser = gson.fromJson(body, TempResponse::class.java)
            }
            override fun onFailure(call: okhttp3.Call, e: IOException) {
                println(call)
                println(e)
                println("FAIL")
            }
        })
    }

    /**
     * cheaks the states of the lights in all rooms
     */
    private fun checkAll(){
    }

    /**
     * Changes the lights in one room
     * @param room ID of the room
     * @param isChecked State of the switch
     */
    private fun changeLights(room:Int, isChecked: Boolean){
        var url = "/lights"

        var enable = ""

        if(isChecked){
            enable = "on"
        }else if(!isChecked){
            enable = "off"
        }
        val getURL ="$baseURL$url?room=$room&enabled=$enable"

        val request = Request.Builder().url(getURL).build()
        val client = OkHttpClient()

        client.newCall(request).enqueue(object: Callback{
            override fun onResponse(call: okhttp3.Call, response: Response) {
                var body = response.body?.string().toString()
                body.trimIndent()

                println(body)

                //var mUser = gson.fromJson(body, TempResponse::class.java)
            }
            override fun onFailure(call: okhttp3.Call, e: IOException) {
                println(call)
                println(e)
                println("FAIL")
            }
        })
    }

    /**
     * Turn the automatic lights system on/off
     */
    private fun setAuto(isChecked: Boolean){
        var url = "/autosystem"

        var enable = ""

        if(isChecked){
            enable = "on"
        }else if(!isChecked){
            enable = "off"
        }
        val getURL ="$baseURL$url?enabled=$enable"
        println(getURL)
        val request = Request.Builder().url(getURL).build()
        val client = OkHttpClient()

        client.newCall(request).enqueue(object: Callback{
            override fun onResponse(call: okhttp3.Call, response: Response) {
                var body = response.body?.string().toString()
                body.trimIndent()

                println(body)

                //var mUser = gson.fromJson(body, TempResponse::class.java)
            }
            override fun onFailure(call: okhttp3.Call, e: IOException) {
                println(call)
                println(e)
                println("FAIL")
            }
        })
    }

    /**
     * Gets the current status of the Auto System
     */
    private fun getAutoRequest(){
        val url = "/autosystem"
        val getURL = baseURL + url

        val request = Request.Builder().url(getURL).build()
        val client = OkHttpClient()

        client.newCall(request).enqueue(object: Callback{
            override fun onResponse(call: okhttp3.Call, response: Response) {
                var body = response.body?.string().toString()
                body.trimIndent()

                println(body)
                var mUser = gson.fromJson(body, AutoSystem::class.java)

                if(mUser.message=="Current status: On"){
                    val generalAutoSwitch = findViewById<Switch>(R.id.autoSwitchGeneral)
                    runOnUiThread {generalAutoSwitch.isChecked = true}
                }
                else{
                    val generalAutoSwitch = findViewById<Switch>(R.id.autoSwitchGeneral)
                    runOnUiThread {generalAutoSwitch.isChecked = false}

                }


            }
            override fun onFailure(call: okhttp3.Call, e: IOException) {
                println(call)
                println(e)
                println("FAIL")
            }
        })
    }

    /**
     * Changes Minimum Luminosity
     */
    private fun changeMiniLumi(){
        val builder = AlertDialog.Builder(this)
        val inflater = layoutInflater
        builder.setTitle("Enter Minimum Luminosity Value")


        val dialogLayout = inflater.inflate(R.layout.alert_dialog_with_edittext, null)
        val editText  = dialogLayout.findViewById<EditText>(R.id.editText)
        editText.setRawInputType(TYPE_CLASS_NUMBER)
        builder.setView(dialogLayout)
        builder.setPositiveButton("OK") { _, _ -> updateMiniLumi(editText.text.toString()) }
        builder.show()
    }

    /**
     * Updates Minimum Luminosity in the UI and in the Arduino
     */
    private fun updateMiniLumi(lumi:String){
        var url = "/minilum"
            val getURL = "$baseURL$url?lum=$lumi"

            val request = Request.Builder().url(getURL).build()
            println(getURL)
            println(request)
            val client = OkHttpClient()

            client.newCall(request).enqueue(object: Callback{
                override fun onResponse(call: okhttp3.Call, response: Response) {
                    var body = response.body?.string().toString()
                    body.trimIndent()

                    val tv1: TextView = findViewById(R.id.lumiMiniValue)
                    runOnUiThread { tv1.text = "$lumi" }

                }
                override fun onFailure(call: okhttp3.Call, e: IOException) {
                    println(call)
                    println(e)
                    println("FAIL")
                }
            })
    }

    /**
     * Prints some feedback when user switches the Automatic lights
     * @param isChecked Current Automatic Lights state
     */
    private fun  printAutomatic(isChecked: Boolean){
        val message = if (isChecked) "All Lights:AUTO ON" else "All Lights:AUTO OFF"
        Log.v("TEST", message)
        Toast.makeText(
            this@MainActivity, message,
            Toast.LENGTH_SHORT
        ).show()
    }

    /**
     * Prints some feedback when user switches the lights
     * @param isChecked Current Light state
     * @param name Message to print
     */
    private fun  printLights(isChecked: Boolean, name: String){
        val message = if (isChecked) "$name:ON" else "$name:OFF"
        Log.v("TEST", message)
        Toast.makeText(
            this@MainActivity, message,
            Toast.LENGTH_SHORT
        ).show()
    }

    /**
     * Updates the Minimum Luminosity value display on the App
     */
    private fun  getMiniLumi(){
        var url = "/minilum"
        val getURL = baseURL + url

        val request = Request.Builder().url(getURL).build()
        println(getURL)
        println(request)
        val client = OkHttpClient()

        client.newCall(request).enqueue(object: Callback{
            override fun onResponse(call: okhttp3.Call, response: Response) {
                var body = response.body?.string().toString()
                body.trimIndent()

                var mUser = gson.fromJson(body, SingleResponse::class.java)
                val lumi = mUser.message
                val tv1: TextView = findViewById(R.id.lumiMiniValue)
                runOnUiThread { tv1.text = "$lumi" }

            }
            override fun onFailure(call: okhttp3.Call, e: IOException) {
                println(call)
                println(e)
                println("FAIL")
            }
        })
    }

    /**
     * Updates the Luminosity value display on the App
     */
    private fun updateLumi(){
        var url = "/luminosity"
        val getURL = baseURL + url

        val request = Request.Builder().url(getURL).build()
        println(getURL)
        println(request)
        val client = OkHttpClient()

        client.newCall(request).enqueue(object: Callback{
            override fun onResponse(call: okhttp3.Call, response: Response) {
                var body = response.body?.string().toString()
                body.trimIndent()


                var mUser = gson.fromJson(body, SingleResponse::class.java)
                val lumi = mUser.message
                val tv1: TextView = findViewById(R.id.lumiValue)
                runOnUiThread { tv1.text = "$lumi" }

            }
            override fun onFailure(call: okhttp3.Call, e: IOException) {
                println(call)
                println(e)
                println("FAIL")
            }
        })
    }

    /**
     * Updates the Temperature value display on the App
     */
    private fun  updateTemp(){

        var url = "/temperature"
        val getURL = baseURL + url

        val request = Request.Builder().url(getURL).build()
        println(getURL)
        println(request)
        val client = OkHttpClient()

        client.newCall(request).enqueue(object: Callback{
            override fun onResponse(call: okhttp3.Call, response: Response) {
                var body = response.body?.string().toString()
                body.trimIndent()


                var mUser = gson.fromJson(body, TempResponse::class.java)
                val temp = mUser.message
                val tv1: TextView = findViewById(R.id.tempValue)
                runOnUiThread { tv1.text = "$temp" }

            }
            override fun onFailure(call: okhttp3.Call, e: IOException) {
                println(call)
                println(e)
                println("FAIL")
            }
        })
    }

    /**
     * Send a GET request to an endpoint
     * @param url End point
     */
    private fun getRequest(url: String) {
        var body = ""
        val getURL = baseURL + url
        val request = Request.Builder().url(getURL).build()
        println(getURL)
        println(request)
        val client = OkHttpClient()

        client.newCall(request).enqueue(object: Callback{
            override fun onResponse(call: okhttp3.Call, response: Response) {
                body = response.body?.string().toString()
            }
            override fun onFailure(call: okhttp3.Call, e: IOException) {
                println(call)
                println(e)
                println("FAIL")
            }
        })
    }

    /**
     * Send a Post request to an endpoint
     * @param url End point
     * @param postBody message
     */
    private fun postRequest(url: String, postBody: String) {
        val postURL = baseURL + url

        val client = OkHttpClient()

        val postBody = """
        |Releases
        |--------
        |
        | * _1.0_ May 6, 2013
        | * _1.1_ June 15, 2013
        | * _1.2_ August 11, 2013
        |""".trimMargin()

        val requestBody = postBody.toRequestBody(MEDIA_TYPE_MARKDOWN)

        val request = Request.Builder().method("POST", requestBody).url(postURL).build()

        client.newCall(request).enqueue(object: Callback{
            override fun onResponse(call: okhttp3.Call, response: Response) {
                println(response.body!!.string())
            }
            override fun onFailure(call: okhttp3.Call, e: IOException) {
                println("FAIL")
            }
        })
    }

    /**
     * Request Body Type
     */
    companion object {
        val MEDIA_TYPE_MARKDOWN = "text/x-markdown; charset=utf-8".toMediaType()
    }
}