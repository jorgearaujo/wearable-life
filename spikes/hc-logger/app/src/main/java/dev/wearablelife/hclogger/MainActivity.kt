package dev.wearablelife.hclogger

import android.graphics.Typeface
import android.os.Bundle
import android.view.ViewGroup.LayoutParams.MATCH_PARENT
import android.view.ViewGroup.LayoutParams.WRAP_CONTENT
import android.widget.Button
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import androidx.activity.ComponentActivity
import androidx.health.connect.client.HealthConnectClient
import androidx.health.connect.client.PermissionController
import androidx.lifecycle.lifecycleScope
import java.io.File
import kotlinx.coroutines.launch
import org.json.JSONObject

/** The only screen: permission state, a "Read now" button, and a summary of the last poll. */
class MainActivity : ComponentActivity() {
    private lateinit var status: TextView
    private lateinit var readNow: Button

    private val requestPermissions =
        registerForActivityResult(PermissionController.createRequestPermissionResultContract()) { poll("open") }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val pad = (16 * resources.displayMetrics.density).toInt()

        val grant = Button(this).apply {
            text = "Grant permissions"
            setOnClickListener { requestMissingPermissions() }
        }
        readNow = Button(this).apply {
            text = "Read now"
            setOnClickListener { poll("manual") }
        }
        status = TextView(this).apply {
            typeface = Typeface.MONOSPACE
            textSize = 12f
            setTextIsSelectable(true)
        }
        val column = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(pad, pad, pad, pad)
            addView(grant, MATCH_PARENT, WRAP_CONTENT)
            addView(readNow, MATCH_PARENT, WRAP_CONTENT)
            addView(status, MATCH_PARENT, WRAP_CONTENT)
        }
        setContentView(ScrollView(this).apply {
            fitsSystemWindows = true
            addView(column)
        })

        PollWorker.schedule(this)
    }

    override fun onResume() {
        super.onResume()
        poll("open")
    }

    private fun requestMissingPermissions() {
        if (HealthConnectClient.getSdkStatus(this) != HealthConnectClient.SDK_AVAILABLE) return
        val client = HealthConnectClient.getOrCreate(this)
        lifecycleScope.launch {
            val wanted = Poller.readPermissions(client.features)
            val missing = wanted - client.permissionController.getGrantedPermissions()
            if (missing.isNotEmpty()) requestPermissions.launch(missing)
        }
    }

    private fun poll(trigger: String) {
        readNow.isEnabled = false
        status.text = "Reading…"
        lifecycleScope.launch {
            val run = Poller.poll(this@MainActivity, trigger)
            status.text = render(run)
            readNow.isEnabled = true
        }
    }

    /** Counts and states only; no health values are shown. */
    private fun render(run: JSONObject): String = buildString {
        val prefs = getSharedPreferences(Poller.PREFS, MODE_PRIVATE)
        appendLine("Last poll: ${run.optString("at")} (${run.optString("trigger")}, ${run.optLong("durationMs")} ms)")
        appendLine("Health Connect status: ${sdkStatusText(run.optInt("sdkStatus"))}")
        run.optString("error").takeIf { it.isNotEmpty() }?.let { appendLine("Error: $it") }
        appendLine("Next alarm: ${run.opt("nextAlarm")}")
        run.optJSONObject("features")?.let { appendLine("Features: $it") }
        appendLine()
        appendLine("%-26s %-9s %6s %8s".format("type", "this poll", "", "total"))
        val types = run.optJSONObject("types")
        for (type in LOGGED_TYPES) {
            val t = types?.optJSONObject(type.name)
            val thisPoll = when {
                t == null -> "-"
                t.has("skipped") -> t.getString("skipped")
                t.has("error") -> "ERROR"
                else -> "+${t.optInt("upserts")} -${t.optInt("deletes")}"
            }
            appendLine("%-26s %-16s %8d".format(type.name, thisPoll, prefs.getLong("total.${type.name}", 0)))
            t?.optString("error")?.takeIf { it.isNotEmpty() }?.let { appendLine("   $it") }
        }
        appendLine()
        appendLine("observations.jsonl: ${File(filesDir, Poller.OBSERVATIONS_FILE).length() / 1024} KB")
        appendLine("runs.jsonl: ${File(filesDir, Poller.RUNS_FILE).length() / 1024} KB")
        appendLine()
        appendLine("This app only reads. Data stays on this phone until you copy it over USB.")
    }

    private fun sdkStatusText(status: Int) = when (status) {
        HealthConnectClient.SDK_AVAILABLE -> "available"
        HealthConnectClient.SDK_UNAVAILABLE -> "not available on this phone"
        HealthConnectClient.SDK_UNAVAILABLE_PROVIDER_UPDATE_REQUIRED -> "needs install or update"
        else -> "unknown ($status)"
    }
}
