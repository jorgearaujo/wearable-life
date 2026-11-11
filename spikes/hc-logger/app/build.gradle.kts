plugins {
    id("com.android.application")
}

android {
    namespace = "dev.wearablelife.hclogger"
    compileSdk = 37

    defaultConfig {
        applicationId = "dev.wearablelife.hclogger"
        minSdk = 28
        targetSdk = 36
        versionCode = 1
        versionName = "0.1"
    }

    // Debug builds only: the data is pulled off the phone with `adb run-as`.
    buildTypes {
        debug {
            isDebuggable = true
        }
    }
}

// MindfulnessSessionRecord is still marked experimental in connect-client 1.1.0.
kotlin {
    compilerOptions {
        optIn.add("androidx.health.connect.client.feature.ExperimentalMindfulnessSessionApi")
    }
}

dependencies {
    implementation("androidx.health.connect:connect-client:1.1.0")
    implementation("androidx.work:work-runtime-ktx:2.12.0")
    implementation("androidx.activity:activity:1.13.0")
}
