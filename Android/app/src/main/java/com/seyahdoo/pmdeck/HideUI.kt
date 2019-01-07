package com.seyahdoo.pmdeck

import java.io.DataOutputStream
import java.io.IOException


class HideUI {

    companion object {

        /**
         * Uses Root access to enable and disable SystemUI.
         * @param enabled Decide whether to enable or disable.
         */
        fun setSystemUIEnabled(enabled:Boolean) {
            try {
                val p = Runtime.getRuntime().exec("su")
                val os = DataOutputStream(p.outputStream)
                os.writeBytes(
                    "pm " + (if (enabled) "enable" else "disable")
                            + " com.android.systemui\n"
                )
                os.writeBytes("exit\n")
                os.flush()
            } catch (e:IOException) {
                e.printStackTrace()
            }

        }

    }



}