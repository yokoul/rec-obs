# rec-obs
Solution scryptée pour piloter la relation entre OBS et pyCA afin d'automatiser les changements de scènes et produire un direct (via ffmpeg) et un enregistrement séparés sur de multiples instances d'OBS en simultanés.

## Notes de version
Cette version intègre le pilotage streaming en plus du recording. Cela permet de définir le modèle d'écriture pour les adresses de streaming en lien avec une version adaptée de fichier de configuration.
Testée sur Antmedia Server, le fonctionnement est correct.
Le problème restant la gestion multilangue en srt lors de l'usage des fonctions de streaming d'OBS qui sont limitée à un modèle 1xvidéo/1xaudio.
Un backup de la configuration testée sur OBS est intégrée en .zip init/ pour référence.

## Installation
L'installation nécessite préalablement d'avoir :
- instaler OBS (latest) avec le module compat 4.9x pour le websocket
- instaler docker desktop
- instaler ou créer les scènes que l'on souhaite voir être enchainée sur OBS (Landing, Live) et testé les signaux vidéos et audios ad hoc

Ensuite il suffit de git rec-obs dans le dossier C:\rec-obs de son poste et d'effectuer l'initialisation de pyCA sur docker.

Pour initialiser pyCA sur docker, il est nécessaire de mettre à jour le fichier ``init/pyca.conf`` en particulier les valeurs suivantes :

> [agent]
>> name

> [server]
>> url<br>
username<br>
password<br>

Une fois cela effectué, il est possible d'initier pyCA avec la commande<br>
``docker-compose -p mypycaname -f poco.yml up``<br>
depuis le dossier ``C:\rec-obs\init\``


[GitHubLink]:https://github.com/yokoul/rec-obs - *version 1.1 au 05.03.2023*