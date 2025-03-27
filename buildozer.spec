[app]

# Название приложения
title = MOA Calculator

# Имя пакета (только строчные буквы и цифры)
package.name = moacalculator

# Домен (обычно в reverse-DNS формате)
package.domain = org.vitaem

# Версия приложения (format: major.minor.revision)
version = 1.0

# Требуемые модули Python
requirements = 
    python3,
    setuptools==65.5.0,
    kivy==2.3.0,
    cython==0.29.36,
    pyjnius

# Android API
android.api = 31
android.minapi = 21

# Пути к SDK и NDK (оставьте пустыми для автоматической загрузки)
# android.sdk_path = 
# android.ndk_path = 

# Архитектуры
android.arch = arm64-v8a, armeabi-v7a

# Исходные файлы
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Иконка приложения (разместите в той же директории)
# icon.filename = icon.png

# Ориентация экрана (portrait|landscape|all)
orientation = portrait

# Полноэкранный режим
fullscreen = 0

# Разрешения Android
android.permissions = INTERNET

# Характеристики оборудования
android.features = 
    android.hardware.screen.portrait

# Настройки сборки
android.accept_sdk_license = True
android.release_artifact = .apk
android.enable_androidx = True

# Дополнительные настройки
[buildozer]
# Уровень логгирования (0-2)
log_level = 2

# Папка для сборки
build_dir = ./.buildozer

# Папка с билдами
bin_dir = ./bin

# Отключить автоматическое обновление (для ускорения повторных сборок)
android.skip_update = False

# Версия NDK (рекомендуемая стабильная)
android.ndk = 23b

# Версия инструментов сборки
# android.sdk = 26.1.1
