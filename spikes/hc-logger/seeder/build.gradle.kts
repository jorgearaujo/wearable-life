// Emulator-only helper: writes synthetic records into Health Connect so the logger can be tested.
// Never install this on a phone with real data.
plugins {
    id("com.android.application")
}

android {
    namespace = "dev.wearablelife.hcseeder"
    compileSdk = 37

    defaultConfig {
        // -PseederId=... builds a second copy under another name, to act as a second data source.
        applicationId = (findProperty("seederId") as String?) ?: "dev.wearablelife.hcseeder"
        minSdk = 34
        targetSdk = 36
        versionCode = 1
        versionName = "0.1"
    }
}

kotlin {
    compilerOptions {
        optIn.add("androidx.health.connect.client.feature.ExperimentalMindfulnessSessionApi")
    }
}

dependencies {
    implementation("androidx.health.connect:connect-client:1.1.0")
    implementation("androidx.activity:activity:1.13.0")
}
