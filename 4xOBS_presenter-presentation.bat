@echo off
set CONFIG_FILE=C:\rec-obs\scripts\obs-rec.conf

rem Copie du fichier de configuration versionX
COPY C:\rec-obs\scripts\config-bases\obs-rec-4xOBS.conf %CONFIG_FILE%

rem Lancement d'OBS
cd "C:\obs-studio\bin\64bit\"
START "" "C:\obs-studio\bin\64bit\obs64.exe" --collection "co-test-1" --profile "test-scene-1" --scene "Landing-1" -m --disable-updater
timeout /t 1
START "" "C:\obs-studio\bin\64bit\obs64.exe" --collection "co-test-2" --profile "test-scene-2" --scene "Landing-2" -m --disable-updater
timeout /t 1
START "" "C:\obs-studio\bin\64bit\obs64.exe" --collection "co-test-3" --profile "test-scene-3" --scene "Landing-3" -m --disable-updater
timeout /t 1
START "" "C:\obs-studio\bin\64bit\obs64.exe" --collection "co-test-4" --profile "test-scene-4" --scene "Landing-4" -m --disable-updater
timeout /t 1
