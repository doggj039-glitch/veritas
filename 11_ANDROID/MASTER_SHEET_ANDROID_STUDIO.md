# MASTER SHEET — Build the VERITAS Android APK (for Claude Code on the build machine)

**Audience:** a Claude Code instance running on a machine that HAS Android Studio + the
Android SDK. This machine (Susan's) cannot build (low RAM/disk), so the whole project was
prepared here and shipped to you self-contained. **Your job: turn this folder into an
installed, working APK on a phone.** Everything the app needs is already inside `11_ANDROID/`.

**Prepared:** 2026-07-13, by Claude Code on Susan's Linux Mint machine.
**Ground truth:** if anything here conflicts with the code, the code wins — read it, don't guess.

---

## 0. What you are building (context)
VERITAS phone-first edition: a **Chaquopy (Python-on-Android) + WebView** app. It runs the
SAME Python engine as the desktop (`veritas_server.py`) *inside the app* on `127.0.0.1:8737`,
and points a full-screen WebView at `m.html` (the mobile UI: **Define · Dictionary · Library ·
Notes**). Read-aloud is bridged to the phone's native `TextToSpeech`. No server, no cloud, no
account — a self-contained offline constitutional dictionary.

**Already done for you (do NOT redo):**
- `app/src/main/assets/veritas-data.zip` (**134 MB, LEAN**) is baked in — the SQLite library
  (`VERITAS_definitions_library.db`, 5,130 verbatim Johnson 1773 entries) + engine + web + the
  10 founding docs. Verified on desktop to boot and answer `/api/resolve`, `/api/entry`,
  `/api/dictbrowse`, and serve `m.html`. On first launch the app unzips it to
  `filesDir/veritas/…` (that's why the first screen is black for a few seconds).
- `res/mipmap-*/ic_launcher.png` (+ `_round`) — a gold-"V"-on-dark launcher icon at all 5
  densities (raster, so it works on `minSdk 24`).
- `gradle/wrapper/gradle-wrapper.properties` pins **Gradle 8.4**. Android Studio finishes the
  wrapper (`gradlew` + jar) on first sync.
- Engine is **pure Python standard library** (`json, sqlite3, re, http.server, urllib`) —
  **no pip dependencies**. Chaquopy just needs its own Python runtime (auto-downloaded).

**Pinned toolchain (in `build.gradle` / `app/build.gradle`):** AGP **8.1.1**, Chaquopy
**16.0.0**, Kotlin **1.8.21**, compileSdk **34**, minSdk **24**, targetSdk **34**,
ABI **arm64-v8a only**, applicationId `law.veritas.app`.

---

## 1. Preflight (verify the machine + the folder)
**What:** confirm you can build and the project is intact.
- Android Studio installed; Android SDK present. Check: `sdkmanager --list_installed` (or open
  Studio ▸ SDK Manager). You need **SDK Platform 34**, **Build-Tools 34.x**, and an **NDK**
  (Chaquopy compiles native glue — any recent NDK, e.g. 25.x/26.x, is fine).
- **Internet is required for the FIRST build** (Gradle downloads AGP, Chaquopy's Python
  runtime, androidx). After that it can build offline.
- Disk: **~15–20 GB free**; RAM **8 GB+**.
- Confirm the payload is here (run from inside `11_ANDROID/`):
  ```
  test -f app/src/main/assets/veritas-data.zip && du -h app/src/main/assets/veritas-data.zip   # ~134M
  ls app/src/main/res/mipmap-xxhdpi/ic_launcher.png                                             # exists
  ```
  If `veritas-data.zip` is MISSING, see §6 (rebuild it) — but it should be present.
**Why:** a missing SDK/NDK or a truncated zip (flaky USB copy) are the two most likely blockers;
catch them before a 10-minute Gradle sync.

## 2. Point the project at your SDK
**What:** create `local.properties` in this folder (`11_ANDROID/`) with your SDK path — e.g.
`sdk.dir=/home/<you>/Android/Sdk` (Linux) or the Studio-managed path. Opening the project in
Android Studio usually writes this for you; do it by hand only if a build complains
"SDK location not found."
**Why:** `local.properties` is machine-specific and intentionally NOT shipped.

## 3. Open + sync in Android Studio
**What:** `File ▸ Open ▸` select the **`11_ANDROID`** folder (the one with `settings.gradle`).
Let **Gradle sync** run to completion. Accept any prompt to download the Gradle wrapper /
missing SDK components. If it offers an **AGP upgrade**, you may **decline** (the pinned
versions are a known-good set) — but see §5 if it refuses to sync.
- CLI equivalent (headless): `./gradlew --version` then `./gradlew assembleDebug`.
**Why:** the first sync is where version/SDK mismatches surface; resolve them here, not mid-build.

## 4. Build the APK
**What (GUI):** `Build ▸ Build Bundle(s) / APK(s) ▸ Build APK(s)`. When it finishes, click
**locate** — or find it at:
```
app/build/outputs/apk/debug/app-debug.apk
```
**What (CLI):** `./gradlew assembleDebug`  → same path.
This debug APK is auto-signed with the debug key and is directly installable. (For a
shareable/release APK: `Build ▸ Generate Signed Bundle / APK` and make a keystore — optional.)
**Why:** debug build is the fastest path to a testable app; no keystore ceremony needed to
sideload it.

## 5. Install on a phone
**What:** use a **real arm64 phone** (this build is arm64-only — see §7 about emulators).
- USB debugging on: `adb install -r app/build/outputs/apk/debug/app-debug.apk`
- or copy the `.apk` to the phone and tap it (allow "install from this source").
- Launch **VERITAS**. **Expect a few seconds of black screen on first run** (unzip + Python
  boot); then the Define tab appears.
**Why:** the arm64 filter keeps the APK small; it means x86 emulators won't install it.

## 6. Verify on device (acceptance test)
Tap through and confirm:
- **Define:** type `commerce` → baseline card shows the verbatim Johnson 1773 sense; tap
  **"Define the Drift (N) ▾"** → Webster/Black's snapshots by year.
- **Dictionary:** browse loads (jump-to + scroll); tap a word → jumps to Define.
- **Library:** open a founding document → full-screen reader scrolls.
- **Notes:** add a note → persists (kill + reopen the app, still there).
- **Read-aloud:** the 🔊 on a card speaks in the **phone's native voice** (this is the TTS
  bridge, not Piper).
Report exactly which of these pass/fail.

---

## 6b. (Only if the zip is missing/corrupt) rebuild the data asset
`assemble_assets.sh` builds `veritas-data.zip` from the desktop VERITAS source tree —
which is NOT on this build machine, so you normally CANNOT rerun it here. If the zip is
missing, get a fresh copy of `11_ANDROID/` from Susan's USB rather than rebuilding.
(For reference, on the source machine: `VERITAS_SRC="…/VERITAS v.3" ./assemble_assets.sh`
= LEAN ~134 MB; `--full` ~280 MB adds the FTS5 corpora for concordance.) **After any data
change, bump `assetVersion` in `MainActivity.kt`** so the phone re-extracts.

## 7. Troubleshooting (most-likely first)
| Symptom | Fix |
|---|---|
| Gradle sync fails on **plugin/AGP version** | Your installed SDK/Studio may be newer. Bump **together**: AGP → the version your Studio recommends, Kotlin to match, Chaquopy to its latest (`com.chaquo.python:gradle`). Keep `compileSdk`/`targetSdk` = an installed platform. |
| **"SDK location not found"** | Add `local.properties` with `sdk.dir=…` (see §2). |
| **"licenses not accepted"** / missing SDK components | `yes \| sdkmanager --licenses`, then re-sync. Or accept in Studio ▸ SDK Manager. |
| **"NDK not configured"** / Chaquopy NDK error | Install an NDK via SDK Manager (SDK Tools ▸ NDK). Chaquopy 16 needs it to assemble the arm64 Python. |
| **`INSTALL_FAILED_NO_MATCHING_ABIS`** | The APK is **arm64-only**. Use a real arm64 phone, an **arm64 emulator image**, OR add `"x86_64"` to `ndk { abiFilters … }` in `app/build.gradle` (bigger APK) for x86 emulators. |
| App installs but **black screen forever** | Open **Logcat**, filter `python`/`chaquopy`. Usually a Python traceback. Confirm the asset extracted: `adb shell run-as law.veritas.app ls files/veritas/00_APP`. |
| Logcat shows a Python **SyntaxError** | Chaquopy's Python is too old for the engine. In `app/build.gradle` `defaultConfig`, set `python { version "3.11" }` (or 3.12), re-sync, rebuild. |
| `sqlite3`/**FTS5** error | Chaquopy's sqlite3 normally includes FTS5. Only the (not-in-mobile) concordance needs it; Define/Dictionary/Library/Notes do NOT — so this shouldn't block a LEAN build. |
| Build OK, **no launcher icon** | Icons are at `res/mipmap-*/ic_launcher.png`. If a density is missing after a bad copy, re-copy `11_ANDROID/app/src/main/res/` from the USB. |

## 8. Do / Don't
- **DON'T** add pip dependencies — the engine is stdlib-only; keep it that way (fast, small, offline).
- **DON'T** change `minSdk`/ABI without reason. `arm64-v8a` + `minSdk 24` covers real phones.
- **DON'T** touch `m.html`/engine logic to "fix" mobile — the same files run on desktop; report issues back instead.
- **DO** keep read-aloud on the native `TextToSpeech` bridge (no Piper on ARM).
- **Note:** offline dictation (Vosk) exists on the DESKTOP edition only; it is **not** in the
  mobile UI yet. Read-aloud (TTS) is; speech-to-text (STT) is a later mobile task.

## 9. Report back to Susan
Plain English: (a) did it build, (b) the APK path/size, (c) installed on which phone, (d) which
of the §6 checks passed, (e) any error you hit and what fixed it. She reads this to know the
phone edition is real — not the build internals.
