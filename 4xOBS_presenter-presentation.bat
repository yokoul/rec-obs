@echo off
set CONFIG_FILE=C:\rec-obs\scripts\obs-rec.conf

rem Copie du fichier de configuration versionX
COPY C:\rec-obs\scripts\config-bases\obs-rec-4xOBS.conf %CONFIG_FILE%

rem Lancement d'OBS
cd "C:\Program Files\obs-studio\bin\64bit\"
START "" "C:\Program Files\obs-studio\bin\64bit\obs64.exe" --profile "co-test-1" --collection "test-scene-1" --scene "Landing" -m --disable-updater
timeout /t 1
START "" "C:\Program Files\obs-studio\bin\64bit\obs64.exe" --profile "co-test-2" --collection "test-scene-2" --scene "Landing" -m --disable-updater
timeout /t 1
START "" "C:\Program Files\obs-studio\bin\64bit\obs64.exe" --profile "co-test-3" --collection "test-scene-3" --scene "Landing" -m --disable-updater
timeout /t 1
START "" "C:\Program Files\obs-studio\bin\64bit\obs64.exe" --profile "co-test-4" --collection "test-scene-4" --scene "Landing" -m --disable-updater
timeout /t 1
