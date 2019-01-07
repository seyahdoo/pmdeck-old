package com.seyahdoo.pmdeck

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.util.Base64
import android.util.Log
import android.view.KeyEvent
import android.view.MotionEvent
import android.view.View
import android.widget.ImageButton
import kotlinx.android.synthetic.main.activity_main.*

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

        con.openConnection()

        buttonList.forEachIndexed{ index, element ->
            element.setOnTouchListener { v:View, e:MotionEvent ->
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
            con.closeConnection()
            con.openConnection()
            return true
        }else if (keyCode == KeyEvent.KEYCODE_VOLUME_DOWN){
            //setSystemUIEnabled(false);
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
            try {
                val proc =
                    Runtime.getRuntime().exec(arrayOf("am", "startservice", "-n", "com.android.systemui/.SystemUIService"))
                proc.waitFor()
            } catch (e: Exception) {
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
