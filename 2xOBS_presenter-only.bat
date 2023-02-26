@echo off
set CONFIG_FILE=C:\rec-obs\scripts\obs-rec.conf

rem Copie du fichier de configuration versionX
COPY C:\rec-obs\scripts\config-bases\obs-rec-2xOBS.conf %CONFIG_FILE%

rem Lancement d'OBS
cd "C:\Program Files\obs-studio\bin\64bit\"
START "" "C:\Program Files\obs-studio\bin\64bit\obs64.exe" --profile "presenter-live" --collection "8lang-presenter" --scene "Landing" -m --disable-updater
timeout /t 1
START "" "C:\Program Files\obs-studio\bin\64bit\obs64.exe" --profile "presenter-rec" --collection "8lang-presenter" --scene "Landing" -m --disable-updater
timeout /t 1
