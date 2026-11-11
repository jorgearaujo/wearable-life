// Godot Android plugin (v2): a Kotlin library that reads today's step count from Health Connect.
// Build with `./gradlew copyAar`; the AAR lands in ../addons/hc_bridge/.
plugins {
    id("com.android.library") version "9.5.1"
}

android {
    namespace = "dev.wearablelife.hcbridge"
    compileSdk = 36

    defaultConfig {
        minSdk = 28
    }
}

dependencies {
    compileOnly("org.godotengine:godot:4.7.2.stable")
    implementation("androidx.health.connect:connect-client:1.1.0")
    // Same version connect-client already brings in at runtime; needed here only to compile.
    compileOnly("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
}

tasks.register<Copy>("copyAar") {
    dependsOn("assembleRelease")
    from(layout.buildDirectory.file("outputs/aar/hcbridge-release.aar"))
    into("../addons/hc_bridge")
    rename { "hcbridge.aar" }
}
