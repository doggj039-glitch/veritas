package law.veritas.app

import android.annotation.SuppressLint
import android.os.Bundle
import android.speech.tts.TextToSpeech
import android.webkit.JavascriptInterface
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.appcompat.app.AppCompatActivity
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import java.io.File
import java.util.Locale
import java.util.zip.ZipInputStream

/**
 * VERITAS — phone-first edition.
 *
 * Model: run the SAME Python engine (veritas_server) inside the app via Chaquopy,
 * bound to 127.0.0.1:8737, and point a full-screen WebView at m.html. The only
 * native bridge the phone UI needs is read-aloud → Android TextToSpeech, which
 * overrides the web app's window.VSpeak(). (PDF / external-link bridges are only
 * needed if My-Sources / Favorites are later added to the mobile UI — see README.)
 */
class MainActivity : AppCompatActivity() {

    private val port = 8737
    private lateinit var web: WebView
    private var tts: TextToSpeech? = null
    // Bump ASSET_VERSION whenever the bundled veritas-data.zip changes, to force re-extract.
    private val assetVersion = 1

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // 1) one-time: unzip the bundled data tree (library.db + engine + web) to files dir
        val dataDir = File(filesDir, "veritas")
        val stamp = File(filesDir, "asset.v")
        if (!dataDir.exists() || stamp.readTextOrEmpty() != assetVersion.toString()) {
            extractAsset("veritas-data.zip", filesDir)   // creates filesDir/veritas/...
            stamp.writeText(assetVersion.toString())
        }

        // 2) native voice for read-aloud
        tts = TextToSpeech(this) { status ->
            if (status == TextToSpeech.SUCCESS) tts?.language = Locale.US
        }

        // 3) start the Python engine on a background thread
        if (!Python.isStarted()) Python.start(AndroidPlatform(this))
        Thread {
            Python.getInstance().getModule("veritas_boot")
                .callAttr("run", dataDir.absolutePath, port)   // blocking serve_forever
        }.apply { isDaemon = true; start() }

        // 4) the WebView
        web = WebView(this)
        setContentView(web)
        web.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true                 // localStorage (notes/syllabus) + IndexedDB
            databaseEnabled = true
            allowFileAccess = true
            mediaPlaybackRequiresUserGesture = false
        }
        web.addJavascriptInterface(Bridge(), "Android")
        web.webViewClient = object : WebViewClient() {
            override fun onPageFinished(v: WebView?, url: String?) {
                // route the web app's read-aloud through the phone's own voice
                v?.evaluateJavascript(
                    "window.VSpeak=function(t){try{Android.speak(''+t)}catch(e){}};" +
                    "window.VStop=function(){try{Android.stop()}catch(e){}};", null)
            }
        }

        // 5) wait for the engine, then load the phone UI
        Thread {
            val url = "http://127.0.0.1:$port/m.html"
            repeat(80) { if (ping(url)) return@Thread also { runOnUiThread { web.loadUrl(url) } } ; Thread.sleep(250) }
            runOnUiThread { web.loadUrl(url) }       // load anyway after ~20s
        }.apply { isDaemon = true; start() }
    }

    /** JS-callable bridge exposed as `Android` in the WebView. */
    inner class Bridge {
        @JavascriptInterface fun speak(text: String) {
            tts?.speak(text, TextToSpeech.QUEUE_FLUSH, null, "veritas")
        }
        @JavascriptInterface fun stop() { tts?.stop() }
    }

    private fun ping(url: String): Boolean = try {
        (java.net.URL(url).openConnection() as java.net.HttpURLConnection).run {
            connectTimeout = 500; requestMethod = "HEAD"; responseCode; disconnect(); true
        }
    } catch (e: Exception) { false }

    private fun extractAsset(name: String, outDir: File) {
        assets.open(name).use { input ->
            ZipInputStream(input).use { zip ->
                var e = zip.nextEntry
                while (e != null) {
                    val f = File(outDir, e.name)
                    if (e.isDirectory) f.mkdirs() else {
                        f.parentFile?.mkdirs()
                        f.outputStream().use { zip.copyTo(it) }
                    }
                    e = zip.nextEntry
                }
            }
        }
    }

    private fun File.readTextOrEmpty(): String = try { if (exists()) readText() else "" } catch (e: Exception) { "" }

    override fun onDestroy() { tts?.shutdown(); super.onDestroy() }

    override fun onBackPressed() { if (web.canGoBack()) web.goBack() else super.onBackPressed() }
}
