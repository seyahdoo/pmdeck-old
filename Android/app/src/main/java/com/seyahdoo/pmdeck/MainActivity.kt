package com.seyahdoo.pmdeck

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Color
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.os.Debug
import android.util.Base64
import android.util.Log
import android.view.KeyEvent
import android.view.MotionEvent
import android.view.View
import android.widget.Button
import android.widget.ImageButton
import kotlinx.android.synthetic.main.activity_main.*

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val button_list: List<ImageButton> = listOf(btn0,btn1,btn2,btn3,btn4,btn5,btn6,btn7,btn8,btn9,btn10,btn11,btn12,btn13,btn14);

        val con = Connection()

        con.setOnDataListener {

            val spl = it.split(";")

            try {
                val image = button_list[(spl[0]).toInt()]
                val decodedString = Base64.decode(spl[1], Base64.DEFAULT);
                var bitmap: Bitmap = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.size)
                bitmap = Bitmap.createScaledBitmap(bitmap, image.measuredWidth, image.measuredHeight, true);
                runOnUiThread {
                    image.setImageBitmap(bitmap)
                }

            }catch (e:Exception){
                e.printStackTrace()
            }

        }

        con.openConnection()

        button_list.forEachIndexed{ index,element ->
            element.setOnTouchListener { v:View, e:MotionEvent ->
                when (e.action){
                    MotionEvent.ACTION_DOWN -> {
                        Log.d("MainActivity", "$index Down")
                        con.sendMessage("$index,0;")
                    }
                    MotionEvent.ACTION_UP -> {
                        Log.d("MainActivity", "$index Up")
                        con.sendMessage("$index,1;")
                    }
                }

                return@setOnTouchListener true
            }
        }





        //TODO do this with root

        val v = window.decorView
        v.systemUiVisibility = (View.SYSTEM_UI_FLAG_LOW_PROFILE
                or View.SYSTEM_UI_FLAG_FULLSCREEN
                or View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                or View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                or View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                or View.SYSTEM_UI_FLAG_HIDE_NAVIGATION)


    }

    var swap:Boolean = true;

    override fun onKeyDown(keyCode: Int, event: KeyEvent?): Boolean {

        if (keyCode == KeyEvent.KEYCODE_VOLUME_UP){


            return true
        }else if (keyCode == KeyEvent.KEYCODE_VOLUME_DOWN){
            swap = !swap;
            HideUI.setSystemUIEnabled(swap);
            return true
        }

        return true
    }


}
