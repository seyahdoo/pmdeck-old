package com.seyahdoo.pmdeck

import android.content.Context
import android.content.pm.ServiceInfo
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.net.nsd.NsdManager
import android.net.nsd.NsdServiceInfo
import android.os.Build
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.util.Base64
import android.util.Log
import android.view.KeyEvent
import android.view.MotionEvent
import android.view.View
import android.widget.ImageButton
import kotlinx.android.synthetic.main.activity_main.*
import it.ennova.zerxconf.ZeRXconf
import java.net.InetAddress
import android.content.Context.NSD_SERVICE
import android.net.wifi.WifiInfo
import android.net.wifi.WifiManager
import android.support.v4.content.ContextCompat.getSystemService
import org.jetbrains.anko.doAsync
import rx.Subscription
import java.util.jar.Attributes
import javax.jmdns.JmDNS
import java.io.IOException
import java.net.NetworkInterface
import java.net.UnknownHostException
import javax.jmdns.JmmDNS
import javax.jmdns.ServiceEvent
import javax.jmdns.ServiceListener


class MainActivity : AppCompatActivity() {

    private val con: Connection = Connection()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val buttonList: List<ImageButton> = listOf(btn0,btn1,btn2,btn3,btn4,btn5,btn6,btn7,btn8,btn9,btn10,btn11,btn12,btn13,btn14);

        con.setOnDataListener {

            val spl = it.split(";")

            try {
                val image = buttonList[(spl[0]).toInt()]
                val decodedString = Base64.decode(spl[1], Base64.DEFAULT);
                var bitmap: Bitmap = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.size)
                bitmap = Bitmap.createScaledBitmap(bitmap, image.measuredWidth, image.measuredHeight, true);
                runOnUiThread {
                    image.setImageBitmap(bitmap)
                }

            }catch (e: Exception){
                e.printStackTrace()
            }

        }

//        ZeRXconf.startDiscovery(this, "_pmdeck._tcp.").subscribe({
//            Log.e("Discovery","Found a new service ${it.address!!}:${it.servicePort}")
//            con.closeConnection()
//            con.openConnection(it.address!!, it.servicePort)
//        }, {
//            Log.e("Main Activity", it.toString())
//        })

        val context = this

        doAsync {
            val d = NetworkDiscovery(context)
            d.findServers {
                Log.e("Discovery", "Found ${it.inetAddresses}:${it.port}")
                con.closeConnection()
                con.openConnection(it.inetAddresses[0],it.port)
            }
        }




        buttonList.forEachIndexed{ index, element ->
            element.setOnTouchListener { _:View, e:MotionEvent ->
                when (e.action){
                    MotionEvent.ACTION_DOWN -> {
                        con.sendMessage("$index,0;")
                    }
                    MotionEvent.ACTION_UP -> {
                        con.sendMessage("$index,1;")
                    }
                }

                return@setOnTouchListener true
            }
        }


    }

    var swap:Boolean = true;

    override fun onKeyDown(keyCode: Int, event: KeyEvent?): Boolean {

        if (keyCode == KeyEvent.KEYCODE_VOLUME_UP){
            RebirthHelper.doRestart(this)
            return true
        }else if (keyCode == KeyEvent.KEYCODE_VOLUME_DOWN){
            swap = !swap;
            setSystemUIEnabled(swap);
            return true
        }

        return true
    }



    /**
     * Uses Root access to enable and disable SystemUI.
     * @param enabled Decide whether to enable or disable.
     */
    fun setSystemUIEnabled(enabled:Boolean) {

        if (enabled){
            //Not working :\
            //Show
            var proc: Process? = null
            try {
                proc = Runtime.getRuntime()
                    .exec(arrayOf("su", "-c", "am startservice -n com.android.systemui/.SystemUIService"))
            } catch (e: Exception) {
                Log.w("Main", "Failed to kill task bar (1).")
                e.printStackTrace()
            }

            try {
                proc!!.waitFor()
            } catch (e: Exception) {
                Log.w("Main", "Failed to kill task bar (2).")
                e.printStackTrace()
            }


        }else{
            try {
                var ProcID = "42"

                //REQUIRES ROOT
                val proc = Runtime.getRuntime()
                    .exec(arrayOf("su", "-c", "service call activity $ProcID s16 com.android.systemui")) //WAS 79
                proc.waitFor()

            } catch (e: Exception) {
                e.printStackTrace()
            }
        }

    }

}
