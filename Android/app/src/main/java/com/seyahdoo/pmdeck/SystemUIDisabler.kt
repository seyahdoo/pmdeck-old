package com.seyahdoo.pmdeck

import android.util.Log

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