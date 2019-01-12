package com.seyahdoo.pmdeck

import org.jetbrains.anko.doAsync
import java.io.*
import java.lang.Exception
import java.net.InetAddress
import java.net.Socket
import java.util.*
import java.util.concurrent.locks.Lock
import java.util.concurrent.locks.ReentrantLock
import kotlin.concurrent.withLock


class Connection {

    var socket: Socket? = null;
    var writer: PrintWriter? = null;

    val lock: Lock = ReentrantLock()

    //var ip: InetAddress? = null
    //var port: Int = 0

    class ShouldContinue(){
        var cont:Boolean = true;
    }

    private var lastReaderContinue: ShouldContinue? = null;

    fun openConnection(ip:InetAddress, port:Int) {

        doAsync {
            try {
                socket = Socket(ip, port)
                socket?.soTimeout = 10000
                writer = PrintWriter(socket!!.getOutputStream())
                val inputReader = BufferedReader(InputStreamReader(socket?.getInputStream()));
                reader(ShouldContinue(), inputReader)
            } catch (e: IOException) {
                e.printStackTrace()
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

    var OnDataCallback: ((String)->Unit)? = null

    fun setOnDataListener(listener: (String) -> Unit){
        OnDataCallback = listener;
    }

    fun reader(shouldContinue: ShouldContinue, bufreader: BufferedReader) {
        lastReaderContinue = shouldContinue
        doAsync {
            while (shouldContinue.cont) {
                val input: String = bufreader.readLine() ?: continue
                OnDataCallback?.invoke(input)
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