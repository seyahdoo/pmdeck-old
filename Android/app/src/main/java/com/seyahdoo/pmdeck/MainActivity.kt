package com.seyahdoo.pmdeck

import android.annotation.SuppressLint
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Color
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.util.Base64
import android.util.Log
import android.view.KeyEvent
import android.view.MotionEvent
import android.view.View
import android.widget.ImageButton
import android.widget.Toast
import com.danimahardhika.cafebar.CafeBar
import com.danimahardhika.cafebar.CafeBarTheme
import kotlinx.android.synthetic.main.activity_main.*

class MainActivity : AppCompatActivity() {

    var Synced:Boolean = true
    var SyncTrying:Boolean = false
    var SyncPass:String = "123456"
    var SyncCon:Connection? = null
    var PassAccepted:Boolean = false
    var Pass:String = "0"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        //val sharedPref = this?.getPreferences(Context.MODE_PRIVATE)
        //Synced = sharedPref.getBoolean("Synced",false)
        //Pass = sharedPref.getString("Pass","0")

        val buttonList: List<ImageButton> = listOf(btn0,btn1,btn2,btn3,btn4,btn5,btn6,btn7,btn8,btn9,btn10,btn11,btn12,btn13,btn14);

        val controlListener = @SuppressLint("Range")
        fun (con:Connection, s:String){
            for (msg in s.split(";")){
                val spl = msg.split(":");
                val cmd = spl[0]
                when (cmd){
                    "IMAGE" -> {
                        if (!Synced || (Synced && !PassAccepted)){
                            con.closeConnection()
                            return
                        }
                        try {
                            val args = spl[1].split(",")
                            val image = buttonList[(args[0]).toInt()]
                            val decodedString = Base64.decode(args[1], Base64.DEFAULT);
                            var bitmap: Bitmap = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.size)
                            bitmap = Bitmap.createScaledBitmap(bitmap, image.measuredWidth, image.measuredHeight, true);
                            runOnUiThread {
                                image.setImageBitmap(bitmap)
                            }
                        }catch (e: Exception){
                            e.printStackTrace()
                        }
                    }
                    "PING" -> {
                        con.sendMessage("PONG;")
                    }
                    "CONN" -> {
                        try {
                            val args = spl[1].split(",")
                            if (args[0] == Pass){
                                PassAccepted = true
                                con.sendMessage("CONNACCEPT;")
                            }
                        }catch (e:Exception){
                            con.closeConnection()
                        }
                    }
                    "SYNCREJ" -> {
                        con.closeConnection()
                    }
                    "SYNCTRY" -> {
                        if (Synced) return
                        if (SyncTrying) return
                        try {
                            val args = spl[1].split(",")
                            SyncPass = args[0]
                            SyncTrying = true
                            SyncCon = con
                            //Open Sync UI

                            CafeBar.builder(this)
                                .theme(CafeBarTheme.LIGHT)
                                .floating(true)
                                .swipeToDismiss(true)
                                .duration(Int.MAX_VALUE)
                                .content("Sync request came Do you accept? Password is $SyncPass ")
                                .positiveText("Accept")
                                .positiveColor(Color.BLUE)
                                .negativeText("Reject")
                                .negativeColor(Color.RED)
                                .onPositive {
                                    if (!SyncTrying) return@onPositive
                                    SyncCon?.sendMessage("SYNCACCEPT:${SyncPass};")
                                    Synced = true
                                    SyncTrying = false
                                    Pass = SyncPass
                                    SyncPass = "0"
                                    it.dismiss()
                                }
                                .onNegative {
                                    if (!SyncTrying) return@onNegative
                                    SyncCon?.sendMessage("SYNCREJ;")
                                    SyncTrying = false
                                    SyncPass = "0"
                                    SyncCon?.closeConnection()
                                    it.dismiss()
                                }
                                .show();

                        }catch (e:Exception){
                            e.printStackTrace()
                            Log.e("Network Listener","Closing Connection, Stuff Happened")
                            con.closeConnection()
                        }
                    }
                }
            }
        }

        buttonList.forEachIndexed{ index, element ->
            element.setOnTouchListener { _:View, e:MotionEvent ->
                if (!Synced) return@setOnTouchListener true
                when (e.action){
                    MotionEvent.ACTION_DOWN -> {
                        Connection.openConnections.forEach {
                            it.sendMessage("BTNEVENT:$index,0;")
                        }
                    }
                    MotionEvent.ACTION_UP -> {
                        Connection.openConnections.forEach {
                            it.sendMessage("BTNEVENT:$index,1;")
                        }
                    }
                }

                return@setOnTouchListener true
            }
        }

        doThreaded {
            val d = NetworkDiscovery(this@MainActivity)
            d.findServers {
                Log.e("Discovery", "Found ${it.inetAddresses}:${it.port}")
                val con = Connection()
                con.setOnDataListener(controlListener)
                con.openConnection(it.inetAddresses[0],it.port) {
                    if(Synced){
                        con.sendMessage("CONN:${getUID()};")
                    }else{
                        con.sendMessage("SYNCREQ:${getUID()};")
                    }
                }

            }
        }

    }

    var swap:Boolean = true;

    override fun onKeyDown(keyCode: Int, event: KeyEvent?): Boolean {
        if (keyCode == KeyEvent.KEYCODE_VOLUME_UP){
            RebirthHelper.doRestart(this)

        }else if (keyCode == KeyEvent.KEYCODE_VOLUME_DOWN){
            //swap = !swap;
            //setSystemUIEnabled(swap);

        }
        return true
    }


    override fun onKeyLongPress(keyCode: Int, event: KeyEvent): Boolean {
        if (keyCode == KeyEvent.KEYCODE_VOLUME_DOWN) {
            Toast.makeText(getApplicationContext(),"Disconecting and UnSyncing",Toast.LENGTH_SHORT).show();
            Connection.openConnections.forEach {
                it.closeConnection()
            }
            Synced = false
            SyncTrying = false
            SyncPass = "0"
            return true
        }
        return super.onKeyLongPress(keyCode, event)
    }



}
