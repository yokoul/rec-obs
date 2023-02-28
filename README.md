# rec-obs
Solution scryptée pour piloter la relation entre OBS et pyCA afin d'automatiser les changements de scènes et produire un direct (via ffmpeg) et un enregistrement séparés sur différentes instances d'OBS.

## Installation
L'installation nécessite préalablement d'avoir :
- installé OBS (latest) avec le module compat 4.9x pour le websocket
- installé docker desktop
- installé ou créer les scènes que l'on souhaite voir être enchainée sur OBS (Landing, Live) et testé les signaux vidéos et audios ad hoc

Ensuite il suffit de git rec-obs dans le dossier C:\rec-obs de son poste et d'effectuer l'initialisation de pyCA sur docker.

Pour initialisé pyCA sur docker, il est nécessaire de mettre à jour le fichier init/pyca.conf en particulier les valeurs suivantes :
> [agent]
>> [name]
> [server]
>> [url] /
>>[username]
>>[password]
``
Une fois cela effectué, il est possible d'initier pyCA avec la commande
``docker-compose -p mypycaname -f poco.yml up``
depuis le dossier C:\rec-obs\init\

*version 1.0 au 28.02.2023*