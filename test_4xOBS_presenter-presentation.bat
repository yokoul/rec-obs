@echo off
set CONFIG_FILE=C:\rec-obs\scripts\obs-rec.conf

rem Copie du fichier de configuration versionX
COPY C:\rec-obs\scripts\config-bases\obs-rec-4xOBS.conf %CONFIG_FILE%

rem Lancement d'OBS
cd C:\obs-studio\bin\64bit
START "" obs64.exe --profile "test-scene-1" --collection "collection-test" --scene "Landing" -m --disable-updater
timeout /t 1
START "" obs64.exe --profile "test-scene-2" --collection "collection-test" --scene "Landing" -m --disable-updater
timeout /t 1
START "" obs64.exe --profile "test-scene-3" --collection "collection-test" --scene "Landing" -m --disable-updater
timeout /t 1
START "" obs64.exe --profile "test-scene-4" --collection "collection-test" --scene "Landing" -m --disable-updater
timeout /t 1
