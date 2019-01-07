package com.seyahdoo.pmdeck

import org.jetbrains.anko.doAsync
import java.io.*
import java.net.Socket
import java.util.*
import java.util.concurrent.locks.Lock
import java.util.concurrent.locks.ReentrantLock
import kotlin.concurrent.withLock


class Connection {

    var socket: Socket? = null;
    var writer: PrintWriter? = null;
    var inputReader: BufferedReader? = null;

    val ip = "192.168.1.33"
    val port = 23997

    val lock: Lock = ReentrantLock()

    fun openConnection() {

        doAsync {
            try {
                socket = Socket(ip, port)
                writer = PrintWriter(socket!!.getOutputStream())
                inputReader = BufferedReader(InputStreamReader(socket?.getInputStream()));

                reader()

            } catch (e: IOException) {
                e.printStackTrace()
            }

        }



    }

    fun closeConnection(){
        doAsync {
            inputReader?.close()
            writer?.close()
            socket?.close()
        }
    }

    interface OnDataListener {
        fun onData(s: String)
    }

    var OnDataCallback: ((String)->Unit)? = null

    fun setOnDataListener(listener: (String) -> Unit){
        OnDataCallback = listener;
    }

    fun reader() {
        doAsync {
            while (true) {
                val input: String = inputReader?.readLine() ?: continue
                OnDataCallback?.invoke(input)
            }
        }
    }

    val queue: Queue<String> = ArrayDeque<String>()

    fun sendMessage(message:String){
        queue.add(message)

        doAsync {
            lock.withLock {
                writer?.write(queue.remove());
                writer?.flush()
                null
            }
        }

    }

}