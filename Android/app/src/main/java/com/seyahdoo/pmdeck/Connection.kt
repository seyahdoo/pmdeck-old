package com.seyahdoo.pmdeck

import android.util.Log
import org.jetbrains.anko.doAsync
import java.io.*
import java.lang.Exception
import java.net.InetAddress
import java.net.Socket
import java.net.SocketException
import kotlin.math.log

class Connection {

    companion object {
        var openConnections:MutableList<Connection> = mutableListOf()
    }

    var socket: Socket? = null;
    var writer: PrintWriter? = null;

    class ShouldContinue(){
        var cont:Boolean = true;
    }

    private var lastReaderContinue: ShouldContinue? = null;

    fun openConnection(ip:InetAddress, port:Int, onSuccess:()->Unit) {
        doThreaded {
            try {
                socket = Socket(ip, port)
                socket?.soTimeout = 10000
                writer = PrintWriter(socket!!.getOutputStream())
                val inputReader = BufferedReader(InputStreamReader(socket?.getInputStream()));
                reader(ShouldContinue(), inputReader)
                openConnections.add(this)
                onSuccess()
            } catch (e: IOException) {
                Log.e("Connection", e.toString());
            }
        }
    }

    fun closeConnection(){
        doThreaded {
            Log.e("Connection","Closing connection")
            openConnections.remove(this);

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
                try {
                    val input: String = bufreader.readLine() ?: continue
                    Log.e("Message Received",input)
                    OnDataCallback?.invoke(this@Connection,input)
                } catch (e:Exception){
                    this.closeConnection()
                }
            }
        }
    }

    fun sendMessage(message:String){
        Log.e("Message Sent",message)
        try{
            writer?.write(message)
            writer?.flush()
        }catch (e: Exception){
            closeConnection()
        }

    }

}