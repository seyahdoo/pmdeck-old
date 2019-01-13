package com.seyahdoo.pmdeck

import android.util.Log
import org.jetbrains.anko.doAsync
import java.io.*
import java.lang.Exception
import java.net.InetAddress
import java.net.Socket

class Connection {

    var socket: Socket? = null;
    var writer: PrintWriter? = null;

    class ShouldContinue(){
        var cont:Boolean = true;
    }

    private var lastReaderContinue: ShouldContinue? = null;

    fun openConnection(ip:InetAddress, port:Int) {
        doThreaded {
            try {
                socket = Socket(ip, port)
                socket?.soTimeout = 10000
                writer = PrintWriter(socket!!.getOutputStream())
                val inputReader = BufferedReader(InputStreamReader(socket?.getInputStream()));
                reader(ShouldContinue(), inputReader)
            } catch (e: IOException) {
                Log.e("Connection", e.toString());
            }
        }
    }

    fun closeConnection(){
        doAsync {
            lastReaderContinue?.cont = false;
            writer?.close()
            socket?.close()

            lastReaderContinue = null;
            writer = null
            socket = null
        }
    }

    interface OnDataListener {
        fun onData(s: String)
    }

    var OnDataCallback: ((Connection,String)->Unit)? = null

    fun setOnDataListener(listener: (Connection,String) -> Unit){
        OnDataCallback = listener;
    }

    fun reader(shouldContinue: ShouldContinue, bufreader: BufferedReader) {
        lastReaderContinue = shouldContinue
        doThreaded {
            while (shouldContinue.cont) {
                val input: String = bufreader.readLine() ?: continue
                OnDataCallback?.invoke(this@Connection,input)
            }
        }
    }

    fun sendMessage(message:String){
        try{
            writer?.write(message)
            writer?.flush()
        }catch (e: Exception){
            closeConnection()
        }

    }

}