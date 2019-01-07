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

    val ip = "192.168.1.33"
    val port = 23997

    val lock: Lock = ReentrantLock()

    class ShouldContinue(){
        var cont:Boolean = true;
    }

    private var lastReaderContinue: ShouldContinue? = null;

    fun openConnection() {

        doAsync {
            try {
                socket = Socket(ip, port)
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