package com.seyahdoo.pmdeck

fun <T> T.doThreaded (func: ()->Unit) {
    Thread(Runnable {
        func()
    }).start()
}