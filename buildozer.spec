[app]
title = Document Scanner
package.name = documentscanner
package.domain = org.scanner
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,plyer,requests
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.1.0
fullscreen = 0
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 29
android.minapi = 21
android.sdk = 29
android.ndk = 23b
android.accept_sdk_license = True
android.arch = arm64-v8a
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
